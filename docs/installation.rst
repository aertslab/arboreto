
.. image:: https://img.shields.io/badge/bioconda-0.1.5-blue.svg
    :alt: Bioconda package
    :target: https://anaconda.org/bioconda/arboreto

.. image:: https://img.shields.io/badge/pypi-0.1.5-blue.svg
    :alt: PyPI package
    :target: https://pypi.python.org/pypi?:action=display&name=arboreto&version=0.1.5

-----

Installation Guide
==================

.. _anaconda: https://www.anaconda.com/download/#macos
.. _miniconda: https://conda.io/miniconda.html
.. _conda: https://conda.io/docs/user-guide/getting-started.html
.. _numpy: http://www.numpy.org/
.. _scipy: https://www.scipy.org/

.. _pypi: https://pypi.python.org/pypi/arboreto/
.. _pip: https://pip.pypa.io/en/stable/
.. _git: https://git-scm.com/
.. _github: https://github.com/tmoerman/arboreto
.. _repository: https://github.com/tmoerman/arboreto

There are different options to install Arboreto.

.. hint::

  It is **highly recommended** to prepare a Python environment with the Anaconda_
  or Miniconda_ distribution and install Arboreto using the
  conda_ package manager.

  This avoids complexities in ensuring that libraries like NumPy_ and SciPy_
  link against an optimized implementation of linear algebra routines.

Install using conda (recommended)
---------------------------------

.. _bioconda: https://bioconda.github.io/
.. _available: https://anaconda.org/bioconda/arboreto

The arboreto is available_ from bioconda_, a distribution of bioinformatics
software realized as a channel for the versatile conda_ package manager.

.. code-block:: bash

  $ conda install -c bioconda arboreto


Install using pip
-----------------

The arboreto package is available from PyPI_ (Python Package Index), a repository
of software for the Python programming language. Using pip_, installing the arboreto package is straightforward:

.. code-block:: bash

    $ pip install arboreto

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

Check out the installation
--------------------------

.. code-block:: bash

    $ pip show arboreto

    Name: arboreto
    Version: 0.1.5
    Summary: Scalable gene regulatory network inference using tree-based ensemble regressors
    Home-page: https://github.com/tmoerman/arboreto
    Author: Thomas Moerman
    Author-email: thomas.moerman@gmail.com
    License: BSD 3-Clause License
    Location: /vsc-hard-mounts/leuven-data/software/biomed/Anaconda/5-Python-3.6/lib/python3.6/site-packages
    Requires: scipy, scikit-learn, numpy, pandas, dask, distributed
