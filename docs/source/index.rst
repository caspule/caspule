CASPULE — Setup • Simulate • Analyze Sticker–Spacer Polymers
============================================================

**CASPULE**, (**C**)omputational  (**A**)nalysis of (**S**)ticker Spacer (**P**)olymeric (**C**)ondensates (**U**)sing (**L**)AMMPS (**E**)ngine, is a pipeline for Langevin Dynamics simulations of coarse-grained biopolymers. It automates system setup, `LAMMPS <https://www.lammps.org/#gsc.tab=0>`_ simulation, and analysis of sticker–spacer polymer phase behavior. It provides an end-to-end reproducible computational protocol to simulate and analyze biological condensates. 

Overview
========
CASPULE is a **three-stage pipeline** for simulations of sticker–spacer polymers:

- **Step 1 — Setup:** Build arbitrary **lengths** and **patterns**; generate Packmol + Moltemplate inputs and a LAMMPS-ready ``*.data`` (initial condition).
- **Step 2 — Simulate:** Run **Langevin dynamics** (with optional **metadynamics** via Colvars) in LAMMPS; supports MPI + load balancing.
- **Step 3 — Analyze:** Turn trajectories/restarts into **cluster statistics**, **bonded-sticker fractions**, **radial profiles**, and **energy timecourses**.

.. figure:: /_static/img/graphical_summary.gif

   :alt: CASPULE pipeline (setup, simulate, analyze)
   :align: center
   :figwidth: 100%

Why CASPULE?
------------
- **Arbitrary patterns & lengths:** Repeatable block templates let you sweep architectures systematically.
- **Saturating interaction:** Single-valent sticker interaction (to mimic saturable biomolecular interactions) and tunable ``E_s`` vs ``E_ns``.
- **Batteries-included analysis:** Reproducible Python tools for kinetics and steady-state structure.

Quick Start (End-to-End)
========================

Prerequisites
-------------
Ensure these are on ``$PATH`` (or module-loaded):

- `packmol <https://m3g.github.io/packmol/>`_
- `moltemplate <https://www.moltemplate.org/>`_ 
- **LAMMPS** with ``fix bond/create/random``, ``bond/break``, Colvars (for metadynamics), MPI build recommended
- Python 3 with the packages listed in :doc:`usage/installation`

Step 1 — Setup (build data + inputs)
------------------------------------
Run the setup wrapper; it orchestrates all sub-steps.

::

   bash create_InitCoor.sh

Behind the scenes, CASPULE executes:

1. ``python3 LT_writer.py            <n>  <seg_pattern>``             (make block templates)
2. ``python3 writePackmolInput.py    <n>  <NA> <NB> <L>  populate_tmp.inp  IC_tmp.xyz``
3. ``python3 writeSysLT.py           <n>  <NA> <NB> <L>  b70_N200_L<L>.lt``
4. ``packmol < populate_tmp.inp``
5. ``moltemplate.sh -xyz IC_tmp.xyz b70_N200_L<L>.lt -nocheck``
6. ``python3 updateColVar.py         IC_tmp.xyz  N200_Rg_L<L>.colvars  <L> <n> <NA> <NB> <seg_pattern>``
7. ``python3 updateInput.py          Template_input.in  <L>``
8. ``python3 fix_datafiles.py        b70_N200_L<L>.data``

Artifacts produced:

::

   IC_tmp.xyz
   polyA_n<n>.lt, polyB_n<n>.lt
   b70_N200_L<L>.lt
   b70_N200_L<L>.data
   b70_N200_L<L>.in
   N200_Rg_L<L>.colvars
   submit_b70_N200_L<L>.sh

Step 2 — Simulate (Langevin ± Metadynamics)
-------------------------------------------
**Vanilla Langevin:**

::

   mpirun -np 40 lmp -in b70_N200_L<L>.in

Notes
=====

**Specific interaction**  
Single-valent stickers via ``fix bond/create/random`` + ``bond/break``,  
with shifted-harmonic bonds (well depth ``E_s``).

**Non-specific interaction**  
LJ (``pair_style lj/cut``) with well depth ``E_ns``;  
LJ interactions between bonded beads are excluded (``special_bonds lj 0 1 1 angle yes``).

**Typical parameter choices**  
- ``r0 = 1.122 σ`` with ``σ = 10 Å``  
- ``r_cut = r0 + 1.5 Å``  
- ``T = 310 K``  
- timestep 20–30 fs  
- ``tdamp ≈ 500 fs``

**Parallel scaling rule of thumb**  
~500 beads / CPU; enable simulation load balancing for spatially heterogenous systems  
(``comm_style tiled`` + ``fix balance``).

**Metadynamics (optional):** supply Colvars (e.g., ``N200_Rg_L<L>.colvars``) to accelerate process of interest (clustering, coalescence etc.) along user defined collective variables (Rg, Inter-cluster distance etc.).

Step 3 — Analyze (one-command reports)
--------------------------------------
Use the analysis scripts in :doc:`usage/data_analysis` to compute:

- **Cluster size distributions** (graph-based from ``*.restart``)
- **Bonded-sticker fraction vs time**
- **Radial density profiles** (stickers vs spacers)
- **Potential energy timecourses** (convergence diagnostics)

Example:

::

   python3 analysis/cluster_size_distribution.py   /path/to/sim_folder
   python3 analysis/bonded_sticker_fraction.py     /path/to/Thermo_*.dat
   python3 analysis/radial_profiles.py             /path/to/restarts



Get Started / Learn More
========================
.. toctree::
   :maxdepth: 2
   :caption: Contents:

   usage/installation
   usage/model_overview
   usage/pipeline
   usage/example_system_setup
   usage/simulation_output
   usage/data_analysis
   api/modules

Contributing & Issues
---------------------
Please open issues or PRs on the repository. Include your LAMMPS version/tag and whether Colvars + bond/create/random are enabled.

