#!/usr/bin/env python3
"""
Quick helper to visualise the *chain-neighbour histogram* for **one**
LAMMPS ``final_state_*.DATA`` snapshot.

Typical usage
-------------
>>> from analysis.plot_neighCount import plot_neighbour_hist
>>> plot_neighbour_hist("final_state_Run1.DATA")   # shows the figure

The helper is intentionally lightweight: no CLI, no batch mode – just one
function that returns the Matplotlib ``Axes`` so the caller can style or
save the figure as desired.
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional
from collections import Counter

import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.axes import Axes


font = {'family': 'arial', 'size': 16}
plt.rc('font', **font)

# ──────────────────────────────────────────────────────────────────────────
# internal utilities
# ──────────────────────────────────────────────────────────────────────────
def _build_chain_graph(snapshot: Path) -> nx.MultiGraph:
    """
    Parse a LAMMPS ``*.DATA`` file and return a graph whose **nodes** are
    molecules (chains) and whose **edges** are *type-3* bonds connecting
    atoms in **different** molecules.
    """
    atom2mol: dict[int, int] = {}
    edges: list[tuple[int, int]] = []

    section = None
    with snapshot.open() as fh:
        for raw in fh:
            line = raw.strip()
            low  = line.lower()

            if low.startswith("atoms"):
                section = "atoms"
                continue
            if low.startswith("bonds"):
                section = "bonds"
                continue
            if low.startswith(("velocities", "angles", "masses",
                                "pair coeffs", "angle coeffs")):
                section = None
                continue
            if not line:
                continue

            if section == "atoms" and line[0].isdigit():
                aid, mid = map(int, line.split()[:2])
                atom2mol[aid] = mid

            elif section == "bonds" and line[0].isdigit():
                _, btype, a1, a2, *_ = line.split()
                if int(btype) == 3:          # only sticker–sticker bonds
                    edges.append((int(a1), int(a2)))

    G = nx.MultiGraph()
    G.add_nodes_from(set(atom2mol.values()))

    for a1, a2 in edges:
        m1, m2 = atom2mol[a1], atom2mol[a2]
        if m1 != m2:
            G.add_edge(m1, m2)

    return G


# ──────────────────────────────────────────────────────────────────────────
# public helper
# ──────────────────────────────────────────────────────────────────────────
def plot_neighbour_hist(snapshot_file: str | Path,
                        ax: Optional[Axes] = None,
                        colour: str = "tab:blue") -> Axes:
    """
    Bar-plot the degree distribution (# neighbours per chain) for one snapshot.

    Parameters
    ----------
    snapshot_file
        Path to a ``final_state_*.DATA`` file.
    ax
        Existing Matplotlib ``Axes`` to draw on.  If *None* (default) a new
        ``Figure`` + ``Axes`` is created.
    colour
        Matplotlib bar colour.

    Returns
    -------
    matplotlib.axes.Axes
        The axis containing the plotted histogram.
    """
    snapshot_file = Path(snapshot_file)

    G = _build_chain_graph(snapshot_file)
    degs = [d for _, d in nx.Graph(G).degree()]         # collapse multiedges
    hist = Counter(degs)

    xs = sorted(hist)
    ys = [hist[x] for x in xs]

    if ax is None:
        _, ax = plt.subplots(figsize=(6, 4))

    if xs:
        ax.bar(xs, ys, color=colour)
    else:
        ax.text(0.5, 0.5, "no data", ha="center", va="center",
                fontsize=9, color="grey")
        ax.set_facecolor("#f7f7f7")

    ax.set_xlabel("# of neighbours (degree)")
    ax.set_ylabel("# of chains")
    ax.set_title(snapshot_file.name)
    ax.set_xticks(xs)
    ax.set_xlim(-0.5, max(xs, default=0) + 0.5)
    ax.grid(axis="y", linestyle=":", linewidth=0.4)
    plt.tight_layout()

    return ax
