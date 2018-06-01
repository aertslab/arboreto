python run_arboreto.py --grnboost2 \
  -i ../resources/dream5/net1/net1_expression_data.tsv \
  -tf ../resources/dream5/net1/net1_transcription_factors.tsv \
  -o net1_output.tsv \
  > net1_run_log.txt
python run_arboreto.py --grnboost2 \
  -i ../resources/dream5/net3/net3_expression_data.tsv \
  -tf ../resources/dream5/net3/net3_transcription_factors.tsv \
  -o net3_output.tsv \
  > net3_run_log.txt
python run_arboreto.py --grnboost2 \
  -i ../resources/dream5/net4/net4_expression_data.tsv \
  -tf ../resources/dream5/net4/net4_transcription_factors.tsv \
  -o net4_output.tsv \
  > net4_run_log.txt



