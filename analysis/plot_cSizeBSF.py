#!/usr/bin/env python3
"""
Quick helper to visualise *cluster size* vs *bound-sticker fraction* (BSF)
for **one** LAMMPS ``final_state_*.DATA`` snapshot.

Typical usage
-------------
>>> from analysis.plot_cSizeBSF import plot_cSizeBSF
>>> plot_bsf("final_state_Run1.DATA")     # shows the figure

The helper is intentionally lightweight: no CLI, no batch mode – just one
function that returns the Matplotlib ``Axes`` so the caller can style or
save the figure as desired.
"""

from __future__ import annotations

from pathlib import Path
from collections import defaultdict
from typing import Optional

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes import Axes


# ──────────────────────────────────────────────────────────────────────────
# low-level parsers
# ──────────────────────────────────────────────────────────────────────────
def _parse_snapshot(path: Path) -> tuple[dict[int, int], dict[int, int], list[tuple[int, int]]]:
    """
    Read a LAMMPS ``*.DATA`` file and extract minimal topology.

    Returns
    -------
    id2mol : dict[int, int]
        Atom-ID → molecule-ID.
    id2type : dict[int, int]
        Atom-ID → atom type.
    bonds : list[tuple[int, int]]
        List of bonded atom pairs as ID tuples (order doesn’t matter).
    """
    id2mol, id2type, bonds = {}, {}, []
    section = None

    with path.open() as fh:
        for raw in fh:
            line = raw.strip()
            llow = line.lower()

            if llow.startswith("atoms"):
                section = "atoms"
                continue
            if llow.startswith("bonds"):
                section = "bonds"
                continue
            if llow.startswith(("angles", "velocities", "masses", "pair coeffs", "angle coeffs")):
                section = None
                continue
            if not line:
                continue

            if section == "atoms" and line[0].isdigit():
                aid, mid, atype = map(int, line.split()[:3])
                id2mol[aid] = mid
                id2type[aid] = atype

            elif section == "bonds" and line[0].isdigit():
                parts = line.split()
                if len(parts) >= 4:
                    bonds.append((int(parts[2]), int(parts[3])))

    return id2mol, id2type, bonds


def _clusters_with_bsf(id2mol: dict[int, int],
                       id2type: dict[int, int],
                       bonds: list[tuple[int, int]]) -> list[tuple[int, float]]:
    """
    Identify clusters and compute their BSF.

    Returns
    -------
    list[tuple[int, float]]
        Each tuple is ``(cluster_size_in_chains, bsf)``.
    """
    if not id2mol:
        return []

    # union–find over atoms
    atom_ids = list(id2mol)
    id2idx = {aid: i for i, aid in enumerate(atom_ids)}
    parent = list(range(len(atom_ids)))

    def find(i: int) -> int:
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i

    def union(i: int, j: int) -> None:
        ri, rj = find(i), find(j)
        if ri != rj:
            parent[rj] = ri

    for a, b in bonds:
        if a in id2idx and b in id2idx:
            union(id2idx[a], id2idx[b])

    root2atoms: dict[int, list[int]] = defaultdict(list)
    for idx, aid in enumerate(atom_ids):
        root2atoms[find(idx)].append(aid)

    bond_set = {tuple(sorted(pair)) for pair in bonds}
    clusters = []

    for aids in root2atoms.values():
        size = len({id2mol[aid] for aid in aids})  # # of chains in the cluster

        # sticker types: 1 and 3
        n1 = sum(id2type[aid] == 1 for aid in aids)
        n3 = sum(id2type[aid] == 3 for aid in aids)
        possible = min(n1, n3)
        actual = 0

        if possible:
            stickers = [aid for aid in aids if id2type[aid] in (1, 3)]
            for i, a in enumerate(stickers):
                for b in stickers[i + 1:]:
                    if {id2type[a], id2type[b]} == {1, 3}:
                        if tuple(sorted((a, b))) in bond_set:
                            actual += 1

        bsf = actual / possible if possible else 0.0
        clusters.append((size, bsf))

    return clusters


# ──────────────────────────────────────────────────────────────────────────
# public helper
# ──────────────────────────────────────────────────────────────────────────
def plot_cSizeBSF(snapshot_file: str | Path,
             ax: Optional[Axes] = None,
             colour: str = "tab:blue") -> Axes:
    """
    Scatter-plot *cluster size* vs *bound-sticker fraction* for one snapshot.

    Parameters
    ----------
    snapshot_file
        Path to a ``final_state_*.DATA`` file.
    ax
        Existing Matplotlib ``Axes`` to draw on.  If *None* (default) a new
        ``Figure`` + ``Axes`` is created.
    colour
        Matplotlib-compatible colour for the markers.

    Returns
    -------
    matplotlib.axes.Axes
        The axis containing the plotted data.
    """
    snapshot_file = Path(snapshot_file)
    id2mol, id2type, bonds = _parse_snapshot(snapshot_file)
    clusters = _clusters_with_bsf(id2mol, id2type, bonds)

    xs = [c[0] for c in clusters]
    ys = [c[1] for c in clusters]

    if ax is None:
        _, ax = plt.subplots()

    if xs:
        ax.scatter(xs, ys, s=20, alpha=0.75, color=colour)
    else:
        ax.text(0.5, 0.5, "no data", ha="center", va="center",
                fontsize=9, color="grey")
        ax.set_facecolor("#f7f7f7")

    ax.set_xlabel("Cluster size (chains)")
    ax.set_ylabel("Bound-sticker fraction (BSF)")
    ax.set_title(snapshot_file.name)
    ax.set_xlim(0.5, max(xs, default=1) + 0.5)
    ax.set_ylim(0.0, 1.05)
    ax.grid(True, linestyle=":", linewidth=0.4)

    return ax
