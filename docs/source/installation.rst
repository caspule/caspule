Installation
============

This guide walks you through compiling **LAMMPS 3 Mar 2020** with the
custom ``bond/create/random`` fix needed for the *generate_InitCond*
polymer-network examples.  
The steps assume access to an FASRC‐style cluster, but they also work
on any system that provides recent CMake, GCC ≥ 14, and Open MPI.

.. note::

   ``bond/create/random`` is *not* part of vanilla 3 Mar 2020.
   We patch it in manually from the
   `pdebuyl/lammps *fbc_random* branch <https://github.com/pdebuyl/lammps/tree/fbc_random/src/MC>`_.

Prerequisites
-------------

1. **Start an interactive job**

   .. code-block:: bash

      salloc -p test --mem 4G -t 0-3:00

2. **Load build tools**

   .. code-block:: bash

      module avail  # just to confirm the names below
      module load cmake/3.31.6-fasrc01
      module load gcc/14.2.0-fasrc01
      module load openmpi/5.0.5-fasrc01

Source code
-----------

3. **Download and unpack LAMMPS 3 Mar 2020**

   .. code-block:: bash

      wget https://download.lammps.org/tars/lammps-3Mar2020.tar.gz
      tar -xf lammps-3Mar2020.tar.gz
      cd lammps-3Mar2020

4. **Add the patched fix**

   Copy the two files below into *src/MC* (create the folder if absent):

   .. code-block:: bash

      cp /path/to/fix_bond_create_random.cpp src/MC/
      cp /path/to/fix_bond_create_random.h   src/MC/

   (They come from the *fbc_random* branch linked above.)

Configure & build
-----------------

5. **Create a build directory**

   .. code-block:: bash

      mkdir build && cd build

6. **Configure with CMake** (MPI build):

   .. code-block:: bash

      cmake ../cmake -DBUILD_MPI=on

7. **Enable required packages**

   The 2020 release still uses old package names:

   .. code-block:: bash

      cmake -DPKG_MC=on \
            -DPKG_MOLECULE=on \
            -DPKG_USER-MISC=on \
            -DPKG_USER-COLVARS=on .

8. **Compile**

   .. code-block:: bash

      cmake --build . -j$(nproc)

   The resulting executable is:

   ``lammps-3Mar2020/build/lmp``

Sanity check
------------

Verify that the new fix is available:

.. code-block:: bash

   ./lmp -h | grep bond/create/random

Expected output::

   bond/create/random       Create bonds (random partner selection)  [MC]

If nothing appears, the patch was not picked up—revisit **Step 4** or
ensure ``-DPKG_MC=on`` was passed to CMake.

Optional: Python wrapper
------------------------

If you plan to control LAMMPS from Jupyter/NumPy:

.. code-block:: bash

   pip install --user lammps-cython

Troubleshooting
---------------

* **“Package MC is not enabled”**  
  Re-run CMake with ``-DPKG_MC=on`` and rebuild.

* **“New bond exceeded bonds per atom …”**  
  Increase *maxbond* in your ``bond/create/random`` command or raise
  ``extra/special/per/atom`` in the ``read_data`` section.

With LAMMPS successfully built you can run the *generate_InitCond*
pipeline and companion analysis notebooks without further modification.
