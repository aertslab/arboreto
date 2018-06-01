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

    tf_names = load_tf_names(tf_path)

    print('starting GRNBoost2 inference')

    network_df = grnboost2(expression_data=df,
                           tf_names=tf_names,
                           verbose=True)

    network_df.to_csv(net_out_path, sep='\t', index=False)

    end_time = time.time()

    print('wall time: {} seconds'.format(end_time - start_time))
