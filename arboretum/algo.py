"""
Top-level functions.
"""

import pandas as pd
from distributed import Client, LocalCluster
from arboretum.core import create_graph, DEMON_SEED, SGBM_KWARGS, RF_KWARGS


def grnboost2(expression_data,
              gene_names=None,
              tf_names='all',
              client='local',
              limit=None,
              seed=DEMON_SEED):
    """
    Launch arboretum with GRNBoost2 profile.

    :param expression_data:
    :param gene_names:
    :param tf_names:
    :param client:
    :param limit:
    :param seed:
    :return:
    """

    return diy(expression_data=expression_data, regressor_type='GBM', regressor_kwargs=SGBM_KWARGS,
               gene_names=gene_names, tf_names=tf_names, client=client, limit=limit, seed=seed)


def genie3(expression_data,
           gene_names=None,
           tf_names='all',
           client='local',
           limit=None,
           seed=DEMON_SEED):
    """
    Launch arboretum with GENIE3 profile.

    :param expression_data:
    :param gene_names:
    :param tf_names:
    :param client:
    :param limit:
    :param seed:
    :return:
    """

    return diy(expression_data=expression_data, regressor_type='RF', regressor_kwargs=RF_KWARGS,
               gene_names=gene_names, tf_names=tf_names, client=client, limit=limit, seed=seed)


def diy(expression_data,
        regressor_type,
        regressor_kwargs,
        gene_names=None,
        tf_names='all',
        client='local',
        limit=None,
        seed=DEMON_SEED):
    """
    :param expression_data:
    :param regressor_type:
    :param regressor_kwargs:
    :param gene_names:
    :param tf_names:
    :param client:
    :param limit:
    :param seed:
    :return:
    """

    client = _prepare_client(client)

    try:
        expression_matrix, gene_names, tf_names = _prepare_input(expression_data, gene_names, tf_names)

        graph = create_graph(expression_matrix,
                             gene_names,
                             tf_names,
                             client=client,
                             regressor_type=regressor_type,
                             regressor_kwargs=regressor_kwargs,
                             limit=limit,
                             seed=seed)

        return client.compute(graph, sync=True).sort_values(by='importance', ascending=False)
    finally:
        client.shutdown()


def _prepare_client(client):
    """
    :param client: one of:
                   * None
                   * verbatim: 'local'
                   * string address
                   * a Client instance
    :return: a Client instance in function of the input
    :raises: ValueError if no valid client input was provided.
    """

    if client is None:
        return Client(LocalCluster())

    if isinstance(client, str) and client.lower() == 'local':
        return Client(LocalCluster())

    elif isinstance(client, str) and client.lower() != 'local':
        return Client(client)

    elif isinstance(client, Client):
        return client

    else:
        raise ValueError("Invalid client specified {}".format(str(client)))


def _prepare_input(expression_data,
                   gene_names,
                   tf_names):
    """
    Wrangle the inputs into the correct formats.

    :param expression_data: accepts one of:
                            * a pandas DataFrame (rows=observations, columns=genes)
                            * a dense 2D numpy.ndarray
                            * a sparse scipy.sparce.csc_matrix
    :param gene_names: optional list of gene names. Used in conjunction with passing a numpy.ndarray as the value for
                       expression_data.
    :param tf_names: optional list of transcription factors. If None, all gene_names will be used.

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
