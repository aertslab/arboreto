User Guide
==========

Package Overview
----------------

Arboretum consists of following python modules:

``arboretum.algo``
~~~~~~~~~~~~~~~~~~

* Intended for most users.
* Access point for launching GRNBoost2 or GENIE3 on local or distributed hardware.

``arboretum.core``
~~~~~~~~~~~~~~~~~~

* Intended for advanced users.
* Contains the low-level building blocks of the arboretum framework.

.. Dependencies Overview
 ---------------------
 Arboretum uses well-established libraries from the Python ecosystem.


Input / Output
--------------

.. _pandas: https://pandas.pydata.org/
.. _DataFrame: http://pandas.pydata.org/pandas-docs/stable/dsintro.html#dataframe

Arboretum accepts as input:

* an expression matrix
* (optionally) a list of gene names in the expression matrix
* (optionally) a list of candidate regulators (transcription factors).

Arboretum returns as output:

* a Pandas_ DataFrame with columns ``['TF', 'target', 'importance'``.






Single-node
-----------

Clustered
---------
