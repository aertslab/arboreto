#!/usr/bin/env bash

# Script used to perform performance tests on 10k, 20k, 30k, 40k subsets of the Macosko dataset on
# 1x25, 2x25, 3x25, 4x25, 5x25 Dask workers on the VSC front nodes (512GB ram, 2x12 hyperthreaded Xeon CPUs)


# work dir (absolute)
# export wd="/media/tmo/data/work/datasets/macosko/in/"
export wd="/ddn1/vol1/staging/leuven/stg_00002/lcb/tmoerman/data/macosko/"
# target dir (relative)
export td=$1
# Dask scheduler address
export address="tcp://10.118.224.134:8789"

# algorithm (swap with desired algorithm)
# algo="grnboost2"
algo="genie3"

echo "wd: " ${wd}
echo "td: " ${td}
echo "scheduler address: " ${address}

echo "macosko 40k subset with ${algo}"
python run_arboreto.py --${algo} -a ${address} -i ${wd}macosko_40k.tsv.gz -tf ${wd}mm9_TFs.upper.txt -o ${td}/macosko_40k_network.${algo}.tsv > ${td}/macosko_40k_log.${algo}.txt
wait

echo "macosko 30k subset with ${algo}"
python run_arboreto.py --${algo} -a ${address} -i ${wd}macosko_30k.tsv.gz -tf ${wd}mm9_TFs.upper.txt -o ${td}/macosko_30k_network.${algo}.tsv > ${td}/macosko_30k_log.${algo}.txt
wait

echo "macosko 20k subset with ${algo}"
python run_arboreto.py --${algo} -a ${address} -i ${wd}macosko_20k.tsv.gz -tf ${wd}mm9_TFs.upper.txt -o ${td}/macosko_20k_network.${algo}.tsv > ${td}/macosko_20k_log.${algo}.txt
wait

echo "macosko 10k subset with ${algo}"
python run_arboreto.py --${algo} -a ${address} -i ${wd}macosko_10k.tsv.gz -tf ${wd}mm9_TFs.upper.txt -o ${td}/macosko_10k_network.${algo}.tsv > ${td}/macosko_10k_log.${algo}.txt

echo "all subsets done with ${algo}"
