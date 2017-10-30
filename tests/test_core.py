"""
Tests for the arboretum.core package.
"""

import unittest
from unittest import TestCase
from arboretum.dream5.utils import *


net1_ex_path = '../resources/net1/net1_expression_data.tsv'
net1_tf_path = '../resources/net1/net1_transcription_factors.tsv'

net1_shape = (805, 1643)

net1_matrix = load_expression_matrix(net1_ex_path)
net1_gene_names = load_gene_names(net1_ex_path)
net1_tf_names = load_tf_names(net1_tf_path, net1_gene_names)
net1_tf_matrix = to_tf_matrix(net1_matrix, net1_gene_names, net1_tf_names)


class IsOobHeuristicSupportedTests(TestCase):

    def test_RF(self):
        self.assertFalse(is_oob_heuristic_supported("RF", {}))

    def test_non_stochastic_GBM(self):
        self.assertFalse(is_oob_heuristic_supported("GBM", {}))

    def test_stochastic_GBM(self):
        self.assertFalse(is_oob_heuristic_supported("GBM", {'subsample': 1}))

        self.assertTrue(is_oob_heuristic_supported("GBM", {'subsample': 0.9}))


class ToTFMatrixTests(TestCase):

    def test_TF_matrix(self):
        self.assertEquals(net1_tf_matrix.shape, (805, 195))


class InferLinksTests(TestCase):  # slow

    TF = 0
    NO_TF = 200

    def inner(self, regressor_type, regressor_kwargs, target_idx):
        target_gene_name = net1_gene_names[target_idx]
        target_gene_expression = net1_matrix[:, target_idx]

        links_df = infer_links(regressor_type,
                               regressor_kwargs,
                               net1_tf_matrix,
                               net1_tf_names,
                               target_gene_name,
                               target_gene_expression)

        self.assertListEqual(list(links_df.columns), ['TF', 'target', 'importance'])

        self.assertFalse(target_gene_name in links_df['TF'].values)

    def test_smoke_fit_RF_model(self):
        self.inner("RF", RF_KWARGS, self.TF)
        self.inner("RF", RF_KWARGS, self.NO_TF)

    def test_smoke_fit_ET_model(self):
        self.inner("ET", ET_KWARGS, self.TF)
        self.inner("ET", ET_KWARGS, self.NO_TF)

    def test_smoke_fit_GBM_model(self):
        self.inner("GBM", GBM_KWARGS, self.TF)
        self.inner("GBM", GBM_KWARGS, self.NO_TF)

    def test_smoke_fit_stochastic_GBM_model(self):
        self.inner("GBM", SGBM_KWARGS, self.TF)
        self.inner("GBM", SGBM_KWARGS, self.NO_TF)


class CleanTFMatrixTests(TestCase):

    tf_matrix = to_tf_matrix(net1_matrix, net1_gene_names, net1_tf_names)

    target_is_TF = "G1"
    target_not_TF = "G666"

    def test_target_is_TF(self):
        (clean_tf_matrix, clean_tf_names) = clean(self.tf_matrix, net1_tf_names, self.target_is_TF)

        self.assertEquals(clean_tf_matrix.shape[1], self.tf_matrix.shape[1] - 1)
        self.assertEquals(len(clean_tf_names), len(net1_tf_names) - 1)

        self.assertTrue(self.target_is_TF in net1_tf_names)
        self.assertFalse(self.target_is_TF in clean_tf_names)

    def test_target_not_TF(self):
        (clean_tf_matrix, clean_tf_names) = clean(self.tf_matrix, net1_tf_names, self.target_not_TF)

        self.assertEquals(clean_tf_matrix.shape, self.tf_matrix.shape)
        self.assertEquals(clean_tf_names, net1_tf_names)


# class InferLinksTests(TestCase):


class TargetGeneIndicesTest(TestCase):

    gene_names = ['A', 'B', 'C', 'D', 'E']

    def test_subset(self):
        self.assertEquals([0, 2, 4], target_gene_indices(self.gene_names, ['A', 'C', 'E']))

    def test_all(self):
        self.assertEquals([0, 1, 2, 3, 4], target_gene_indices(self.gene_names, 'all'))

    def test_top(self):
        self.assertEquals([0, 1, 2], target_gene_indices(self.gene_names, 3))

        self.assertEquals([0, 1, 2, 3, 4], target_gene_indices(self.gene_names, 6))

        with self.assertRaises(AssertionError):
            target_gene_indices(self.gene_names, 0)

    def test_error(self):
        with self.assertRaises(ValueError):
            target_gene_indices(self.gene_names, 'some')


class Dream5Net1Tests(TestCase):

    def test_load_net1_matrix(self):
        self.assertEquals(net1_shape, net1_matrix.shape)

    def test_load_net1_gene_names(self):
        self.assertEquals(net1_shape[1], len(net1_gene_names))

    def test_load_net1_tf_names(self):
        self.assertEquals(195, len(net1_tf_names))


if __name__ == '__main__':
    unittest.main()
