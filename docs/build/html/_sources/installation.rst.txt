Installation
============
This short guide shows three practical ways to obtain **LAMMPS** with the
``bond/create/random`` fix that you need for the polymer‐network examples in
*generate_InitCond*:

* **Conda-Forge binary** – easiest, already includes *EXTRA-BOND*.
* **Spack package** – similarly painless, great for HPC clusters.
* **Build from source with CMake** – needed if you want the very latest
  features or special compiler options.

.. note::

   The ``bond/create/random`` style lives in the **EXTRA-BOND** package
   (commit 07 Sep 2022 and later).  Whatever route you choose, just make sure
   that *EXTRA-BOND* ends up **ON**.

----------------------------------------------------
1. Conda-Forge (Linux, macOS, Windows WSL)
----------------------------------------------------
::

   # create a fresh environment called “lammps”
   conda create -n lammps -c conda-forge lammps
   conda activate lammps

The ``lammps`` meta-package published on *conda-forge* is built with almost
every optional package **including** ``EXTRA-BOND``.  Confirm with::

   lmp -h | grep bond/create/random

If you see the line, you’re good to go.

----------------------------------------------------
2. Spack (particularly handy on clusters)
----------------------------------------------------
::

   spack install lammps +extra-bond +molecule  # add any other “+pkg” you need
   spack load lammps

Unlike Conda, *Spack* lets you toggle individual packages at install time.
The “+extra-bond” variant turns on **EXTRA-BOND** in the generated CMake
configuration.

----------------------------------------------------
3. Build from source with CMake
----------------------------------------------------
.. code-block:: bash

   git clone https://github.com/lammps/lammps.git
   mkdir -p lammps/build && cd lammps/build

   cmake ../cmake \
     -DPKG_MOLECULE=yes \        # needed for read_data on polymer topologies
     -DPKG_EXTRA-BOND=yes \      # <-- bond/create/random lives here
     -DCMAKE_INSTALL_PREFIX=$HOME/.local \
     -DLAMMPS_EXCEPTIONS=yes     # nicer run-time error messages

   make -j$(nproc)
   make install    # installs into $HOME/.local by default

Add *OpenMP* or *MPI* flags if you want parallel execution, e.g.
``-DBUILD_OMP=yes`` or ``-DBUILD_MPI=yes``.

----------------------------------------------------
Sanity check
----------------------------------------------------
Whichever route you picked, always verify the fix is present:

.. code-block:: bash

   $ lmp -h | grep bond/create/random
     bond/create/random       Create bonds (random partner selection)  [EXTRA-BOND]

If nothing appears, the binary you are calling was *not* compiled with
**EXTRA-BOND** – revisit the steps above.

----------------------------------------------------
(Optional) Python wrapper
----------------------------------------------------
If you plan to drive LAMMPS from Python notebooks:

.. code-block:: bash

   # Conda/Spack installs the wrapper automatically.
   # For a manual build:
   pip install --user lammps-cython

----------------------------------------------------
Troubleshooting
----------------------------------------------------

* **“Package extra-bond is not enabled”** – you are pointing to an old binary.
  Make sure ``$(which lmp)`` is the executable you just installed.

* **“New bond exceeded bonds per atom …”** – increase the *maxbond* argument in
  your ``bond/create/random`` fix or raise ``extra/special/per/atom`` when you
  call ``read_data``.  (See the *LAMMPS* docs for details.)

With LAMMPS properly installed you can now run the example pipeline and the
analysis notebooks without modification.
