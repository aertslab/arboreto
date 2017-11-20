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


def diy(expression_df,
        regressor_type,
        regressor_kwargs,
        tf_names='all',
        gene_names=None,
        client=None,
        limit=None,
        seed=DEMON_SEED):
    """
    Launch arboretum in DIY mode, the user specifies regressor type and kwargs.

    :param expression_df:
    :param regressor_type:
    :param regressor_kwargs:
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
    else:
        expression_matrix = expression_data
        assert expression_matrix.shape[1] == len(gene_names)

    if tf_names is None:
        tf_names = gene_names
    else:
        if len(tf_names) == 0:
            raise ValueError('Specified tf_names is empty')

        if not set(gene_names).intersection(set(tf_names)):
            raise ValueError('Intersection of gene_names and tf_names is empty.')

    return expression_matrix, gene_names, tf_names
