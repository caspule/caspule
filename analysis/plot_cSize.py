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


font = {'family': 'arial', 'size': 16}
plt.rc('font', **font)

def _read_snapshot(file_path: Path) -> Tuple[List[int], List[Tuple[int, int]]]:
    mol_ids: list[int] = []
    bonds: list[Tuple[int, int]] = []
    atom_to_mol: dict[int, int] = {}      # NEW

    mode = None
    with file_path.open() as fh:
        for line in fh:
            clean = line.strip()
            low  = clean.lower()

            # --- section switches -------------------------------------------------
            if low.startswith("atoms"):
                mode = "atoms"
                continue
            if low.startswith("bonds"):
                mode = "bonds"
                continue
            if low.startswith(("angles",          # anything we don’t need
                                "velocities",
                                "impropers",
                                "dihedrals")):
                mode = None
                continue

            if not clean or clean[0].isalpha():
                continue

            # --- data lines -------------------------------------------------------
            if mode == "atoms":
                # atom-ID, mol-ID, …
                atom_id, mol_id = int(clean.split()[0]), int(clean.split()[1])
                atom_to_mol[atom_id] = mol_id
                mol_ids.append(mol_id)

            elif mode == "bonds":
                # bond-ID, type, atom-i, atom-j
                _, _, a, b = clean.split()[:4]
                bonds.append((int(a), int(b)))

    # convert atom-level bonds → molecule-level bonds
    mol_bonds = [(atom_to_mol[a], atom_to_mol[b]) for a, b in bonds]
    return mol_ids, mol_bonds


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
