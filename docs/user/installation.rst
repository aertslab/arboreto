Installation Guide
==================

.. _anaconda: https://www.anaconda.com/download/#macos
.. _miniconda: https://conda.io/miniconda.html
.. _conda: https://conda.io/docs/user-guide/getting-started.html
.. _numpy: http://www.numpy.org/
.. _scipy: https://www.scipy.org/

.. caution:: **Python Environment**

    It is highly recommended to prepare a Python environment with the Anaconda_
    or Miniconda_ distribution and install arboretum's dependencies using the
    conda_ package manager.

    - NumPy
    - SciPy
    - scikit-learn
    - pandas
    - dask
    - distributed

    This avoids complexities in ensuring that libraries like NumPy_ and SciPy_
    link against an optimized implementation of linear algebra routines.

Install using pip
-----------------

.. _pypi: https://pypi.python.org/pypi/arboretum/
.. _pip: https://pip.pypa.io/en/stable/
.. _git: https://git-scm.com/

The arboretum package is available from PyPI_ (Python Package Index), a repository
of software for the Python programming language.

Using pip_, installing the arboretum package is straightforward:

.. code-block:: bash

    $ pip install arboretum

.. note::
    You can use pip_ to install arboretum in an Anaconda_ environment.

.. .. caution::

    TODO

    Although pip is able to take care of installing arboretum's dependencies,
    we recommend preparing an Anaconda_ environment (or using it as your main
    Python installation) with following dependencies already installed using
    conda_:

    .. code-block:: bash

        * numpy
        * scipy
        * scikit-learn
        * pandas
        * dask
        * distributed

Install using conda
-------------------

    TODO

Install from source
-------------------

    TODO
