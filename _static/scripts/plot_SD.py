#!/usr/bin/env python3
"""
plot_SD
=======

Sticker *Dissociation Events* helper.

Reads a ``BondData_<foo>.dat`` file that stores **cumulative** formation
and break counts; this function plots *per-interval* dissociation events.
"""

from pathlib import Path
from typing import Optional

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.axes import Axes


def plot_sd(file_path: str | Path, ax: Optional[Axes] = None) -> Axes:
    """
    Plot *sticker dissociation events* (Δ broken bonds per thermo dump).

    Parameters
    ----------
    file_path
        Path to ``BondData_<foo>.dat`` with three columns::

            0  timestep
            1  cumulative formed bonds
            2  cumulative broken bonds
    ax
        Optional axis.

    Returns
    -------
    matplotlib.axes.Axes
        Axis with a bar chart (or line) of dissociation events vs step.
    """
    file_path = Path(file_path)
    raw = np.loadtxt(file_path, comments="#")
    step      = raw[:, 0]
    cum_break = raw[:, 2]

    # convert cumulative -> per-interval
    d_break = np.diff(cum_break)
    step_mid = step[1:]  # centre points

    if ax is None:
        _, ax = plt.subplots()

    ax.bar(step_mid, d_break, width=step_mid[1] - step_mid[0])
    ax.set_xlabel("Simulation steps")
    ax.set_ylabel("Broken bonds per interval")
    ax.set_title(file_path.name)

    return ax
