#!/usr/bin/env bash

python run_arboreto.py --grnboost2 \
-i ../resources/dream5/net1/net1_expression_data.tsv \
-tf ../resources/dream5/net1/net1_transcription_factors.tsv \
-o net1_output.tsv \
> net1_run_log.txt