import pandas as pd

from distributed import Client, LocalCluster
from arboreto.utils import load_tf_names
from arboreto.algo import grnboost2

if __name__ == '__main__':

    in_file  = 'net1_expression_data.tsv'
    tf_file  = 'net1_transcription_factors.tsv'
    out_file = 'net1_grn_output.tsv'

    # ex_matrix is a DataFrame with gene names as column names
    ex_matrix = pd.read_csv(in_file, sep='\t')

    # tf_names is read using a utility function included in Arboreto
    tf_names = load_tf_names(tf_file)

    # instantiate a custom Dask distributed Client
    client = Client(LocalCluster())

    # compute the GRN
    network = grnboost2(expression_data=ex_matrix,
                        tf_names=tf_names,
                        client_or_address=client)

    # write the GRN to file
    network.to_csv(out_file, sep='\t', index=False, header=False)