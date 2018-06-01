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
.. _`dask.distributed`: http://distributed.readthedocs.io
.. _`set up`: http://distributed.readthedocs.io/en/latest/setup.html
.. _`network setup documentation`: http://distributed.readthedocs.io/en/latest/setup.html
.. _jupyter: http://jupyter.org/
.. _`scikit-learn`: http://scikit-learn.org/

.. contents::
    :depth: 1
    :local:

Modules overview
----------------

Arboreto consists of multiple python modules:

``arboreto.algo``
~~~~~~~~~~~~~~~~~~

* Intended for **typical users**.
* Access point for launching GRNBoost2_ or GENIE3_ on local or distributed hardware.

``arboreto.core``
~~~~~~~~~~~~~~~~~~

* Intended for **advanced users**.
* Contains the low-level building blocks of the Arboreto framework.

``arboreto.utils``
~~~~~~~~~~~~~~~~~~~

* Contains small utility functions.

Dependencies Overview
---------------------

Arboreto uses well-established libraries from the Python ecosystem. Arboreto
avoids being a proverbial "batteries-included" library, as such an approach often
entails unnecessary complexity and maintenance. Arboreto aims at doing only one
thing, and doing it well.

Concretely, the user will be exposed to one or more of following dependencies:

* Pandas_ or NumPy_: the user is expected to provide the input data in an expected format. Pandas_ and NumPy_ are well equipped with functions for data preprocessing.
* Dask.distributed_: to run Arboreto on a cluster, the user is responsible for setting up a network of a scheduler and workers.
* scikit-learn_: relevant for advanced users only. Arboreto can run "DIY" inference where the user provides their own parameters for the Random Forest or Gradient Boosting regressors.


Input / Output
--------------

**INPUT**

* an expression matrix (rows = observations, columns = genes)
    * either a Pandas_ DataFrame_ or a NumPy_ ndarray_
* a list of gene names corresponding to the columns of the expression matrix
    * optional
* a list of transcription factors (a.k.a. TFs)
    * optional

**OUTPUT**

* regulatory links
    * a Pandas_ DataFrame_ ``['TF', 'target', 'importance']``

.. _`net1_expression_data.tsv`: https://github.com/tmoerman/arboreto/tree/master/resources/dream5/net1/net1_expression_data.tsv
.. _`net1_transcription_factors.tsv`: https://github.com/tmoerman/arboreto/tree/master/resources/dream5/net1/net1_transcription_factors.tsv
.. _resources: https://github.com/tmoerman/arboreto/tree/master/resources/

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

.. figure:: https://github.com/tmoerman/arboreto/blob/master/img/user_guide_figure1.png?raw=true
    :alt: User Guide Figure 1

In the following code snippet, we launch network inference with grnboost2_ by
specifying the ``expression_data`` as a DataFrame_.

.. code-block:: python
    :caption: *Expression matrix as a Pandas DataFrame*
    :emphasize-lines: 5

    import pandas as pd
    from arboreto.utils import load_tf_names
    from arboreto.algo import grnboost2

    if __name__ == '__main__':
        # ex_matrix is a DataFrame with gene names as column names
        ex_matrix = pd.read_csv(<ex_path>, sep='\t')

        # tf_names is read using a utility function included in Arboreto
        tf_names = load_tf_names(<tf_path>)

        network = grnboost2(expression_data=ex_matrix,
                            tf_names=tf_names)

        network.to_csv('output.tsv', sep='\t', index=False, header=False)

.. note::

    Notice the emphasized line:

    .. code-block:: python
        :emphasize-lines: 1

        if __name__ == '__main__':
            # ... code ...

    This is a Python idiom necessary in situations where the code spawns new
    Python processes, which Dask does under the hood of the ``grnboost2`` and
    ``genie3`` functions to parallelize the workload.

Expression matrix as a NumPy ``ndarray``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Arboreto also supports specifying the expression matrix as a Numpy_ ndarray_
(in our case: a 2-dimensional matrix). In this case, the gene names must be
specified explicitly.

.. figure:: https://github.com/tmoerman/arboreto/blob/master/img/user_guide_figure2.png?raw=true
    :alt: User Guide Figure 2

.. caution::

    You must specify the gene names in the same order as their corresponding
    columns of the NumPy_ matrix. **Getting this right is the user's responsibility.**

.. code-block:: python
    :emphasize-lines: 20
    :caption: *Expression matrix as a NumPy ndarray*

    import numpy as np
    from arboreto.utils import load_tf_names
    from arboreto.algo import grnboost2

    if __name__ == '__main__':
        # ex_matrix is a numpy ndarray, which has no notion of column names
        ex_matrix = np.genfromtxt(<ex_path>, delimiter='\t', skip_header=1)

        # we read the gene names from the first line of the file
        with open(<ex_path>) as file:
            gene_names = [gene.strip() for gene in file.readline().split('\t')]

        # sanity check to verify the ndarray's nr of columns equals the length of the gene_names list
        assert ex_matrix.shape[1] == len(gene_names)

        # tf_names is read using a utility function included in Arboreto
        tf_names = load_tf_names(<tf_path>)

        network = grnboost2(expression_data=ex_matrix,
                            gene_names=gene_names,  # specify the gene_names
                            tf_names=tf_names)

        network.to_csv('output.tsv', sep='\t', index=False, header=False)

Running with a custom Dask Client
---------------------------------

Arboreto uses `Dask.distributed`_ to parallelize its workloads. When the user
doesn't specify a dask distributed Client_ explicitly, Arboreto will create a
LocalCluster_ and a Client_ pointing to it.

Alternatively, you can create and configure your own Client_ instance and pass
it on to Arboreto. Situations where this is useful include:

* inferring multiple networks from different datasets
* inferring multiple networks using different parameters from the same dataset
* the user requires custom configuration for the LocalCluster (memory limit, nr of processes, etc.)

Following snippet illustrates running the gene regulatory network inference
multiple times, with different initialization seed values. We create one Client_
and pass it to the different inference steps.

.. code-block:: python
    :emphasize-lines: 8, 9, 10, 11, 20, 25
    :caption: *Running with a custom Dask Client*

    import pandas as pd
    from arboreto.utils import load_tf_names
    from arboreto.algo import grnboost2
    from distributed import LocalCluster, Client

    if __name__ == '__main__':
        # create custom LocalCluster and Client instances
        local_cluster = LocalCluster(n_workers=10,
                                     threads_per_worker=1,
                                     memory_limit=8e9)
        custom_client = Client(local_cluster)

        # load the data
        ex_matrix = pd.read_csv(<ex_path>, sep='\t')
        tf_names = load_tf_names(<tf_path>)

        # run GRN inference multiple times
        network_666 = grnboost2(expression_data=ex_matrix,
                                tf_names=tf_names,
                                client_or_address=custom_client,  # specify the custom client
                                seed=666)

        network_777 = grnboost2(expression_data=ex_matrix,
                                tf_names=tf_names,
                                client_or_address=custom_client,  # specify the custom client
                                seed=777)

        # close the Client and LocalCluster after use
        client.close()
        local_cluster.close()

        network_666.to_csv('output_666.tsv', sep='\t', index=False, header=False)
        network_777.to_csv('output_777.tsv', sep='\t', index=False, header=False)

Running with a Dask distributed scheduler
-----------------------------------------

Arboreto was designed to run gene regulatory network inference in a distributed
setting. In distributed mode, some effort by the user or a systems administrator
is required to `set up`_ a dask.distributed ``scheduler`` and some ``workers``.

.. tip::

    Please refer to the Dask distributed `network setup documentation`_ for
    instructions on how to set up a Dask distributed cluster.

Following diagram illustrates a possible topology of a Dask distributed cluster.

.. figure:: https://github.com/tmoerman/arboreto/blob/master/img/user_guide_figure3.png?raw=true
    :alt: User Guide Figure 3

* ``node_1`` runs a Python script, console or a Jupyter_ notebook server, a Client_ instance is configured with the TCP address of the distributed scheduler, running on ``node_2``
* ``node_2`` runs a distributed scheduler and 10 workers pointing to the scheduler
* ``node_3`` runs 10 distributed workers pointing to the scheduler
* ``node_4`` runs 10 distributed workers pointing to the scheduler

With a small modification to the code, we can infer a regulatory network using all
workers connected to the `distributed scheduler`_. We specify a Client_ that is
connected to the Dask `distributed scheduler`_ and pass it as an argument to the
inference function.

.. code-block:: python
    :emphasize-lines: 10, 11, 15
    :caption: *Running with a Dask distributed scheduler*

    import pandas as pd
    from arboreto.utils import load_tf_names
    from arboreto.algo import grnboost2
    from distributed import Client

    if __name__ == '__main__':
        ex_matrix = pd.read_csv(<ex_path>, sep='\t')
        tf_names = load_tf_names(<tf_path>)

        scheduler_address = 'tcp://10.118.224.134:8786'  # example address of the remote scheduler
        cluster_client = Client(scheduler_address)       # create a custom Client

        network = grnboost2(expression_data=ex_matrix,
                            tf_names=tf_names,
                            client_or_address=cluster_client)  # specify Client connected to the remote scheduler

        network.to_csv('output.tsv', sep='\t', index=False, header=False)


.. In local mode, the user does not need to know the details of the underlying
 computation framework. However, in distributed mode, some effort by the user or
 a systems administrator is required to `set up`_ a dask.distributed ``scheduler``
 and some ``workers``.


 Connecting to a distributed scheduler is possible by:

 #. specifying the IP/port of a running scheduler:

     example

 #. passing a Dask.distributed client instance:

    example
