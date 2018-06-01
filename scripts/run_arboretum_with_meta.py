'''
File created to address the reviewer's comment: how many trees were used
'''

import pandas as pd
import time
import sys

from arboreto.utils import load_tf_names
from arboreto.algo import *
from distributed import Client

if __name__ == '__main__':

    ex_path = sys.argv[1]
    tf_path = sys.argv[2]
    net_out_path = sys.argv[3]
    meta_out_path = sys.argv[4]

    start_time = time.time()

    expression_matrix = pd.read_csv(ex_path, sep='\t')
    tf_names = load_tf_names(tf_path)
    gene_names = expression_matrix.columns
    client = Client(LocalCluster())

    print(client._repr_html_())

    network_graph, meta_graph = create_graph(expression_matrix.as_matrix(),
                                             gene_names,
                                             tf_names,
                                             "GBM",
                                             SGBM_KWARGS,
                                             client=client, # broadcast!
                                             early_stop_window_length=25,
                                             include_meta=True)

    # Good!
    a, b = client.persist([network_graph, meta_graph])
    network_df = a.compute(sync=True)
    meta_df = b.compute(sync=True)

    # Bad!
    # network_df, meta_df = client.compute([network_graph, meta_graph], sync=True)

    if client:
        client.close()

    network_df.to_csv(net_out_path, sep='\t', index=False)
    meta_df.to_csv(meta_out_path, sep='\t', index=False)

    end_time = time.time()

    print('wall time: {} seconds'.format(end_time - start_time))