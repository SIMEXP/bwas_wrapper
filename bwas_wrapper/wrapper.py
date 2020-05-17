from bwas_wrapper.BWAS import BWAS_cpu

def wrapper(df):
    """
    A wrapper for the BWAS library.

    Parameters
    ----------
    :paramater df: a pandas data frame. Each row is a subject. The first column will be treated as the variable "of interest" in a regression model. This would be for example a dummy variable with 0s and 1s for a group comparison. The other columns will be used as confonds in the analysis. The wrapper expects to find a column called "files", with the name of a nifti file for that subject. This column will not be excluded from the analysis.

    Note
    ----
    The files need to point to *fully preprocessed* 4D nifti files. No detrending or smoothing can be applied.
    """
    a = 1
    return a
