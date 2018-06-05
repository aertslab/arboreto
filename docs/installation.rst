Installation Guide
==================

.. _anaconda: https://www.anaconda.com/download/#macos
.. _miniconda: https://conda.io/miniconda.html
.. _conda: https://conda.io/docs/user-guide/getting-started.html
.. _numpy: http://www.numpy.org/
.. _scipy: https://www.scipy.org/

.. caution:: **Python Environment**

    It is highly recommended to prepare a Python environment with the Anaconda_
    or Miniconda_ distribution and install Arboreto's dependencies using the
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

.. _pypi: https://pypi.python.org/pypi/arboreto/
.. _pip: https://pip.pypa.io/en/stable/
.. _git: https://git-scm.com/
.. _github: https://github.com/tmoerman/arboreto
.. _repository: https://github.com/tmoerman/arboreto

The arboreto package is available from PyPI_ (Python Package Index), a repository
of software for the Python programming language.

Using pip_, installing the arboreto package is straightforward:

.. code-block:: bash

    $ pip install arboreto

Check out the installation:

.. code-block:: bash

    $ pip show arboreto

    Name: arboreto
    Version: 0.1.4
    Summary: Scalable gene regulatory network inference using tree-based ensemble regressors
    Home-page: https://github.com/tmoerman/arboreto
    Author: Thomas Moerman
    Author-email: thomas.moerman@gmail.com
    License: BSD 3-Clause License
    Location: /vsc-hard-mounts/leuven-data/software/biomed/Anaconda/5-Python-3.6/lib/python3.6/site-packages
    Requires: scipy, scikit-learn, numpy, pandas, dask, distributed

.. note::
    You can use pip_ to install arboreto in an Anaconda_ environment.

.. .. caution::

    TODO

    Although pip is able to take care of installing arboreto's dependencies,
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

Installing Arboreto from source is possible using following steps:

1. clone the Github_ repository_ using the git_ tool:

.. code-block:: bash

    $ git clone https://github.com/tmoerman/arboreto.git
    $ cd arboreto

2. build Arboreto using the provided script:

.. code-block:: bash

    $ ./pypi_build.sh

3. install the freshly built Arboreto package using pip_:

.. code-block:: bash

    $ pip install dist/*
