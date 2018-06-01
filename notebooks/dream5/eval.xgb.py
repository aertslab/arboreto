
from dreamtools import D5C4

nw1 = "net1_xgb.tsv"
nw3 = "net3_xgb.tsv"
nw4 = "net4_xgb.tsv"

s = D5C4()
filenames = [nw1, nw3, nw4]
score = s.score(filenames)
print(score)
