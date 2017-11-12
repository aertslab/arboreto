"""
Top-level API functions.
"""

import pandas as pd
import numpy as np

from distributed import Client, LocalCluster
from arboretum.core import create_graph, DEMON_SEED


def grnboost2(expression_data,
              tf_names='all',
              gene_names=None,
              client=None,
              limit=None,
              seed=DEMON_SEED):
    """
    Launch arboretum with the GRNBoost2 inference profile.

    :param expression_data:
    :param tf_names:
    :param gene_names:
    :param client:
    :param limit:
    :param seed:
    :return:
    """

    expression_matrix, gene_names, tf_names = _clean_input(expression_data, gene_names, tf_names)

    if client is None:
        client = Client(LocalCluster())

    # graph = create_graph(expression_matrix,
    #                      gene_names,
    #                      tf_names,
    #
    #                      )

    return None


def genie3(expression_df,
           tf_names='all',
           gene_names=None,
           client=None,
           limit=None,
           seed=DEMON_SEED):
    """
    Launch arboretum with the GENIE3 inference profile.

    :param expression_df:
    :param tf_names:
    :param gene_names:
    :param client:
    :param limit:
    :param seed:
    :return:
    """


def _clean_input(expression_data,
                 gene_names,
                 tf_names):
    """
    Wrangle the inputs into the correct formats.

    :param expression_data: a pandas DataFrame (rows=observations, columns=genes) or a 2D numpy.ndarray.
    :param gene_names: optional list of gene names. Used in conjunction with passing a numpy.ndarray as the value for
                       expression_data.
    :param tf_names: optional list of transcription factors. If None, all gene_names will be used.
    :return: Returns a triple: np.ndarray, a list of gene name strings, a list of transcription factor name strings.
    """

    if isinstance(expression_data, pd.DataFrame):
        expression_matrix = expression_data.as_matrix()
        gene_names = list(expression_matrix.columns)
    elif isinstance(expression_data, np.ndarray):
        expression_matrix = expression_data
        assert expression_matrix.shape[1] == len(gene_names)
    else:
        raise ValueError('`expression_matrix` must be either a pandas DataFrame or a numpy ndarray.'
                         'Instead got: {0}'.format(str(type(expression_data))))

    if tf_names is None:
        tf_names = gene_names
    else:
        assert len(tf_names) > 0

    return expression_matrix, gene_names, tf_names
