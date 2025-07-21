Installation
============

This guide walks you through compiling **LAMMPS 3 Mar 2020** with the
custom ``bond/create/random`` fix needed for the *generate_InitCond*
polymer-network examples.  Two build environments are supported:

- **Harvard FASRC-style cluster** (CMake, GCC ≥ 14, Open MPI modules)
- **macOS** (Conda environment, CMake, Open MPI)

.. note::

   The ``bond/create/random`` fix is *not* part of vanilla 3 Mar 2020.
   We patch it in manually from the
   `pdebuyl/lammps *fbc_random* branch <https://github.com/pdebuyl/lammps/tree/fbc_random/src/MC>`_.

Prerequisites (Harvard cluster)
--------------------------------

1. **Start an interactive job**:

   .. code-block:: bash

      salloc -p test --mem 4G -t 0-3:00

2. **Load build tools**:

   .. code-block:: bash

      module avail    # confirm available module names
      module load cmake/3.31.6-fasrc01
      module load gcc/14.2.0-fasrc01
      module load openmpi/5.0.5-fasrc01

Source code
-----------

3. **Download and unpack LAMMPS 3 Mar 2020**:

   .. code-block:: bash

      wget https://download.lammps.org/tars/lammps-3Mar2020.tar.gz
      tar -xf lammps-3Mar2020.tar.gz
      cd lammps-3Mar2020

4. **Add the patched fix** (create the directory if absent):

   .. code-block:: bash

      mkdir -p src/MC
      cp /path/to/fix_bond_create_random.cpp src/MC/
      cp /path/to/fix_bond_create_random.h   src/MC/

Configure & build (Harvard cluster)
-----------------------------------

5. **Create a build directory**:

   .. code-block:: bash

      mkdir build && cd build

6. **Configure with CMake** (MPI build):

   .. code-block:: bash

      cmake ../cmake -DBUILD_MPI=on

7. **Enable required packages** (old package names):

   .. code-block:: bash

      cmake -DPKG_MC=on \
            -DPKG_MOLECULE=on \
            -DPKG_USER-MISC=on \
            -DPKG_USER-COLVARS=on .

8. **Compile**:

   .. code-block:: bash

      cmake --build . -j$(nproc)

   The resulting executable will be in::

      build/lmp

Sanity check
------------

Verify that the new fix is available:

.. code-block:: bash

   ./lmp -h | grep bond/create/random

Expected output::

   bond/create/random       Create bonds (random partner selection)  [MC]

Prerequisites (macOS)
---------------------

1. **Install Conda and create a new environment**:

   .. code-block:: bash

      # Assumes Miniconda or Anaconda is already installed
      conda create -n lammps_env
      conda activate lammps_env

2. **Install compilers and tools via Conda**:

   .. code-block:: bash

      conda install -c conda-forge cxx-compiler
      conda install -c conda-forge cmake=3.31.6
      conda install -c conda-forge openmpi

Configure & build (macOS)
-------------------------

3. **Download and unpack LAMMPS 3 Mar 2020** (same as step 3 above):

   .. code-block:: bash

      curl -O https://download.lammps.org/tars/lammps-3Mar2020.tar.gz
      tar -xf lammps-3Mar2020.tar.gz
      cd lammps-3Mar2020

4. **Add the patched fix** (same as step 4 above).

5. **Create a build directory**:

   .. code-block:: bash

      mkdir build && cd build

6. **Configure with CMake** (specify C++14 standard):

   .. code-block:: bash

      cmake ../cmake -DCMAKE_CXX_STANDARD=14

7. **Enable required packages**:

   .. code-block:: bash

      cmake -DPKG_MC=on \
            -DPKG_MOLECULE=on \
            -DPKG_USER-MISC=on \
            -DPKG_USER-COLVARS=on .

8. **Compile** (same as in step 8 above):

   .. code-block:: bash

      cmake --build . -j$(sysctl -n hw.ncpu)

   The executable will be in::

      build/lmp

Optional: Python wrapper
------------------------

If you plan to control LAMMPS from Jupyter or NumPy, install the Cython wrapper:

.. code-block:: bash

   pip install --user lammps-cython

Troubleshooting
---------------

* **“Package MC is not enabled”**  
  Re-run CMake with ``-DPKG_MC=on`` and rebuild.

* **“New bond exceeded bonds per atom …”**  
  Increase your ``maxbond`` setting in the ``bond/create/random`` command or raise
  ``extra/special/per/atom`` in the ``read_data`` section.
