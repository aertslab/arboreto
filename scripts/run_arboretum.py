"""
Python script for Arboreto with command line interface support.
"""

import argparse
import pandas as pd
import time

from pathlib import Path
from arboreto.algo import genie3, grnboost2
from arboreto.utils import load_tf_names
from distributed import Client

parser = argparse.ArgumentParser()
parser.add_argument('-i', type=str, required=True, help='the expression matrix file (required)')
parser.add_argument('-tf', type=str, required=True, help='the transcription factors file (required)')
parser.add_argument('-o', type=str, required=True, help='the file for the network output (required)')
parser.add_argument('-a', '--scheduler_address', required=False, help='Dask scheduler address (optional)')
parser.add_argument('--genie3', help='use GENIE3', action='store_true')
parser.add_argument('--grnboost2', help='use GRNBoost2 (default)', action='store_true')
parser.add_argument('--dry-run', action='store_true', help='test input without launching inference runs (optional)')
parser.add_argument('--seed', type=int, required=False, default=None,
                    help='Seed value for regressor random state initialization (optional)')


if __name__ == '__main__':

    # ------------------ #
    # VALIDATE ARGUMENTS #
    # ------------------ #

    args = parser.parse_args()

    print('validating args {}'.format(str(args)))

    if not Path(args.i).is_file():
        raise ValueError('input file "{}" does not exist'.format(args.i))

    if not Path(args.tf).is_file():
        raise ValueError('tf file "{}" does not exists'.format(args.tf))

    if not (args.genie3 or args.grnboost2):
        raise ValueError('you must choose an inference algorithm "--genie3" or "--grnboost2"')

    print('arguments valid\n')

    # ---------------- #
    # START WALL CLOCK #
    # ---------------- #

    start_time = time.time()

    # ---------------------- #
    # READ EXPRESSION MATRIX #
    # ---------------------- #

    print('reading expression matrix from "{}"'.format(args.i))

    expression_matrix = pd.read_csv(args.i, sep='\t')

    print('expression matrix shape: {}'.format(str(expression_matrix.shape)))
    em_time = time.time()
    print('expression matrix read in {} seconds\n'.format(em_time - start_time))

    # -------------------------- #
    # READ TRANSCRIPTION FACTORS #
    # -------------------------- #

    print('reading transcription factors from "{}"'.format(args.tf))

    tf_names = load_tf_names(args.tf)

    gene_names = expression_matrix.columns
    tfs_in_matrix = set(tf_names).intersection(set(gene_names))
    print('{} transcription factors in common with expression matrix\n'.format(str(len(tfs_in_matrix))))

    # ------------- #
    # INFER NETWORK #
    # ------------- #

    if args.genie3:
        inf_algo = genie3
        inf_algo_name = 'GENIE3'
    else:
        inf_algo = grnboost2
        inf_algo_name = 'GRNBoost2'

    if not args.dry_run:
        print('inferring network with {}'.format(inf_algo_name))

        if args.scheduler_address:
            print('using remote scheduler {}'.format(args.scheduler_address))
            client = Client(args.scheduler_address)
            print(client._repr_html_())
        else:
            client = None
            print('no scheduler address specified, continuing with Dask LocalCluster')

        network_df = inf_algo(expression_data=expression_matrix,
                              tf_names=tf_names,
                              client_or_address=client,
                              seed=args.seed)

        if client:
            client.shutdown()

        inf_time = time.time()
        print('network inference completed in {} seconds'.format(str(inf_time - start_time)))
        network_df.to_csv(args.o, sep='\t')
        print('network written to "{}"\n'.format(args.o))
    else:
        print('dry run: not inferring network with {}\n'.format(inf_algo_name))

    # -------------- #
    # END WALL CLOCK #
    # -------------- #

    end_time = time.time()

    print('wall time: {} seconds'.format(end_time - start_time))
