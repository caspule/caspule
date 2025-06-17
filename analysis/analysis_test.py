#!/usr/bin/env python3
"""
analysis_test.py – generate the standard diagnostic plots
"""
from plot_BSF           import plot_bsf
from plot_PE            import plot_pe
from plot_cSize         import plot_csize
from plot_radialDist    import plot_radial_distribution
from plot_SD            import plot_sd

import matplotlib.pyplot as plt

path = "/Volumes/dkanovich/2024/decrease_bSize/run_uniform"

# --- build figures ---------------------------------------------------------
plot_bsf(              f"{path}/Thermo_b70_N200_L300.dat", 13800, 2000)
plot_pe(               f"{path}/Thermo_b70_N200_L300.dat")
plot_csize(            f"{path}/final_state_b70_N200_L300.DATA")
plot_radial_distribution(f"{path}/final_state_b70_N200_L300.DATA")
plot_sd(               f"{path}/BondData_b70_N200_L300.dat")

# --- show everything that was just drawn -----------------------------------
plt.show()          # ← no positional arguments
