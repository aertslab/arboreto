
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


Install into a new conda environment
************************************

.. _conda environment: https://conda.io/docs/user-guide/tasks/manage-environments.html#
..

You can easily install arboreto into a fresh `conda environment`_.
See [1]_ for a better understanding of the how and what of Python environments.

Following code snippet creates a new conda environment called "arboreto-env"
and installs arboreto and all its dependencies into that environment.

.. code-block:: bash

  # create the conda environment named "arboreto-env"
  $ conda create --name arboreto-env

  # activate the conda environment we just created
  $ source activate arboreto-env

  # note: your terminal will indicate which environment is active on the left
  (arboreto-env) $ ...

  # install arboreto into the "arboreto-env" environment (hit Y to proceed)
  (arboreto-env) $ conda install -c bioconda arboreto

.. You can now (for example) start an ipython session and use arboreto interactively.

..  .. code-block:: bash
..   (arboreto-env) $ ipython
..
..       Python 3.5.5 |Anaconda custom (64-bit)| (default, Mar 12 2018, 23:12:44)
..       Type 'copyright', 'credits' or 'license' for more information
..       IPython 6.2.1 -- An enhanced Interactive Python. Type '?' for help.
..
..       In [1]: from arboreto.algo import grnboost2
..
..       In [2]: ...
..
..       # when you're done in the ipython session
..       In [666] exit()


When you're done, deactivate the "arboreto-env" environment as follows:

.. code-block:: bash

  # deactivate the current environment
  (arboreto-env) $ source deactivate

  # as you will see: the environment indication has disappeared.
  $ ...


.. __: https://medium.freecodecamp.org/why-you-need-python-environments-and-how-to-manage-them-with-conda-85f155f4353c

.. [1] `Why you need Python environments and how to manage them with Conda -- Gergely Szerovay`__


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
