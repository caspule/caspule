#!/usr/bin/env python3
"""
analysis_test.py – generate the standard diagnostic plots
"""
from plot_BSF           import plot_bsf
from plot_PE            import plot_pe
from plot_cSize         import plot_csize
from plot_radialDist    import plot_radial_distribution
from plot_SD            import plot_sd
from plot_pair_bonds    import plot_pair_bond_hist
from plot_cSizeBSF      import plot_cSizeBSF
from plot_neighCount    import plot_neighbour_hist
from plot_sticker_dist  import plot_sticker_hist

import matplotlib.pyplot as plt

path = "/Volumes/dkanovich/2024/dispersed_phase/run_uniform/Ens_0.30_Es_6.00/final_state_Run1.DATA"  # Change this to your actual simulation folder path

# --- build figures ---------------------------------------------------------
# REPLACE THESE WITH YOUR ACTUAL FILE NAMES
plot_bsf(              f"{path}/Thermo_Run1.dat", 13800, 2000)
plot_pe(               f"{path}/Thermo_b70_N200_L300.dat")
plot_csize(            f"{path}/final_state_Run1.DATA")
plot_radial_distribution(f"{path}/final_state_b70_N200_L300.DATA")
plot_sd(               f"{path}/BondData_b70_N200_L300.dat")
plot_pair_bond_hist(f"{path}")
plot_cSizeBSF(f"{path}")
plot_neighbour_hist(f"{path}")
plot_sticker_hist(f"{path}")

# --- show everything that was just drawn -----------------------------------
plt.show()          # ← no positional arguments
