#!/usr/bin/env python3
"""
Quick helper to plot the *inter-molecular type-1/3 distance histogram* for
one or several LAMMPS ``final_state_*.DATA`` snapshots.

Typical usage
-------------
>>> from analysis.plot_sticker_dist import plot_sticker_hist
>>> plot_sticker_hist("final_state_Run1.DATA")                 # single file
>>> plot_sticker_hist([
...     "restart_term/final_state_Ens_0.30_Es_8.00.DATA",
...     "restart_uniform/final_state_Ens_0.30_Es_8.00.DATA",
... ], bins_w=0.2, max_r=900)                                  # overlay

The helper is intentionally lightweight: no CLI, no batch mode – just one
function that returns the Matplotlib ``Axes`` so the caller can style or
save the figure as desired.
"""

from __future__ import annotations

from pathlib import Path
from typing import Iterable, Optional, Sequence

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.cm import get_cmap
from scipy.spatial.distance import pdist
import networkx as nx   # only to satisfy IDEs; not used at runtime


font = {'family': 'arial', 'size': 16}
plt.rc('font', **font)

# ──────────────────────────────────────────────────────────────────────────
# internal parser
# ──────────────────────────────────────────────────────────────────────────
_SECTION_END = {
    "velocities", "bonds", "angles", "dihedrals",
    "impropers", "masses", "pair", "angle",
    "dihedral", "improper",
}


def _type13_atoms(path: Path) -> tuple[np.ndarray, np.ndarray]:
    """
    Return (molecule IDs, coordinates) for atoms of type **1** or **3**.

    If < 2 such atoms are present, raises ``ValueError``.
    """
    mols, xyz = [], []
    in_atoms = False

    with path.open() as fh:
        for raw in fh:
            line = raw.strip()
            if not line:
                continue

            low = line.lower()
            if not in_atoms and low.startswith("atoms"):
                in_atoms = True
                continue
            if in_atoms and any(low.startswith(k) for k in _SECTION_END):
                break

            if in_atoms and line[0].isdigit():
                parts = line.split()
                if len(parts) < 7:
                    continue
                atype = int(parts[2])
                if atype in (1, 3):
                    mols.append(int(parts[1]))
                    xyz.append(tuple(map(float, parts[4:7])))

    if len(mols) < 2:
        raise ValueError("fewer than two type-1/3 atoms")

    return np.fromiter(mols, int), np.asarray(xyz, float)


def _distances_between_molecules(mol_ids: np.ndarray,
                                 coords: np.ndarray) -> np.ndarray:
    """
    Return a 1-D array of distances between atoms that sit on *different*
    molecule IDs.
    """
    iu = np.triu_indices(len(mol_ids), 1)
    mask = mol_ids[iu[0]] != mol_ids[iu[1]]
    return pdist(coords)[mask]


# ──────────────────────────────────────────────────────────────────────────
# public helper
# ──────────────────────────────────────────────────────────────────────────
def plot_sticker_hist(
    snapshots: "str | Path | Sequence[str | Path]",
    *,
    bins_w: float = 0.2,
    max_r: float = 900.0,
    log_scale: bool = False,
    labels: Optional[Sequence[str]] = None,
    ax: Optional[Axes] = None,
) -> Axes:
    """
    Overlay raw-count histograms of type-1/3 inter-molecular distances.

    Parameters
    ----------
    snapshots
        A single path or a sequence of paths to ``final_state_*.DATA`` files.
    bins_w
        Bin width Δr in σ (default **0.2**).
    max_r
        Maximum distance considered (default **900 σ**).
    log_scale
        If *True*, apply log-scale to the y-axis.
    labels
        Optional legend labels; by default the parent folder names.
    ax
        Existing Matplotlib ``Axes`` to draw on.  If *None* a new one is
        created.

    Returns
    -------
    matplotlib.axes.Axes
        The axis containing the plotted histograms.
    """
    # normalise input
    if isinstance(snapshots, (str, Path)):
        snapshot_paths = [Path(snapshots)]
    else:
        snapshot_paths = [Path(p) for p in snapshots]

    if labels and len(labels) != len(snapshot_paths):
        raise ValueError("`labels` length must match `snapshots` length")
    if labels is None:
        labels = [p.parent.name for p in snapshot_paths]

    # prepare common bins
    nbins = int(np.ceil(max_r / bins_w))
    bins = np.linspace(0.0, nbins * bins_w, nbins + 1)

    histograms = []
    for path in snapshot_paths:
        try:
            mols, coords = _type13_atoms(path)
        except ValueError:
            histograms.append(np.zeros(nbins))
            continue
        dists = _distances_between_molecules(mols, coords)
        hist, _ = np.histogram(dists, bins=bins)
        histograms.append(hist)

    if ax is None:
        _, ax = plt.subplots(figsize=(8, 5))

    cmap = get_cmap("tab10")
    colours = [cmap(i % 10) for i in range(len(histograms))]
    centres = 0.5 * (bins[:-1] + bins[1:])

    for hist, lbl, col in zip(histograms, labels, colours):
        ax.plot(centres, hist, drawstyle="steps-mid", color=col, label=lbl)

    if log_scale:
        ax.set_yscale("log")

    ax.set_xlabel(r"Distance $r\;(\sigma)$")
    ax.set_ylabel("Raw count per bin")
    ax.set_title("Type-1/3 inter-molecular distance histograms")
    ax.legend(fontsize="small")
    ax.grid(axis="y", linestyle=":", linewidth=0.4)
    plt.tight_layout()

    return ax
