"""
Tests for arboreto.algo.
"""

from unittest import TestCase, skip
import numpy as np
import pandas as pd

from scipy.sparse import csc_matrix
from distributed import Client, LocalCluster
from os.path import join

from arboreto.algo import _prepare_input, _prepare_client
from arboreto.algo import grnboost2, genie3
from arboreto.utils import *
from tests import resources_path


class PrepareClientTest(TestCase):

    def test_None(self):
        client, shutdown_callback = _prepare_client(None)

        self.assertIn('127.0.0.1', client.scheduler.address)

        shutdown_callback()

    def test_local(self):
        client, shutdown_callback = _prepare_client('local')

        self.assertIn('127.0.0.1', client.scheduler.address)

        shutdown_callback()

    def test_client(self):
        lc = LocalCluster(diagnostics_port=None)
        passed = Client(lc)

        client, shutdown_callback = _prepare_client(passed)

        self.assertEquals(client, passed)

        shutdown_callback()
        passed.close()
        lc.close()
        lc.status

        self.assertEquals(lc.status.value, 'closed')

    def test_address(self):
        with self.assertRaises(Exception) as context:
            address = 'tcp://127.0.0.2:12345'
            _prepare_client(address)

        self.assertIn('Timed out trying to connect to tcp://127.0.0.2:12345 after 10 s', str(context.exception))

    def test_other(self):
        with self.assertRaises(Exception) as context:
            _prepare_client(666)

        self.assertIn('Invalid client specified', str(context.exception))


zeisel_small_path = join(resources_path, 'sparse/zeisel_small.tsv')
zeisel_tfs_path = join(resources_path, 'sparse/zeisel_tfs.txt')

df = pd.read_csv(zeisel_small_path, sep='\t')
tfs = load_tf_names(zeisel_tfs_path)


class PrepareInputTest(TestCase):

    def test_DataFrame(self):
        m, g, t = _prepare_input(expression_data=df,
                                 gene_names=None,
                                 tf_names=tfs)

        self.assertTrue(isinstance(m, np.ndarray))
        self.assertEquals((500, 50), m.shape)
        self.assertEquals(50, len(g))
        self.assertEquals(4, len(t))

    def test_numpy_dense_matrix(self):
        m, g, t = _prepare_input(expression_data=df.to_numpy(),
                                 gene_names=list(df.columns),
                                 tf_names=tfs)

        self.assertTrue(isinstance(m, np.ndarray))
        self.assertEquals((500, 50), m.shape)
        self.assertEquals(50, len(g))
        self.assertEquals(4, len(t))

    def test_scipy_csc_matrix(self):
        csc = csc_matrix(df.to_numpy())

        m, g, t = _prepare_input(expression_data=csc,
                                 gene_names=list(df.columns),
                                 tf_names=tfs)

        self.assertTrue(isinstance(m, csc_matrix))
        self.assertEquals((500, 50), m.shape)
        self.assertEquals(50, len(g))
        self.assertEquals(4, len(t))


class LaunchTests(TestCase):

    def test_launch_grnboost2(self):
        network_df = grnboost2(df, tf_names=tfs)

        self.assertGreater(len(network_df), 100)

    def test_launch_genie3(self):
        network_df = genie3(df, tf_names=tfs)

        self.assertGreater(len(network_df), 100)
