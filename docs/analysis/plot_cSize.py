#!/usr/bin/env python3
"""
Compute a *cluster-size distribution* (in **molecules**) from **one**
LAMMPS ``*.DATA`` snapshot and display it as a bar chart.

For simplicity the connectivity is extracted directly from the “Bonds”
section; no fancy spatial search is performed.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from pathlib import Path
from typing import Optional, Tuple, List

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from matplotlib.axes import Axes


def _read_snapshot(file_path: Path) -> Tuple[List[int], List[Tuple[int, int]]]:
    """Return (mol_ids, bonds) from a LAMMPS DATA file (very lightweight)."""
    mol_ids: list[int] = []
    bonds: list[Tuple[int, int]] = []

    mode = None
    with file_path.open() as fh:
        for line in fh:
            clean = line.strip()
            if clean.lower().startswith("atoms"):
                mode = "atoms"
                continue
            if clean.lower().startswith("bonds"):
                mode = "bonds"
                continue
            if not clean or clean[0].isalpha():
                continue

            if mode == "atoms":
                parts = clean.split()
                if len(parts) >= 3:
                    mol_ids.append(int(parts[1]))
            elif mode == "bonds":
                parts = clean.split()
                if len(parts) >= 4:
                    bonds.append((int(parts[2]), int(parts[3])))

    return mol_ids, bonds


def plot_csize(data_file: str | Path, ax: Optional[Axes] = None) -> Axes:
    """
    Plot the *fraction of molecules* in clusters of size *s* for **one** snapshot.

    Parameters
    ----------
    data_file
        LAMMPS ``*.DATA`` snapshot (with Atoms/Bonds sections).
    ax
        Optional Matplotlib axis.

    Returns
    -------
    matplotlib.axes.Axes
        Bar chart of *y(s)*.

    Notes
    -----
    * Cluster size here means **number of molecules** (``mol`` IDs)
      in the connected component.
    * Uses `networkx` for the connected-component search.
    """
    data_file = Path(data_file)
    mol_ids, bonds = _read_snapshot(data_file)

    G = nx.Graph()
    G.add_nodes_from(mol_ids)
    # build edges *between molecules* (collapse atom IDs -> mol IDs)
    for a, b in bonds:
        G.add_edge(a, b)

    # Connected components in molecule space
    sizes = [len(cc) for cc in nx.connected_components(G)]
    total_mols = len(set(mol_ids))
    dist = Counter(sizes)

    xs = np.array(sorted(dist))
    ys = np.array([dist[s] * s / total_mols for s in xs])

    if ax is None:
        _, ax = plt.subplots()
    ax.bar(xs, ys, width=1.4)
    ax.set_xlabel("Cluster size (molecules)")
    ax.set_ylabel("Fraction of molecules in clusters of size s")
    ax.set_title(data_file.name)

    return ax
