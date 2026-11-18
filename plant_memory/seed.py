"""
Seed the knowledge store with realistic, grounded diagnostic knowledge.

These entries represent the kind of institutional knowledge a plant accumulates
over years of operation: known failure modes, diagnosed root causes, and
corrective actions. Each is grounded to the specific tags / equipment it
depends on, so drift detection can reason about them. In production this content
would instead accrete from real agent investigations via `capture` and `inbox`.
"""
from __future__ import annotations

from .drift import stamp_groundings
from .plant_state import load_base_state
from .schema import Grounding, KnowledgeEntry
from .store import save_entry


def _g(kind, ref, aspect, note=""):
    return Grounding(kind=kind, ref=ref, aspect=aspect, note=note)


def _seed_entries() -> list[KnowledgeEntry]:
    E = []

    E.append(KnowledgeEntry(
        id="km-0001",
        title="High steam temperature from desuperheater spray valve sticking",
        category="root_cause",
        statement="Steam outlet temperature excursions above 545 °C are most often caused by the primary desuperheater spray valve sticking closed, not by over-firing.",
        body=("When TE_8332A drifts above its normal band while main steam flow and firing are "
              "steady, suspect the desuperheater spray path before the combustion side. A "
              "sticking TV_8329ZC keeps desuperheating water flow (YJJWSLL) low despite a rising "
              "temperature error, so the loop cannot pull the temperature back.\n\n"
              "Per trb_high_steam_temperature (Rev 3.1): confirm valve response against controller "
              "demand before adjusting firing."),
        corrective_actions=[
            "Stroke-test TV_8329ZC against controller demand; free or replace the actuator if it lags.",
            "Verify desuperheating water flow YJJWSLL responds when the valve opens.",
            "Hold firing steady until the spray path is confirmed healthy to avoid masking the fault.",
        ],
        groundings=[
            _g("tag", "TE_8332A", "normal_range", "excursion defined against the 530–545 °C band"),
            _g("tag", "TE_8332A", "setpoints", "Hi/HiHi alarm thresholds define the excursion"),
            _g("tag", "TV_8329ZC", "presence", "spray valve is the implicated actuator"),
            _g("tag", "YJJWSLL", "presence", "desuperheating water flow is the corrective path"),
            _g("kg_node", "steam_water_system", "connections", "desuperheater sits in this system"),
        ],
        evidence=["trb_high_steam_temperature Rev 3.1", "investigation 2022-03-29"],
        confidence=0.9, tags_referenced=["TE_8332A", "TV_8329ZC", "YJJWSLL"], source="seed",
        author="plant SME",
    ))

    E.append(KnowledgeEntry(
        id="km-0002",
        title="Low steam temperature from excess desuperheating during load swings",
        category="root_cause",
        statement="Steam temperature dips below 530 °C during load swings are usually excess desuperheating, not loss of firing.",
        body=("On a falling load the desuperheater can over-inject before the controller catches up, "
              "pulling TE_8332A below its band. Check YJJWSLL against load before assuming a bed or "
              "combustion problem."),
        corrective_actions=[
            "Reduce desuperheating water flow YJJWSLL rate-limit during load-down transients.",
            "Retune the steam-temperature loop for asymmetric load ramps.",
        ],
        groundings=[
            _g("tag", "TE_8332A", "normal_range", "dip defined against the 530–545 °C band"),
            _g("tag", "TE_8332A", "setpoints", "Lo alarm threshold defines the dip"),
            _g("tag", "YJJWSLL", "presence", "over-injection is the cause"),
            _g("tag", "ZZQBCHLL", "presence", "main steam flow indicates load"),
        ],
        evidence=["trb_low_steam_temperature Rev 2.4"],
        confidence=0.82, tags_referenced=["TE_8332A", "YJJWSLL", "ZZQBCHLL"], source="seed",
        author="plant SME",
    ))

    E.append(KnowledgeEntry(
        id="km-0003",
        title="IDF high vibration from bearing wear",
        category="failure_mode",
        statement="A slow rise in induced-draft-fan bearing vibration toward the 4.5 mm/s alarm indicates progressive bearing wear and should be trended, not ignored.",
        body=("YFJ3_ZD1 and YFJ3_ZD2 climbing over days — while motor current YFJ3_AI stays normal — "
              "points to mechanical bearing degradation rather than an aerodynamic or load issue. "
              "Per mnt_idf_bearing_inspection (Rev 1.8), schedule inspection before the Alarm level."),
        corrective_actions=[
            "Trend YFJ3_ZD1/ZD2; schedule bearing inspection before the 4.5 mm/s Alarm level.",
            "Check lubrication and bearing temperature per mnt_idf_bearing_inspection Rev 1.8.",
        ],
        groundings=[
            _g("tag", "YFJ3_ZD1", "setpoints", "Alert/Alarm/Trip thresholds define the escalation"),
            _g("tag", "YFJ3_ZD2", "setpoints", "second bearing point"),
            _g("tag", "YFJ3_AI", "presence", "normal current rules out load-side cause"),
            _g("kg_node", "induced_draft_fan", "presence", "the affected equipment"),
            _g("kg_node", "induced_draft_fan", "connections", "draft-control coupling matters"),
        ],
        evidence=["mnt_idf_bearing_inspection Rev 1.8", "trb_idf_high_vibration Rev 2.0"],
        confidence=0.88, tags_referenced=["YFJ3_ZD1", "YFJ3_ZD2", "YFJ3_AI"], source="seed",
        author="reliability eng",
    ))

    E.append(KnowledgeEntry(
        id="km-0004",
        title="Backpass fouling signalled by rising economizer flue-gas outlet temperature",
        category="failure_mode",
        statement="A steady multi-day rise in economizer flue-gas outlet temperature (TE_8319A/B) is the earliest indicator of backpass fouling.",
        body=("As backpass surfaces foul, heat transfer drops and flue gas leaves the economizer "
              "hotter. This precedes any steam-side symptom, so TE_8319A/B trending is the best "
              "early-warning signal for a soot-blow or wash decision."),
        corrective_actions=[
            "Trend TE_8319A/B daily; schedule soot-blowing when the rise exceeds the review band.",
            "Cross-check against O2 (AIR_8301A/B) to rule out excess-air masking.",
        ],
        groundings=[
            _g("tag", "TE_8319A", "presence", "left economizer outlet gas temp"),
            _g("tag", "TE_8319B", "presence", "right economizer outlet gas temp"),
            _g("tag", "TE_8319A", "setpoints", "Hi threshold bounds the healthy range"),
            _g("kg_node", "economizer", "presence", "the fouling surface"),
        ],
        evidence=["mnt_superheater_tube_inspection Rev 1.2"],
        confidence=0.85, tags_referenced=["TE_8319A", "TE_8319B"], source="seed",
        author="plant SME",
    ))

    E.append(KnowledgeEntry(
        id="km-0005",
        title="Low flue-gas O2 indicates incomplete combustion risk",
        category="convention",
        statement="Flue-gas O2 (AIR_8301A/B) below the 2.0 % Lo setpoint risks incomplete combustion and CO breakthrough; raise excess air before other actions.",
        body=("The economizer-inlet O2 pair is the guardrail for combustion completeness. Sustained "
              "readings near LoLo (1.5 %) warrant immediate excess-air correction."),
        corrective_actions=[
            "Increase secondary air (FT_8302) to restore O2 above the 2.0 % Lo setpoint.",
            "Verify both O2 analyzers agree; a single-sided reading may indicate analyzer drift.",
        ],
        groundings=[
            _g("tag", "AIR_8301A", "setpoints", "LoLo/Lo O2 guardrails"),
            _g("tag", "AIR_8301B", "setpoints", "right analyzer guardrails"),
            _g("tag", "FT_8302", "presence", "secondary air is the corrective lever"),
            _g("kg_node", "combustion_system", "presence", "combustion completeness"),
        ],
        evidence=["ctrl_alarm_setpoint_register Rev 4.2"],
        confidence=0.8, tags_referenced=["AIR_8301A", "AIR_8301B", "FT_8302"], source="seed",
        author="controls eng",
    ))

    E.append(KnowledgeEntry(
        id="km-0006",
        title="Furnace draft instability from draft-control coupling",
        category="root_cause",
        statement="Oscillating upper-furnace pressure (PT_8313A–F) with steady firing points to a draft-control loop / IDF coupling problem, not a combustion upset.",
        body=("When the six furnace-pressure points swing together while combustion is steady, the "
              "furnace-draft control loop and its IDF actuator are the suspects. Check loop tuning "
              "and IDF response per ctrl_furnace_draft_loop."),
        corrective_actions=[
            "Review furnace-draft loop tuning; check for IDF damper/VFD hunting.",
            "Confirm PT_8313A–F sensors agree; a single outlier suggests a sensor fault instead.",
        ],
        groundings=[
            _g("tag", "PT_8313A", "setpoints", "furnace pressure alarm band"),
            _g("tag", "PT_8313D", "setpoints", "furnace pressure alarm band"),
            _g("kg_node", "draft_system", "connections", "draft-control coupling"),
            _g("kg_node", "furnace_draft_control_loop", "presence", "the implicated loop"),
        ],
        evidence=["ctrl_furnace_draft_loop Rev 1.5"],
        confidence=0.78, tags_referenced=["PT_8313A", "PT_8313D"], source="seed",
        author="controls eng",
    ))

    E.append(KnowledgeEntry(
        id="km-0007",
        title="Cyclone separator ΔP loss indicates solids carryover",
        category="failure_mode",
        statement="A drop in cyclone separator differential pressure (ZCLCCY/YCLCCY) below the healthy band signals loss of solids capture and bed inventory carryover.",
        body=("Falling cyclone ΔP means the separator is passing solids, degrading combustion "
              "efficiency and loading the backpass. Correlate with hearth ΔP (SXLTCYZ/YY)."),
        corrective_actions=[
            "Inspect cyclone per mnt_cyclone_inspection; check for refractory or dipleg issues.",
            "Cross-check hearth ΔP SXLTCYZ/SXLTCYY for bed-inventory loss.",
        ],
        groundings=[
            _g("tag", "ZCLCCY", "setpoints", "cyclone ΔP healthy band"),
            _g("tag", "YCLCCY", "setpoints", "right cyclone ΔP"),
            _g("kg_node", "cyclone_separator_left", "presence", "the affected equipment"),
        ],
        evidence=["mnt_cyclone_inspection Rev 1.1"],
        confidence=0.8, tags_referenced=["ZCLCCY", "YCLCCY"], source="seed",
        author="reliability eng",
    ))

    E.append(KnowledgeEntry(
        id="km-0008",
        title="IDF motor current spike from downstream restriction",
        category="root_cause",
        statement="A rise in IDF motor current (YFJ3_AI) toward the 280 A alarm with stable vibration usually means increased draft resistance (fouling/damper), not a bearing problem.",
        body=("Distinguish current-side from mechanical faults: high YFJ3_AI with normal YFJ3_ZD1/ZD2 "
              "implies the fan is working harder against downstream resistance."),
        corrective_actions=[
            "Inspect downstream flue path and dampers for restriction/fouling.",
            "Confirm YFJ3_ZD1/ZD2 remain normal to exclude a mechanical cause.",
        ],
        groundings=[
            _g("tag", "YFJ3_AI", "setpoints", "Alarm/Trip current thresholds"),
            _g("tag", "YFJ3_ZD1", "presence", "normal vibration excludes mechanical cause"),
            _g("kg_node", "induced_draft_fan", "connections", "downstream flue path"),
        ],
        evidence=["ds_induced_draft_fan Rev 2.2"],
        confidence=0.76, tags_referenced=["YFJ3_AI", "YFJ3_ZD1"], source="seed",
        author="reliability eng",
    ))

    E.append(KnowledgeEntry(
        id="km-0009",
        title="Low primary air flow degrades bed fluidization",
        category="failure_mode",
        statement="Primary fan outlet flow (FT_8301) near its Lo setpoint threatens bed fluidization and can trigger temperature and pressure instability across the furnace.",
        body=("Adequate primary air is the precondition for stable fluidization. A drop toward the "
              "70,000 m³/h Lo threshold should be treated as a leading indicator for combustion "
              "instability."),
        corrective_actions=[
            "Restore primary fan output above the Lo setpoint before adjusting fuel.",
            "Check primary air preheater outlet temp TE_8303 for coupled effects.",
        ],
        groundings=[
            _g("tag", "FT_8301", "setpoints", "LoLo/Lo primary-air guardrails"),
            _g("tag", "TE_8303", "presence", "preheat coupling"),
            _g("kg_node", "primary_air_system", "presence", "the affected system"),
        ],
        evidence=["ds_cfb_furnace Rev 1.0"],
        confidence=0.79, tags_referenced=["FT_8301", "TE_8303"], source="seed",
        author="plant SME",
    ))

    E.append(KnowledgeEntry(
        id="km-0010",
        title="Steam drum pressure high-high precedes safety-valve lift",
        category="convention",
        statement="Steam drum pressure (PTCA_8322A) reaching HiHi (10.5 MPa) is the last operator-actionable margin before safety-valve lift; act on firing immediately.",
        body=("Treat the HiHi drum-pressure alarm as an immediate firing-reduction trigger. Per "
              "ds_steam_drum, the margin to relief is small at this point."),
        corrective_actions=[
            "Reduce firing immediately on PTCA_8322A HiHi to arrest the pressure rise.",
            "Verify outlet steam pressure PTCA_8324 tracks and the turbine/vent path is available.",
        ],
        groundings=[
            _g("tag", "PTCA_8322A", "setpoints", "Hi/HiHi/HiHiHi drum-pressure thresholds"),
            _g("tag", "PTCA_8324", "presence", "outlet pressure cross-check"),
            _g("kg_node", "steam_water_system", "presence", "steam side"),
        ],
        evidence=["ds_steam_drum Rev 1.4", "safe_emergency_response Rev 3.0"],
        confidence=0.87, tags_referenced=["PTCA_8322A", "PTCA_8324"], source="seed",
        author="operations",
    ))

    E.append(KnowledgeEntry(
        id="km-0011",
        title="Hearth differential pressure tracks bed inventory",
        category="convention",
        statement="Hearth differential pressure (SXLTCYZ/SXLTCYY) is the primary indicator of bed inventory; a fall below 800 Pa Lo signals inventory loss.",
        body=("Bed inventory cannot be measured directly; hearth ΔP is the proxy. Falling ΔP means "
              "solids are leaving faster than they are returned — check cyclone/return-air path."),
        corrective_actions=[
            "On low hearth ΔP, check return-air chamber flows FT_8306A/B and cyclone capture.",
            "Add bed material per cold-start/inventory procedure if inventory is confirmed low.",
        ],
        groundings=[
            _g("tag", "SXLTCYZ", "setpoints", "hearth ΔP Lo guardrail"),
            _g("tag", "SXLTCYY", "setpoints", "right hearth ΔP"),
            _g("tag", "FT_8306A", "presence", "return-air coupling"),
            _g("kg_node", "combustion_system", "presence", "bed lives here"),
        ],
        evidence=["ds_cfb_furnace Rev 1.0"],
        confidence=0.81, tags_referenced=["SXLTCYZ", "SXLTCYY", "FT_8306A"], source="seed",
        author="plant SME",
    ))

    E.append(KnowledgeEntry(
        id="km-0012",
        title="ML anomaly model baseline assumes March steady-state distribution",
        category="decision",
        statement="The steam-temperature anomaly model was trained on the March steady-state distribution of TE_8332A; a sustained distribution shift invalidates its thresholds.",
        body=("The Isolation-Forest / MSPC baseline encodes the operating distribution of the primary "
              "KPI and its correlated tags at model-build time. If the process moves (feedstock, load "
              "regime, recalibration), the learned normal region no longer applies and the model must "
              "be re-baselined — this entry exists so drift flags that dependency explicitly."),
        corrective_actions=[
            "Re-baseline the anomaly model when TE_8332A distribution drift is confirmed.",
            "Re-validate contribution rankings against the new operating regime.",
        ],
        groundings=[
            _g("tag", "TE_8332A", "distribution", "model baseline depends on the KPI distribution"),
            _g("tag", "TE_8332A", "normal_range", "thresholds tied to the normal band"),
            _g("tag", "ZZQBCHLL", "distribution", "load distribution feeds the model"),
        ],
        evidence=["ml_fault_detection baseline", "mspc_analysis baseline"],
        confidence=0.75, tags_referenced=["TE_8332A", "ZZQBCHLL"], source="seed",
        author="data/ML eng",
    ))

    E.append(KnowledgeEntry(
        id="km-0013",
        title="Secondary air preheater outlet temperature bounds combustion-air quality",
        category="convention",
        statement="Secondary air preheater outlet temperature (TE_8304) outside 145–230 °C degrades combustion-air quality and O2 control stability.",
        body=("Preheat quality couples to combustion stability. Track TE_8304 alongside O2 when "
              "diagnosing combustion-side upsets."),
        corrective_actions=[
            "Check preheater performance if TE_8304 leaves its band.",
            "Correlate with secondary fan flow FT_8302 and O2 trends.",
        ],
        groundings=[
            _g("tag", "TE_8304", "setpoints", "preheat outlet band"),
            _g("tag", "FT_8302", "presence", "secondary air coupling"),
            _g("kg_node", "secondary_air_system", "presence", "the system"),
        ],
        evidence=["ctrl_alarm_setpoint_register Rev 4.2"],
        confidence=0.74, tags_referenced=["TE_8304", "FT_8302"], source="seed",
        author="controls eng",
    ))

    E.append(KnowledgeEntry(
        id="km-0014",
        title="Return-air chamber flow imbalance stresses one furnace side",
        category="failure_mode",
        statement="A persistent left/right imbalance between FT_8306A and FT_8306B loads one side of the furnace and shows up as asymmetric hearth ΔP.",
        body=("The return-air chambers should be balanced. A sustained split indicates a damper or "
              "dipleg problem on the low side and is an early cause of asymmetric bed behaviour."),
        corrective_actions=[
            "Balance return-air dampers to equalize FT_8306A/FT_8306B.",
            "Inspect the low-side dipleg per mnt_cyclone_inspection.",
        ],
        groundings=[
            _g("tag", "FT_8306A", "setpoints", "return-air flow band (left)"),
            _g("tag", "FT_8306B", "setpoints", "return-air flow band (right)"),
            _g("tag", "SXLTCYZ", "presence", "asymmetry shows in hearth ΔP"),
        ],
        evidence=["mnt_cyclone_inspection Rev 1.1"],
        confidence=0.72, tags_referenced=["FT_8306A", "FT_8306B", "SXLTCYZ"], source="seed",
        author="reliability eng",
    ))

    return E


def seed(reset: bool = False) -> int:
    """Write the seed knowledge to the store. Returns the number of entries."""
    base = load_base_state(with_data_stats=True)
    entries = _seed_entries()
    for e in entries:
        stamp_groundings(base, e.groundings)
        save_entry(e)
    return len(entries)


if __name__ == "__main__":
    n = seed()
    print(f"seeded {n} knowledge entries")
