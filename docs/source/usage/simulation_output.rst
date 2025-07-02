Simulation Output
=================

This page documents all of the primary output files produced by the
pipeline and by LAMMPS during and after the simulation.  Each subsection
shows a representative excerpt (or header) from the file, followed by a
line-by-line explanation of its contents.  No analysis is performed
here—just plain descriptions of what each column or section means.

Thermodynamic Data: ``Thermo_<fName>.dat``
------------------------------------------

Below is the header line and the first few rows of a typical thermodynamic
output file:

.. code-block:: text

    # Steps Temp KinEng PotEng Epair Ebond Eangle Bonds
    1000000 309.9092980089979 12932.006720561228 2421.2753602970483 -5608.9113003346756 -1676.5739699962255 9706.7606306279486 14845
    2000000 308.4459769650038 12870.944733402906 580.1671941493225 -6212.513108889987 -2765.9452470589113 9558.625550098221 15019
    3000000 308.9000673416380 12889.893180061661 -663.6937637213039 -6715.222056123977 -3378.1828104342594 9429.711102836933 15138
    4000000 307.9393191012913 12849.802731724838 -1247.4935140060538 -7047.389388496154 -3702.186514574762 9502.082389064863 15199

Explanation
~~~~~~~~~~~

1. **Header**

   ``# Steps Temp KinEng PotEng Epair Ebond Eangle Bonds``

   * `Steps` – Current LAMMPS timestep.  
   * `Temp` – Instantaneous temperature (K).  
   * `KinEng` – Total kinetic energy (kcal mol⁻¹).  
   * `PotEng` – Total potential energy.  
   * `Epair` – Pairwise (non-bonded) energy.  
   * `Ebond` – Bond energy.  
   * `Eangle` – Angle energy.  
   * `Bonds` – Total number of bonds at that step.

2. **First data row** (for example  
   ``1000000 309.909… 12932.0067 …``) follows the same column order.

Bond-Formation/Breaking Data: ``BondData_<fName>.dat``
------------------------------------------------------

Snippet:

.. code-block:: text

    1000000 1566 521
    2000000 2417 1198
    3000000 3330 1992
    4000000 4191 2792

*Columns*

* **Step** – Timestep of the record.  
* **Cumulative Bonds Formed** – Total new bonds so far.  
* **Cumulative Bonds Broken** – Total breaks so far.

Collective-Variable Trajectory: ``<fName>.colvars.traj``
--------------------------------------------------------

.. code-block:: text

    # step         Rg1
           0    2.76034911120119e+02
       50000    2.74510753203738e+02
      100000    2.73564239569613e+02
      150000    2.73851073534982e+02

* **step** – LAMMPS timestep.  
* **Rg1** – Radius of gyration (Å).

LAMMPS Dump Trajectory: ``traj_<fName>.dump``
---------------------------------------------

Each block begins with ``ITEM: TIMESTEP`` and ends with an ``ATOMS``
table:

.. code-block:: text

    ITEM: TIMESTEP
    0
    ITEM: NUMBER OF ATOMS
    14000
    ITEM: BOX BOUNDS pp pp pp
    -4.20e+02 4.20e+02
    -4.20e+02 4.20e+02
    -4.20e+02 4.20e+02
    ITEM: ATOMS id type mol mass x y z xu yu zu
    10550 4 151 1000 -184.08 -109.786 -288.422 -184.08 -109.786 -288.422
    …

Key columns are `id`, `type`, `mol`, `mass`, wrapped (`x y z`) and
unwrapped (`xu yu zu`) coordinates.

Colvars Metadynamics Hills: ``<fName>.colvars.meta-radgy.hills.traj``
--------------------------------------------------------------------

.. code-block:: text

               0     2.65169992360953e+02    1.00000000000000e+00   2.00000000000000e-01
             500     2.65195448031953e+02    1.00000000000000e+00   2.00000000000000e-01
            1000     2.65215417786256e+02    1.00000000000000e+00   2.00000000000000e-01

Columns: index (colvar steps), R<sub>g</sub>, hill height, hill width.

Potential of Mean Force (PMF): ``<fName>.pmf``
----------------------------------------------

.. code-block:: text

    # 1
    #          0         1       277  0
     0.5  1711.9
     1.5  1711.9
     2.5  1711.9

* **First column** – Bin centre (Å).  
* **Second column** – PMF value (kcal mol⁻¹).

Restart Files
-------------

Intermediate restarts (``<fName>_tp_*.restart``)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Binary snapshots written every *dt_restart* steps let you resume from an
earlier point by replacing the line:

.. code-block:: text

    read_data b70_N200_L300.data extra/special/per/atom 50s

with 

.. code-block:: text

    read_restart <fName>_tp_25000000.restart

Final restart (``final_state_<fName>.restart``)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Written at the end of the run; useful for visualisation or as
the starting point for a new simulation.

LAMMPS Log File: ``<fName>.log``
--------------------------------

Captures start-up messages, warnings/errors and (optionally) thermo
output.  A typical header:

.. code-block:: text

    LAMMPS (5Dec20)
    Reading data file ...
      orthogonal box = (-420 420) x (-420 420) y (-420 420) z
      14000 atoms
      13800 bonds
      13600 angles

Summary of All Simulation Outputs
---------------------------------

* **``Thermo_<fName>.dat``** – step, temperature, energies & bond count.  
* **``BondData_<fName>.dat``** – cumulative bonds formed/broken.  
* **``<fName>.colvars.traj``** – colvar history.  
* **``traj_<fName>.dump``** – full atom snapshots.  
* **``<fName>.colvars.meta-radgy.hills.traj``** – metadynamics hills.  
* **``<fName>.pmf``** – final PMF vs colvar.  
* **``<fName>_tp_*.restart``** – periodic binary restarts.  
* **``final_state_<fName>.restart``** – last restart in the run.  
* **``<fName>.log``** – LAMMPS log (setup, warnings, optional thermo).
