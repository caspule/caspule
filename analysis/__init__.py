"""
analysis
========
Tiny convenience package that re-exports the single plotting helper
from each module so users can do ::

    from analysis import plot_pe, plot_bsf, ...

Nothing is executed at import time – only functions are exposed.
"""

from .plot_PE import plot_pe              # noqa: F401
from .plot_BSF import plot_bsf            # noqa: F401
from .plot_SD import plot_sd              # noqa: F401
from .plot_cSize import plot_csize        # noqa: F401
from .plot_radialDist import plot_radial_distribution as plot_radialDist  # noqa: F401
