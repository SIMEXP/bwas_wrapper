# BWAS wrapper

This is a wrapper for the [BWAS library](https://github.com/weikanggong/BWAS).

This is a hack, designed to make it easier to install the BWAS library and run multiple contrasts on a single dataset.
 * `requirements.txt` lists necessary libraries for the project.
 * `requirements_bwas.txt` lists necessary libraries for just BWAS.
 * `bwas_wrapper.py` contains the code to run a BWAS analysis from a pandas data frame. The frame has all necessary covariates and a list of files. Symlinks and a temporary folder will be automatically created to run the contrast.
 * `bwas_demo.ipynb` a small demo showing how to run an analysis on a public dataset.
