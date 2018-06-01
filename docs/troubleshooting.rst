.. _`Running with a custom Dask Client`: index.html#running-with-a-custom-dask-client
.. _localcluster: http://distributed.readthedocs.io/en/latest/local-cluster.html?highlight=localcluster#distributed.deploy.local.LocalCluster
.. _client: http://distributed.readthedocs.io/en/latest/client.html
.. _`web interface`: http://distributed.readthedocs.io/en/latest/web.html
.. _`GradientBoostingRegressor API`: http://scikit-learn.org/stable/modules/generated/sklearn.ensemble.GradientBoostingRegressor.html#sklearn.ensemble.GradientBoostingRegressor.fit
.. _`scikit-learn`: http://scikit-learn.org
.. _pandas: https://pandas.pydata.org/
.. _numpy: http://www.numpy.org/

----

FAQ
===

.. contents::
    :local:

Q: How can I use the Dask diagnostics (bokeh) dashboard?
--------------------------------------------------------

Dask distributed features a nice `web interface`_ for monitoring the execution
of a Dask computation graph.

.. image:: https://github.com/tmoerman/arboreto/blob/master/img/daskboard.gif?raw=true
    :alt: Dask diagnostics dashboard

By default, when no custom Client is specified, Arboreto creates a LocalCluster_
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

In order to maintain an API that is as lean is possible, Arboreto adopts
the scikit-learn convention (rows=observations, columns=features). This means that
the user is responsible for providing the data in the right shape.

Fortunately, the Pandas_ and Numpy_ libraries feature all the necessary functions
to preprocess your data.

Example: reading a transposed text file with Pandas
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    df = pd.read_csv(<ex_path>, index_col=0, sep='\t').T

.. caution::

    Don't carelessly copy/paste above snippet. Take into account absence or presence
    of 1 or multiple header lines in the file.

    **Always check whether the your DataFrame has the expected dimensions**!

    .. code-block:: python

        In[10]: df.shape

        Out[10]: (17650, 14086)  # example



Q: Different runs produce different network outputs, why?
---------------------------------------------------------

.. _GRNBoost2: algorithms.html#grnboost2
.. _GENIE3: algorithms.html#id1
.. _seed: https://docs.scipy.org/doc/numpy/reference/generated/numpy.random.RandomState.html

Both GENIE3_ and GRNBoost2_ are based on stochastic machine learning techniques,
which use a random number generator internally to perform random sub-sampling of
observations and features when building decision trees.

To stabilize the output, Arboreto accepts a seed_ value that is used to initialize
the random number generator used by the machine learning algorithms.

.. code-block:: python
    :emphasize-lines: 3

    network_df = grnboost2(expression_data=ex_matrix,
                           tf_names=tf_names,
                           seed=777)

----

Troubleshooting
===============

.. contents::
    :local:

Bokeh error when launching Dask scheduler
-----------------------------------------

.. _`Github issue`: https://github.com/dask/distributed/issues/1515

.. code-block:: bash

    vsc12345@r6i0n5 ~ 12:00 $ dask-scheduler

    distributed.scheduler - INFO - -----------------------------------------------
    distributed.scheduler - INFO - Could not launch service: ('bokeh', 8787)
    Traceback (most recent call last):
    File "/data/leuven/software/biomed/Anaconda/5-Python-3.6/lib/python3.6/site-packages/distributed/scheduler.py", line 430, in start_services
        service.listen((listen_ip, port))
        File "/data/leuven/software/biomed/Anaconda/5-Python-3.6/lib/python3.6/site-packages/distributed/bokeh/core.py", line 31, in listen
            **kwargs)
    File "/data/leuven/software/biomed/Anaconda/5-Python-3.6/lib/python3.6/site-packages/bokeh/server/server.py", line 371, in __init__
        tornado_app = BokehTornado(applications, extra_websocket_origins=extra_websocket_origins, prefix=self.prefix, **kwargs)
    TypeError: __init__() got an unexpected keyword argument 'host'
    distributed.scheduler - INFO -   Scheduler at: tcp://10.118.224.134:8786
    distributed.scheduler - INFO -        http at:                     :9786
    distributed.scheduler - INFO - Local Directory:    /tmp/scheduler-y6b8mnih
    distributed.scheduler - INFO - -----------------------------------------------
    distributed.scheduler - INFO - Receive client connection: Client-7b476bf6-c6d8-11e7-b839-a0040220fe80
    distributed.scheduler - INFO - End scheduler at 'tcp://:8786'

* **known error**: see `Github issue`_ (closed), fixed in Dask.distributed version ``0.20.0``
* **workaround**: launch with bokeh disabled: ``dask-scheduler --no-bokeh``
* **solution**: upgrade to Dask distributed ``0.20.0`` or higher

Workers do not connect with Dask scheduler
------------------------------------------

We have observed that sometimes when running the ``dask-worker`` command, the
workers start but no connections are made to the scheduler.

**Solutions**:

* delete the ``dask-worker-space`` directory before starting the workers.
* specifying the ``local_dir`` (with enough space) when instantiating a Dask
distributed ``Client``:

.. code-block:: python3
    :emphasize-lines: 2,3

    >>> from dask.distributed import Client, LocalCluster
    >>> worker_kwargs = {'local_dir': '/tmp'}
    >>> cluster = LocalCluster(**worker_kwargs)
    >>> client = Client(cluster)
    >>> client

    <Client: scheduler='tcp://127.0.0.1:41803' processes=28 cores=28>

* **Github issue**: https://github.com/dask/distributed/issues/1707
