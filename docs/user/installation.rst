Installation Guide
==================

.. _anaconda: https://www.anaconda.com/download/#macos
.. _miniconda: https://conda.io/miniconda.html
.. _conda: https://conda.io/docs/user-guide/getting-started.html
.. _numpy: http://www.numpy.org/
.. _scipy: https://www.scipy.org/

.. caution:: **Python Environment**

    It is highly recommended to prepare a Python environment with the Anaconda_
    or Miniconda_ distribution and install Arboretum's dependencies using the
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
.. _github: https://github.com/tmoerman/arboretum
.. _repository: https://github.com/tmoerman/arboretum

The arboretum package is available from PyPI_ (Python Package Index), a repository
of software for the Python programming language.

Using pip_, installing the arboretum package is straightforward:

.. code-block:: bash

    $ pip install arboretum

Check out the installation:

.. code-block:: bash

    $ pip show arboretum

    Name: arboretum
    Version: 0.1.3
    Summary: Scalable gene regulatory network inference using tree-based ensemble regressors
    Home-page: https://github.com/tmoerman/arboretum
    Author: Thomas Moerman
    Author-email: thomas.moerman@gmail.com
    License: BSD 3-Clause License
    Location: /vsc-hard-mounts/leuven-data/software/biomed/Anaconda/5-Python-3.6/lib/python3.6/site-packages
    Requires: scipy, scikit-learn, numpy, pandas, dask, distributed

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

.. Install using conda
 -------------------
    TODO

Install from source
-------------------

Installing Arboretum from source is possible using following steps:

1. clone the Github_ repository_ using the git_ tool:

.. code-block:: bash

    $ git clone https://github.com/tmoerman/arboretum.git
    $ cd arboretum

2. build Arboretum using the provided script:

.. code-block:: bash

    $ ./pypi_build.sh

3. install the freshly built Arboretum package using pip_:

.. code-block:: bash

    $ pip install dist/*
