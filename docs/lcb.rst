.. _lcb: https://gbiomed.kuleuven.be/english/research/50000622/lcb
.. _vsc: https://www.vscentrum.be/
.. _Gert: https://gbiomed.kuleuven.be/english/research/50000622/lcb/people/00079808
.. _Mark: https://gbiomed.kuleuven.be/english/research/50000622/lcb/people/00089478
.. _ssh: https://en.wikipedia.org/wiki/Secure_Shell
.. _`port forwarding`: https://help.ubuntu.com/community/SSH/OpenSSH/PortForwarding
.. _`terminal multiplexer`: https://en.wikipedia.org/wiki/Terminal_multiplexer
.. _tmux: https://github.com/tmux/tmux/wiki
.. _jupyter: http://jupyter.org/
.. _`jupyter lab`: https://github.com/jupyterlab/jupyterlab
.. _`installation guide`: installation.html
.. _`known issue`: #known-issues
.. _`github issue`: https://github.com/dask/distributed/issues/1515
.. _`diagnostics dashboard`: http://distributed.readthedocs.io/en/latest/web.html
.. _`Running with a Dask distributed scheduler`: userguide.html#running-with-a-dask-distributed-scheduler

LCB Notes
=========

This page contains additional documentation relevant for the Stein Aerts Lab of
Computation Biology (LCB_).

.. contents::
    :depth: 2
    :local:

VSC access
----------

First you will need access to the VSC_ front nodes. For this, a VSC_ account is
required plus additional ssh_ configuration.

.. tip::

    Kindly ask Gert_ for assistance setting up your ssh_ configuration for the VSC using the
    ``https://git.aertslab.org/connect_to_servers/`` script.


Front nodes
~~~~~~~~~~~

We will work with following machines:

=========   ========    =======================     ======
Alias       HostName    CPU                         Memory
=========   ========    =======================     ======
hpc2-big1   r10n1       10 core (20 threads)        256 GB
hpc2-big2   r10n2       10 core (20 threads)        256 GB
hpc2-big3   r6i0n5      2x 12-core (48 threads)     512 GB
hpc2-big4   r6i0n12     2x 12-core (48 threads)     512 GB
hpc2-big5   r6i0n13     2x 12-core (48 threads)     512 GB
hpc2-big6   r6i1n12     2x 12-core (48 threads)     512 GB
hpc2-big7   r6i1n13     2x 12-core (48 threads)     512 GB
=========   ========    =======================     ======

The aliases are the ones defined by the ``https://git.aertslab.org/connect_to_servers/`` script.

Running Arboreto on the front nodes
------------------------------------

Following section describes the steps requires for inferring a GRN using Arboreto
in distributed mode, using the front nodes.

.. tip::

    Setting up a Dask.distributed cluster requires ssh access to multiple nodes.
    We recommend using a `terminal multiplexer`_ tool like tmux_ for managing
    multiple ssh sessions.

    On the VSC_, tmux_ is available by loading following module:

    .. code-block:: bash

        $ module load tmux/2.5-foss-2014a

We will set up a cluster using about half the CPU resources of the 5 larger nodes
(``hpc2-big3`` to ``hpc2-big7``). One of the large nodes will also host the
Dask scheduler. One a smaller node, we run a Jupyter_ notebook server from which we
run the GRN inference using Arboreto.


.. figure:: https://github.com/tmoerman/arboreto/blob/master/img/lcb/distributed.png?raw=true
    :alt: LCB front nodes distributed architecture
    :align: center

    LCB front nodes distributed architecture

0. Software preparation
~~~~~~~~~~~~~~~~~~~~~~~

As recommended in the `Installation Guide`_, we will use an Anaconda distribution.
On the front nodes we do this by loading a module:

.. code-block:: bash
    :caption: ``vsc12345@r6i0n5``

    $ module load Anaconda/5-Python-3.6

We obviously need Arboreto (make sure you have the latest version):

.. code-block:: bash
    :caption: ``vsc12345@r6i0n5``

    $ pip install arboreto

    $ pip show arboreto

    Name: arboreto
    Version: 0.1.5
    Summary: Scalable gene regulatory network inference using tree-based ensemble regressors
    Home-page: https://github.com/tmoerman/arboreto
    Author: Thomas Moerman
    Author-email: thomas.moerman@gmail.com
    License: BSD 3-Clause License
    Location: /vsc-hard-mounts/leuven-data/software/biomed/Anaconda/5-Python-3.6/lib/python3.6/site-packages
    Requires: scikit-learn, dask, numpy, scipy, distributed, pandas

We now proceed with launching the Dask scheduler and workers. Make sure that on
the nodes, the Anaconda module was loaded like explained above.

1. Starting the Dask scheduler
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

On node ``r6i0n5``, we launch the Dask scheduler.

.. code-block:: bash
    :emphasize-lines: 4, 5
    :caption: ``vsc12345@r6i0n5``

    $ dask-scheduler

    distributed.scheduler - INFO - -----------------------------------------------                                                                                                                      │distributed.worker - INFO -         Registered to:  tcp://10.118.224.134:8786
    distributed.scheduler - INFO -   Scheduler at: tcp://10.118.224.134:8786                                                                                                                            │distributed.worker - INFO - -------------------------------------------------
    distributed.scheduler - INFO -       bokeh at:                    :35874                                                                                                                            │distributed.worker - INFO -         Registered to:  tcp://10.118.224.134:8786
    distributed.scheduler - INFO - Local Directory:    /tmp/scheduler-wu5odlrh                                                                                                                          │distributed.worker - INFO - -------------------------------------------------
    distributed.scheduler - INFO - -----------------------------------------------

The command launches 2 services:

* The Dask scheduler on address: ``tcp://10.118.224.134:8786``
* The Dask `diagnostics dashboard`_ on address: ``tcp://10.118.224.134:35874``

.. tip::

    The Dask `diagnostics dashboard`_ is useful for monitoring the progress of
    long-running Dask jobs. In order to view the dashboard, which runs on the VSC
    front node ``r6i0n5``, use ssh `port forwarding`_ as follows:

    .. code-block:: bash

        ssh -L 8787:localhost:35874 hpc2-big3

    You can now view the Dask dashboard on url: ``http://localhost:8787``.

2. Adding workers to the scheduler
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _nice: https://en.wikipedia.org/wiki/Nice_%28Unix%29

We will need the scheduler address: ``tcp://10.118.224.134:8786`` (highlighted
above) when launching worker processes connected to the scheduler.

First, we launch 24 worker processes on the same machine where the scheduler is
running:

.. code-block:: bash
    :caption: ``vsc12345@r6i0n5``

    $ nice -n 10 dask-worker tcp://10.118.224.134:8786 --nprocs 24 --nthreads 1

The command above consists of several parts, let's briefly discuss them:

* ``nice -n 10``

    Setting a nice_ value of higher than 0 gives the process a lower priority,
    which is sometimes desirable to not highjack the resources on compute nodes
    used by multiple users.

    Setting a nice_ value is **entirely optional** and up to the person setting up
    the distributed network. You can safely omit this.

* ``dask-worker tcp://10.118.224.134:8786 --nprocs 24 --nthreads 1``

    Spins up 24 worker processes with 1 thread per process. For Arboreto, it is
    recommended to always set ``--nthreads 1``.

    In this case we have chosen 24 processes because we planned to use only half
    the CPU capacity of the front nodes.

In the terminal where the scheduler was launched, you should see messages indicating
workers have been connected to the scheduler:

.. code-block:: bash

    distributed.scheduler - INFO - Register tcp://10.118.224.134:43342
    distributed.scheduler - INFO - Starting worker compute stream, tcp://10.118.224.134:43342

We now repeat the same command on the other compute nodes that will run Dask worker processes:

.. code-block:: bash
    :caption: ``vsc12345@r6i0n12``

    $ nice -n 10 dask-worker tcp://10.118.224.134:8786 --nprocs 24 --nthreads 1

.. code-block:: bash
    :caption: ``vsc12345@r6i0n13``

    $ nice -n 10 dask-worker tcp://10.118.224.134:8786 --nprocs 24 --nthreads 1

.. code-block:: bash
    :caption: ``vsc12345@r6i1n12``

    $ nice -n 10 dask-worker tcp://10.118.224.134:8786 --nprocs 24 --nthreads 1

.. code-block:: bash
    :caption: ``vsc12345@r6i1n13``

    $ nice -n 10 dask-worker tcp://10.118.224.134:8786 --nprocs 24 --nthreads 1

3. Running Arboreto from a Jupyter notebook
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

So far, we have a scheduler running with 5*24 worker processes connected to it and
a diagnostics dashboard. Let's now run a Jupyter_ notebook or `Jupyter Lab`_
server so that we can interact with the Dask cluster from within a Jupyter_ environment.

.. code-block:: bash
    :caption: ``vsc12345@r10n2``
    :emphasize-lines: 1, 14, 15, 16

    $ jupyter lab --port 9999 --no-browser

    [I 12:16:08.725 LabApp] JupyterLab alpha preview extension loaded from /data/leuven/software/biomed/Anaconda/5-Python-3.6/lib/python3.6/site-packages/jupyterlab
    JupyterLab v0.27.0
    Known labextensions:
    [I 12:16:08.739 LabApp] Running the core application with no additional extensions or settings
    [I 12:16:08.766 LabApp] Serving notebooks from local directory: /ddn1/vol1/staging/leuven/stg_00002/lcb/tmoerman/nb
    [I 12:16:08.766 LabApp] 0 active kernels
    [I 12:16:08.766 LabApp] The Jupyter Notebook is running at:
    [I 12:16:08.766 LabApp] http://localhost:9999/?token=2dca6ce946265895846795c4983191c9f76ba954f414efdf
    [I 12:16:08.766 LabApp] Use Control-C to stop this server and shut down all kernels (twice to skip confirmation).
    [C 12:16:08.767 LabApp]

        Copy/paste this URL into your browser when you connect for the first time,
        to login with a token:
            http://localhost:9999/?token=2dca6ce946265895846795c4983191c9f76ba954f414efdf

Again, use ssh `port forwarding`_ to access the notebook server. Execute following
command in a shell on your *local* machine:

.. code-block:: bash
    :caption: ``localhost``

    $ ssh -L 9999:localhost:9999 hpc2-big2

To access the notebook open a browser and navigate to following url:

    ``http://localhost:9999/?token=2dca6ce946265895846795c4983191c9f76ba954f414efdf``

.. note::

    Using Jupyter is **entirely optional**. Everything explained in the following
    section is equally applicable to running Arboreto from a simple Python session
    or script.

    As an example, please consider `this script <https://github.com/tmoerman/arboreto/blob/master/scripts/run_arboreto.py>`_. Remember that the main code
    should be in a code block protected by:

    .. code-block:: python
        :emphasize-lines: 1

        if __name__ == '__main__':
            # ... code ...

Now we are ready to create a new notebook in Jupyter and write some Python code
to check whether the cluster was set up correctly:

.. code-block:: python

    In [1]: from distributed import Client

    In [2]: client = Client('tcp://10.118.224.134:8786')

    In [3]: client

    Out[3]:

        Client
        * Scheduler: tcp://10.118.224.134:8786
        * Dashboard: http://10.118.224.134:35874

        Cluster
        * Workers: 120
        * Cores: 120
        * Memory: 1354.63 GB

The cluster is set up and ready for Arboreto GRN inference work. Please review
the section `Running with a Dask distributed scheduler`_ on how to use Arboreto in distributed mode.

To run in distributed mode, we need to make one modification to the code launching
the inference algorithm: specifying ``client_or_address`` in the (in this case) ``genie3`` function:

.. code-block:: python
    :emphasize-lines: 3

    network_df = genie3(expression_data=ex_matrix,
                        tf_names=tf_names,
                        client_or_address=client)

While our computation is running, we can consult the Dask `diagnostics dashboard`_
to monitor progress. Point a browser to ``localhost:8787/status``, you should see
a dynamic visualization like this:

.. figure:: https://github.com/tmoerman/arboreto/blob/master/img/lcb/dashboard_front_nodes.png?raw=true
    :align: center

    Dask diagnostics dashboard visualizing Arboreto progress

Note the progress gauges in the bottom:

    ``infer_data`` --> ``693 / 14086`` means that 693 out of 14086 inference steps
    have been completed so far. As the inference steps entail almost the entire
    workload of the algorithm, this is a pretty accurate progress indicator.
