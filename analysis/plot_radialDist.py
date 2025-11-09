#!/usr/bin/env python3
"""
Volume-normalised **radial density** of stickers (types 1 & 3) and spacers
(types 2 & 4) from a single LAMMPS ``*.DATA`` snapshot.

The function

1. reads atomic coordinates,
2. finds the geometric centre,
3. bins distances into spherical shells (default 30),
4. normalises by shell volume and by total sticker / spacer count,
5. plots two lines on the same axis.
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional, Tuple, List

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.axes import Axes


font = {'family': 'arial', 'size': 16}
plt.rc('font', **font)

def _load_atoms(file_path: Path) -> List[Tuple[int, float, float, float]]:
    """Return list of tuples (type, x, y, z)."""
    atoms: list[Tuple[int, float, float, float]] = []
    with file_path.open() as fh:
        mode = None
        for line in fh:
            clean = line.strip()
            if clean.lower().startswith("atoms"):
                mode = "atoms"
                continue
            if clean.lower().startswith(("bonds", "angles", "velocities")):
                mode = None
            if not clean or clean[0].isalpha() or mode != "atoms":
                continue

            parts = clean.split()
            if len(parts) >= 7:
                atoms.append(
                    (int(parts[2]), float(parts[4]), float(parts[5]), float(parts[6]))
                )
    return atoms


def _geometry(atoms):
    pos = np.array([[x, y, z] for _, x, y, z in atoms])
    centre = pos.mean(axis=0)
    dist = np.linalg.norm(pos - centre, axis=1)
    types = np.array([t for t, *_ in atoms])
    return types, dist


def plot_radial_distribution(
    data_file: str | Path, nbins: int = 30, ax: Optional[Axes] = None
) -> Axes:
    """
    Plot volume-normalised radial distribution for *one* snapshot.

    Parameters
    ----------
    data_file
        LAMMPS snapshot (``*.DATA``) with coordinates.
    nbins
        Number of spherical shells between r=0 and r_max.
    ax
        Optional axis.

    Returns
    -------
    matplotlib.axes.Axes
        Axis with two lines (stickers & spacers).
    """
    atoms = _load_atoms(Path(data_file))
    types, r = _geometry(atoms)

    r_max = r.max()
    edges = np.linspace(0, r_max, nbins + 1)
    vols = (4 / 3) * np.pi * (edges[1:] ** 3 - edges[:-1] ** 3)
    centres = 0.5 * (edges[1:] + edges[:-1])

    st_mask = np.isin(types, (1, 3))
    sp_mask = np.isin(types, (2, 4))

    hist_st, _ = np.histogram(r[st_mask], bins=edges)
    hist_sp, _ = np.histogram(r[sp_mask], bins=edges)

    dens_st = hist_st / vols / hist_st.sum()
    dens_sp = hist_sp / vols / hist_sp.sum()

    if ax is None:
        _, ax = plt.subplots()

    ax.plot(centres, dens_st, marker="*", label="Stickers (1&3)")
    ax.plot(centres, dens_sp, marker="o", label="Spacers  (2&4)")
    ax.set_xlabel("r [Å]")
    ax.set_ylabel("Normalised density")
    ax.set_title(Path(data_file).name)
    ax.legend()

    return ax
