Example System Setup
====================

This section walks through a complete, working example:
1. Defining a small polymer system and generate initial configuration (.data) file
2. Launching a short LAMMPS simulation
3. Examining the key output files and results

.. note::

   A ready-to-download folder with example scripts and files is available at our `GitHub repository <https://github.com/caspule/caspule/tree/main/example>_`.

Generating Initial Condition
-----------------------------------------------------

Below is a line-by-line breakdown of the key commands in `create_InitCoor.sh`. Each code snippet is followed by its purpose.

.. code-block:: bash

    n=10 # segment count

Sets the variable `n` to `10`, which means each polymer chain will consist of 10 repeats of the segment pattern.

.. code-block:: bash

    seg=2212212 # segment pattern

Assigns the pattern string `2212212` to `seg`. Each digit indicates whether that bead is a “sticker” (`1`) or a “spacer” (`2`).

.. code-block:: bash

    NA=100 # A-chain count
    NB=100 # B-chain count

`NA=100` means we will create 100 copies of the “A” polymer, and `NB=100` creates 100 copies of the “B” polymer.

.. code-block:: bash

    L=300

Sets the half-box length to 300 Å in each direction.

.. code-block:: bash

    pck_inp='populate_tmp.inp'
    pck_out='IC_tmp.xyz'

- `pck_inp='populate_tmp.inp'` is the name of the Packmol input file to be generated.
- `pck_out='IC_tmp.xyz'` is the name of the XYZ file that Packmol will produce (initial coordinates for LAMMPS).

.. code-block:: bash

    cvfile='N400_Rg_L700.colvars'
    sysName="b70_N200_L$L.lt"
    dataFile="b70_N200_L$L.data"
    lmp_input='Template_input.in'

- `cvfile='N400_Rg_L700.colvars'` is the template Colvars input file used by `updateColVar.py`.
- `sysName="b70_N200_L$L.lt"` resolves to `b70_N200_L300.lt`, the Moltemplate system file.
- `dataFile="b70_N200_L$L.data"` resolves to `b70_N200_L300.data`, which Moltemplate outputs.
- `lmp_input='Template_input.in'` is the LAMMPS input template that `updateInput.py` will read and customize.

.. code-block:: bash

    python3 LT_writer.py $n $seg

Runs `LT_writer.py 10 2212212`, generating:
- `polyA_n10.lt`
- `polyB_n10.lt`
- `polyA_n10_mono.xyz`
- `polyB_n10_mono.xyz`

.. code-block:: bash

    python3 writePackmolInput.py $n $NA $NB $L $pck_inp $pck_out

Runs `writePackmolInput.py 10 100 100 300 populate_tmp.inp IC_tmp.xyz`. Creates `populate_tmp.inp` to place 100 A-chains and 100 B-chains inside a 600 Å cube.

.. code-block:: bash

    python3 writeSysLT.py $n $NA $NB $L $sysName

Runs `writeSysLT.py 10 100 100 300 b70_N200_L300.lt`, producing:
- `b70_N200_L300.lt`, which imports `polyA_n10.lt` and `polyB_n10.lt`, defines 100 copies each, and writes the boundary.

.. code-block:: bash

    packmol < $pck_inp

Feeds `populate_tmp.inp` into Packmol. The output is `IC_tmp.xyz`, the initial coordinates for all 200 polymers.

.. code-block:: bash

    moltemplate.sh -xyz $pck_out $sysName -nocheck

Runs Moltemplate on `IC_tmp.xyz b70_N200_L300.lt`, producing `b70_N200_L300.data` (the LAMMPS data file).

.. code-block:: bash

    python3 updateColVar.py $pck_out $cvfile $L $n $NA $NB $seg

Runs `updateColVar.py IC_tmp.xyz N400_Rg_L700.colvars 300 10 100 100 2212212`, which:
- Computes the initial :math:`R_{g}` and box dimensions from `IC_tmp.xyz`.
- Writes `N200_Rg_L300.colvars`, updating `upperBoundary`, `upperWalls`, and `atomNumbers`.

.. code-block:: bash

    python3 updateInput.py $lmp_input $L

Runs `updateInput.py Template_input.in 300`, which reads `Template_input.in` and writes:
- `b70_N200_L300.in`
- `submit_b70_N200_L300.sh`
Inserting correct filenames (e.g., `read_data b70_N200_L300.data`).

.. code-block:: bash

    python3 fix_datafiles.py $dataFile

Runs `fix_datafiles.py b70_N200_L300.data`, which:
- Changes “2 bond types” → “3 bond types”
- Inserts “50 extra bond per atom”

Inspecting “b70_N200_L500.data”
------------------------------

Below is a trimmed excerpt from `b70_N200_L500.data`, broken into sections.

.. code-block:: text

    LAMMPS Description

A comment/header indicating this is a Moltemplate-generated data file.

.. code-block:: text

    14000  atoms
    13800  bonds
    13600  angles
    0  dihedrals
    0  impropers

- `14000 atoms`: total beads in the system.
- `13800 bonds`: total harmonic bonds between neighboring beads.
- `13600 angles`: total angles.
- `0 dihedrals` / `0 impropers`: none present.

.. code-block:: text

    4  atom types
    3  bond types
    50 extra bond per atom
    2  angle types
    0  dihedral types
    0  improper types

- `4 atom types`: four distinct bead types (A, AL, B, BL).
- `3 bond types`: three bond types (one added by `fix_datafiles.py`).
- `50 extra bond per atom`: allocated by `fix_datafiles.py`.
- `2 angle types`: two unique angle parameters.
- `0 dihedral types` / `0 improper types`: none used.

.. code-block:: text

    -420.0 420.0 xlo xhi
    -420.0 420.0 ylo yhi
    -420.0 420.0 zlo zhi

Simulation box ranges from –420 Å to +420 Å in each dimension (since `L=300` plus buffer).

.. code-block:: text

    Masses

The “Masses” section begins here.

.. code-block:: text

    1 1000  # A
    2 1000  # AL
    3 1000  # B
    4 1000  # BL

- Type 1 (A) mass = 1000 amu.
- Type 2 (AL) mass = 1000 amu.
- Type 3 (B) mass = 1000 amu.
- Type 4 (BL) mass = 1000 amu.

.. code-block:: text

    Atoms

Begins atom definitions.

.. code-block:: text

    1 1 2 0  71.348682 -75.514994 -53.224331
    2 1 2 0  70.344153 -73.813962 -52.912221

- `1 1 2 0 71.348682 -75.514994 -53.224331`:
  - Atom ID = 1
  - Molecule ID = 1
  - Type = 2 (AL)
  - Charge = 0
  - Coordinates = (71.348682, –75.514994, –53.224331)

*(…continues for all 14 000 atoms…)*

.. code-block:: text

    Bonds

Begins bond definitions.

.. code-block:: text

    1 1 1 2
    2 1 2 3
    3 1 3 4

- `1 1 1 2`: Bond ID = 1, Type = 1, connects atom 1–2.
- `2 1 2 3`: Bond ID = 2, Type = 1, connects atom 2–3.
- `3 1 3 4`: Bond ID = 3, Type = 1, connects atom 3–4.

*(…continues for all 13 800 bonds…)*

.. code-block:: text

    Angles

Begins angle definitions.

.. code-block:: text

    1 1 1 2 3
    2 1 2 3 4

- `1 1 1 2 3`: Angle ID = 1, Type = 1, between atoms (1, 2, 3).
- `2 1 2 3 4`: Angle ID = 2, Type = 1, between atoms (2, 3, 4).

*(…continues for all 13 600 angles…)*

Inspecting “N200_Rg_L500.colvars”
--------------------------------

Below is the full `N200_Rg_L500.colvars`, with each block explained.

.. code-block:: text

    colvarsTrajFrequency 50000
    colvarsRestartFrequency 50000

- `colvarsTrajFrequency 50000`: Write colvar trajectory every 50 000 steps.
- `colvarsRestartFrequency 50000`: Write colvar restart file every 50 000 steps.

.. code-block:: text

    colvar {
       name Rg1

Starts a colvar block named `Rg1`.

.. code-block:: text

       lowerBoundary 0.0
       upperBoundary 280

- `lowerBoundary 0.0`: Minimum :math:`R_{g}` value.
- `upperBoundary 280`: Maximum :math:`R_{g}` value.

.. code-block:: text

       gyration {
          atoms {
             atomNumbers {
                36 71 106 141 176 211 246 281 316 351 386 421 456 491
                526 561 596 631 666 701 736 771 806 841 876 911 946 981
                1016 1051 1086 1121 1156 1191 1226 1261 1296 1331 1366
                1401 1436 1471 1506 1541 1576 1611 1646 1681 1716 1751
                1786 1821 1856 1891 1926 1961 1996 2031 2066 2101 2136
                2171 2206 2241 2276 2311 2346 2381 2416 2451 2486 2521
                2556 2591 2626 2661 2696 2731 2766 2801 2836 2871 2906
                2941 2976 3011 3046 3081 3116 3151 3186 3221 3256 3291
                3326 3361 3396 3431 3466 3501 3536 3571 3606 3641 3676
                3711 3746 3781 3816 3851 3886 3921 3956 3991 4026 4061
                4096 4131 4166 4201 4236 4271 4306 4341 4376 4411 4446
                4481 4516 4551 4586 4621 4656 4691 4726 4761 4796 4831
                4866 4901 4936 4971 5006 5041 5076 5111 5146 5181 5216
                5251 5286 5321 5356 5391 5426 5461 5496 5531 5566 5601
                5636 5671 5706 5741 5776 5811 5846 5881 5916 5951 5986
                6021 6056 6091 6126 6161 6196 6231 6266 6301 6336 6371
                6406 6441 6476 6511 6546 6581 6616 6651 6686 6721 6756
                6791 6826 6861 6896 6931 6966 7001 7036 7071 7106 7141
                7176 7211 7246 7281 7316 7351 7386 7421 7456 7491 7526
                7561 7596 7631 7666 7701 7736 7771 7806 7841 7876 7911
                7946 7981 8016 8051 8086 8121 8156 8191 8226 8261 8296
                8331 8366 8401 8436 8471 8506 8541 8576 8611 8646 8681
                8716 8751 8786 8821 8856 8891 8926 8961 8996 9031 9066
                9101 9136 9171 9206 9241 9276 9311 9346 9381 9416 9451
                9486 9521 9556 9591 9626 9661 9696 9731 9766 9801 9836
                9871 9906 9941 9976 10011 10046 10081 10116 10151 10186
                10221 10256 10291 10326 10361 10396 10431 10466 10501
                10536 10571 10606 10641 10676 10711 10746 10781 10816
                10851 10886 10921 10956 10991 11026 11061 11096 11131
                11166 11201 11236 11271 11306 11341 11376 11411 11446
                11481 11516 11551 11586 11621 11656 11691 11726 11761
                11796 11831 11866 11901 11936 11971 12006 12041 12076
                12111 12146 12181 12216 12251 12286 12321 12356 12391
                12426 12461 12496 12531 12566 12601 12636 12671 12706
                12741 12776 12811 12846 12881 12916 12951 12986 13021
                13056 13091 13126 13161 13196 13231 13266 13301 13336
                13371 13406 13441 13476 13511 13546 13616 13651 13686
                13721 13756 13791 13826 13861 13896 13931 13966
             }
          }
       }

Lists all atom indices which will experience metadynamic bias.

.. code-block:: text

    metadynamics {
       name meta-radgy
       colvars Rg1
       hillWeight 0.2
       newHillFrequency 500
       dumpFreeEnergyFile yes
       writeHillsTrajectory on
       hillwidth 1.0
       wellTempered on
       biasTemperature 310
    }

- `metadynamics {`: Begins a metadynamics block.
- `name meta-radgy`: Names the bias “meta-radgy.”
- `colvars Rg1`: Applies metadynamics on `Rg1`.
- `hillWeight 0.2`: Gaussian hill height = 0.2 kcal/mol.
- `newHillFrequency 500`: New hill every 500 steps.
- `dumpFreeEnergyFile yes`: Write free‐energy profile.
- `writeHillsTrajectory on`: Save hill history.
- `hillwidth 1.0`: Gaussian width = 1 Å.
- `wellTempered on`: Enable well-tempered MD.
- `biasTemperature 310`: Bias temperature = 310 K.

.. code-block:: text

    harmonicWalls {
       name wall_Rg
       colvars Rg1
       upperWalls 275
       upperWallConstant 20.0
    }

- `harmonicWalls {`: Begins a harmonic-walls block.
- `name wall_Rg`: Names this constraint “wall_Rg.”
- `colvars Rg1`: Applies the wall to colvar `Rg1`.
- `upperWalls 275`: Place a hard wall at :math:`R_{g}` = 275 Å.
- `upperWallConstant 20.0`: Wall force constant = 20 kcal/mol/Å².

Inspecting “b70_N200_L500.in”
-----------------------------

Below is the LAMMPS input file, split into logical blocks with explanations.

.. code-block:: text

    variable T equal 310

Defines LAMMPS variable `T` (temperature) = 310 K.

.. code-block:: text

    variable seed equal 14327

Sets the random seed for Langevin dynamics and bond creation = 14327.

.. code-block:: text

    variable fName string b70_N200_L300

Defines `fName` = “b70_N200_L300”, used to name log, data, and output files.

.. code-block:: text

    log ${fName}.log

Directs LAMMPS console output into `b70_N200_L300.log`.

.. code-block:: text

    units           real
    boundary p p p
    atom_style      full

- `units real`: Use real-units (Å, fs, kcal/mol).
- `boundary p p p`: Periodic boundary in x, y, z.
- `atom_style full`: Each atom has charge, bonds, angles, etc.

.. code-block:: text

    neighbor 1.9 bin
    neigh_modify every 1 delay 1 check yes

- `neighbor 1.9 bin`: Build neighbor list with 1.9 Å skin, bin‐sorting.
- `neigh_modify every 1 delay 1 check yes`: Update neighbor list every step, no delay.

.. code-block:: text

    read_data b70_N200_L300.data extra/special/per/atom 50

Reads the data file `b70_N200_L300.data`, allowing 50 special bond tags per atom.

.. code-block:: text

    angle_style  cosine
    angle_coeff   *  2  # K (energy unit)

- `angle_style cosine`: Use a cosine-based angle potential.
- `angle_coeff * 2`: Force constant K = 2 for all angle types.

.. code-block:: text

    bond_style   hybrid harmonic harmonic/shift/cut
    bond_coeff   1   harmonic 3   10
    bond_coeff   2   harmonic 3   10
    bond_coeff   3   harmonic/shift/cut 6   11.22   12.72

- `bond_style hybrid harmonic harmonic/shift/cut`: Use hybrid bond potentials.
- `bond_coeff 1 harmonic 3 10`: Type 1 bonds: K = 3, length = 10 Å.
- `bond_coeff 2 harmonic 3 10`: Type 2 bonds: K = 3, length = 10 Å.
- `bond_coeff 3 harmonic/shift/cut 6 11.22 12.72`: Type 3 (sticker-sticker)bonds: K = 6, eq = 11.22 Å, cutoff = 12.72 Å.

.. code-block:: text

    pair_style lj/cut 25
    pair_coeff * * 0.3 10 25

- `pair_style lj/cut 25`: Lennard-Jones with 25 Å cutoff.
- `pair_coeff * * 0.3 10 25`: For all pairs, ε = 0.3 kcal/mol, σ = 10 Å, cutoff = 25 Å.

.. code-block:: text

    special_bonds lj 0 1 1 angle yes

Skip LJ for directly bonded 1‑2 pairs while retaining full LJ on 1‑3 pairs that form angles/dihedrals and on all 1‑4 neighbors.

.. code-block:: text

    minimize 1.0e-4 1.0e-6 100000 100000 # force_tol, energy_tol, maxiter, maxeval

- Minimize with:
  - Force tol = 1×10⁻⁴ kcal/mol·Å
  - Energy tol = 1×10⁻⁶ kcal/mol
  - Max iterations = 100 000
  - Max energy evaluations = 100 000

.. code-block:: text

    # further equilibrate the system before bond formation takes place
    fix fxlan all langevin $T $T 500 ${seed}
    fix fxnve all nve
    timestep 0.1
    run 10000

- `fix fxlan all langevin $T $T 500 ${seed}`: Langevin thermostat at 310 K, damping = 500 fs, seed = 14327.
- `fix fxnve all nve`: NVE integration combined with Langevin.
- `timestep 0.1`: 0.1 fs timestep.
- `run 10000`: Run 10 000 steps to equilibrate.

.. code-block:: text

    unfix fxlan
    unfix fxnve
    reset_timestep 0

- `unfix fxlan` / `unfix fxnve`: Remove previous fixes.
- `reset_timestep 0`: Reset the step counter to 0.

.. code-block:: text

    variable t equal step
    variable steps equal 400000000
    variable dt_thermo equal 1000000
    variable dt_movie equal 10000000
    variable dt_restart equal 40000000

- `variable t equal step`: Convenience variable for the current timestep.
- `variable steps equal 400000000`: Production run length = 400 million steps.
- `variable dt_thermo equal 1000000`: Thermo output every 1 000 000 steps.
- `variable dt_movie equal 10000000`: Dump trajectory every 10 000 000 steps.
- `variable dt_restart equal 40000000`: Write intermediate restart every 40 000 000 steps.

.. code-block:: text

    group rxnSites type 1 3
    fix CV_Rg all colvars N200_Rg_L300.colvars output ${fName}

- `group rxnSites type 1 3`: Define group “rxnSites” containing atom types 1 & 3 (stickers).
- `fix CV_Rg all colvars N200_Rg_L300.colvars output ${fName}`: Attach Colvars using `N200_Rg_L300.colvars`, writing output prefixed by `b70_N200_L300`.

.. code-block:: text

    fix bondc rxnSites bond/create/random 20 1 3 12.72 3 prob 1 ${seed}

Every 20 steps, attempt to form a type 3 bond between atoms of type 1 & 3 if separation ≤ 12.72 Å, with probability 1, seed = 14327.

.. code-block:: text

    fix bondbr rxnSites bond/break 20 3 12.72 prob 1 ${seed}

Every 20 steps, attempt to break existing type 3 bonds if length > 12.72 Å, with probability 1.

.. code-block:: text

    variable frmbnd equal f_bondc[2]
    variable brkbnd equal f_bondbr[2]
    fix saveBond all print ${dt_thermo} "$t ${frmbnd} ${brkbnd}" file BondData_${fName}.dat screen no

- `variable frmbnd equal f_bondc[2]`: Number of bonds formed so far.
- `variable brkbnd equal f_bondbr[2]`: Number of bonds broken so far.
- `fix saveBond all print ${dt_thermo} "$t ${frmbnd} ${brkbnd}" file BondData_b70_N200_L300.dat screen no`: Write `<step> <formed> <broken>` every 1 000 000 steps.

.. code-block:: text

    thermo_style    custom step epair pe ke ebond eangle temp bonds
    thermo          ${dt_thermo}
    fix saveThermo all print ${dt_thermo} "$t $(temp) $(ke) $(pe) $(epair) $(ebond) $(eangle) $(bonds)" file Thermo_${fName}.dat title "# Steps Temp KinEng PotEng Epair Ebond Eangle Bonds" screen no

- `thermo_style custom ...`: Select which quantities to print in thermo output.
- `thermo ${dt_thermo}`: Print thermo every 1 000 000 steps.
- `fix saveThermo ...`: Write the same set (`step temp ke pe epair ebond eangle bonds`) to `Thermo_b70_N200_L300.dat`.

.. code-block:: text

    ############################ Langevin Dynamics ###############################
    fix fxlan all langevin $T $T 500 ${seed}
    fix fxnve all nve

Reapply Langevin + NVE for the production run after resetting the timestep.

.. code-block:: text

    comm_style      tiled
    fix fxbal all balance 1000 1.1 rcb

- `comm_style tiled`: Use tiled communication for parallel performance.
- `fix fxbal all balance 1000 1.1 rcb`: Every 1000 steps, rebalance domains using recursive coordinate bisection.

.. code-block:: text

    timestep 30

Switch to a 30 fs timestep for production dynamics.

.. code-block:: text

    dump coor all custom ${dt_movie} traj_${fName}.dump id type mol mass x y z xu yu zu

Every 10 000 000 steps, write atom coordinates (ID, type, molecule ID, mass, x y z, xu yu zu) to `traj_b70_N200_L300.dump`.

.. code-block:: text

    run ${steps}
    write_restart final_state_${fName}.restart

- `run ${steps}`: Execute the production run for 400 000 000 steps.
- `write_restart final_state_b70_N200_L300.restart`: At the end, write the final restart file.

