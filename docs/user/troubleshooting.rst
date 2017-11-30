.. _`Running with a custom Dask Client`: index.html#running-with-a-custom-dask-client
.. _localcluster: http://distributed.readthedocs.io/en/latest/local-cluster.html?highlight=localcluster#distributed.deploy.local.LocalCluster
.. _client: http://distributed.readthedocs.io/en/latest/client.html
.. _`web interface`: http://distributed.readthedocs.io/en/latest/web.html
.. _`GradientBoostingRegressor API`: http://scikit-learn.org/stable/modules/generated/sklearn.ensemble.GradientBoostingRegressor.html#sklearn.ensemble.GradientBoostingRegressor.fit
.. _`scikit-learn`: http://scikit-learn.org
.. _pandas: https://pandas.pydata.org/
.. _numpy: http://www.numpy.org/

.. contents:: Page contents

----

FAQ
===

Q: How can I use the Dask diagnostics (bokeh) dashboard?
--------------------------------------------------------

Dask distributed features a nice `web interface`_ for monitoring the execution
of a Dask computation graph.

.. image:: https://github.com/tmoerman/arboretum/blob/master/img/daskboard.gif?raw=true
    :alt: Dask diagnostics dashboard

By default, when no custom Client is specified, Arboretum creates a LocalCluster_
instance with the diagnostics dashboard **disabled**:

.. code-block:: python

    ...
    local_cluster = LocalCluster(diagnostics_port=None)
    client = Client(local_cluster)
    ...

You can easily create a custom LocalCluster_, with the dashboard enabled, and
pass a custom Client_ connected to that cluster to the GRN inference algorithm:

.. code-block:: python
    :emphasize-lines: 1, 8

    local_cluster = LocalCluster()  # diagnostics dashboard is enabled
    custom_client = Client(local_cluster)

    ...

    network = grnboost2(expression_data=ex_matrix,
                        tf_names=tf_names,
                        client=custom_client)  # specify the custom client

By default, the dashboard is available on port ``8787``.

For more information, consult:

* Dask `web interface`_ documentation
* `Running with a custom Dask Client`_

Q: My gene expression matrix is transposed, what now?
-----------------------------------------------------

The Python `scikit-learn`_ library expects data in a format where rows represent
observations and columns represent features (in our case: genes), for example, see the
`GradientBoostingRegressor API`_.

However, in some fields (like single-cell genomics), the default is inversed: the rows represent
genes and the columns represent the observations.

In order to maintain an API that is as lean is possible, Arboretum adopts
the scikit-learn convention (rows=observations, columns=features). This means that
the user is responsible for providing the data in the right shape.

Fortunately, the Pandas_ and Numpy_ libraries feature all the necessary functions
to preprocess your data.

Example: reading a transposed text file with Pandas
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    df = pd.read_csv(<ex_path>, index_col=0, header=None, sep='\t').T


Troubleshooting
===============
