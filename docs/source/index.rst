Welcome to CASPULE’s documentation!
=============================================

This project uses a single Bash wrapper (`create_InitCoor.sh`) together with six Python scripts to generate Packmol + Moltemplate input files and produce LAMMPS‐ready data files.

Graphical Summary
-----------------

.. image:: /_static/img/graphical_summary.gif
   :alt: Graphical summary of the init-conditions pipeline
   :target: /_static/img/graphical_summary.gif
   :align: center

Quick Start
-----------

1. **Ensure prerequisites are on your PATH**  
   - `packmol`  
   - `moltemplate.sh`  
   - A LAMMPS binary (e.g., `lmp_serial`)  

2. **Run the pipeline**  
   ::

       bash create_InitCoor.sh

   Behind the scenes, this executes:

   1. ``python3 LT_writer.py  <n>  <seg_pattern>``  
   2. ``python3 writePackmolInput.py  <n>  <NA>  <NB>  <L>  populate_tmp.inp  IC_tmp.xyz``  
   3. ``python3 writeSysLT.py  <n>  <NA>  <NB>  <L>  b70_N200_L<L>.lt``  
   4. ``packmol < populate_tmp.inp``  
   5. ``moltemplate.sh -xyz IC_tmp.xyz b70_N200_L<L>.lt -nocheck``  
   6. ``python3 updateColVar.py  IC_tmp.xyz  N400_Rg_L700.colvars  <L>  <n>  <NA>  <NB>  <seg_pattern>``  
   7. ``python3 updateInput.py  Template_input.in  <L>``  
   8. ``python3 fix_datafiles.py  b70_N200_L<L>.data``  

3. **After successful execution**, you will find:  
   ::

       IC_tmp.xyz
       polyA_n<n>.lt, polyB_n<n>.lt
       b70_N200_L<L>.lt
       b70_N200_L<L>.data
       b70_N200_L<L>.in
       N200_Rg_L<L>.colvars
       submit_b70_N200_L<L>.sh  

   You can then launch LAMMPS with:  
   ::

       lmp_serial -in b70_N200_L<L>.in

Documentation Sections
----------------------

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   usage/installation
   usage/pipeline
   usage/example_system_setup
   usage/simulation_output
   usage/data_analysis
   api/modules



