
.. Root of all chi docs

.. _GitHub: https://github.com/DavAug/chi
.. _Myokit: https://myokit.com

.. module:: chi

.. toctree::
    :hidden:
    :maxdepth: 2

    getting_started/index.rst
    api/index.rst

Welcome to Chi's documentation!
=====================================

**Chi** is an open source Python package hosted on GitHub_,
which is designed for pharmacokinetic and pharmacodynamic (PKPD) modelling.

The main features of Chi are

- Simulation of treatment responses to custom dosing regimens, using pharmacokinetic & pharmacodynamic (PKPD) models, physiology-based pharmacokinetic (PBPK) models, and/or quantitative systems pharmacology (QSP) models.
- Inference of model parameters from measurements, clinical factors, and/or genetic factors (classical or Bayesian).
- Simulation of treatment response variability across individuals (hierarchical models/non-linear mixed effects models).
- Inference of population parameters from measurements, clinical factors, and/or genetic factors (classical or Bayesian).
- Simulation of structured populations, where inter-individual variability can be partially explained by covariates, such as clinical or genetic factors.
- Inference of model parameters in a structured population from measurements, clinical factors, and/or genetic factors (classical or Bayesian).
- Dosing regimen optimisation and model-informed precision dosing (MIPD).

This page provides tutorials to illustrate some of Chi's functionality, and a detailed API documentation as a complete reference to all of Chi's functions and classes.

.. note::
    Chi is being continuously developed and improved.
    So if you find any bugs or have any suggestions for improvement, please
    don't hesitate to reach out to us and share your feedback.

Install instructions
--------------------

Chi can be installed in two steps (one step if you are using Windows):
1. installation of a c-library called sundials; and 2. installation of Chi.

Step 1: Installation of sundials
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Chi uses the open source Python package Myokit_ to solve ordinary differential equations
and compute their sensitivities efficiently. Myokit_ does this using a c-library called sundials.
You can install Sundials on your computer by entering the below commands in your terminal:

- On Ubuntu, you can execute the below command to install Sundials using ``apt-get``:

.. code-block:: bash

    apt-get install libsundials-dev


- On MacOs, you can execute the below command to install Sundials using ``brew``:

.. code-block:: bash

    brew install sundials

- On Windows, Sundials does not need to be installed manually. Chi will install Sundials automatically.

Step 2: Installation of Chi
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Chi is distributed with PiPy which means that you can pip install Chi with

.. code-block:: bash

    pip install chi-drm

If you haven't installed Sundials at this point, you will likely get some messages from ``myokit`` complaining
that it cannot find Sundials on your machine. In that case, please go back to step 1.

Note that you need to install ``chi-drm``, and not ``chi``, to install this package.
This has the simple reason that the name ``chi`` was already taken in PiPy when we wanted to
distribute our package.

Now you are all done and have access to all of Chi's functionality. You can import chi in your python scripts with

.. code-block:: python

    import chi

We hope you enjoy using Chi. We are looking forward to seeing which insights you will generate for the pharmaceutical community.

To get some idea what you can and what you cannot do with Chi, we recommend that you have a look at the tutorials on the following pages.
The API documentation can be found `here <https://chi.readthedocs.io/en/latest/api/index.html>`_.

.. note::
    Note that the package is distributed in PiPy under the name ``chi-drm``
    while in your python scripts you can import the package under the name
    ``chi``.

Citing & giving credit
----------------------

Chi is open source and free to use, and we hope that you will find it useful! To help us to continue developing & maintaining the software,
please cite our software in your work

Citation string
^^^^^^^^^^^^^^^
.. code-block:: text

    Augustin, D., (2024). Chi: A Python package for treatment response modelling. Journal of Open Source Software, 9(94), 5925, https://doi.org/10.21105/joss.05925

BibTeX
^^^^^^
.. code-block:: text

    @article{
        Augustin2024,
        doi = {10.21105/joss.05925},
        url = {https://doi.org/10.21105/joss.05925},
        year = {2024},
        publisher = {The Open Journal},
        volume = {9},
        number = {94},
        pages = {5925},
        author = {David Augustin},
        title = {Chi: A Python package for treatment response modelling},
        journal = {Journal of Open Source Software}
    }
