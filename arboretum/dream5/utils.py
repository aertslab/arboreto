"""
Utility functions for reading DREAM5 data.
"""

import numpy as np


def load_expression_matrix(path, delimiter='\t'):
    """
    :param path: the path of the dream challenge expression data file.
    :param delimiter: the delimiter used in the file.
    :return: a numpy matrix.
    """

    return np.genfromtxt(path, delimiter=delimiter, skip_header=1)


def load_gene_names(path, delimiter='\t'):
    """
    :param path: the path of the dream challenge expression data file.
    :param delimiter: the delimiter used in the file.
    :return: a list of gene names.
    """

    with open(path) as file:
        gene_names = [gene.strip() for gene in file.readline().split(delimiter)]

    return gene_names


def load_tf_names(path, gene_names):
    """
    :param path: the path of the transcription factor list file.
    :param gene_names: the list of gene names in the expression data.
    :return: a list of transcription factor names read from the file, intersected with the gene_names list.
    """

    with open(path) as file:
        tfs_in_file = [line.strip() for line in file.readlines()]

    return [tf for tf in tfs_in_file if tf in gene_names]
