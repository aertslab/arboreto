.. image:: https://github.com/tmoerman/arboreto/blob/master/img/arboreto.png?raw=true
    :alt: arboreto
    :align: left

.. image:: https://travis-ci.org/tmoerman/arboreto.svg?branch=master
    :alt: Build Status
    :target: https://travis-ci.org/tmoerman/arboreto

.. image:: https://readthedocs.org/projects/arboreto/badge/?version=latest
    :alt: Documentation Status
    :target: http://arboreto.readthedocs.io/en/latest/?badge=latest

.. image:: https://img.shields.io/badge/bioconda-0.1.5-blue.svg
    :alt: Bioconda package
    :target: https://anaconda.org/bioconda/arboreto

.. image:: https://img.shields.io/badge/pypi-0.1.5-blue.svg
    :alt: PyPI package
    :target: https://pypi.python.org/pypi?:action=display&name=arboreto&version=0.1.5

----

.. _arboreto: https://github.com/tmoerman/arboreto
.. _`arboreto documentation`: https://arboreto.readthedocs.io
.. _notebooks: https://github.com/tmoerman/arboreto/tree/master/notebooks
.. _issue: https://github.com/tmoerman/arboreto/issues/new
.. _github: https://github.com/tmoerman/arboreto
.. _pypi: https://pypi.python.org/pypi/arboreto/
.. _bioconda: https://anaconda.org/bioconda/arboreto

.. _dask: https://dask.pydata.org/en/latest/
.. _`dask distributed`: https://distributed.readthedocs.io/en/latest/

.. _GENIE3: http://www.montefiore.ulg.ac.be/~huynh-thu/GENIE3.html
.. _`Random Forest`: https://en.wikipedia.org/wiki/Random_forest
.. _ExtraTrees: https://en.wikipedia.org/wiki/Random_forest#ExtraTrees
.. _`Stochastic Gradient Boosting Machine`: https://en.wikipedia.org/wiki/Gradient_boosting#Stochastic_gradient_boosting
.. _`early-stopping`: https://en.wikipedia.org/wiki/Early_stopping

.. _pip: https://pip.pypa.io/en/stable/installing/
.. _installation: installation.html
.. _examples: examples.html
.. _`user guide`: userguide.html
.. _`GRN inference algorithms`: algorithms.html

Inferring a gene regulatory network (GRN) from gene expression data is a computationally expensive task, exacerbated by increasing data sizes due to advances
in high-throughput gene profiling technology.

.. sidebar:: **Quick Start**

    * `Installation`_
    * `User guide`_
    * Report an issue_
    * Source code at Github_
    * Releases at Bioconda_ and PyPI_

The *Arboreto* software library addresses this issue by providing a computational strategy that allows executing the class of GRN inference algorithms
exemplified by GENIE3_ [1]_ on hardware ranging from a single computer to a multi-node compute cluster. This class of GRN inference algorithms is defined by
a series of steps, one for each target gene in the dataset, where the most important candidates from a set of regulators are determined from a regression
model to predict a target gene's expression profile.

Members of the above class of GRN inference algorithms are attractive from a computational point of view because they are parallelizable by nature. In arboreto,
we specify the parallelizable computation as a Dask_ graph [2]_, a data structure that represents the task schedule of a computation. A Dask scheduler assigns the
tasks in a Dask graph to the available computational resources. Arboreto uses the `Dask distributed`_ scheduler to
spread out the computational tasks over multiple processes running on one or multiple machines.

Arboreto currently supports 2 `GRN inference algorithms`_:

1. **GRNBoost2**: fast GRN inference algorithm using `stochastic Gradient Boosting Machine`_ [3]_ regression with `early-stopping`_ regularization, the Arboreto flagship algorithm.

2. **GENIE3**: the popular classic GRN inference algorithm using `Random Forest`_ (RF) or ExtraTrees_ (ET) regression.

Usage Example
=============

.. code-block:: python

    # import python modules
    import pandas as pd
    from arboreto.utils import load_tf_names
    from arboreto.algo import grnboost2

    if __name__ == '__main__':
        # load the data
        ex_matrix = pd.read_csv(<ex_path>, sep='\t')
        tf_names = load_tf_names(<tf_path>)

        # infer the gene regulatory network
        network = grnboost2(expression_data=ex_matrix,
                            tf_names=tf_names)

        network.head()

====  ======  ==========
TF    target  importance
====  ======  ==========
G109  G1406   151.648784
G16   G1440   136.741815
G188  G938    124.707570
G10   G1312   124.195566
G48   G1419   121.488200
====  ======  ==========

Check out more examples_.

License
=======

.. _license: https://github.com/tmoerman/arboreto/blob/master/LICENSE.txt

BSD 3-Clause License_

pySCENIC
========

.. _pySCENIC: https://github.com/aertslab/pySCENIC
.. _SCENIC: https://aertslab.org/#scenic

Arboreto is a component in pySCENIC_: a lightning-fast python implementation of
the SCENIC_ pipeline [5]_ (Single-Cell rEgulatory Network Inference and Clustering)
which enables biologists to infer transcription factors, gene regulatory networks
and cell types from single-cell RNA-seq data.

References
==========

.. [1] Huynh-Thu VA, Irrthum A, Wehenkel L, Geurts P (2010) Inferring Regulatory Networks from Expression Data Using Tree-Based Methods. PLoS ONE
.. [2] Rocklin, M. (2015). Dask: parallel computation with blocked algorithms and task scheduling. In Proceedings of the 14th Python in Science Conference (pp. 130-136).
.. [3] Friedman, J. H. (2002). Stochastic gradient boosting. Computational Statistics & Data Analysis, 38(4), 367-378.
.. [4] Marbach, D., Costello, J. C., Kuffner, R., Vega, N. M., Prill, R. J., Camacho, D. M., ... & Dream5 Consortium. (2012). Wisdom of crowds for robust gene network inference. Nature methods, 9(8), 796-804.
.. [5] Aibar S, Bravo Gonzalez-Blas C, Moerman T, Wouters J, Huynh-Thu VA, Imrichova H, Kalender Atak Z, Hulselmans G, Dewaele M, Rambow F, Geurts P, Aerts J, Marine C, van den Oord J, Aerts S. SCENIC: Single-cell regulatory network inference and clustering. Nature Methods 14, 1083–1086 (2017). doi: 10.1038/nmeth.4463

.. toctree::
    :maxdepth: 2
    :hidden:

    installation
    userguide
    examples
    algorithms
    concept
    troubleshooting
    lcb
