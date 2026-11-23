"""
MOC dependency graph and change-impact propagation.

This is the core of computable Management of Change. It does three things:

1. **Computes the change itself.**  A change is the set of (asset, facet) pairs
   whose fingerprint differs between the plant state before and after:

       Δ(S, S') = { (a, φ) : fp(a, φ, S) ≠ fp(a, φ, S') }

   so a replacement-in-kind is *provable*: Δ = ∅.

2. **Builds a physical propagation graph** from the process knowledge graph.
   Process streams (FLOW), measurement (sensor PART_OF equipment), control
   coupling (FEEDBACK_TO / ACTUATED_BY / CONTROLLED_BY), left/right symmetry and
   KPI influence become weighted directed edges w_e in (0, 1].

3. **Propagates a disturbance** from the changed assets with a max-product
   score, computed exactly by Dijkstra on edge costs -ln w_e:

       s(v) = max over paths p : sources -> v  of  s0(source) * prod_{e in p} w_e

   Every reached node keeps its most-likely path, which is the explanation an
   engineer reads ("IDF -> furnace draft -> O2 analyser").
"""
from __future__ import annotations

import heapq
import math
from collections import defaultdict

from . import plantdata
from .fingerprint import fingerprint
from .plant_state import PlantState

TAG_FACETS = ("presence", "normal_range", "setpoints", "distribution")
NODE_FACETS = ("presence", "connections")

# Engineering priors for physical coupling, one per relation type. They are
# replaced by data-calibrated weights where the historian supports it
# (see calibrate.py).
PRIOR_WEIGHTS = {
    "MEASURES": 0.90,        # equipment state <-> its own sensor
    "FLOW": 0.70,            # downstream along a process stream
    "FLOW_BACK": 0.35,       # upstream (back-pressure, draft) along a stream
    "CONTROL": 0.60,         # sensor -> loop -> actuator, equipment <-> loop
    "SYMMETRIC": 0.60,       # left/right twin equipment and sensors
    "KPI": 0.40,             # documented influence on the steam-temperature KPI
}
THETA = 0.05                 # propagation cut-off: scores below this are noise


# ---------------------------------------------------------------------------
# 1. The change, computed
# ---------------------------------------------------------------------------

def diff_states(before: PlantState, after: PlantState) -> list[tuple[str, str, str]]:
    """All (kind, asset, facet) whose fingerprint differs between two states."""
    out = []
    tags = set(before.tags) | set(after.tags)
    for t in sorted(tags):
        for f in TAG_FACETS:
            a = fingerprint(before, "tag", t, f) if before.tag_exists(t) else "∅"
            b = fingerprint(after, "tag", t, f) if after.tag_exists(t) else "∅"
            if a != b:
                out.append(("tag", t, f))
    nodes = set(before.nodes) | set(after.nodes)
    for n in sorted(nodes):
        for f in NODE_FACETS:
            a = fingerprint(before, "kg_node", n, f) if before.node_exists(n) else "∅"
            b = fingerprint(after, "kg_node", n, f) if after.node_exists(n) else "∅"
            if a != b:
                out.append(("kg_node", n, f))
    return out


def is_replacement_in_kind(before: PlantState, after: PlantState) -> bool:
    """RIK holds exactly when no facet fingerprint moved."""
    return not diff_states(before, after)


# ---------------------------------------------------------------------------
# 2. Physical propagation graph
# ---------------------------------------------------------------------------

def physical_graph(weights: dict | None = None,
                   tag_weights: dict | None = None) -> dict[str, list]:
    """Directed weighted adjacency {u: [(v, w, relation)]} over KG nodes.

    `tag_weights` optionally overrides the weight of the sensor-to-sensor
    coupling with data-calibrated values {(u_tag, v_tag): w}.
    """
    W = dict(PRIOR_WEIGHTS)
    if weights:
        W.update(weights)
    k = plantdata.kg()
    ntype = {n["node_id"]: n["node_type"] for n in k["nodes"]}
    adj: dict[str, list] = defaultdict(list)

    def add(u, v, w, rel):
        if w > 0:
            adj[u].append((v, w, rel))

    for l in k["links"]:
        u, v, et = l["source"], l["target"], l["edge_type"]
        if et == "FLOW":
            add(u, v, W["FLOW"], "flows to")
            add(v, u, W["FLOW_BACK"], "back-pressure on")
        elif et == "PART_OF" and ntype.get(u) == "Sensor":
            add(u, v, W["MEASURES"], "is measured on")      # sensor -> equipment
            add(v, u, W["MEASURES"], "is measured by")      # equipment -> sensor
        elif et in ("FEEDBACK_TO", "ACTUATED_BY", "CONTROLLED_BY"):
            add(u, v, W["CONTROL"], "controls")
            add(v, u, W["CONTROL"], "is controlled with")
        elif et == "SYMMETRIC_PAIR":
            add(u, v, W["SYMMETRIC"], "mirrors")
            add(v, u, W["SYMMETRIC"], "mirrors")
        elif et == "AFFECTS_KPI":
            add(u, v, W["KPI"], "affects")
    if tag_weights:
        for (u, v), w in tag_weights.items():
            add(u, v, w, "co-varies with (data)")
    return adj


def propagate(sources: dict[str, float], adj: dict[str, list],
              theta: float = THETA) -> dict[str, dict]:
    """Max-product propagation, exact via Dijkstra on cost = -ln(score).

    Returns {node: {"score": s, "prev": predecessor, "rel": relation}}.
    """
    best: dict[str, dict] = {}
    heap = []
    for s, s0 in sources.items():
        if s0 > 0:
            heapq.heappush(heap, (-math.log(s0), s, None, None))
    while heap:
        cost, u, prev, rel = heapq.heappop(heap)
        if u in best:
            continue
        score = math.exp(-cost)
        if score < theta:
            break
        best[u] = {"score": score, "prev": prev, "rel": rel}
        for v, w, r in adj.get(u, ()):
            if v not in best:
                heapq.heappush(heap, (cost - math.log(w), v, u, r))
    return best


def explain(node: str, reach: dict[str, dict]) -> list[str]:
    """Most-likely path from a change source to `node`, as readable hops."""
    names = {n["node_id"]: n.get("name", n["node_id"]) for n in plantdata.kg()["nodes"]}
    hops, cur = [], node
    while cur is not None and cur in reach:
        hops.append(names.get(cur, cur))
        cur = reach[cur]["prev"]
    return list(reversed(hops))


def tag_to_tag_scores(adj: dict[str, list] | None = None,
                      theta: float = 0.0) -> dict[tuple[str, str], float]:
    """Graph predictor: s_G(u -> v) for every ordered pair of sensor tags."""
    adj = adj or physical_graph()
    _, tags, _ = plantdata.historian()
    out = {}
    for u in tags:
        reach = propagate({u: 1.0}, adj, theta=max(theta, 1e-6))
        for v in tags:
            if v != u:
                out[(u, v)] = reach.get(v, {}).get("score", 0.0)
    return out


def disturbance_sources(change: list[tuple[str, str, str]]) -> dict[str, float]:
    """Which assets a change physically disturbs, with initial strength s0.

    Alarm limits and normal ranges are information, not physics: changing them
    does not move the process, so they start no physical propagation. Equipment
    rewiring, identity changes and operating-distribution shifts do. Losing a
    sensor that feeds a control loop degrades that loop.
    """
    k = plantdata.kg()
    feeds = defaultdict(list)
    for l in k["links"]:
        if l["edge_type"] == "FEEDBACK_TO":
            feeds[l["source"]].append(l["target"])
    src: dict[str, float] = {}
    for kind, ref, facet in change:
        if kind == "kg_node" and facet in ("connections", "presence"):
            src[ref] = max(src.get(ref, 0), 1.0)
        elif kind == "tag" and facet == "distribution":
            src[ref] = max(src.get(ref, 0), 1.0)
        elif kind == "tag" and facet == "presence":
            for loop in feeds.get(ref, []):
                src[loop] = max(src.get(loop, 0), 0.8)
    return src
