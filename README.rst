.. image:: img/arboretum.png
    :alt: arboretum
    :scale: 100%
    :align: left

.. image:: https://travis-ci.org/tmoerman/arboretum.svg?branch=master
    :alt: Build Status
    :target: https://travis-ci.org/tmoerman/arboretum

.. image:: https://readthedocs.org/projects/arboretum/badge/?version=latest
    :alt: Documentation Status
    :target: http://arboretum.readthedocs.io/en/latest/?badge=latest

.. epigraph::

    The most satisfactory definition of man from the scientific point of view is probably Man the Tool-maker.
    
    -- Kenneth Oakley

.. _arboretum: https://arboretum.readthedocs.io
.. _`arboretum documentation`: https://arboretum.readthedocs.io
.. _notebooks: https://github.com/tmoerman/arboretum/tree/master/notebooks
.. _issue: https://github.com/tmoerman/arboretum/issues/new

.. _dask: https://dask.pydata.org/en/latest/
.. _`dask distributed`: https://distributed.readthedocs.io/en/latest/

.. _GENIE3: http://www.montefiore.ulg.ac.be/~huynh-thu/GENIE3.html
.. _`Random Forest`: https://en.wikipedia.org/wiki/Random_forest
.. _ExtraTrees: https://en.wikipedia.org/wiki/Random_forest#ExtraTrees
.. _`Stochastic Gradient Boosting Machine`: https://en.wikipedia.org/wiki/Gradient_boosting#Stochastic_gradient_boosting
.. _`early-stopping`: https://en.wikipedia.org/wiki/Early_stopping

Inferring a gene regulatory network (GRN) from gene expression data is a computationally expensive task, exacerbated by increasing data sizes due to advances
in high-throughput gene profiling technology.

The *arboretum_* software library addresses this issue by providing a computational strategy that allows executing the class of GRN inference algorithms
exemplified by GENIE3_ [1] on hardware ranging from a single computer to a multi-node compute cluster. This class of GRN inference algorithms is defined by
a series of steps, one for each target gene in the network, where the most important candidates from a set of regulators are determined from a regression
model to predict a target gene's expression profile.

Members of the above class of GRN inference algorithms are attractive from a computational point of view because they are parallelizable by nature. In arboretum,
we specify the parallelizable computation as a dask graph [2], a data structure that represents the task schedule of a computation. A dask scheduler assigns the
tasks in a dask graph to the available computational resources. Arboretum uses the `dask distributed`_ scheduler to
spread out the computational tasks over multiple processes running on one or multiple machines.

Arboretum currently supports 2 GRN inference algorithms:

* **GENIE3**: the classic GRN inference algorithm using `Random Forest`_ (RF) or ExtraTrees_ (ET) regression.
* **GRNBoost2**: a novel and fast GRN inference algorithm using `Stochastic Gradient Boosting Machine`_ (SGBM) [3] regression with `early-stopping`_ regularization.

References
**********

1. Huynh-Thu VA, Irrthum A, Wehenkel L, Geurts P (2010) Inferring Regulatory Networks from Expression Data Using Tree-Based Methods. PLoS ONE
2. Rocklin, M. (2015). Dask: parallel computation with blocked algorithms and task scheduling. In Proceedings of the 14th Python in Science Conference (pp. 130-136).
3. Friedman, J. H. (2002). Stochastic gradient boosting. Computational Statistics & Data Analysis, 38(4), 367-378.
4. Marbach, D., Costello, J. C., Kuffner, R., Vega, N. M., Prill, R. J., Camacho, D. M., ... & Dream5 Consortium. (2012). Wisdom of crowds for robust gene network inference. Nature methods, 9(8), 796-804.

Get Started
***********

Arboretum was conceived with the working bioinformatician or data scientist in mind. We provide extensive documentation and examples to help you get up to speed with the library.

* Read the `arboretum documentation`_.
* Browse example notebooks_.
* Report an issue_.

License
*******

BSD 3-Clause License
