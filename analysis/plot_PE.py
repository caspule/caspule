#!/usr/bin/env python3
"""
Small helper to plot **potential energy vs. simulation step** from a single
LAMMPS ``Thermo_<foo>.dat`` file.

.. rubric:: Typical usage

>>> from analysis.plot_PE import plot_pe
>>> plot_pe("Thermo_example.dat")   # show the figure

Only one public function is provided so that the module appears cleanly
in the *API Reference*.
"""
# ----------------------------------------------------------------------
from pathlib import Path
from typing import Optional

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
# ----------------------------------------------------------------------


font = {'family': 'arial', 'size': 16}
plt.rc('font', **font)

def plot_pe(file_path: str | Path, ax: Optional[Axes] = None) -> Axes:
    """
    Plot *potential energy* (column 3) as a function of *timestep* (column 0).

    Parameters
    ----------
    file_path
        Path to a ``Thermo_<foo>.dat`` file.
    ax
        Existing axis to draw on, or *None* (create new).

    Returns
    -------
    matplotlib.axes.Axes
        Axis containing the plotted line.
    """
    file_path = Path(file_path)
    data = np.loadtxt(file_path, comments="#")
    steps, pot = data[:, 0], data[:, 3]

    if ax is None:
        _, ax = plt.subplots()
    ax.plot(steps, pot, lw=1.2)
    ax.set_xlabel("Simulation steps")
    ax.set_ylabel("Potential energy [kcal/mol]")
    ax.set_title(file_path.name)
    return ax
