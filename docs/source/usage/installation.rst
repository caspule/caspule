Installation
============

This guide provides steps on how to compile **LAMMPS 3 Mar 2020** with the
custom ``bond/create/random`` fix needed to define intersticker crosslinks, and set up the Python tools used for
**data analysis**. 

We provide two examples of setting up the environment:

- **High Performance Computing (Harvard FASRC cluster in our example) facility** (CMake, GCC ≥ 14, Open MPI modules); this procedure can be easily adapted to personal linux (or WSL in Windows) machines.
- **macOS** (Conda environment, CMake, Open MPI)

.. note::

   The ``bond/create/random`` fix is *not* part of vanilla 3 Mar 2020.
   We patch it in manually from the
   `pdebuyl/lammps fbc_random branch <https://github.com/pdebuyl/lammps/tree/fbc_random/src/MC>`_.

Install Packmol & Moltemplate
-----------------------------

CASPULE Step 1 requires **Packmol** and **Moltemplate** on your ``$PATH``.

**Conda (recommended, Linux/macOS):**

.. code-block:: bash

   conda install -c conda-forge packmol moltemplate

**From source / project pages:**

- Packmol: `official site <https://m3g.iqm.unicamp.br/packmol>`_ (download + build)
- Moltemplate: `docs & downloads <https://moltemplate.org/>`_  |  `GitHub <https://github.com/jewettaij/moltemplate>`_

Verify:

.. code-block:: bash

   packmol -v
   moltemplate.sh -h | head -n 5

Python environment (analysis tools)
-----------------------------------

CASPULE’s analysis scripts expect Python ≥ 3.9 and the packages below.

**Conda (one line):**

.. code-block:: bash

   conda create -n caspule_py python=3.11 numpy scipy pandas matplotlib networkx tqdm numba h5py  # optional: seaborn mdtraj
   conda activate caspule_py

**Pip (inside a clean venv):**

.. code-block:: bash

   python -m venv .venv && source .venv/bin/activate
   pip install --upgrade pip
   pip install numpy scipy pandas matplotlib networkx tqdm numba h5py  # optional: seaborn mdtraj

Optional (Python↔LAMMPS):

.. code-block:: bash

   pip install --user lammps-cython

Harvard cluster: prerequisites
------------------------------

1. **Start an interactive job**:

   .. code-block:: bash

      salloc -p test --mem 4G -t 0-3:00

2. **Load build tools**:

   .. code-block:: bash

      module avail    # confirm available module names
      module load cmake/3.31.6-fasrc01
      module load gcc/14.2.0-fasrc01
      module load openmpi/5.0.5-fasrc01

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

macOS: prerequisites
--------------------

1. **Install Conda and create a new environment**:

   .. code-block:: bash

      conda create -n lammps_env
      conda activate lammps_env

2. **Install compilers and tools via Conda**:

   .. code-block:: bash

      conda install -c conda-forge cxx-compiler
      conda install -c conda-forge cmake=3.31.6
      conda install -c conda-forge openmpi

Configure & build (macOS)
-------------------------

3. **Download and unpack LAMMPS 3 Mar 2020** (same as above):

   .. code-block:: bash

      curl -O https://download.lammps.org/tars/lammps-3Mar2020.tar.gz
      tar -xf lammps-3Mar2020.tar.gz
      cd lammps-3Mar2020

4. **Add the patched fix** (same as above).

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

8. **Compile**:

   .. code-block:: bash

      cmake --build . -j$(sysctl -n hw.ncpu)

   The executable will be in::

      build/lmp

Troubleshooting
---------------

* **“Packmol/Moltemplate not found”**  
  Confirm they’re installed and on ``$PATH`` (see commands above).

* **“Package MC is not enabled”**  
  Re-run CMake with ``-DPKG_MC=on`` and rebuild.

* **“New bond exceeded bonds per atom …”**  
  Increase ``maxbond`` in the ``bond/create/random`` command or raise
  ``extra/special/per/atom`` in the ``read_data`` section.
