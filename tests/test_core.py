"""
Tests for the arboretum.core package.
"""

import unittest
from unittest import TestCase
from arboretum.dream5.utils import *

import dask

net1_ex_path = '../resources/dream5/net1/net1_expression_data.tsv'
net1_tf_path = '../resources/dream5/net1/net1_transcription_factors.tsv'

net1_shape = (805, 1643)

net1_ex_matrix = load_expression_matrix(net1_ex_path)
net1_gene_names = load_gene_names(net1_ex_path)
net1_tf_names = load_tf_names(net1_tf_path, net1_gene_names)
net1_tf_matrix = to_tf_matrix(net1_ex_matrix, net1_gene_names, net1_tf_names)


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


class RegressorToDataTests(TestCase):  # slow

    TF = 0
    NO_TF = 200

    def inner(self, regressor_type, regressor_kwargs, target_idx, seed=DEMON_SEED):
        target_gene_name = net1_gene_names[target_idx]
        target_gene_expression = net1_ex_matrix[:, target_idx]

        links_df, meta_df = regressor_to_data(regressor_type,
                                              regressor_kwargs,
                                              net1_tf_matrix,
                                              net1_tf_names,
                                              target_gene_name,
                                              target_gene_expression,
                                              include_meta=True,
                                              seed=seed)

        self.assertEqual(meta_df['target'][0], target_gene_name)

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

    def test_smoke_fit_stochastic_GBM_model_seed_None(self):
        self.inner("GBM", SGBM_KWARGS, self.TF, seed=None)


class ComputeGraphTests(TestCase):  # slow

    test_range = range(200, 205)

    def test_net1_only_links_3_targets(self):
        graph = create_graph(net1_ex_matrix,
                             net1_gene_names,
                             net1_tf_names,
                             "GBM",
                             SGBM_KWARGS,
                             target_genes=list(self.test_range))

        network_df = graph.compute(get=dask.get)

        self.assertEquals(len(self.test_range), len(network_df['target'].unique()))

    def test_net1_links_and_meta_3_targets(self):
        network_graph, meta_graph = create_graph(net1_ex_matrix,
                                                 net1_gene_names,
                                                 net1_tf_names,
                                                 "GBM",
                                                 SGBM_KWARGS,
                                                 target_genes=list(self.test_range),
                                                 include_meta=True,
                                                 early_stop_window_length=30)

        result = dask.compute(network_graph, meta_graph)

        network_df = result[0]
        meta_df = result[1]

        self.assertEquals(len(self.test_range), len(network_df['target'].unique()))
        self.assertEquals(len(self.test_range), len(meta_df['target'].unique()))


class EarlyStopMonitorTests(TestCase):

    def test_window_boundaries(self):
        m = EarlyStopMonitor()

        self.assertEqual(m.window_boundaries(0), (0, 1))
        self.assertEqual(m.window_boundaries(1), (0, 2))
        self.assertEqual(m.window_boundaries(2), (0, 3))
        self.assertEqual(m.window_boundaries(3), (0, 4))
        self.assertEqual(m.window_boundaries(4), (0, 5))
        self.assertEqual(m.window_boundaries(5), (0, 6))
        self.assertEqual(m.window_boundaries(6), (0, 7))
        self.assertEqual(m.window_boundaries(7), (0, 8))
        self.assertEqual(m.window_boundaries(8), (0, 9))
        self.assertEqual(m.window_boundaries(9), (0, 10))
        self.assertEqual(m.window_boundaries(10), (1, 11))


class CleanTFMatrixTests(TestCase):

    tf_matrix = to_tf_matrix(net1_ex_matrix, net1_gene_names, net1_tf_names)

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


class TargetGeneIndicesTest(TestCase):

    gene_names = ['A', 'B', 'C', 'D', 'E']

    def test_empty(self):
        self.assertEquals([], target_gene_indices(self.gene_names, []))

    def test_subset_strings(self):
        self.assertEquals([0, 2, 4], target_gene_indices(self.gene_names, ['A', 'C', 'E']))

    def test_subset_ints(self):
        self.assertEquals([0, 2, 4], target_gene_indices(self.gene_names, [0, 2, 4]))

    def test_all(self):
        self.assertEquals([0, 1, 2, 3, 4], target_gene_indices(self.gene_names, 'all'))

    def test_top(self):
        self.assertEquals([0, 1, 2], target_gene_indices(self.gene_names, 3))

        self.assertEquals([0, 1, 2, 3, 4], target_gene_indices(self.gene_names, 6))

        with self.assertRaises(AssertionError):
            target_gene_indices(self.gene_names, 0)

    def test_mixed_types(self):
        with self.assertRaises(ValueError):
            target_gene_indices(self.gene_names, ['A', 2, 3])

    def test_error(self):
        with self.assertRaises(ValueError):
            target_gene_indices(self.gene_names, 'some')


class Dream5Net1Tests(TestCase):

    def test_load_net1_matrix(self):
        self.assertEquals(net1_shape, net1_ex_matrix.shape)

    def test_load_net1_gene_names(self):
        self.assertEquals(net1_shape[1], len(net1_gene_names))

    def test_load_net1_tf_names(self):
        self.assertEquals(195, len(net1_tf_names))


if __name__ == '__main__':
    unittest.main()
