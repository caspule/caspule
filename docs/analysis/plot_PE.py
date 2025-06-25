#!/usr/bin/env python3
"""
Quick helper to visualise *potential energy* vs *simulation time* for **one**
LAMMPS ``Thermo_<foo>.dat`` file.

Typical usage
-------------
>>> from analysis.plot_PE import plot_pe
>>> plot_pe("Thermo_example.dat")        # shows the figure

The helper is intentionally lightweight: no CLI, no batch mode – just one
function that returns the Matplotlib ``Axes`` so the caller can style or
save the figure as desired.
"""

from pathlib import Path
from typing import Optional

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.axes import Axes


def plot_pe(file_path: str | Path, ax: Optional[Axes] = None) -> Axes:
    """
    Plot *potential energy* (column 3) as a function of *timestep* (column 0).

    Parameters
    ----------
    file_path
        Path to a single ``Thermo_<foo>.dat`` file written by LAMMPS
        (header lines may start with “#”; they are ignored).
    ax
        Existing Matplotlib ``Axes`` to draw on.  If *None* (default) a new
        ``Figure`` + ``Axes`` is created internally.

    Returns
    -------
    matplotlib.axes.Axes
        The axis containing the plotted line.  Use ``ax.figure`` to access
        the parent figure.

    Notes
    -----
    The column mapping assumes the *custom thermo_style* used in the docs:

    =====  ========================
    Col.#  Quantity
    -----  ------------------------
      0    timestep
      1    temperature (unused)
      2    kinetic energy (unused)
      3    *potential energy* (plotted)
    =====  ========================

    Examples
    --------
    >>> ax = plot_pe("run/Thermo_test.dat")
    >>> ax.set_ylim(-8_000, 2_000)       # custom tweak
    >>> ax.figure.savefig("PE_trace.png")
    """
    file_path = Path(file_path)
    data = np.loadtxt(file_path, comments="#")

    steps = data[:, 0]
    pot   = data[:, 3]

    if ax is None:
        _, ax = plt.subplots()

    ax.plot(steps, pot, lw=1.2)
    ax.set_xlabel("Simulation steps")
    ax.set_ylabel("Potential energy [kcal/mol]")
    ax.set_title(file_path.name)

    return ax
