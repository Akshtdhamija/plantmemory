"""Core guarantees of PlantMemory's computable MOC, checked on the real boiler data."""
import json

import pytest

from plant_memory import alarm_replay, mocgraph, moc, plantdata
from plant_memory.drift import evaluate_all
from plant_memory.plant_state import load_base_state
from plant_memory.simulate import SCENARIOS
from plant_memory.store import load_all


@pytest.fixture(scope="module")
def base():
    return load_base_state(with_data_stats=True)


def test_null_change_flags_nothing(base):
    health = [getattr(d.health, "value", d.health) for d in evaluate_all(load_all(), base)]
    assert health and all(h == "intact" for h in health)


@pytest.mark.parametrize("name", list(SCENARIOS))
def test_flagged_equals_affected(base, name):
    """Locality: the flagged set equals the set grounded to a moved facet."""
    after = SCENARIOS[name].apply(base)
    delta = {(r, f) for _, r, f in mocgraph.diff_states(base, after)}
    entries = load_all()
    truth = {e.id for e in entries if any((g.ref, g.aspect) in delta for g in e.groundings)}
    flagged = {d.entry_id for d in evaluate_all(entries, after)
               if getattr(d.health, "value", d.health) != "intact"}
    assert flagged == truth


def test_replacement_in_kind_is_computed(base):
    assert mocgraph.is_replacement_in_kind(base, SCENARIOS["idf_bearing_rik"].apply(base))
    assert not mocgraph.is_replacement_in_kind(base, SCENARIOS["idf_bearing_upgrade"].apply(base))


def test_alarm_replay_reproduces_the_log():
    from collections import Counter
    r = alarm_replay.replay()
    log = Counter((a["tag"], a["level"]) for a in plantdata.alarms())
    assert r["total"] == len(plantdata.alarms())
    assert all(log[k] == v["activations"] for k, v in r["per_alarm"].items())


def test_max_product_propagation_is_exact():
    adj = {"a": [("b", 0.5, "x"), ("c", 0.9, "x")], "c": [("b", 0.9, "x")]}
    reach = mocgraph.propagate({"a": 1.0}, adj, theta=0.0)
    assert reach["b"]["score"] == pytest.approx(0.81)          # via c, not the direct 0.5
    assert reach["b"]["prev"] == "c"


def test_confidence_decay_matches_hand_derivation(base):
    e = next(x for x in load_all() if x.id == "km-0003")       # IDF bearing-wear entry
    d = next(x for x in evaluate_all([e], SCENARIOS["idf_bearing_upgrade"].apply(base)))
    assert d.confidence == pytest.approx(0.88 * (1 - 4 * 0.35 / 5), abs=1e-3)


def test_audit_chain_detects_tampering(tmp_path, monkeypatch):
    log = tmp_path / "audit.log"
    monkeypatch.setattr(moc, "AUDIT_LOG", str(log))
    for i in range(4):
        moc.audit("event", f"moc-{i:04d}", "tester", {"i": i})
    assert moc.verify_audit()["ok"]
    rows = log.read_text().splitlines()
    r = json.loads(rows[1]); r["actor"] = "intruder"
    rows[1] = json.dumps(r, sort_keys=True, separators=(",", ":"))
    log.write_text("\n".join(rows) + "\n")
    res = moc.verify_audit()
    assert not res["ok"] and res["broken_at"] == 1
