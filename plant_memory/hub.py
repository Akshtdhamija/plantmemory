"""
PlantMemory Hub — a local web dashboard.

A dependency-free HTTP server (stdlib only) that exposes the PlantMemory engine
as a small JSON API and serves a single-page dashboard. Everything runs on
127.0.0.1; nothing is uploaded anywhere. This is where a person explores the
team's grounded knowledge, drives the drift explorer, reviews the Inbox, and
manages shift Relays.
"""
from __future__ import annotations

import json
import os
import threading
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs

from .paths import EVAL_DIR

STATIC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hub_static")


# ---------------------------------------------------------------------------
# API implementation (thin wrappers over the engine)
# ---------------------------------------------------------------------------

def _load_ctx(scenario=None):
    from .store import load_all
    from .plant_state import load_base_state
    from .simulate import get_scenario
    entries = load_all()
    base = load_base_state(with_data_stats=True)
    state = get_scenario(scenario).apply(base) if scenario else base
    return entries, base, state


def api_overview(scenario=None):
    from .drift import evaluate_all, summarize
    from .simulate import SCENARIOS
    from . import inbox, relay, moc
    entries, base, state = _load_ctx(scenario)
    base_h = summarize(evaluate_all(entries, base))
    health = summarize(evaluate_all(entries, state)) if scenario else base_h
    return {
        "corpus_size": len(entries),
        "scenario": scenario,
        "health": health,
        "base_health": base_h,
        "scenarios": [{"name": n, "kind": sc.kind, "description": sc.description,
                       "moc_object": getattr(sc, "moc_object", "material"),
                       "moc_class": getattr(sc, "moc_class", "Technical change")}
                      for n, sc in SCENARIOS.items()],
        "pending_proposals": len(inbox.list_proposals("pending")),
        "open_relays": len(relay.list_relays("open")),
        "open_moc": len(moc.list_moc("in_review")),
        "categories": _category_counts(entries),
    }


def api_moc_assess(scenario=None):
    from . import moc
    if not scenario:
        return {"scenario": None, "impacted": [], "impacted_count": 0}
    return moc.assess(scenario)


def api_moc_list():
    from . import moc
    return {"records": moc.list_moc(), "overdue": moc.overdue(), "audit": moc.verify_audit()}


def api_org(person=None):
    from . import org, plantdata
    people = plantdata.roster()
    if not person:
        return {"people": people}
    return {"people": people, "assessment": org.assess_departure(person)}


_SCAN_CACHE = {}


def api_unmanaged():
    """Changes the detector sees in the historian, matched against approved MOCs."""
    if "scan" not in _SCAN_CACHE:
        from . import unmanaged
        hits = unmanaged.scan()
        by_tag = {}
        for h in hits:
            by_tag.setdefault(h["tag"], []).append(h["time"])
        _SCAN_CACHE["scan"] = {"detections": len(hits), "tags": len(by_tag),
                               "by_tag": sorted(({"tag": t, "count": len(v), "first": v[0]}
                                                 for t, v in by_tag.items()),
                                                key=lambda x: -x["count"])}
    return _SCAN_CACHE["scan"]


def _category_counts(entries):
    from collections import Counter
    c = Counter(e.category for e in entries)
    return dict(c)


def api_knowledge(scenario=None):
    from .drift import evaluate_all
    entries, base, state = _load_ctx(scenario)
    drifts = {d.entry_id: d for d in evaluate_all(entries, state)}
    out = []
    for e in entries:
        d = drifts.get(e.id)
        out.append({
            "id": e.id, "title": e.title, "category": e.category,
            "statement": e.statement, "confidence": e.confidence,
            "author": e.author, "source": e.source,
            "tags_referenced": e.tags_referenced,
            "n_groundings": len(e.groundings),
            "health": d.health if d else "intact",
            "live_confidence": d.confidence if d else e.confidence,
            "reasons": [g.detail for g in d.groundings if g.detail] if d else [],
        })
    return {"scenario": scenario, "entries": out}


def api_entry(entry_id, scenario=None):
    from .drift import evaluate_entry
    from .store import load_entry
    entries, base, state = _load_ctx(scenario)
    e = load_entry(entry_id)
    if not e:
        return None
    d = evaluate_entry(e, state)
    ed = e.to_dict()
    ed["drift"] = d.to_dict()
    return ed


def api_drift(scenario=None):
    from .drift import evaluate_all, summarize
    entries, base, state = _load_ctx(scenario)
    drifts = evaluate_all(entries, state)
    return {"scenario": scenario, "summary": summarize(drifts),
            "entries": [d.to_dict() for d in drifts]}


def api_graph(scenario=None):
    """Return the plant knowledge graph with a layered layout and drift overlay."""
    from .drift import evaluate_all
    entries, base, state = _load_ctx(scenario)

    # which tags / nodes are affected under this scenario
    changed_tags, changed_nodes, missing = set(), set(), set()
    grounded_tags, grounded_nodes = set(), set()
    for e in entries:
        for g in e.groundings:
            (grounded_tags if g.kind == "tag" else grounded_nodes).add(g.ref)
    for d in evaluate_all(entries, state):
        for g in d.groundings:
            if g.status == "changed":
                (changed_tags if g.grounding.kind == "tag" else changed_nodes).add(g.grounding.ref)
            elif g.status == "missing":
                missing.add(g.grounding.ref)

    # layered layout by node_type
    order = ["Boundary", "System", "Equipment", "Sensor", "ProcessVariable",
             "ControlLoop", "OperatingMode", "Plant"]
    cols = {t: [] for t in order}
    for nid, n in base.nodes.items():
        cols.setdefault(n.get("node_type", "Other"), []).append(nid)
    nodes = []
    for ci, t in enumerate(order):
        ids = cols.get(t, [])
        for ri, nid in enumerate(ids):
            n = base.nodes[nid]
            nodes.append({
                "id": nid, "type": t, "name": n.get("name", nid),
                "col": ci, "row": ri, "n_rows": max(len(ids), 1),
                # sensor node_ids equal tag names, so a changed/grounded tag lights
                # up its sensor node too.
                "grounded": nid in grounded_nodes or nid in grounded_tags,
                "changed": nid in changed_nodes or nid in changed_tags,
                "missing": nid in missing,
            })
    # edges (from base adjacency, deduped)
    seen = set()
    edges = []
    for nid, adj in base.adjacency.items():
        for et, nb in adj:
            key = tuple(sorted([nid, nb])) + (et,)
            if key in seen or nb not in base.nodes:
                continue
            seen.add(key)
            edges.append({"source": nid, "target": nb, "type": et})
    return {"scenario": scenario, "nodes": nodes, "edges": edges,
            "changed_tags": sorted(changed_tags), "changed_nodes": sorted(changed_nodes),
            "columns": order}


def api_evaluate():
    from .evaluate import evaluate_full
    return evaluate_full(make_plots=True)


def api_inbox():
    from . import inbox
    return {"proposals": inbox.list_proposals()}


def api_relays():
    from . import relay
    return {"relays": relay.list_relays()}


# ---------------------------------------------------------------------------
# HTTP handler
# ---------------------------------------------------------------------------

class Handler(BaseHTTPRequestHandler):
    server_version = "PlantMemoryHub/0.1"

    def log_message(self, *a):
        pass  # quiet

    def _send(self, obj, code=200, ctype="application/json"):
        body = obj if isinstance(obj, bytes) else json.dumps(obj).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _static(self, path):
        fp = os.path.join(STATIC_DIR, path)
        if not os.path.isfile(fp):
            self._send({"error": "not found"}, 404)
            return
        ctype = {"html": "text/html", "js": "application/javascript",
                 "css": "text/css", "png": "image/png"}.get(path.rsplit(".", 1)[-1], "text/plain")
        with open(fp, "rb") as f:
            self._send(f.read(), 200, ctype + "; charset=utf-8" if ctype.startswith("text") else ctype)

    def _body_json(self):
        length = int(self.headers.get("Content-Length", 0) or 0)
        if not length:
            return {}
        try:
            return json.loads(self.rfile.read(length).decode("utf-8"))
        except Exception:
            return {}

    def do_GET(self):
        u = urlparse(self.path)
        q = parse_qs(u.query)
        scen = q.get("scenario", [None])[0] or None
        try:
            if u.path in ("/", "/index.html"):
                return self._static("index.html")
            if u.path in ("/app.js", "/style.css"):
                return self._static(u.path.lstrip("/"))
            if u.path.startswith("/plots/"):
                name = os.path.basename(u.path)
                fp = os.path.join(EVAL_DIR, name)
                if os.path.isfile(fp):
                    with open(fp, "rb") as f:
                        return self._send(f.read(), 200, "image/png")
                return self._send({"error": "no plot"}, 404)

            if u.path == "/api/overview":
                return self._send(api_overview(scen))
            if u.path == "/api/knowledge":
                return self._send(api_knowledge(scen))
            if u.path.startswith("/api/knowledge/"):
                eid = u.path.rsplit("/", 1)[-1]
                r = api_entry(eid, scen)
                return self._send(r if r else {"error": "not found"}, 200 if r else 404)
            if u.path == "/api/drift":
                return self._send(api_drift(scen))
            if u.path == "/api/graph":
                return self._send(api_graph(scen))
            if u.path == "/api/evaluate":
                return self._send(api_evaluate())
            if u.path == "/api/inbox":
                return self._send(api_inbox())
            if u.path == "/api/relays":
                return self._send(api_relays())
            if u.path == "/api/moc/assess":
                return self._send(api_moc_assess(scen))
            if u.path == "/api/moc":
                return self._send(api_moc_list())
            if u.path == "/api/org":
                return self._send(api_org(q.get("person", [None])[0]))
            if u.path == "/api/moc/unmanaged":
                return self._send(api_unmanaged())
            if u.path.startswith("/api/moc/") and u.path.endswith("/package"):
                from . import moc
                p = moc.export_package(u.path.split("/")[3])
                with open(p, encoding="utf-8") as f:
                    return self._send(f.read().encode("utf-8"), 200, "text/markdown; charset=utf-8")
            return self._send({"error": "unknown route"}, 404)
        except Exception as exc:
            import traceback
            traceback.print_exc()
            return self._send({"error": str(exc)}, 500)

    def do_POST(self):
        u = urlparse(self.path)
        data = self._body_json()
        try:
            from . import inbox, relay
            if u.path.startswith("/api/inbox/") and u.path.endswith("/approve"):
                pid = u.path.split("/")[3]
                e = inbox.approve_proposal(pid, approver=data.get("by", "reviewer"))
                return self._send({"ok": True, "entry_id": e.id})
            if u.path.startswith("/api/inbox/") and u.path.endswith("/reject"):
                pid = u.path.split("/")[3]
                inbox.reject_proposal(pid, reviewer=data.get("by", "reviewer"),
                                      reason=data.get("reason", ""))
                return self._send({"ok": True})
            if u.path == "/api/relays":
                r = relay.create_relay(
                    title=data.get("title", "Handoff"), summary=data.get("summary", ""),
                    from_member=data.get("by", "engineer"), to=data.get("to", "team"),
                    scenario=data.get("scenario") or None)
                return self._send({"ok": True, "relay": r})
            if u.path.startswith("/api/relays/") and u.path.endswith("/take"):
                rid = u.path.split("/")[3]
                return self._send({"ok": True, "relay": relay.take_relay(rid, data.get("by", "engineer"))})
            if u.path.startswith("/api/relays/") and u.path.endswith("/close"):
                rid = u.path.split("/")[3]
                return self._send({"ok": True, "relay": relay.close_relay(rid, data.get("by", "engineer"))})
            from . import moc
            if u.path == "/api/moc/raise":
                r = moc.raise_moc(data.get("scenario"), originator=data.get("by", "engineer"),
                                  reason=data.get("reason", ""))
                return self._send({"ok": True, "moc": r})
            if u.path.startswith("/api/moc/") and u.path.endswith("/approve"):
                mid = u.path.split("/")[3]
                return self._send({"ok": True, "moc": moc.decide_moc(
                    mid, decision="approved", approver=data.get("by", "approver"),
                    note=data.get("note", ""))})
            if u.path.startswith("/api/moc/") and u.path.endswith("/reject"):
                mid = u.path.split("/")[3]
                return self._send({"ok": True, "moc": moc.decide_moc(
                    mid, decision="rejected", approver=data.get("by", "approver"),
                    note=data.get("note", ""))})
            steps = {"implement": moc.implement, "pssr": moc.complete_pssr,
                     "verify": moc.verify_change, "close": moc.close_moc}
            if u.path.startswith("/api/moc/") and u.path.rsplit("/", 1)[-1] in steps:
                mid, step = u.path.split("/")[3], u.path.rsplit("/", 1)[-1]
                return self._send({"ok": True, "moc": steps[step](mid)})
            return self._send({"error": "unknown route"}, 404)
        except Exception as exc:
            return self._send({"error": str(exc)}, 500)


def run_hub(port=7700, open_browser=True, host=None):
    from .store import load_all
    if not load_all():
        from .seed import seed
        print("[hub] empty store -> seeding demo knowledge")
        seed(reset=True)
    # Bind host: default to loopback, but honour PLANTMEMORY_HOST (e.g. 0.0.0.0
    # inside a container). The browser URL always points at localhost.
    host = host or os.environ.get("PLANTMEMORY_HOST", "127.0.0.1")
    httpd = ThreadingHTTPServer((host, port), Handler)
    url = f"http://127.0.0.1:{port}/"
    print(f"PlantMemory Hub running at {url}  (Ctrl+C to stop)")
    if open_browser:
        threading.Timer(0.6, lambda: webbrowser.open(url)).start()
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[hub] stopped")
        httpd.shutdown()
