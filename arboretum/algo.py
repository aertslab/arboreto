"""
Top-level functions.
"""

import pandas as pd
from distributed import Client, LocalCluster
from arboretum.core import create_graph, SGBM_KWARGS, RF_KWARGS


def grnboost2(expression_data,
              gene_names=None,
              tf_names='all',
              client_or_address='local',
              limit=None,
              seed=None):
    """
    Launch arboretum with [GRNBoost2] profile.

    :param expression_data: one of:
           * a pandas DataFrame (rows=observations, columns=genes)
           * a dense 2D numpy.ndarray
           * a sparse scipy.sparce.csc_matrix
    :param gene_names: optional list of gene names (strings). Required when a (dense or sparse) matrix is passed as
                       'expression_data' instead of a DataFrame.
    :param tf_names: optional list of transcription factors. If None or 'all', the list of gene_names will be used.
    :param client_or_address: one of:
           * None or 'local': a new Client(LocalCluster()) will be used to perform the computation.
           * string address: a new Client(address) will be used to perform the computation.
           * a Client instance: the specified Client instance will be used to perform the computation.
    :param limit: optional number (int) of top regulatory links to return. Default None.
    :param seed: optional random seed for the regressors. Default None.
    :return: a pandas DataFrame['TF', 'target', 'importance'] representing the inferred gene regulatory links.
    """

    return diy(expression_data=expression_data, regressor_type='GBM', regressor_kwargs=SGBM_KWARGS,
               gene_names=gene_names, tf_names=tf_names, client_or_address=client_or_address, limit=limit, seed=seed)


def genie3(expression_data,
           gene_names=None,
           tf_names='all',
           client_or_address='local',
           limit=None,
           seed=None):
    """
    Launch arboretum with [GENIE3] profile.

    :param expression_data: one of:
           * a pandas DataFrame (rows=observations, columns=genes)
           * a dense 2D numpy.ndarray
           * a sparse scipy.sparce.csc_matrix
    :param gene_names: optional list of gene names (strings). Required when a (dense or sparse) matrix is passed as
                       'expression_data' instead of a DataFrame.
    :param tf_names: optional list of transcription factors. If None or 'all', the list of gene_names will be used.
    :param client_or_address: one of:
           * None or 'local': a new Client(LocalCluster()) will be used to perform the computation.
           * string address: a new Client(address) will be used to perform the computation.
           * a Client instance: the specified Client instance will be used to perform the computation.
    :param limit: optional number (int) of top regulatory links to return. Default None.
    :param seed: optional random seed for the regressors. Default None.
    :return: a pandas DataFrame['TF', 'target', 'importance'] representing the inferred gene regulatory links.
    """

    return diy(expression_data=expression_data, regressor_type='RF', regressor_kwargs=RF_KWARGS,
               gene_names=gene_names, tf_names=tf_names, client_or_address=client_or_address, limit=limit, seed=seed)


def diy(expression_data,
        regressor_type,
        regressor_kwargs,
        gene_names=None,
        tf_names='all',
        client_or_address='local',
        limit=None,
        seed=None):
    """
    :param expression_data: one of:
           * a pandas DataFrame (rows=observations, columns=genes)
           * a dense 2D numpy.ndarray
           * a sparse scipy.sparce.csc_matrix
    :param regressor_type: string. One of: 'RF', 'GBM', 'ET'. Case insensitive.
    :param regressor_kwargs: a dictionary of key-value pairs that configures the regressor.
    :param gene_names: optional list of gene names (strings). Required when a (dense or sparse) matrix is passed as
                       'expression_data' instead of a DataFrame.
    :param tf_names: optional list of transcription factors. If None or 'all', the list of gene_names will be used.
    :param client_or_address: one of:
           * None or 'local': a new Client(LocalCluster()) will be used to perform the computation.
           * string address: a new Client(address) will be used to perform the computation.
           * a Client instance: the specified Client instance will be used to perform the computation.
    :param limit: optional number (int) of top regulatory links to return. Default None.
    :param seed: optional random seed for the regressors. Default 666. Use None for random seed.
    :return: a pandas DataFrame['TF', 'target', 'importance'] representing the inferred gene regulatory links.
    """

    client_or_address, shutdown_callback = _prepare_client(client_or_address)

    try:
        expression_matrix, gene_names, tf_names = _prepare_input(expression_data, gene_names, tf_names)

        graph = create_graph(expression_matrix,
                             gene_names,
                             tf_names,
                             client=client_or_address,
                             regressor_type=regressor_type,
                             regressor_kwargs=regressor_kwargs,
                             limit=limit,
                             seed=seed)

        return client_or_address.compute(graph, sync=True).sort_values(by='importance', ascending=False)
    finally:
        shutdown_callback()


def _prepare_client(client_or_address):
    """
    :param client_or_address: one of:
           * None
           * verbatim: 'local'
           * string address
           * a Client instance
    :return: a tuple: (Client instance, shutdown callback function).
    :raises: ValueError if no valid client input was provided.
    """

    if client_or_address is None:
        client = Client(LocalCluster())

        return client, lambda: client.shutdown()

    if isinstance(client_or_address, str) and client_or_address.lower() == 'local':
        client = Client(LocalCluster())

        return client, lambda: client.shutdown()

    elif isinstance(client_or_address, str) and client_or_address.lower() != 'local':
        client = Client(client_or_address)

        return client, lambda: client.shutdown()

    elif isinstance(client_or_address, Client):
        return client_or_address, lambda: None

    else:
        raise ValueError("Invalid client specified {}".format(str(client_or_address)))


def _prepare_input(expression_data,
                   gene_names,
                   tf_names):
    """
    Wrangle the inputs into the correct formats.

    :param expression_data: one of:
                            * a pandas DataFrame (rows=observations, columns=genes)
                            * a dense 2D numpy.ndarray
                            * a sparse scipy.sparce.csc_matrix
    :param gene_names: optional list of gene names (strings).
                       Required when a (dense or sparse) matrix is passed as 'expression_data' instead of a DataFrame.
    :param tf_names: optional list of transcription factors. If None or 'all', the list of gene_names will be used.
    :return: a triple of:
             1. a np.ndarray or scipy.sparse.csc_matrix
             2. a list of gene name strings
             3. a list of transcription factor name strings.
    """

    if isinstance(expression_data, pd.DataFrame):
        expression_matrix = expression_data.as_matrix()
        gene_names = list(expression_data.columns)
    else:
        expression_matrix = expression_data
        assert expression_matrix.shape[1] == len(gene_names)

    if tf_names is None:
        tf_names = gene_names
    elif tf_names == 'all':
        tf_names = gene_names
    else:
        if len(tf_names) == 0:
            raise ValueError('Specified tf_names is empty')

        if not set(gene_names).intersection(set(tf_names)):
            raise ValueError('Intersection of gene_names and tf_names is empty.')

    return expression_matrix, gene_names, tf_names
