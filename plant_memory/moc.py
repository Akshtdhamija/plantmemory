"""
Management of Change (MOC): workflow, approvals, package and audit trail.

PlantMemory turns MOC's manual impact-assessment step into a computation
(impact.py) and keeps the authorisation human. A change moves through

    in_review -> approved | rejected -> implemented -> pssr_complete
              -> verified | reopened -> closed

* Each MOC record embeds its full impact assessment (knowledge, procedures,
  alarms with replay, models, people, physical propagation, risk tier).
* The risk tier decides the required sign-offs; the change is approved only when
  every required role has approved, and rejected if any role rejects.
* Types follow CCPS practice: permanent, temporary (with an expiry that is
  tracked and escalated) and emergency (implemented first, retrospective review
  due within EMERGENCY_REVIEW_H hours). Replacement-in-kind is exempt and is
  *computed*: the change set is empty.
* Every state change is appended to a hash-chained audit log,
      h_i = SHA-256( h_{i-1} || canonical(record_i) ),
  so altering any past entry breaks every later hash and is detected.
"""
from __future__ import annotations

import glob
import hashlib
import json
import os
from datetime import datetime, timedelta

from .paths import MOC_DIR, ensure_dirs
from .simulate import SCENARIOS, get_scenario
from .store import now_iso

MATERIAL, ORGANISATIONAL = "material", "organisational"
EMERGENCY_REVIEW_H = 72
AUDIT_LOG = os.path.join(MOC_DIR, "audit.log")
PACKAGE_DIR = os.path.join(MOC_DIR, "packages")

PSSR_TEMPLATE = [
    "Construction / installation is in accordance with the design specification",
    "Safety, operating, maintenance and emergency procedures are in place and adequate",
    "Process safety information (P&IDs, datasheets, setpoint register) is updated",
    "Alarm limits and interlocks are configured as approved and tested",
    "Affected personnel are trained and informed",
    "Flagged knowledge has been re-validated by a qualified reviewer",
    "Process-monitoring models with moved inputs are revalidated",
]


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------

def _next_moc_id() -> str:
    ensure_dirs()
    nums = [int(os.path.basename(p)[4:8]) for p in glob.glob(os.path.join(MOC_DIR, "moc-*.json"))
            if os.path.basename(p)[4:8].isdigit()]
    return f"moc-{(max(nums) + 1) if nums else 1:04d}"


def _path(moc_id: str) -> str:
    return os.path.join(MOC_DIR, f"{moc_id}.json")


def _save(rec: dict) -> None:
    with open(_path(rec["moc_id"]), "w", encoding="utf-8") as f:
        json.dump(rec, f, indent=2, default=str)


def _canon(x) -> str:
    return json.dumps(x, sort_keys=True, separators=(",", ":"), default=str)


def audit(event: str, moc_id: str, actor: str, detail: dict | None = None) -> dict:
    """Append one hash-chained entry to the audit log."""
    ensure_dirs()
    prev = "0" * 64
    if os.path.isfile(AUDIT_LOG):
        with open(AUDIT_LOG, encoding="utf-8") as f:
            lines = [l for l in f.read().splitlines() if l.strip()]
        if lines:
            prev = json.loads(lines[-1])["hash"]
    body = {"t": now_iso(), "event": event, "moc_id": moc_id, "actor": actor,
            "detail": detail or {}}
    h = hashlib.sha256((prev + _canon(body)).encode()).hexdigest()
    row = {**body, "prev": prev, "hash": h}
    with open(AUDIT_LOG, "a", encoding="utf-8") as f:
        f.write(_canon(row) + "\n")
    return row


def verify_audit() -> dict:
    """Recompute the chain; report the first broken link, if any."""
    if not os.path.isfile(AUDIT_LOG):
        return {"ok": True, "entries": 0}
    prev = "0" * 64
    with open(AUDIT_LOG, encoding="utf-8") as f:
        rows = [json.loads(l) for l in f.read().splitlines() if l.strip()]
    for i, r in enumerate(rows):
        body = {k: v for k, v in r.items() if k not in ("prev", "hash")}
        h = hashlib.sha256((prev + _canon(body)).encode()).hexdigest()
        if r.get("prev") != prev or r.get("hash") != h:
            return {"ok": False, "entries": len(rows), "broken_at": i}
        prev = r["hash"]
    return {"ok": True, "entries": len(rows), "head": prev}


# ---------------------------------------------------------------------------
# assessment (computable impact)
# ---------------------------------------------------------------------------

def assess(scenario_name: str) -> dict:
    """Full computable assessment, plus the compact fields the hub view uses."""
    from .impact import assess as full
    a = full(scenario_name)
    k = a["knowledge"]
    n_broken = sum(1 for x in k if x["health"] == "broken")
    n_review = sum(1 for x in k if x["health"] == "review")
    tier = a["risk"]["tier"]
    if a["replacement_in_kind"]:
        rec = {"level": "clear", "text": "Replacement in kind: no facet fingerprint moved. "
                                         "Exempt from MOC."}
    elif n_broken:
        rec = {"level": "action-required",
               "text": f"{tier} change. {n_broken} knowledge item(s) depend on an asset this "
                       f"change removes; re-author or retire them before authorisation."}
    elif k or a["procedures"] or a["alarms"]:
        rec = {"level": "review",
               "text": f"{tier} change (R = {a['risk']['R']}). {len(k)} knowledge item(s), "
                       f"{len(a['procedures'])} procedure(s) and {len(a['alarms'])} alarm "
                       f"limit(s) must be re-confirmed; the rest carries over."}
    else:
        rec = {"level": "clear", "text": "No encoded knowledge, procedure or alarm depends on "
                                         "what this change touches."}
    a.update({
        "kind": get_scenario(scenario_name).kind,
        "impacted": [{"entry_id": x["id"], "title": x["title"], "health": x["health"],
                      "confidence_before": x["conf_before"], "confidence_after": x["conf_after"],
                      "reasons": x["reasons"]} for x in k],
        "impacted_count": len(k), "n_broken": n_broken, "n_review": n_review,
        "unaffected": a["corpus_size"] - len(k), "recommendation": rec,
    })
    return a


# ---------------------------------------------------------------------------
# workflow
# ---------------------------------------------------------------------------

def raise_moc(scenario_name: str, *, originator: str = "engineer", title: str = "",
              reason: str = "", moc_type: str = "permanent", expires_days: int = 30) -> dict:
    ensure_dirs()
    a = assess(scenario_name)
    sc = SCENARIOS.get(scenario_name)
    now = datetime.now()
    status = "closed" if a["replacement_in_kind"] else "in_review"
    rec = {
        "moc_id": _next_moc_id(), "status": status, "type": moc_type,
        "title": title or (sc.description if sc else scenario_name),
        "scenario": scenario_name, "moc_object": a["moc_object"], "moc_class": a["moc_class"],
        "originator": originator, "reason": reason,
        "tier": a["risk"]["tier"], "required_signoffs": a["approvers"],
        "signoffs": {}, "pssr": {item: None for item in PSSR_TEMPLATE} if a["pssr_required"] else {},
        "verification": None, "assessment": a,
        "expires_at": (now + timedelta(days=expires_days)).isoformat(timespec="seconds")
        if moc_type == "temporary" else "",
        "retro_review_due": (now + timedelta(hours=EMERGENCY_REVIEW_H)).isoformat(timespec="seconds")
        if moc_type == "emergency" else "",
        "decided_by": "", "decision_note": "", "created_at": now_iso(), "decided_at": "",
        "history": [{"t": now_iso(), "status": status, "by": originator}],
    }
    _save(rec)
    audit("raised", rec["moc_id"], originator,
          {"scenario": scenario_name, "tier": rec["tier"], "type": moc_type,
           "change_set": a["change_set"]})
    return rec


def sign(moc_id: str, signer: str, decision: str, note: str = "") -> dict:
    """One role's sign-off. Approved when all required roles approve."""
    rec = _get_or_raise(moc_id)
    if rec["status"] != "in_review":
        raise ValueError(f"{moc_id} is {rec['status']}, not in review")
    if decision not in ("approved", "rejected"):
        raise ValueError("decision must be approved or rejected")
    rec["signoffs"][signer] = {"decision": decision, "note": note, "t": now_iso()}
    audit(f"signoff:{decision}", moc_id, signer, {"note": note})
    if decision == "rejected":
        _move(rec, "rejected", signer, note)
    elif all(rec["signoffs"].get(r, {}).get("decision") == "approved"
             for r in rec["required_signoffs"]):
        _move(rec, "approved", signer, "all required sign-offs received")
    _save(rec)
    return rec


def decide_moc(moc_id: str, *, decision: str, approver: str = "approver", note: str = "") -> dict:
    """Single-click decision from the hub: the approver signs for every required role."""
    rec = _get_or_raise(moc_id)
    if decision == "rejected":
        rec = sign(moc_id, approver, "rejected", note)
    else:
        for r in rec["required_signoffs"]:
            rec = sign(moc_id, r, "approved", note or f"approved via hub by {approver}")
            if rec["status"] != "in_review":
                break
        if rec["status"] == "in_review":              # no required roles
            _move(rec, "approved", approver, note)
    rec["decided_by"] = approver
    _save(rec)
    return rec


def implement(moc_id: str, by: str = "operations") -> dict:
    rec = _get_or_raise(moc_id)
    if rec["status"] != "approved" and rec["type"] != "emergency":
        raise ValueError("only an approved (or emergency) change can be implemented")
    _move(rec, "implemented", by)
    _save(rec)
    return rec


def complete_pssr(moc_id: str, results: dict[str, bool] | None = None, by: str = "P10") -> dict:
    rec = _get_or_raise(moc_id)
    for item in rec["pssr"]:
        rec["pssr"][item] = True if results is None else bool(results.get(item, False))
    if all(rec["pssr"].values()):
        _move(rec, "pssr_complete", by)
    _save(rec)
    return rec


def verify_change(moc_id: str) -> dict:
    """Compare what the plant did after the change against what was predicted."""
    from .model_moc import DATA_EFFECTS
    from .unmanaged import verify
    rec = _get_or_raise(moc_id)
    a = rec["assessment"]
    expected = {r.split(":")[1] for r in a["change_set"]} | {
        p["asset"] for p in a.get("physical", [])}
    effects = DATA_EFFECTS.get(rec["scenario"], {})
    v = verify(expected, effects) if effects else {"note": "no measurable data effect to verify"}
    rec["verification"] = v
    _move(rec, "reopened" if v.get("unanticipated") else "verified", "verifier")
    _save(rec)
    return rec


def close_moc(moc_id: str, by: str = "P12") -> dict:
    rec = _get_or_raise(moc_id)
    blockers = []
    if rec["status"] not in ("verified", "pssr_complete", "implemented"):
        blockers.append(f"status is {rec['status']}")
    if rec["pssr"] and not all(rec["pssr"].values()):
        blockers.append("PSSR incomplete")
    if (rec.get("verification") or {}).get("unanticipated"):
        blockers.append("unanticipated impact found in verification")
    if blockers:
        raise ValueError("cannot close: " + "; ".join(blockers))
    _move(rec, "closed", by)
    _save(rec)
    return rec


def overdue() -> list[dict]:
    """Temporary changes past expiry and emergency changes past their review window."""
    now = datetime.now().isoformat(timespec="seconds")
    out = []
    for r in list_moc():
        if r["status"] == "closed":
            continue
        if r.get("expires_at") and r["expires_at"] < now:
            out.append({"moc_id": r["moc_id"], "why": "temporary change past expiry"})
        if r.get("retro_review_due") and r["retro_review_due"] < now and r["status"] != "approved":
            out.append({"moc_id": r["moc_id"], "why": "emergency change past retrospective review"})
    return out


def _move(rec, status, by, note=""):
    rec["status"] = status
    rec.setdefault("history", []).append({"t": now_iso(), "status": status, "by": by, "note": note})
    if status in ("approved", "rejected"):
        rec["decided_at"] = now_iso()
        rec["decision_note"] = note
    audit(f"status:{status}", rec["moc_id"], by, {"note": note})


def _get_or_raise(moc_id):
    rec = get_moc(moc_id)
    if rec is None:
        raise KeyError(f"unknown MOC record '{moc_id}'")
    for k, v in (("history", []), ("signoffs", {}), ("required_signoffs", []),
                 ("pssr", {}), ("type", "permanent")):
        rec.setdefault(k, v)
    return rec


def get_moc(moc_id: str) -> dict | None:
    p = _path(moc_id)
    if not os.path.isfile(p):
        return None
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def list_moc(status: str | None = None) -> list[dict]:
    ensure_dirs()
    out = []
    for p in sorted(glob.glob(os.path.join(MOC_DIR, "moc-*.json"))):
        with open(p, encoding="utf-8") as f:
            rec = json.load(f)
        if status and rec.get("status") != status:
            continue
        out.append(rec)
    out.sort(key=lambda r: r.get("created_at", ""), reverse=True)
    return out


# ---------------------------------------------------------------------------
# MOC package
# ---------------------------------------------------------------------------

def export_package(moc_id: str) -> str:
    """Write the MOC dossier as Markdown and return its path."""
    rec = _get_or_raise(moc_id)
    a = rec["assessment"]
    r = a["risk"]
    L = [f"# MOC package {rec['moc_id']}: {rec['title']}", "",
         f"- **Object of change:** {rec['moc_object']} ({rec['moc_class']})",
         f"- **Type:** {rec['type']}   **Status:** {rec['status']}   **Originator:** {rec['originator']}",
         f"- **Risk:** S = {r['S']}, L = {r['L']}, R = {r['R']}  ->  **{r['tier']}**",
         f"- **Severity driven by:** {'; '.join(r['severity_from'])}",
         f"- **Likelihood driven by:** {'; '.join(r['likelihood_from'])}", "",
         "## 1. Change set (computed)", ""]
    L += [f"- `{c}`" for c in a["change_set"]] or ["- none (replacement in kind)"]
    L += ["", "## 2. Knowledge to re-validate", ""]
    L += [f"- **{k['health']}** {k['id']}: {k['title']} (confidence {k['conf_before']} -> "
          f"{k['conf_after']}); reviewers: {', '.join(a['reviewers'].get(k['id'], [])) or 'none qualified'}"
          for k in a["knowledge"]] or ["- none"]
    L += ["", "## 3. Procedures and documents to revise", ""]
    L += [f"- {p['doc_id']} Rev {p['revision']} ({p['type']}): {p['title']}"
          for p in a["procedures"]] or ["- none"]
    L += ["", "## 4. Alarm limits", ""]
    L += [f"- {x['alarm']} ({x['priority']}): {x['old']} -> {x['new']}"
          for x in a["alarms"]] or ["- none changed"]
    if a.get("alarm_replay"):
        rp = a["alarm_replay"]
        L += ["", f"**Alarm replay over the 5-day historian:** activations {rp['total_before']} -> "
                  f"{rp['total_after']}; standing-alarm time {rp['standing_h_before']} h -> "
                  f"{rp['standing_h_after']} h; minimum margin after change "
                  f"{rp['min_margin_after']} sigma."]
        if rp["limit_inside_envelope"]:
            L.append(f"**Warning:** new limit inside the normal operating envelope: "
                     f"{', '.join(rp['limit_inside_envelope'])}.")
    L += ["", "## 5. Physical propagation (most-likely paths)", ""]
    L += [f"- {p['asset']} (score {p['score']}): {' -> '.join(p['path'])}"
          for p in a["physical"][:8]] or ["- no physical disturbance (information-only change)"]
    L += ["", "## 6. Models", ""]
    L += [f"- {m['model']}: {m['verdict']} (moved inputs: {', '.join(m.get('moved_inputs', []))})"
          for m in a["models"]] or ["- no model affected"]
    L += ["", "## 7. Sign-offs", "", "| Role | Decision |", "|---|---|"]
    L += [f"| {s} | {rec['signoffs'].get(s, {}).get('decision', 'pending')} |"
          for s in rec["required_signoffs"]]
    if rec["pssr"]:
        L += ["", "## 8. Pre-startup safety review (PSSR)", ""]
        L += [f"- [{'x' if v else ' '}] {k}" for k, v in rec["pssr"].items()]
        L += ["", "_PSSR per the plant's pre-startup safety check SOP._"]
    os.makedirs(PACKAGE_DIR, exist_ok=True)
    path = os.path.join(PACKAGE_DIR, f"{moc_id}.md")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(L) + "\n")
    audit("package_exported", moc_id, "system", {"path": os.path.basename(path)})
    return path
