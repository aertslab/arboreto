import unittest
from unittest import TestCase

from distributed import Client, LocalCluster
from arboretum.algo import _clean_input, _clean_client


class CleanClientTest(TestCase):

    def test_None(self):
        client = _clean_client(None)

        self.assertIn('127.0.0.1', client.scheduler.address)

    def test_local(self):
        client = _clean_client('local')

        self.assertIn('127.0.0.1', client.scheduler.address)

    def test_client(self):
        passed = Client(LocalCluster())
        client = _clean_client(passed)

        self.assertEqual(client, passed)

    def test_address(self):
        with self.assertRaises(OSError) as context:
            address = 'tcp://127.0.0.2:12345'
            _clean_client(address)

        self.assertIn('Timed out trying to connect to \'tcp://127.0.0.2:12345\'', str(context.exception))

    def test_other(self):
        with self.assertRaises(Exception) as context:
            _clean_client(666)

        self.assertIn('Invalid client specified', str(context.exception))


class CleanInputTest(TestCase):
    
    def test_DataFrame(self):
        self.assertFalse(False)

    def test_numpy_dense_matrix(self):
        self.assertFalse(False)

    def test_scipy_csc_matrix(self):
        self.assertFalse(False)
