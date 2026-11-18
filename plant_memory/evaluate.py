"""
Evaluation — quantify knowledge retention and the cost of change.

The central research claim is that grounded memory lets a plant absorb change by
re-validating only the knowledge tied to what changed, instead of rebuilding all
of it. This module measures that:

  * retained fraction per change scenario
  * a simple cost model: relearn-from-scratch vs targeted re-validation
  * a knowledge x scenario drift matrix (which item drifts under which change)

Outputs machine-readable JSON and, if matplotlib is available, publication-style
figures under plant_memory/store/evaluation/.
"""
from __future__ import annotations

import json
import os
from dataclasses import dataclass

from .drift import evaluate_all, summarize
from .paths import EVAL_DIR, ensure_dirs
from .plant_state import load_base_state
from .schema import DriftStatus, EntryHealth
from .simulate import SCENARIOS, Scenario
from .store import load_all


@dataclass
class ScenarioResult:
    name: str
    kind: str
    description: str
    total: int
    intact: int
    review: int
    broken: int
    flagged: int
    retained_fraction: float
    flagged_entries: list[str]


def run_scenario(entries, base, scenario: Scenario) -> ScenarioResult:
    state = scenario.apply(base)
    drifts = evaluate_all(entries, state)
    s = summarize(drifts)
    flagged = [d.entry_id for d in drifts if d.is_flagged]
    return ScenarioResult(
        name=scenario.name, kind=scenario.kind, description=scenario.description,
        total=s["total"], intact=s["intact"], review=s["review"], broken=s["broken"],
        flagged=s["flagged"], retained_fraction=s["retained_fraction"],
        flagged_entries=flagged,
    )


def cost_model(results: list[ScenarioResult], cost_per_item: float = 1.0) -> dict:
    """Relearn-from-scratch vs targeted re-validation, aggregated over scenarios.

    Relearn-from-scratch: every change forces re-validating the entire corpus.
    Targeted (PlantMemory): only flagged items are re-validated.
    """
    n_changes = len(results)
    if not n_changes:
        return {}
    total = results[0].total
    relearn_cost = sum(total for _ in results) * cost_per_item
    targeted_cost = sum(r.flagged for r in results) * cost_per_item
    savings = relearn_cost - targeted_cost
    return {
        "scenarios": n_changes,
        "corpus_size": total,
        "cost_per_item": cost_per_item,
        "relearn_from_scratch_cost": round(relearn_cost, 2),
        "targeted_revalidation_cost": round(targeted_cost, 2),
        "absolute_savings": round(savings, 2),
        "savings_fraction": round(savings / relearn_cost, 3) if relearn_cost else 0.0,
        "avg_retained_fraction": round(
            sum(r.retained_fraction for r in results) / n_changes, 3),
    }


def drift_matrix(entries, base) -> dict:
    """For each entry x scenario, the drift status (for the heatmap)."""
    scen_names = list(SCENARIOS.keys())
    matrix = {}
    for e in entries:
        row = {}
        for name in scen_names:
            state = SCENARIOS[name].apply(base)
            from .drift import evaluate_entry
            d = evaluate_entry(e, state)
            row[name] = d.health
        matrix[e.id] = {"title": e.title, "row": row}
    return {"scenarios": scen_names, "entries": matrix}


def evaluate_full(cost_per_item: float = 1.0, make_plots: bool = True) -> dict:
    ensure_dirs()
    entries = load_all()
    base = load_base_state(with_data_stats=True)
    results = [run_scenario(entries, base, sc) for sc in SCENARIOS.values()]
    cost = cost_model(results, cost_per_item)
    matrix = drift_matrix(entries, base)

    report = {
        "corpus_size": len(entries),
        "scenarios": [r.__dict__ for r in results],
        "cost_model": cost,
        "drift_matrix": matrix,
    }
    with open(os.path.join(EVAL_DIR, "evaluation.json"), "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    if make_plots:
        try:
            _make_plots(results, cost, matrix)
            report["plots"] = ["retention_by_scenario.png", "cost_comparison.png",
                               "drift_matrix.png"]
        except Exception as exc:
            report["plots_error"] = str(exc)
    return report


# ---------------------------------------------------------------------------
# Figures
# ---------------------------------------------------------------------------

def _make_plots(results, cost, matrix):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import numpy as np

    ink, review_c, broken_c, intact_c = "#1f2937", "#f59e0b", "#ef4444", "#10b981"

    # 1) retention by scenario
    fig, ax = plt.subplots(figsize=(9, 4.5))
    names = [r.name for r in results]
    retained = [r.retained_fraction * 100 for r in results]
    flagged = [100 - x for x in retained]
    ax.bar(names, retained, color=intact_c, label="retained")
    ax.bar(names, flagged, bottom=retained, color=review_c, label="flagged for review")
    ax.set_ylabel("% of knowledge")
    ax.set_title("Knowledge retained vs flagged after each plant change")
    ax.set_ylim(0, 100)
    ax.legend(loc="lower right")
    plt.xticks(rotation=35, ha="right")
    plt.tight_layout()
    fig.savefig(os.path.join(EVAL_DIR, "retention_by_scenario.png"), dpi=140)
    plt.close(fig)

    # 2) cost comparison
    fig, ax = plt.subplots(figsize=(6, 4.5))
    labels = ["Relearn from\nscratch", "PlantMemory\n(targeted)"]
    vals = [cost["relearn_from_scratch_cost"], cost["targeted_revalidation_cost"]]
    bars = ax.bar(labels, vals, color=[broken_c, intact_c])
    ax.set_ylabel(f"re-validation effort (items x {cost['cost_per_item']})")
    ax.set_title(f"Cost of absorbing {cost['scenarios']} plant changes\n"
                 f"{cost['savings_fraction']:.0%} effort saved")
    for b, v in zip(bars, vals):
        ax.text(b.get_x() + b.get_width() / 2, v, str(v), ha="center", va="bottom")
    plt.tight_layout()
    fig.savefig(os.path.join(EVAL_DIR, "cost_comparison.png"), dpi=140)
    plt.close(fig)

    # 3) drift matrix heatmap
    scen = matrix["scenarios"]
    ids = list(matrix["entries"].keys())
    code = {EntryHealth.INTACT: 0, EntryHealth.REVIEW: 1, EntryHealth.BROKEN: 2}
    grid = np.array([[code[matrix["entries"][i]["row"][s]] for s in scen] for i in ids])
    from matplotlib.colors import ListedColormap
    cmap = ListedColormap([intact_c, review_c, broken_c])
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.imshow(grid, cmap=cmap, aspect="auto", vmin=0, vmax=2)
    ax.set_xticks(range(len(scen)))
    ax.set_xticklabels(scen, rotation=35, ha="right")
    ax.set_yticks(range(len(ids)))
    ax.set_yticklabels(ids)
    ax.set_title("Which knowledge drifts under which change\n"
                 "green=intact  amber=review  red=broken")
    plt.tight_layout()
    fig.savefig(os.path.join(EVAL_DIR, "drift_matrix.png"), dpi=140)
    plt.close(fig)


if __name__ == "__main__":
    rep = evaluate_full()
    print(json.dumps(rep["cost_model"], indent=2))
