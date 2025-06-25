#!/usr/bin/env python3
"""
Plot a histogram of the *number of type-1 ⇄ type-3 sticker bonds* between
every pair of chains in a single LAMMPS ``final_state_*.DATA`` snapshot.

Typical usage
-------------
>>> from analysis.plot_pair_bonds import plot_pair_bond_hist
>>> plot_pair_bond_hist("final_state_Run1.DATA")       # shows the figure
"""

from __future__ import annotations

from pathlib import Path
from typing import Iterable, Optional

import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.axes import Axes


# ──────────────────────────────────────────────────────────────────────────
# internal parser
# ──────────────────────────────────────────────────────────────────────────
def _build_chain_multigraph(snapshot: Path) -> nx.MultiGraph:
    """
    Return a **MultiGraph** whose nodes are molecule IDs and whose *parallel*
    edges correspond to bonds joining a **type-1** atom and a **type-3** atom
    that belong to two *different* molecules.
    """
    atom2mol: dict[int, int]   = {}
    atom2type: dict[int, int]  = {}
    candidate_bonds: list[tuple[int, int]] = []

    section = None
    with snapshot.open() as fh:
        for raw in fh:
            line = raw.strip()
            if not line:
                continue

            low = line.lower()
            if low.startswith("atoms"):
                section = "atoms"
                continue
            if low.startswith("bonds"):
                section = "bonds"
                continue
            if low.startswith(("velocities", "angles", "masses",
                                "pair coeffs", "angle coeffs",
                                "angles", "dihedrals", "impropers")):
                section = None
                continue

            if section == "atoms" and line[0].isdigit():
                aid, mid, atype = map(int, line.split()[:3])
                atom2mol[aid]  = mid
                atom2type[aid] = atype

            elif section == "bonds" and line[0].isdigit():
                # bond line: id  type  atom1 atom2
                _, _btype, a1, a2, *_ = line.split()
                candidate_bonds.append((int(a1), int(a2)))

    # --- build graph -----------------------------------------------------
    G = nx.MultiGraph()
    G.add_nodes_from(set(atom2mol.values()))

    for a1, a2 in candidate_bonds:
        t1, t2 = atom2type.get(a1), atom2type.get(a2)
        if {t1, t2} == {1, 3}:                     # sticker pair 1–3
            m1, m2 = atom2mol[a1], atom2mol[a2]
            if m1 != m2:                           # inter-molecular
                G.add_edge(m1, m2)                 # MultiGraph keeps multiedges

    return G


# ──────────────────────────────────────────────────────────────────────────
# public helper
# ──────────────────────────────────────────────────────────────────────────
def plot_pair_bond_hist(
    snapshot_file: str | Path,
    *,
    bins: "int | Iterable[float] | str" = "auto",
    ax: Optional[Axes] = None,
) -> Axes:
    """
    Histogram the multiplicity of type-1⇄type-3 sticker bonds for each
    neighbouring chain pair.

    X-axis  →  # of parallel sticker bonds between a pair of chains  
    Y-axis  →  # of chain pairs exhibiting that count
    """
    snapshot_file = Path(snapshot_file)
    G = _build_chain_multigraph(snapshot_file)

    multiplicities = [
        G.number_of_edges(u, v)           # counts parallel edges
        for u, v in nx.Graph(G).edges()   # unique chain pairs
    ]

    if ax is None:
        _, ax = plt.subplots(figsize=(6, 4))

    if multiplicities:
        ax.hist(multiplicities, bins=bins, edgecolor="black", alpha=0.85)
    else:
        ax.text(0.5, 0.5, "no type-1⇄3 inter-chain bonds", ha="center",
                va="center", fontsize=9, color="grey")
        ax.set_facecolor("#f7f7f7")

    ax.set_xlabel("# type-1 ⇄ type-3 bonds connecting a chain pair")
    ax.set_ylabel("# chain pairs")
    ax.set_title(snapshot_file.name)
    ax.grid(axis="y", linestyle=":", linewidth=0.4)
    plt.tight_layout()

    return ax
