.. _GENIE3: http://www.montefiore.ulg.ac.be/~huynh-thu/GENIE3.html
.. _`Random Forest`: https://en.wikipedia.org/wiki/Random_forest

GRN Inference Algorithms
========================

Arboreto hosts multiple (currently 2, contributions welcome!) algorithms for
inference of gene regulatory networks from high-throughput gene expression data,
for example *single-cell RNA-seq* data.

GRNBoost2
---------

GRNBoost2 is the flagship algorithm for gene regulatory network inference, hosted
in the Arboreto framework. It was conceived as a fast alternative for GENIE3_,
in order to alleviate the processing time required for larger datasets (tens of
thousands of observations).

GRNBoost2 adopts the GRN inference strategy exemplified by GENIE3_, where for
each gene in the dataset, the most important feature are a selected from a trained
regression model and emitted as candidate regulators for the target gene. All
putative regulatory links are compiled into one dataset, representing the inferred
regulatory network.

In GENIE3_,  `Random Forest`_ regression models are trained.


GENIE3
------

We consider GENIE3_ as the blueprint of "multiple regression GRN inference"
strategy. 


DREAM5 benchmark
----------------
