.. _`Running with a custom Dask Client`: index.html#running-with-a-custom-dask-client
.. _localcluster: http://distributed.readthedocs.io/en/latest/local-cluster.html?highlight=localcluster#distributed.deploy.local.LocalCluster
.. _client: http://distributed.readthedocs.io/en/latest/client.html
.. _`web interface`: http://distributed.readthedocs.io/en/latest/web.html

FAQ
===

Q: How can I use the Dask diagnostics (bokeh) dashboard?
--------------------------------------------------------

Dask distributed features a nice `web interface`_ for monitoring your dask jobs
on a scheduler.

.. image:: ../../img/daskboard.gif
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



* `Running with a custom Dask Client`_
* Dask `web interface`_ documentation

Troubleshooting
===============
