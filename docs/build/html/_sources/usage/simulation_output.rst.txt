Simulation Output
=================

This page documents all of the primary output files produced by the pipeline and by LAMMPS during and after the simulation. Each subsection below shows a representative excerpt (or header) from a given file, followed by a line‐by‐line explanation of its contents. No analysis is performed here—just plain descriptions of what each column or section means.

Thermodynamic Data: ``Thermo_<fName>.dat``
-------------------------------------------

Below is the header line and the first few rows of a typical thermodynamic output file, named ``Thermo_<fName>.dat``:

.. code-block:: text

    # Steps Temp KinEng PotEng Epair Ebond Eangle Bonds
    1000000 309.9092980089979 12932.006720561228 2421.2753602970483 -5608.9113003346756 -1676.5739699962255 9706.7606306279486 14845
    2000000 308.4459769650038 12870.944733402906 580.1671941493225 -6212.513108889987 -2765.9452470589113 9558.625550098221 15019
    3000000 308.9000673416380 12889.893180061661 -663.6937637213039 -6715.222056123977 -3378.1828104342594 9429.711102836933 15138
    4000000 307.9393191012913 12849.802731724838 -1247.4935140060538 -7047.389388496154 -3702.186514574762 9502.082389064863 15199

Explanation:

- **Header**:  
  ``# Steps Temp KinEng PotEng Epair Ebond Eangle Bonds``

  1. `Steps`  
     - The current LAMMPS timestep (for example, 1 000 000; 2 000 000; etc.).  
  2. `Temp`  
     - The instantaneous temperature (in Kelvin) at that step.  
  3. `KinEng`  
     - The total kinetic energy of the system (in kcal/mol).  
  4. `PotEng`  
     - The total potential energy (in kcal/mol), equal to the sum of pair, bond, angle, and any other contributions.  
  5. `Epair`  
     - The contribution from pairwise (nonbonded) interactions (in kcal/mol).  
  6. `Ebond`  
     - The energy stored in bonds (in kcal/mol).  
  7. `Eangle`  
     - The energy stored in angles (in kcal/mol).  
  8. `Bonds`  
     - The total number of bonds currently present in the system (including dynamically formed ones).

- **First Data Row** (for example,  
  ``1000000 309.9092980089979 12932.006720561228 2421.2753602970483 -5608.9113003346756 -1676.5739699962255 9706.7606306279486 14845``)  
  1. `1000000` → At timestep 1 000 000.  
  2. `309.9092980089979` → Temperature ≈ 309.91 K.  
  3. `12932.006720561228` → Kinetic energy ≈ 12 932.0 kcal/mol.  
  4. `2421.2753602970483` → Potential energy ≈ 2 421.28 kcal/mol.  
  5. `-5608.9113003346756` → Pair energy ≈ –5 608.91 kcal/mol.  
  6. `-1676.5739699962255` → Bond energy ≈ –1 676.57 kcal/mol.  
  7. `9706.7606306279486` → Angle energy ≈ 9 706.76 kcal/mol.  
  8. `14845` → There are 14 845 bonds at this step.

Subsequent lines follow the same column order at steps 2 000 000, 3 000 000, etc.

Bond‐Formation/Breaking Data: ``BondData_<fName>.dat``
-------------------------------------------------------

Below are a few lines from the cumulative bond data file, named ``BondData_<fName>.dat``:

.. code-block:: text

    1000000 1566 521
    2000000 2417 1198
    3000000 3330 1992
    4000000 4191 2792

Explanation:

- **Columns**:  
  1. **Step**  
     - The LAMMPS timestep at which the data was recorded (every “dt_thermo” steps, for example 1 000 000; 2 000 000; etc.).  
  2. **Cumulative Bonds Formed**  
     - The total number of new bonds formed by the “bond/create” fix up to that step.  
  3. **Cumulative Bonds Broken**  
     - The total number of bonds broken by the “bond/break” fix up to that step.

- **First Row** (``1000000 1566 521``):  
  1. At timestep 1 000 000.  
  2. 1 566 bonds have been formed so far.  
  3. 521 bonds have been broken so far.

- **Second Row** (``2000000 2417 1198``):  
  1. At timestep 2 000 000.  
  2. 2 417 total bonds formed.  
  3. 1 198 total bonds broken.

And so on for additional timesteps.

Collective‐Variable Trajectory: ``<fName>.colvars.traj``
--------------------------------------------------------

Below is the header and a few lines from the colvars trajectory file, named ``<fName>.colvars.traj``:

.. code-block:: text

    # step         Rg1                    
           0    2.76034911120119e+02  
       50000    2.74510753203738e+02  
      100000    2.73564239569613e+02  
      150000    2.73851073534982e+02  

Explanation:

- **Header**:  
  ``# step         Rg1``  
  1. `step`  
     - The LAMMPS timestep at which the colvar (radius of gyration, Rg) was recorded.  
  2. `Rg1`  
     - The computed radius of gyration (in Å) for the polymer ensemble, as specified in the corresponding “.colvars” input file.

- **First Data Row** (``0  2.76034911120119e+02``):  
  1. At timestep 0 (starting point).  
  2. Rg1 ≈ 276.0349 Å.

- **Second Data Row** (``50000  2.74510753203738e+02``):  
  1. At timestep 50 000.  
  2. Rg1 ≈ 274.5108 Å.

- And so on—for every 50 000 steps, a new Rg value is recorded.

LAMMPS Dump Trajectory: ``traj_<fName>.dump``
---------------------------------------------

Below is a representative excerpt from the dump file, named ``traj_<fName>.dump``. Every block begins with a header indicating the timestep, number of atoms, and box bounds. Then the “ATOMS” section lists each atom’s properties.

.. code-block:: text

    ITEM: TIMESTEP
    0
    ITEM: NUMBER OF ATOMS
    14000
    ITEM: BOX BOUNDS pp pp pp
    -4.2000000000000000e+02 4.2000000000000000e+02
    -4.2000000000000000e+02 4.2000000000000000e+02
    -4.2000000000000000e+02 4.2000000000000000e+02
    ITEM: ATOMS id type mol mass x y z xu yu zu
    10550 4 151 1000 -184.08 -109.786 -288.422 -184.08 -109.786 -288.422
    1331  2  20  1000 -182.748 -155.882 -274.969 -182.748 -155.882 -274.969

    … (more atom lines) …

    ITEM: TIMESTEP
    10000000
    ITEM: NUMBER OF ATOMS
    14000
    ITEM: BOX BOUNDS pp pp pp
    -4.2000000000000000e+02 4.2000000000000000e+02
    -4.2000000000000000e+02 4.2000000000000000e+02
    -4.2000000000000000e+02 4.2000000000000000e+02
    ITEM: ATOMS id type mol mass x y z xu yu zu
    10536 4 151 1000 -182.684 -104.62 -299.423 -182.684 -104.62 -299.423
    10540 4 151 1000 -197.195 -86.1441 -295.77 -197.195 -86.1441 -295.77

Explanation:

- **`ITEM: TIMESTEP` / `0`**  
  - Indicates that the following block corresponds to timestep 0.
- **`ITEM: NUMBER OF ATOMS` / `14000`**  
  - There are 14 000 atoms in the system at every dump interval.
- **`ITEM: BOX BOUNDS pp pp pp`**  
  - The box boundaries (periodic in x, y, z):  
    - X: from –420.0 Å to +420.0 Å  
    - Y: from –420.0 Å to +420.0 Å  
    - Z: from –420.0 Å to +420.0 Å
- **`ITEM: ATOMS id type mol mass x y z xu yu zu`**  
  - Columns for each atom line:  
    1. `id` → Atom ID (unique integer).  
    2. `type` → Atom type (1 to 4).  
    3. `mol` → Molecule ID (which polymer the atom belongs to).  
    4. `mass` → Atom mass (in amu).  
    5. `x y z` → Wrapped coordinates (in Å).  
    6. `xu yu zu` → Unwrapped coordinates (in Å).
- **Example atom line**  
  ``10550 4 151 1000 -184.08 -109.786 -288.422 -184.08 -109.786 -288.422``:  
  1. `10550` → Atom ID.  
  2. `4` → Atom type (type 4 = “BL” bead).  
  3. `151` → Molecule ID number (this atom belongs to polymer #151).  
  4. `1000` → Mass of bead = 1000 amu.  
  5. `-184.08 -109.786 -288.422` → Wrapped x, y, z coordinates (inside the box).  
  6. `-184.08 -109.786 -288.422` → Unwrapped coordinates (identical here, no boundary crossing).

- **Next block** at timestep 10 000 000 has the same structure—box bounds remain constant, and new atom coordinates appear.

Colvars Metadynamics Hills: ``<fName>.colvars.meta-radgy.hills.traj``
-----------------------------------------------------------------------

Below is a snippet from the metadynamics hills trajectory file, named ``<fName>.colvars.meta-radgy.hills.traj``:

.. code-block:: text

               0     2.65169992360953e+02    1.00000000000000e+00   2.00000000000000e-01
             500     2.65195448031953e+02    1.00000000000000e+00   2.00000000000000e-01
            1000     2.65215417786256e+02    1.00000000000000e+00   2.00000000000000e-01
            1500     2.65194930116933e+02    1.00000000000000e+00   2.00000000000000e-01
            2000     2.65220340394216e+02    1.00000000000000e+00   2.00000000000000e-01
            2500     2.65191453444289e+02    1.00000000000000e+00   2.00000000000000e-01
            3000     2.65124148120669e+02    1.00000000000000e+00   2.00000000000000e-01

Explanation:

- **Columns**:  
  1. **Time Index** (number of colvar steps, not LAMMPS timesteps)  
     - Here `0`, `500`, `1000`, etc., correspond to successive hills added by metadynamics.  
  2. **Colvar Value (Rg1)**  
     - The R<sub>g</sub> value (in Å) at which a Gaussian hill was deposited (e.g., `2.65169992360953e+02` ≈ 265.17 Å).  
  3. **Hill Weight**  
     - The height of that hill (e.g., `1.00000000000000e+00` = 1 kcal/mol).  
  4. **Hill Width**  
     - The width of the Gaussian hill (e.g., `2.00000000000000e-01` = 0.2 Å).

Each line corresponds to one hill added to the free‐energy bias. Over time, these hills accumulate to reconstruct a free‐energy profile along R<sub>g</sub>.

Potential of Mean Force (PMF): ``<fName>.pmf``
-----------------------------------------------

Below is a small segment of a PMF output file, named ``<fName>.pmf``:

.. code-block:: text

    # 1
    #          0         1       277  0

     0.5  1711.9
     1.5  1711.9
     2.5  1711.9
     3.5  1711.9
     4.5  1711.9

Explanation:

- **Header lines**:  
  - `# 1` → A comment, often indicating the replicate number or block.  
  - `#          0         1       277  0` → Metadata about binning or file format (e.g., bin indices, colvar range, etc.).  
- **Data columns**:  
  1. **Bin Center**  
     - For example, `0.5` means the PMF value at R<sub>g</sub> = 0.5 Å (assuming bins of width 1 Å).  
  2. **PMF Value**  
     - Here `1711.9` is the free‐energy (kcal/mol) at that bin center.

Subsequent lines list PMF at bin centers: 1.5 Å, 2.5 Å, etc.

Restart Files: ``*_tp_*.restart`` and ``final_state_<fName>.restart``
-----------------------------------------------------------------------

There are two types of restart files:

1. **Intermediate Restart Files** (`<fName>_tp_*.restart`)  
   - These appear every “dt_restart” timesteps (for example, 25 000 000; 50 000 000; etc.).  
   - Each contains a binary snapshot of all atom positions, velocities, bonds, and simulation state.  
   - To resume a LAMMPS run from a given restart:  
     .. code-block:: bash

         lmp_serial -r <fName>_tp_25000000.restart -in <restart_input.in>

   - They ensure that, if the job stops early, you can pick up exactly where you left off.

2. **Final Restart File** (`final_state_<fName>.restart`)  
   - Created at the very end of the production run.  
   - Contains the final state of atoms, bonds, and simulation parameters.  
   - Typically used for post‐processing (e.g., visualization in OVITO) or as a starting point for a new simulation.

LAMMPS Log File: ``<fName>.log``
-------------------------------

The LAMMPS log file (``<fName>.log``) captures:

- Startup messages (compiled fixes, commands parsed).  
- “Read_data” confirmation (number of atoms, box dimensions).  
- Warnings or errors encountered during the run.  
- Per‐step thermo output (if not redirected entirely to ``Thermo_<fName>.dat``).  
- Summary information when a restart is written.

A typical snippet might look like:

.. code-block:: text

    LAMMPS (5Dec20)
    Reading data file ...
      orthogonal box = (-420 420) x (-420 420) y (-420 420) z
      14000 atoms
      13800 bonds
      13600 angles
    [Many lines of neighbor lists, fixes applied, etc.]
    Step Temp KinEng PotEng ...
    1000000 309.909 12932.007 2421.2753 ...
    [etc.]

Explanation:

- **“LAMMPS (5Dec20)”**  
  - The version of the LAMMPS executable.  
- **“Reading data file …”**  
  - Confirms which data file was read and its contents.  
- **Box dimensions**  
  - The `orthogonal box = ...` line shows the x/y/z bounds.  
- **Counts**  
  - Number of atoms, bonds, angles, etc.  
- **Fixes and styles**  
  - Details about which styles (e.g., “angle_style cosine”) were activated.  
- **Per‐step Thermo lines** (if not suppressed entirely).  

Even if most thermo is printed to the separate “Thermo_*.dat” file, the log file still records initial setup and any warnings or errors.

Summary of All Simulation Outputs
---------------------------------

Below is a checklist of all output files described above. Each file’s purpose is summarized in one sentence:

- **``Thermo_<fName>.dat``**  
  – Tabulated thermodynamic quantities (step, temperature, kinetic & potential energies, pair/bond/angle energies, and bond count) recorded every “dt_thermo” steps.

- **``BondData_<fName>.dat``**  
  – Cumulative counts of bonds formed and broken at each “dt_thermo” interval.

- **``<fName>.colvars.traj``**  
  – Trajectory of the collective variable(s) (e.g., radius of gyration) recorded at each colvars step.

- **``traj_<fName>.dump``**  
  – Full per‐atom snapshot (ID, type, molecule, mass, wrapped and unwrapped coordinates) every “dt_movie” steps.

- **``<fName>.colvars.meta-radgy.hills.traj``**  
  – Metadynamics hill data: bin center (colvar), hill weight, hill width at each “newHillFrequency” step.

- **``<fName>.pmf``**  
  – Potential of mean force (free‐energy) vs. colvar bin center for the final bias.

- **``<fName>_tp_*.restart``**  
  – Intermediate binary restart files, written every “dt_restart” steps.

- **``final_state_<fName>.restart``**  
  – Final restart file at the end of the production run.

- **``<fName>.log``**  
  – LAMMPS log, containing startup messages, setup summary, any warnings/errors, and (optionally) thermo output.
