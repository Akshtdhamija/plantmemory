"""
MOC for AI models: a process-monitoring model as an asset under change control.

The monitoring model is multivariate statistical process control (MSPC): PCA on
standardised 1-minute means of the boiler tags, trained on normal operation, with

  Hotelling T^2  = sum_{a<=A} t_a^2 / lambda_a
  T^2 limit      = A (n^2 - 1) / (n (n - A)) * F_{alpha}(A, n - A)
  SPE (Q)        = || x - x_hat ||^2 ,  x_hat = P P^T x
  SPE limit      = g * chi^2_{alpha}(h),  g = v / (2m),  h = 2 m^2 / v   (Box 1954)

where m, v are the mean and variance of SPE on the training data. A sample is
flagged when either statistic exceeds its 99 % limit.

The model is *grounded* exactly like knowledge: to the presence and operating
distribution of each input tag. So the same drift engine says when a plant change
invalidates it ("model revalidation required") before it starts raising false
alarms, and a model update is itself a change that needs MOC.
"""
from __future__ import annotations

import numpy as np
from scipy import stats

from . import plantdata
from .calibrate import minute_means
from .drift import evaluate_entry, stamp_groundings
from .plant_state import load_base_state
from .schema import Grounding, KnowledgeEntry

MODEL_ID = "mspc_boiler_v1"
ALPHA = 0.99
VAR_KEEP = 0.90


class MSPCModel:
    def __init__(self, tags):
        self.tags = tags

    def fit(self, M: np.ndarray):
        self.mu = np.nanmean(M, axis=0)
        self.sd = np.nanstd(M, axis=0)
        self.sd[self.sd == 0] = 1.0
        Z = self._z(M)
        U, S, Vt = np.linalg.svd(Z, full_matrices=False)
        lam = S ** 2 / (len(Z) - 1)
        A = int(np.searchsorted(np.cumsum(lam) / lam.sum(), VAR_KEEP) + 1)
        self.P, self.lam, self.A, n = Vt[:A].T, lam[:A], A, len(Z)
        self.t2_lim = A * (n ** 2 - 1) / (n * (n - A)) * stats.f.ppf(ALPHA, A, n - A)
        spe = self._spe(Z)
        m, v = spe.mean(), spe.var()
        g, h = v / (2 * m), 2 * m ** 2 / v
        self.spe_lim = g * stats.chi2.ppf(ALPHA, h)
        return self

    def _z(self, M):
        Z = (M - self.mu) / self.sd
        return np.where(np.isnan(Z), 0.0, Z)

    def _spe(self, Z):
        R = Z - Z @ self.P @ self.P.T
        return (R ** 2).sum(axis=1)

    def score(self, M: np.ndarray) -> dict:
        Z = self._z(M)
        T = Z @ self.P
        t2 = (T ** 2 / self.lam).sum(axis=1)
        spe = self._spe(Z)
        flag = (t2 > self.t2_lim) | (spe > self.spe_lim)
        return {"t2": t2, "spe": spe, "flag": flag,
                "false_alarm_rate": float(flag.mean())}


def _normal_rows(M, tags):
    """Rows of normal operation: KPI inside its 530-545 degC band."""
    k = tags.index("TE_8332A")
    return M[(M[:, k] >= 530) & (M[:, k] <= 545)]


def train() -> tuple[MSPCModel, np.ndarray, np.ndarray, list[str]]:
    """Train on alternating one-hour blocks (even hours), test on the odd hours.

    A plain first-half / second-half split puts different operating regimes on
    each side (the unit drifts over five days), so held-out normal data looks
    abnormal. Interleaved hourly blocks keep train and test disjoint while both
    span the full operating envelope.
    """
    _, tags, X = plantdata.historian()
    M = minute_means(X)
    keep = [j for j in range(M.shape[1]) if np.nanstd(M[:, j]) > 0]
    tags_k = [tags[j] for j in keep]
    M = M[:, keep]
    hour = np.arange(len(M)) // 60
    tr, te = M[hour % 2 == 0], M[hour % 2 == 1]
    model = MSPCModel(tags_k).fit(_normal_rows(tr, tags_k))
    return model, tr, te, tags_k


def operable(M: np.ndarray, tags: list[str], model: MSPCModel) -> bool:
    """A model cannot run if any of its inputs has no data."""
    return all(not np.all(np.isnan(M[:, tags.index(t)])) for t in model.tags)


def model_entry(model: MSPCModel) -> KnowledgeEntry:
    """The model as a grounded asset: presence + distribution of every input."""
    g = []
    for t in model.tags:
        g.append(Grounding(kind="tag", ref=t, aspect="presence",
                           note=f"{MODEL_ID} input"))
        g.append(Grounding(kind="tag", ref=t, aspect="distribution",
                           note=f"{MODEL_ID} trained on this operating distribution"))
    e = KnowledgeEntry(
        id=f"model-{MODEL_ID}", title="MSPC monitoring model (PCA, T2 and SPE)",
        category="decision",
        statement=(f"PCA model with {model.A} components on {len(model.tags)} tags; "
                   f"99% T2 and SPE limits; valid while its input distributions hold."),
        groundings=g, confidence=0.9, source="model_registry", author="P11")
    stamp_groundings(load_base_state(with_data_stats=True), e.groundings)
    return e


def validity(entry: KnowledgeEntry, state) -> dict:
    """PlantMemory's verdict on the model under a (changed) plant state."""
    d = evaluate_entry(entry, state)
    moved = [x.grounding.ref for x in d.groundings if x.status != "intact"]
    verdict = getattr(d.health, "value", d.health)
    return {"verdict": {"intact": "valid", "review": "revalidate",
                        "broken": "broken (input removed)"}[verdict],
            "moved_inputs": sorted(set(moved)), "confidence": d.confidence}


# Data-level transformations that realise a scenario in the measurements.
DATA_EFFECTS = {
    "new_feedstock": {"TE_8332A": ("scale", 1.04), "ZZQBCHLL": ("scale", 0.90)},
    "o2_analyzer_bias": {"AIR_8301A": ("scale", 1.10)},
    "sensor_decommission": {"PT_8313D": ("remove", None)},
}


def apply_effects(M: np.ndarray, tags: list[str], effects: dict) -> np.ndarray:
    M = M.copy()
    for t, (kind, val) in effects.items():
        if t not in tags:
            continue
        j = tags.index(t)
        if kind == "scale":
            M[:, j] = M[:, j] * val
        elif kind == "remove":
            M[:, j] = np.nan
    return M
