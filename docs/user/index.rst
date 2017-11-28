User Guide
==========

.. _pandas: https://pandas.pydata.org/
.. _DataFrame: http://pandas.pydata.org/pandas-docs/stable/dsintro.html#dataframe
.. _DF: http://pandas.pydata.org/pandas-docs/stable/dsintro.html#dataframe
.. _numpy: http://www.numpy.org/
.. _ndarray: https://docs.scipy.org/doc/numpy-1.13.0/reference/generated/numpy.ndarray.html
.. _grnboost2: algorithms.html#grnboost2
.. _genie3: algorithms.html#genie3
.. _`distributed scheduler`: http://distributed.readthedocs.io/en/latest/setup.html
.. _client: http://distributed.readthedocs.io/en/latest/client.html
.. _localcluster: http://distributed.readthedocs.io/en/latest/local-cluster.html?highlight=localcluster#distributed.deploy.local.LocalCluster

Modules overview
----------------

Arboretum consists of multiple python modules:

``arboretum.algo``
~~~~~~~~~~~~~~~~~~

* Intended for **typical users**.
* Access point for launching GRNBoost2_ or GENIE3_ on local or distributed hardware.

``arboretum.core``
~~~~~~~~~~~~~~~~~~

* Intended for **advanced users**.
* Contains the low-level building blocks of the Arboretum framework.

``arboretum.utils``
~~~~~~~~~~~~~~~~~~~

* Contains small utility functions.

.. Dependencies Overview
 ---------------------

 Arboretum uses well-established libraries from the Python ecosystem.


Input / Output
--------------

Arboretum accepts as input:

* an expression matrix (rows = observations, columns = genes)
* (optionally) a list of gene names in the expression matrix
* (optionally) a list of transcription factors (a.k.a. TFs)

Arboretum returns as output:

* a Pandas_ DataFrame_ (DF) with columns ``['TF', 'target', 'importance']``

.. _`net1_expression_data.tsv`: https://github.com/tmoerman/arboretum/tree/master/resources/dream5/net1/net1_expression_data.tsv
.. _`net1_transcription_factors.tsv`: https://github.com/tmoerman/arboretum/tree/master/resources/dream5/net1/net1_transcription_factors.tsv
.. _resources: https://github.com/tmoerman/arboretum/tree/master/resources/

.. tip::

    As data for following code snippets, you can use the data for network 1 from
    the DREAM5 challenge (included in the resources_ folder of the Github repository):

    * ``<ex_path>`` = `net1_expression_data.tsv`_
    * ``<tf_path>`` = `net1_transcription_factors.tsv`_

Expression matrix as a Pandas ``DataFrame``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The input can be specified in a number of ways. Arguably the most straightforward
way is to specify the expression matrix as a Pandas_ DataFrame_, which also contains
the gene names as the column header.

.. parsed-literal::

    .-------------.
    | expression  |
    | matrix (DF_) | ---.      .-----------.
    '-------------'     \\     | GRNBoost2_ |     .------------.
                         :--> |    or     | --> | regulatory |
    .---------------.   /     | GENIE3_    |     | links (DF_) |
    | transcription | -'      '-----------'     '------------'
    | factors       |
    '---------------'

In the following code snippet, we launch network inference with grnboost2_ by
specifying the ``expression_data`` as a DataFrame_.

.. code-block:: python

    # Expression matrix as a Pandas DataFrame

    import pandas as pd

    from arboretum.utils import load_tf_names
    from arboretum.algo import grnboost2

    # ex_matrix is a DataFrame with gene names as column names
    ex_matrix = pd.read_csv(<ex_path>, sep='\t')

    # tf_names is read using a utility function included in Arboretum
    tf_names = load_tf_names(<tf_path>)

    network = grnboost2(expression_data=ex_matrix,
                        tf_names=tf_names)

Expression matrix as a Numpy ``ndarray``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Arboretum also supports specifying the expression matrix as a Numpy_ ndarray_ (matrix).
In this case, the gene names must be specified explicitly.

.. parsed-literal::

    .-------------.
    | expression  |
    | matrix (DF_) | -----.
    '-------------'      |    .-----------.
    .-------------.      |    | GRNBoost2_ |     .------------.
    | gene names  | -----+--> |    or     | --> | regulatory |
    '-------------'      |    | GENIE3_    |     | links (DF_) |
    .---------------.    |    '-----------'     '------------'
    | transcription | ---'
    | factors       |
    '---------------'

.. caution::

    You must specify the gene names in the same order as their corresponding
    columns of the numpy_ matrix. **Getting this right is the user's responsibility.**

.. code-block:: python

    # Expression matrix as a Numpy ndarray

    import numpy as np

    from arboretum.utils import load_tf_names
    from arboretum.algo import grnboost2

    # ex_matrix is a numpy ndarray, which has no notion of column names
    ex_matrix = np.genfromtxt(<ex_path>, delimiter='\t', skip_header=1)

    # we read the gene names from the first line of the file
    with open(<ex_path>) as file:
        gene_names = [gene.strip() for gene in file.readline().split('\t')]

    # sanity check to verify the ndarray's nr of columns equals the length of the gene_names list
    assert ex_matrix.shape[1] == len(gene_names)

    # tf_names is read using a utility function included in Arboretum
    tf_names = load_tf_names(<tf_path>)

    network = grnboost2(expression_data=ex_matrix,
                        gene_names=gene_names,  # we explicitly specify the gene_names
                        tf_names=tf_names)

Running with a custom LocalCluster
----------------------------------

When the user doesn't specify a dask distributed Client_ explicitly, Arboretum
will create a LocalCluster_ and a Client_ pointing to it.

Alternatively, you can create and configure your own LocalCluster_ and Client_
and pass these on to Arboretum. Example situations where this is useful:

* inferring multiple networks from different datasets
* inferring multiple networks, using different parameters, from the same dataset
* the user requires custom configuration for the

.. code-block:: python



Running with a distributed scheduler
------------------------------------

.. _`dask.distributed`: http://distributed.readthedocs.io
.. _`set up`: http://distributed.readthedocs.io/en/latest/setup.html
.. _`network setup documentation`: http://distributed.readthedocs.io/en/latest/setup.html

Arboretum uses `Dask.distributed`_ to parallelize its workloads.

In local mode, the user does not need to know the details of the underlying
computation framework. However, in distributed mode, some effort by the user or
a systems administrator is required to `set up`_ a dask.distributed ``scheduler``
and some ``workers``.

.. tip::

    Please refer to the Dask.distributed `network setup documentation`_.

Arboretum runs in local mode by default, spinning up different python processes
to execute the workload in parallel on the local machine. Thanks to the very
parallelizable nature of the network inference algorithms, we can take the parallelism
a step further by assigning pieces of the workload to different compute nodes.

In a distributed setting, Arboretum supports connecting to a dask distributed
scheduler instead of creating a local scheduler that is used only for the current
network inference.

Connecting to a distributed scheduler is possible by:

#. specifying the IP/port of a running scheduler:

    example

#. passing a Dask.distributed client instance:

    example
