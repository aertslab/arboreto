import pandas as pd
import time
import sys

from arboretum.utils import load_tf_names
from arboretum.algo import *
from distributed import Client

if __name__ == '__main__':

    ex_path = sys.argv[1]
    tf_path = sys.argv[2]
    net_out_path = sys.argv[3]

    start_time = time.time()

    df = pd.read_csv(ex_path, sep='\t')
    df = df.loc[:, (df != 0).any(axis=0)]  # remove all-zero columns

    tf_names = load_tf_names(tf_path)

    client = Client(LocalCluster())

    print('starting GRNBoost inference')

    network_df = grnboost(expression_data=df,
                          n_estimators=500,
                          tf_names=tf_names,
                          client_or_address=client)

    if client:
        client.close()

    network_df.to_csv(net_out_path, sep='\t', index=False)

    end_time = time.time()

    print('wall time: {} seconds'.format(end_time - start_time))