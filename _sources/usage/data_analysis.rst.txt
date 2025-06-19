Data-Analysis Helpers
=====================

.. note::

   These lightweight scripts live in ``docs/_static/scripts`` and are meant
   for **quick, single-file previews** of key observables.

   • **Exactly one input file** is supplied as the *first* positional argument.  
   • Run them from the project root, for example::

       python docs/_static/scripts/plot_PE.py  results/Thermo_run1.dat

   • Each script prints an informative ``--help`` message describing optional
     flags (e.g. custom column numbers, unit conversions).

------------

Potential-Energy Trace
----------------------

**Script** ``plot_PE.py``  
**Input**  ``Thermo_<run>.dat`` (LAMMPS thermo dump)  
**Action** Extracts the *potential energy* column and plots energy vs step
(line plot saved as ``PE.png``).

.. figure:: /_static/img/PE.png
   :width: 70%
   :align: center

   Example potential-energy trace.

------------

Bonded-Sticker Fraction (BSF)
-----------------------------

**Script** ``plot_BSF.py``  
**Input**  ``Thermo_<run>.dat`` (must include running bond count)  
**Action** Computes the instantaneous BSF (fraction of stickers in bonds) and
outputs a BSF-vs-time curve (``BSF.png``).

.. figure:: /_static/img/BSF.png
   :width: 70%
   :align: center

   Example BSF profile.

------------

Sticker Dissociation Events
---------------------------

**Script** ``plot_SD.py``  
**Input**  ``BondData_<run>.dat`` (3-column cumulative *formed* / *broken*
counters)  
**Action** Converts cumulative counts to *per-interval* break events and plots
a line-style time series (``SD.png``).

.. figure:: /_static/img/SD.png
   :width: 70%
   :align: center

   Dissociation events per Δt.

------------

Cluster-Size Distribution
-------------------------

**Script** ``plot_cSize.py``  
**Input**  one LAMMPS ``*.DATA`` snapshot  
**Action** Detects connected components (chains = nodes, sticker bonds =
edges), then plots the fraction of chains in each cluster size *s*
(histogram saved as ``cSize.png``).

.. figure:: /_static/img/cSize.png
   :width: 70%
   :align: center

   Cluster-size histogram.

------------

Radial Sticker / Spacer Density
-------------------------------

**Script** ``plot_radialDist.py``  
**Input**  one ``*.DATA`` snapshot (types 1/3 = stickers, 2/4 = spacers)  
**Action** Computes volume-normalised radial density profiles for stickers and
spacers.  Figure saved as
``RD.png``.

.. figure:: /_static/img/RD.png
   :width: 70%
   :align: center

   Sticker vs spacer radial densities.

------------

Volume-Normalised BSF *(coming soon)*
-------------------------------------

A convenience wrapper will shortly appear that rescales BSF by the simulation
box volume to allow direct comparison between runs of different sizes.

.. figure:: /_static/img/vbsf_placeholder.png
   :width: 70%
   :align: center

   Placeholder – volume-normalised BSF.
