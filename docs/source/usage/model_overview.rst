Model Overview
==============

This page documents the coarse-grained **heterotypic sticker–spacer** model
used to study **condensate coalescence**. The emphasis is on extracting
generic principles rather than reproducing a specific biomolecular system.

.. rubric:: Scope & Rationale

* We model **purely heterotypic** interactions between *complementary*
  sticker types (e.g., inspired by SH3–PRM or SUMO–SIM systems),
  where cross-links generate an intra-condensate network.
* A **two-component** (A/B) formulation serves as a **minimal model** for
  multicomponent biological condensates.
* Insights are expected to transfer to **homotypic** (single-component)
  condensates provided the biopolymer follows a **sticker–spacer architecture**.

.. rubric:: Design choices (at a glance)

.. list-table::
   :header-rows: 1
   :widths: 28 72

   * - **Aspect**
     - **Choice / Consequence**
   * - Sticker valency
     - :math:`1` (saturating); a sticker can participate in only one
       specific bond at a time.
   * - Specific vs nonspecific
     - Specific = reversible bonds between complementary stickers;
       nonspecific = Lennard–Jones contacts between any beads.
   * - Update cadence
     - Bond creation/breaking rules evaluated every **20 timesteps** to
       allow local relaxation after formation.
   * - Energies
     - Inputs in kcal/mol; reported in *kT* with
       :math:`1~kT \approx 0.6~\mathrm{kcal\,mol^{-1}}`.

Polymer Force-Fields
--------------------

Connectivity and flexibility within each chain are enforced with harmonic
bonds and cosine bending terms.

.. rubric:: Bonds

.. math::

   E_{\text{bond}} = K_b \,(R - R_0)^2

with parameters:

.. list-table::
   :header-rows: 1
   :widths: 20 40 40

   * - **Symbol**
     - **Meaning**
     - **Value**
   * - :math:`R`
     - Distance between bonded beads
     - —
   * - :math:`R_0`
     - Equilibrium bond length
     - :math:`10~Å`
   * - :math:`K_b`
     - Bond spring constant
     - :math:`3~\mathrm{kcal\,mol^{-1}\,Å^{-2}}`

.. rubric:: Angles

.. math::

   E_{\text{bend}} = \kappa \,\bigl(1-\cos\theta\bigr)

where :math:`\theta` is the angle between three successive beads and
:math:`\kappa = 2~\mathrm{kcal\,mol^{-1}}` controls bending stiffness.

Specific (Sticker–Sticker) Interactions
---------------------------------------

Complementary stickers interact via **reversible, saturating bonds**
(i.e., **valency = 1**). Bond formation/breaking depends **only** on
inter-sticker distance under the settings below.

.. image:: /_static/img/specific_interaction.png
   :alt: Specific inter-sticker interaction energy vs distance
   :align: center
   :width: 70%
   
.. rubric:: Switching rule

* If two complementary stickers are within :math:`R_\mathrm{cut}`, they
  **form** a bond (probability :math:`p_\mathrm{on}=1`).
* If a bonded pair reaches :math:`R \ge R_\mathrm{cut}`, the bond
  **breaks** (probability :math:`p_\mathrm{off}=1`).
* While bonded, the nonspecific LJ between the pair is **disabled**
  and replaced by the specific potential.

.. rubric:: Specific potential (shifted harmonic)

.. math::

   E_{\text{spec}}(R)
   =
   \frac{E_s}{(R_0 - R_\mathrm{cut})^2}
   \left[(R - R_0)^2 - \bigl(R_\mathrm{cut} - R_0\bigr)^2\right],
   \quad
   \begin{cases}
     E_{\text{spec}}(R_0) = -E_s,\\[2pt]
     E_{\text{spec}}(R_\mathrm{cut}) = 0,\\[2pt]
     E_{\text{spec}}(R>R_\mathrm{cut}) = 0~.
   \end{cases}

Parameters:

.. list-table::
   :header-rows: 1
   :widths: 22 48 30

   * - **Parameter**
     - **Meaning**
     - **Value**
   * - :math:`E_s`
     - Well depth (“specific energy”); sets bond lifetime scale
     - user-set; reported in *kT*
   * - :math:`R_0`
     - Resting bond distance
     - :math:`1.122\,\sigma`
   * - :math:`\sigma`
     - Bead diameter (model length unit)
     - :math:`10~Å`
   * - :math:`R_\mathrm{cut}`
     - Specific bond cutoff
     - :math:`R_0 + 1.5~Å`
   * - :math:`p_\mathrm{on},\,p_\mathrm{off}`
     - Attempt probabilities
     - :math:`1,\,1`

.. rubric:: Kinetics & detailed balance

* With :math:`p_\mathrm{on} = p_\mathrm{off} = 1`, stochasticity stems
  solely from **diffusion** and the **energy landscape**; bond state is
  determined by :math:`R` relative to :math:`R_\mathrm{cut}`.
* The **bond lifetime** scales as
  :math:`\tau_{\text{bond}} \propto e^{E_s/kT}`; dissociation rates show
  Arrhenius behavior,
  :math:`\text{Rate}\propto e^{-E_s/kT}` (consistent with thermal
  equilibration inside the well).
* Bond creation/breaking rules are evaluated once every **20 timesteps**
  to allow newly formed pairs to relax near :math:`R_0`.

Nonspecific (All-Bead) Interactions
-----------------------------------

All bead pairs (stickers and spacers) experience an **isotropic
Lennard–Jones (LJ)** interaction that enforces excluded volume and a
moderate attraction.

.. image:: /_static/img/nonspecific_interaction.png
   :alt: Nonspecific LJ interaction energy vs distance
   :align: center
   :width: 70%

.. math::

   E_{\text{LJ}}(r) = 4\,E_{ns}
   \left[\left(\frac{\sigma}{r}\right)^{12}
        - \left(\frac{\sigma}{r}\right)^6\right]

with a truncation at :math:`R_\mathrm{max}` for efficiency.

.. list-table::
   :header-rows: 1
   :widths: 22 48 30

   * - **Parameter**
     - **Meaning**
     - **Value**
   * - :math:`E_{ns}`
     - LJ well depth (“nonspecific energy”); sets **contact dwell time**
     - user-set; reported in *kT*
   * - :math:`\sigma`
     - Bead diameter
     - :math:`10~Å`
   * - :math:`R_\mathrm{max}`
     - LJ cutoff
     - :math:`2.5\,\sigma`

.. rubric:: Bonds vs. contacts — terminology

* **Bonds** = **specific** sticker–sticker links (single valency,
  governed by :math:`E_s`).
* **Contacts** = **nonspecific** LJ interactions among any beads
  (governed by :math:`E_{ns}`).
* When two complementary stickers are **bonded**, their LJ contact is
  **suppressed** in favor of :math:`E_{\text{spec}}`. Upon bond
  breakage, LJ becomes operative again.

Energy Units & Reporting
------------------------

Simulation inputs use **kcal/mol** for :math:`E_s` and :math:`E_{ns}`.
For analysis and figures, energies are reported in **thermal units**:

.. math::

   1~kT \approx 0.6~\mathrm{kcal\,mol^{-1}}

so that :math:`E/kT` is dimensionless and temperature-explicit.

Quick Reference Tables
----------------------

.. rubric:: Core parameters

.. list-table::
   :header-rows: 1
   :widths: 22 40 38

   * - **Symbol**
     - **Meaning**
     - **Default / Example**
   * - :math:`\sigma`
     - Bead diameter
     - :math:`10~Å`
   * - :math:`R_0` (bonded)
     - Specific bond rest distance
     - :math:`1.122\,\sigma`
   * - :math:`R_\mathrm{cut}` (bonded)
     - Specific bond cutoff
     - :math:`R_0 + 1.5~Å`
   * - :math:`R_\mathrm{max}` (LJ)
     - LJ cutoff
     - :math:`2.5\,\sigma`
   * - :math:`K_b`
     - Bond spring constant
     - :math:`3~\mathrm{kcal\,mol^{-1}\,Å^{-2}}`
   * - :math:`\kappa`
     - Bending stiffness
     - :math:`2~\mathrm{kcal\,mol^{-1}}`
   * - :math:`p_\mathrm{on},\,p_\mathrm{off}`
     - Specific attempt probabilities
     - :math:`1,\,1`
   * - Update cadence
     - Bond (create/break) evaluation interval
     - every **20** timesteps

.. rubric:: Modeling notes

* **Association** is diffusion-limited; **dissociation** requires
  crossing the specific energy barrier set by :math:`E_s`.
* Observed dissociation decays **exponentially** with increasing
  :math:`E_s` (Arrhenius-like), indicating thermalization within the
  specific well and consistency with detailed balance.
