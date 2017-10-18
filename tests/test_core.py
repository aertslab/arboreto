"""
Tests for the arboretum.core package.
"""

import unittest
from unittest import TestCase
from arboretum.core import *
from arboretum.dream5.utils import *


class Dream5Net1Tests(TestCase):

    net1_ex_path = '../resources/net1/net1_expression_data.tsv'
    net1_tf_path = '../resources/net1/net1_transcription_factors.tsv'

    net1_shape = (805, 1643)

    net1_matrix = load_expression_matrix(net1_ex_path)
    net1_gene_names = load_gene_names(net1_ex_path)
    net1_tf_names = load_tf_names(net1_tf_path, net1_gene_names)

    def test_load_net1_matrix(self):
        self.assertEqual(self.net1_shape, self.net1_matrix.shape)

    def test_load_net1_gene_names(self):
        self.assertEqual(self.net1_shape[1], len(self.net1_gene_names))

    def test_load_net1_tf_names(self):
        self.assertEqual(195, len(self.net1_tf_names))

    def test_infer


if __name__ == '__main__':
    unittest.main()
