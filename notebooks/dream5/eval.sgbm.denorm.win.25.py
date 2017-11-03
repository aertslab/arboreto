
from dreamtools import D5C4

nw1 = "net1.sgbm.denorm.tsv"
nw3 = "net3.sgbm.denorm.tsv"
nw4 = "net4.sgbm.denorm.tsv"

s = D5C4()
filenames = [nw1, nw3, nw4]
score = s.score(filenames)
print(score)
