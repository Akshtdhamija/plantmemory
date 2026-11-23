"""
Change simulation — reproducible plant-change scenarios.

Each scenario applies an *override layer* to the base PlantState, standing in for
a real event in the plant's life:

  * sensor recalibration      -> a tag's normal range / setpoints move
  * setpoint retune           -> a single alarm threshold changes
  * equipment upgrade         -> a node's connections/identity change
  * component removal          -> a tag or node disappears
  * distribution / feedstock  -> a tag's operating distribution shifts

Scenarios are the experimental treatments for the evaluation: apply one, run
drift detection, and measure how much knowledge is flagged versus retained.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable

from .plant_state import PlantState, load_base_state


@dataclass
class Scenario:
    name: str
    kind: str                 # recalibration | setpoint | upgrade | removal | distribution | composite
    description: str
    mutate: Callable[[PlantState], PlantState]
    changed_anchors: list[tuple[str, str, str]] = field(default_factory=list)  # (kind,ref,aspect)
    # --- Management-of-Change (MOC) classification ------------------------
    # object  : the MOC "object of change" — material (physical/technical plant
    #           change) vs organisational (procedural / operating-spec / people).
    # moc_class: a readable sub-category for the MOC register.
    moc_object: str = "material"          # "material" | "organisational"
    moc_class: str = "Technical change"

    def apply(self, base: PlantState | None = None) -> PlantState:
        state = (base or load_base_state(with_data_stats=True)).copy()
        state = self.mutate(state)
        state.label = self.name
        return state


# ---------------------------------------------------------------------------
# Override primitives
# ---------------------------------------------------------------------------

def recalibrate_tag(state, tag, new_min=None, new_max=None):
    if tag in state.tags:
        if new_min is not None:
            state.tags[tag]["normal_min"] = new_min
        if new_max is not None:
            state.tags[tag]["normal_max"] = new_max
    return state


def retune_setpoint(state, tag, level, value):
    state.setpoints.setdefault(tag, {})[level] = value
    return state


def shift_distribution(state, tag, mean_factor=1.0, std_factor=1.0):
    st = state.data_stats.get(tag)
    if st:
        st["mean"] = st.get("mean", 0.0) * mean_factor
        st["std"] = st.get("std", 0.0) * std_factor
    else:
        # synthesise a shifted distribution if base stats are unavailable
        state.data_stats[tag] = {"mean": 100.0 * mean_factor, "std": 10.0 * std_factor}
    return state


def upgrade_equipment(state, node_id, rename=None, retype=None,
                      add_edges=None, remove_edges=None):
    """Change a node's identity and/or its connections (an equipment swap)."""
    if node_id in state.nodes:
        if rename:
            state.nodes[node_id] = dict(state.nodes[node_id], name=rename)
        if retype:
            state.nodes[node_id] = dict(state.nodes[node_id], node_type=retype)
        adj = [list(x) for x in state.adjacency.get(node_id, [])]
        for e in (remove_edges or []):
            if list(e) in adj:
                adj.remove(list(e))
        for e in (add_edges or []):
            if list(e) not in adj:
                adj.append(list(e))
        state.adjacency[node_id] = sorted(adj)
    return state


def remove_tag(state, tag):
    state.tags.pop(tag, None)
    state.setpoints.pop(tag, None)
    state.data_stats.pop(tag, None)
    return state


def remove_node(state, node_id):
    state.nodes.pop(node_id, None)
    state.adjacency.pop(node_id, None)
    for nid, adj in state.adjacency.items():
        state.adjacency[nid] = [e for e in adj if e[1] != node_id]
    return state


# ---------------------------------------------------------------------------
# Named scenarios (the professor's cases, made concrete)
# ---------------------------------------------------------------------------

def _s_kpi_rerate(state):
    # Steam-temp KPI re-rated for a new steam contract: band + Hi alarm move.
    recalibrate_tag(state, "TE_8332A", new_min=525.0, new_max=540.0)
    retune_setpoint(state, "TE_8332A", "Hi", 543.0)
    return state


def _s_idf_bearing_upgrade(state):
    # New IDF bearing with tighter vibration spec; draft path re-plumbed.
    retune_setpoint(state, "YFJ3_ZD1", "Alarm", 3.8)
    retune_setpoint(state, "YFJ3_ZD2", "Alarm", 3.8)
    upgrade_equipment(state, "induced_draft_fan",
                      rename="Induced Draft Fan (VFD upgrade)",
                      add_edges=["CONTROLLED_BY", "vfd_controller"])
    return state


def _s_o2_recal(state):
    # Both O2 analyzers recalibrated; Lo guardrail tightened.
    retune_setpoint(state, "AIR_8301A", "Lo", 2.5)
    retune_setpoint(state, "AIR_8301B", "Lo", 2.5)
    return state


def _s_new_feedstock(state):
    # New coal blend shifts the operating distribution of the KPI and load.
    shift_distribution(state, "TE_8332A", mean_factor=1.04)
    shift_distribution(state, "ZZQBCHLL", mean_factor=0.9)
    return state


def _s_economizer_replacement(state):
    # Economizer replaced -> its connections change.
    upgrade_equipment(state, "economizer", rename="Economizer (finned upgrade)",
                      add_edges=["FLOW", "bypass_damper"])
    return state


def _s_drum_setpoint_retune(state):
    retune_setpoint(state, "PTCA_8322A", "HiHi", 10.6)
    return state


def _s_o2_analyzer_bias(state):
    # Left O2 analyser recalibrated with a +10 % span error: limits untouched,
    # but the measured operating distribution moves.
    shift_distribution(state, "AIR_8301A", mean_factor=1.10)
    return state


def _s_idf_bearing_rik(state):
    # Like-for-like IDF bearing swap: same spec, same alarm limits, same wiring.
    # Nothing a fingerprint can see changes, so it is provably replacement-in-kind.
    sp = dict(state.setpoints.get("YFJ3_ZD1", {}))
    retune_setpoint(state, "YFJ3_ZD1", "Alarm", sp.get("Alarm", 4.5))
    return state


def _s_sensor_decommission(state):
    # A furnace-pressure point retired during a DCS migration.
    remove_tag(state, "PT_8313D")
    return state


SCENARIOS: dict[str, Scenario] = {
    "kpi_rerate": Scenario(
        "kpi_rerate", "recalibration",
        "Steam-temperature KPI re-rated (band 525–540 °C, Hi alarm 543 °C) for a new steam contract.",
        _s_kpi_rerate,
        [("tag", "TE_8332A", "normal_range"), ("tag", "TE_8332A", "setpoints")],
        moc_object="organisational", moc_class="Operating-spec change",
    ),
    "idf_bearing_upgrade": Scenario(
        "idf_bearing_upgrade", "upgrade",
        "IDF fitted with new bearings (tighter vibration alarm) and a VFD controller.",
        _s_idf_bearing_upgrade,
        [("tag", "YFJ3_ZD1", "setpoints"), ("tag", "YFJ3_ZD2", "setpoints"),
         ("kg_node", "induced_draft_fan", "connections")],
        moc_object="material", moc_class="Equipment modification",
    ),
    "o2_recal": Scenario(
        "o2_recal", "recalibration",
        "Both flue-gas O2 analyzers recalibrated; Lo guardrail tightened to 2.5 %.",
        _s_o2_recal,
        [("tag", "AIR_8301A", "setpoints"), ("tag", "AIR_8301B", "setpoints")],
        moc_object="material", moc_class="Instrument recalibration",
    ),
    "new_feedstock": Scenario(
        "new_feedstock", "distribution",
        "New coal blend shifts the operating distribution of steam temperature and load.",
        _s_new_feedstock,
        [("tag", "TE_8332A", "distribution"), ("tag", "ZZQBCHLL", "distribution")],
        moc_object="material", moc_class="Feedstock change",
    ),
    "economizer_replacement": Scenario(
        "economizer_replacement", "upgrade",
        "Economizer replaced with a finned upgrade; flue-gas path re-plumbed.",
        _s_economizer_replacement,
        [("kg_node", "economizer", "connections")],
        moc_object="material", moc_class="Equipment replacement",
    ),
    "drum_setpoint_retune": Scenario(
        "drum_setpoint_retune", "setpoint",
        "Steam-drum HiHi pressure setpoint retuned to 10.6 MPa.",
        _s_drum_setpoint_retune,
        [("tag", "PTCA_8322A", "setpoints")],
        moc_object="material", moc_class="Safe-operating-limit change",
    ),
    "sensor_decommission": Scenario(
        "sensor_decommission", "removal",
        "Furnace-pressure point PT_8313D retired during a DCS migration.",
        _s_sensor_decommission,
        [("tag", "PT_8313D", "presence")],
        moc_object="material", moc_class="Instrument decommissioning",
    ),
    "o2_analyzer_bias": Scenario(
        "o2_analyzer_bias", "distribution",
        "Left flue-gas O2 analyser recalibrated with a +10 % span error (limits unchanged).",
        _s_o2_analyzer_bias,
        [("tag", "AIR_8301A", "distribution")],
        moc_object="material", moc_class="Instrument recalibration",
    ),
    "idf_bearing_rik": Scenario(
        "idf_bearing_rik", "replacement",
        "IDF bearing replaced like-for-like (same specification, limits and wiring).",
        _s_idf_bearing_rik,
        [],
        moc_object="material", moc_class="Replacement in kind",
    ),
}


def get_scenario(name: str) -> Scenario:
    if name not in SCENARIOS:
        raise KeyError(f"unknown scenario '{name}'. Available: {', '.join(SCENARIOS)}")
    return SCENARIOS[name]
