#!/usr/bin/env python3
"""
plot_BSF
========

Plot the *Bonded-Sticker Fraction* (BSF) – i.e. the percentage of **newly
formed cross-links** – from a single thermo file that contains a running
``bonds`` column.

Only one public helper is exposed so the module slots cleanly into Sphinx
autodoc.
"""

from pathlib import Path
from typing import Optional

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.axes import Axes


def plot_bsf(
    file_path: str | Path,
    og_bonds: int,
    max_bonds: int,
    ax: Optional[Axes] = None,
) -> Axes:
    """
    Plot *% stickers bonded* vs time from a **single** ``Thermo_*.dat`` file.

    Parameters
    ----------
    file_path
        Thermo file that ends with a ``bonds`` column.
    og_bonds
        Number of *permanent* covalent bonds (baseline to subtract).
    max_bonds
        Maximum possible *new* bonds (denominator for 100 % normalisation).
    ax
        Optional axis to draw on.

    Returns
    -------
    matplotlib.axes.Axes
        Axis containing the BSF trace.

    Raises
    ------
    ValueError
        If the thermofile has fewer than five columns.

    Notes
    -----
    The BSF at timestep *i* is computed as::

        BSF_i = (bonds_i - og_bonds) / max_bonds * 100

    where ``bonds_i`` is taken from the last column of the thermo line.
    """
    file_path = Path(file_path)
    data = np.loadtxt(file_path, comments="#")
    if data.shape[1] < 5:
        raise ValueError("Thermo file must have at least five columns.")

    steps = data[:, 0]
    bond_counts = data[:, -1]

    bsf = (bond_counts - og_bonds) / max_bonds * 100.0

    if ax is None:
        _, ax = plt.subplots()
    ax.plot(steps, bsf, lw=1.2)
    ax.set_xlabel("Simulation steps")
    ax.set_ylabel("% stickers bonded")
    ax.set_title(f"{file_path.name}  (BSF)")

    return ax
