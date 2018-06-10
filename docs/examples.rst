
.. _`python script`: https://github.com/tmoerman/arboreto/blob/master/resources/dream5/net1/run_grnboost2.py
.. _`Example 01 - GRNBoost2 local`: https://nbviewer.jupyter.org/github/tmoerman/arboreto/blob/master/notebooks/examples/ex_01_grnboost2_local.ipynb
.. _`Example 02 - GRNBoost2 with custom Dask Client`: https://nbviewer.jupyter.org/github/tmoerman/arboreto/blob/master/notebooks/examples/ex_02_grnboost2_custom_client.ipynb
.. _`Example 03 - GRNBoost2 with transposed input file`: https://nbviewer.jupyter.org/github/tmoerman/arboreto/blob/master/notebooks/examples/ex_03_grnboost2_transposed_input_file.ipynb
.. _`Jupyter nbviewer`: https://nbviewer.jupyter.org/
.. _pandas: https://pandas.pydata.org/
.. _DataFrame: http://pandas.pydata.org/pandas-docs/stable/dsintro.html#dataframe

Examples
========

Python script
-------------

* Example `python script`_ running GRNBoost2 on files located in the same folder.

    .. code-block:: python
        :caption: *<arboreto repo>/resources/dream5/net1/run_grnboost2.py*

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


    Run as a classic python script:

    .. code-block:: bash

        cd <arboreto repo>/resources/dream5/net1
        python run_grnboost2


Jupyter notebooks
-----------------

Following are links to example Jupyter notebooks that illustrate different
Arboreto usage scenarios (links render notebooks in `Jupyter nbviewer`_).

* `Example 01 - GRNBoost2 local`_

    A basic usage scenario where we infer the gene regulatory network from a single dataset on the local machine.

* `Example 02 - GRNBoost2 with custom Dask Client`_

    A slightly more advanced scenario where we infer the gene regulatory network from a single dataset, using a custom Dask client.

* `Example 03 - GRNBoost2 with transposed input file`_

    Illustrates how to easily prepare the input data using a Pandas_ DataFrame_, in case the input file happens to be transposed with respect to the Arboreto input conventions.
