Concept and Background
======================

Arboreto was conceived to address the need for a faster alternative for the
classic GENIE3 implementation for inferring gene regulatory networks from high-throughput
gene expression profiles.

.. (To understand arboreto, it is useful to understand GENIE3's strategy for inferring
    gene regulatory networks.
    ... here we go again...)

In summary, GENIE3 performs a number of independent learning tasks. This inference
"architecture" suggests two approaches for speeding up the algorithm:

#. Speeding up the individual learning tasks.
#. Specifying the task coordination logic so that the tasks can be executed in parallel on distributed hardware.
