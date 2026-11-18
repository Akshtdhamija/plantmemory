"""PlantMemory command-line interface."""
from __future__ import annotations

import argparse
import json
import sys

from . import __version__


def _print_drift_table(drifts, title):
    from .schema import EntryHealth
    icon = {EntryHealth.INTACT: "  ok ", EntryHealth.REVIEW: "REVIEW", EntryHealth.BROKEN: "BROKEN"}
    print(f"\n{title}")
    print("-" * 76)
    for d in drifts:
        mark = icon.get(d.health, "?")
        line = f"[{mark}] {d.entry_id}  {d.title[:52]:52s} conf={d.confidence:.2f}"
        print(line)
        for g in d.groundings:
            if g.status != "intact":
                print(f"        - {g.status.upper()}: {g.detail or g.grounding.key()}")
    print("-" * 76)


def cmd_seed(args):
    from .seed import seed
    n = seed(reset=True)
    print(f"seeded {n} grounded knowledge entries into the store")


def cmd_list(args):
    from .store import load_all
    entries = load_all()
    if args.json:
        print(json.dumps([e.to_dict() for e in entries], indent=2))
        return
    print(f"{len(entries)} knowledge entries")
    for e in entries:
        print(f"  {e.id}  [{e.category:16s}] {e.title}")


def cmd_show(args):
    from .store import load_entry
    e = load_entry(args.id)
    if not e:
        print(f"no entry {args.id}"); return
    print(json.dumps(e.to_dict(), indent=2) if args.json else _entry_text(e))


def _entry_text(e):
    out = [f"# {e.title}  ({e.id})", f"category: {e.category}   confidence: {e.confidence}",
           f"\n{e.statement}\n"]
    if e.body:
        out.append(e.body)
    if e.corrective_actions:
        out.append("\nCorrective actions:")
        out += [f"  {i}. {a}" for i, a in enumerate(e.corrective_actions, 1)]
    out.append("\nGrounded to:")
    out += [f"  - {g.kind}:{g.ref} ({g.aspect})  fp={g.fingerprint}" for g in e.groundings]
    return "\n".join(out)


def cmd_scenarios(args):
    from .simulate import SCENARIOS
    print("available change scenarios:")
    for name, sc in SCENARIOS.items():
        print(f"  {name:24s} [{sc.kind}]  {sc.description}")


def cmd_drift(args):
    from .store import load_all
    from .plant_state import load_base_state
    from .drift import evaluate_all, summarize
    from .simulate import get_scenario
    entries = load_all()
    base = load_base_state(with_data_stats=True)
    state = get_scenario(args.scenario).apply(base) if args.scenario else base
    drifts = evaluate_all(entries, state)
    s = summarize(drifts)
    if args.json:
        print(json.dumps({"summary": s, "entries": [d.to_dict() for d in drifts]}, indent=2))
        return
    label = f"after change '{args.scenario}'" if args.scenario else "against current base state"
    _print_drift_table(drifts, f"Drift {label}")
    print(f"intact={s['intact']}  review={s['review']}  broken={s['broken']}  "
          f"retained={s['retained_fraction']:.0%}")


def cmd_evaluate(args):
    from .evaluate import evaluate_full
    rep = evaluate_full(cost_per_item=args.cost, make_plots=not args.no_plots)
    print(json.dumps(rep["cost_model"], indent=2))
    if "plots" in rep:
        print("figures written to plant_memory/store/evaluation/")


def cmd_capture(args):
    from .capture import capture_from_summary
    e = capture_from_summary(args.path, author=args.author)
    print(f"captured {e.id}: {e.title}")
    print(f"  grounded to {len(e.groundings)} anchors across "
          f"{len(e.tags_referenced)} tags")


def cmd_inbox(args):
    from . import inbox
    if args.inbox_cmd == "list":
        for r in inbox.list_proposals(args.status):
            print(f"  {r['proposal_id']} [{r['status']:8s}] {r['kind']:10s} "
                  f"{r['entry']['title']}")
    elif args.inbox_cmd == "approve":
        e = inbox.approve_proposal(args.id, approver=args.by)
        print(f"approved -> {e.id}: {e.title}")
    elif args.inbox_cmd == "reject":
        inbox.reject_proposal(args.id, reviewer=args.by, reason=args.reason or "")
        print(f"rejected {args.id}")


def cmd_relay(args):
    from . import relay
    if args.relay_cmd == "list":
        for r in relay.list_relays(args.status):
            print(f"  {r['relay_id']} [{r['status']:6s}] {r['title']}  "
                  f"(flagged={r['context']['flagged_count']})")
    elif args.relay_cmd == "create":
        r = relay.create_relay(title=args.title, summary=args.summary or "",
                               from_member=args.by, to=args.to, scenario=args.scenario)
        print(f"created {r['relay_id']} with {r['context']['flagged_count']} "
              f"flagged items to watch")
    elif args.relay_cmd == "take":
        relay.take_relay(args.id, args.by); print(f"{args.id} taken by {args.by}")
    elif args.relay_cmd == "close":
        relay.close_relay(args.id, args.by); print(f"{args.id} closed")


def cmd_hub(args):
    from .hub import run_hub
    run_hub(port=args.port, open_browser=not args.no_open)


def build_parser():
    p = argparse.ArgumentParser(prog="plant_memory",
                                description="PlantMemory — institutional memory for industrial AI")
    p.add_argument("--version", action="version", version=f"PlantMemory {__version__}")
    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("seed", help="seed the store with grounded knowledge").set_defaults(func=cmd_seed)

    sp = sub.add_parser("list", help="list knowledge entries"); sp.add_argument("--json", action="store_true"); sp.set_defaults(func=cmd_list)
    sp = sub.add_parser("show", help="show one entry"); sp.add_argument("id"); sp.add_argument("--json", action="store_true"); sp.set_defaults(func=cmd_show)
    sub.add_parser("scenarios", help="list change scenarios").set_defaults(func=cmd_scenarios)

    sp = sub.add_parser("drift", help="run drift detection"); sp.add_argument("--scenario"); sp.add_argument("--json", action="store_true"); sp.set_defaults(func=cmd_drift)
    sp = sub.add_parser("evaluate", help="run the full evaluation + plots"); sp.add_argument("--cost", type=float, default=1.0); sp.add_argument("--no-plots", action="store_true"); sp.set_defaults(func=cmd_evaluate)
    sp = sub.add_parser("capture", help="capture knowledge from an audit summary.md"); sp.add_argument("path"); sp.add_argument("--author", default="agent"); sp.set_defaults(func=cmd_capture)

    ib = sub.add_parser("inbox", help="knowledge proposals"); ibs = ib.add_subparsers(dest="inbox_cmd", required=True)
    x = ibs.add_parser("list"); x.add_argument("--status")
    x = ibs.add_parser("approve"); x.add_argument("id"); x.add_argument("--by", default="reviewer")
    x = ibs.add_parser("reject"); x.add_argument("id"); x.add_argument("--by", default="reviewer"); x.add_argument("--reason")
    ib.set_defaults(func=cmd_inbox)

    rl = sub.add_parser("relay", help="shift handoffs"); rls = rl.add_subparsers(dest="relay_cmd", required=True)
    x = rls.add_parser("list"); x.add_argument("--status")
    x = rls.add_parser("create"); x.add_argument("--title", required=True); x.add_argument("--summary"); x.add_argument("--by", default="engineer"); x.add_argument("--to", default="team"); x.add_argument("--scenario")
    x = rls.add_parser("take"); x.add_argument("id"); x.add_argument("--by", default="engineer")
    x = rls.add_parser("close"); x.add_argument("id"); x.add_argument("--by", default="engineer")
    rl.set_defaults(func=cmd_relay)

    sp = sub.add_parser("hub", help="launch the web UI"); sp.add_argument("--port", type=int, default=7700); sp.add_argument("--no-open", action="store_true"); sp.set_defaults(func=cmd_hub)
    return p


def main(argv=None):
    # Windows consoles default to cp1252; force UTF-8 so tag/engineering symbols
    # (Δ, °C, →) print instead of crashing.
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")
        except Exception:
            pass
    args = build_parser().parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main(sys.argv[1:])
