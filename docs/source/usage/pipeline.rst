Pipeline Overview
=================

:file:`create_InitCoor.sh` is the *orchestrator*: edit a few variables at
the top, run it once, and you receive a complete **LAMMPS start-up
folder** containing

* **b70_N200_L<L>.data** — Data file  
* **N200_Rg_L<L>.colvars** — Colvars tuned to the system size  
* **b70_N200_L<L>.in** — Lammps Input (+optional Slurm input script)

The numbered sections below explain every call in the wrapper, 
which files it consumes, and which files it writes.

.. rubric:: Wrapper variables

.. list-table::
   :header-rows: 1
   :widths: 15 70

   * - **Bash var**
     - **Meaning / effect**
   * - ``n``
     - Segment **repeat count** (``10`` → chain length = ``10 × len(seg)``)
   * - ``seg``
     - Sticker/spacer pattern ``2212212`` (``2`` = spacer, ``1`` = sticker)
   * - ``NA`` / ``NB``
     - Number of **A-chains** / **B-chains** (``100`` / ``100``)
   * - ``L``
     - Half-box length (``500 Å``) → Simulation box :math:`[-(L), (L)]^3`

All filenames downstream are built from these numbers, e.g.
:file:`b70_N200_L500.lt` (``b`` = 70 beads, ``N200`` = 100 + 100
chains).

.. rubric:: End-to-end flow

The helper chain executed by *create_InitCoor.sh*:

#. **LT_writer.py** → monomer LT + XYZ  
#. **writePackmolInput.py** → Packmol recipe  
#. **Packmol** → *IC_tmp.xyz*  
#. **writeSysLT.py** → system LT  
#. **Moltemplate** → *b70_N200_L<L>.data*  
#. **updateColVar.py** → *N200_Rg_L<L>.colvars*  
#. **updateInput.py** → *b70_N200_L<L>.in* + Slurm script  
#. **fix_datafiles.py** → patch data file  
#. **lmp_mpi** → run simulation

.. rubric:: Detailed step-by-step

.. rubric:: 3.1 ``LT_writer.py`` — build monomer libraries

.. code-block:: bash

   python3 LT_writer.py "$n" "$seg"

**Creates**

* ``polyA_n<n>.lt``         Moltemplate monomer (types 1 & 2)  
* ``polyB_n<n>.lt``         Moltemplate monomer (types 3 & 4)  
* ``polyA_n<n>_mono.xyz`` & ``polyB_n<n>_mono.xyz`` (single-monomer XYZ)

**Bead taxonomy**

+---------+----------------------------------------------+
| **ID**  | **Role**                                     |
+=========+==============================================+
| **1**   | Sticker (A-chain, specific bonding)          |
+---------+----------------------------------------------+
| **2**   | Spacer  (A-chain, non-specific bonding)      |
+---------+----------------------------------------------+
| **3**   | Sticker (B-chain, specific bonding)          |
+---------+----------------------------------------------+
| **4**   | Spacer  (B-chain, non-specific bonding)      |
+---------+----------------------------------------------+

.. rubric:: 3.2 ``writePackmolInput.py`` — Packmol recipe

.. code-block:: bash

   python3 writePackmolInput.py "$n" "$NA" "$NB" "$L" \
                                populate_tmp.inp IC_tmp.xyz

*Creates* :file:`populate_tmp.inp` containing **two** ``structure`` blocks,
each requesting ``NA`` or ``NB`` copies inside the cube
:math:`[-(L-20), (L-20)]^3` with 10 Å clearance.

.. rubric:: 3.3 Packmol — coordinate packing

.. code-block:: bash

   packmol < populate_tmp.inp      # → IC_tmp.xyz

Replicates monomers, randomises orientation, outputs one XYZ:

.. code-block:: text

   14000
   comment line
   2  -185.4  -92.7   305.1
   1   220.0   44.8   161.9
   …

.. rubric:: 3.4 ``writeSysLT.py`` — system-level LT

.. code-block:: bash

   python3 writeSysLT.py "$n" "$NA" "$NB" "$L" b70_N200_L<L>.lt

Imports the monomer LTs, instantiates *NA + NB* polymers, defines
back-bone bond/angle types, and writes a *Data Boundary* block
± (L) Å.

.. rubric:: 3.5 Moltemplate — LT + XYZ → LAMMPS Data

.. code-block:: bash

   moltemplate.sh -xyz IC_tmp.xyz b70_N200_L<L>.lt -nocheck

*Inputs*

* packed coordinates :file:`IC_tmp.xyz`  
* hierarchy :file:`b70_N200_L<L>.lt`

*Outputs*

* ``b70_N200_L<L>.data`` — canonical LAMMPS *Data* file  
* ``system.in.settings`` — auxiliary pair/bond/angle styles  
* ``*.lt.tmp`` — intermediate JSON (can be deleted)

The ``-nocheck`` flag skips Moltemplate’s expensive overlap checker—we
trust Packmol.

.. rubric:: 3.6 ``updateColVar.py`` — patch the colvars template

.. code-block:: bash

   python3 updateColVar.py IC_tmp.xyz N400_Rg_L700.colvars \
                           "$L" "$n" "$NA" "$NB" "$seg"

* Computes **radius of gyration** from *all* beads.  
* Sets ``upperBoundary = Rg + 10`` and ``upperWalls = Rg + 5``.  
* Generates an ``atomNumbers`` list selecting one bead from the center of each chain to experience metadynamics bias.  
* Writes :file:`N200_Rg_L<L>.colvars`.

.. rubric:: 3.7 ``updateInput.py`` — final *.in* & Slurm launcher

.. code-block:: bash

   python3 updateInput.py Template_input.in "$L"

Performs three substitutions in the template:

1. ``variable fName`` → ``b70_N200_L<L>``  
2. ``read_data``      → correct *Data* filename  
3. ``fix CV_Rg``      → new ``.colvars`` file

*Creates*

* ``b70_N200_L<L>.in`` — production input  
* ``submit_b70_N200_L<L>.sh`` — batch script (28 MPI, 3 days)

.. rubric:: 3.8 ``fix_datafiles.py`` — enable dynamic bonds

* Search-replace ``2  bond types`` → ``3  bond types``  
* Append ``50 extra bond per atom``

Required for LAMMPS’s ``fix bond/create/random`` (**EXTRA-BOND**
package), which forms single-valency sticker–sticker bonds
(**bond type 3**).

.. rubric:: 3.9 Run LAMMPS

.. code-block:: bash

   lmp_mpi -in b70_N200_L<L>.in
   # or
   sbatch submit_b70_N200_L<L>.sh

.. rubric:: File cheat-sheet

.. list-table::
   :header-rows: 1
   :widths: 35 20 30

   * - **File**
     - **Created by**
     - **Consumed by**
   * - ``polyA_n<n>.lt`` / ``polyB_n<n>.lt``
     - ``LT_writer.py``
     - ``writeSysLT.py``
   * - ``polyA_n<n>_mono.xyz`` / ``polyB_n<n>_mono.xyz``
     - ``LT_writer.py``
     - ``writePackmolInput.py``
   * - ``populate_tmp.inp``
     - ``writePackmolInput.py``
     - *Packmol*
   * - ``IC_tmp.xyz``
     - *Packmol*
     - ``writeSysLT.py``, ``updateColVar.py``
   * - ``b70_N200_L<L>.lt``
     - ``writeSysLT.py``
     - *Moltemplate*
   * - ``b70_N200_L<L>.data``
     - *Moltemplate*
     - ``fix_datafiles.py``, ``updateInput.py``
   * - ``N200_Rg_L<L>.colvars``
     - ``updateColVar.py``
     - ``updateInput.py``
   * - ``b70_N200_L<L>.in``
     - ``updateInput.py``
     - *LAMMPS*
   * - ``submit_b70_N200_L<L>.sh``
     - ``updateInput.py``
     - HPC scheduler
