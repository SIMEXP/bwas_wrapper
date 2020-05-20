import os
import tempfile
from bwas_wrapper.BWAS import BWAS_cpu


def wrapper(
    model,
    files,
    output_folder,
    subject_id,
    interest,
    mask=None,
    ncore=1,
    memory_limit_per_core=16,
    CDT=5,
):
    """
    A wrapper for the BWAS library.

    Parameters
    ----------
    :paramater model: each column is a regressor, and each row is a subject.
    :type model: pandas data frame
    :parameter files: files[subject] is the file associated with subject
    :type files: dictionary
    :parameter output_folder: where to save the results of the analysis.
    :type output_folder: string.
    :parameter subject_id: the name of the column in model containing subject IDs
    :type subject_id: string
    :parameter interest: the name of the column of interest in model.
    This would be for example a dummy variable with 0s and 1s for a group
    comparison. The other columns will be used as confonds in the analysis.
    :type interest: string
    :parameter mask: Mask to be used on data. If an instance of masker is passed,
        then its mask will be used. If no mask is given,
        it will be computed automatically by a MultiNiftiMasker with default
        parameters.
    :type mask: Niimg-like object or MultiNiftiMasker instance, optional
    :parameter ncore: Number of CPU to use for this analysis.
    :type ncore: int, optional
    :parameter memory_limit_per_core: The maximum memory limits per CPU (GB)
    :type memory_limit_per_core: int, optional
    :parameter CDT: Cluster defining threshold (z-value), better >= 4.5 for whole brain analysis.
    :type CDT: float, optional

    Note
    ----
    The files need to point to *fully preprocessed* 4D nifti files. No detrending or smoothing can be applied.
    """
    path_analysis = tempfile.TemporaryDirectory()
    print("Creating sym links in the following path: {0}".format(path_analysis.name))
    for idx, subject in enumerate(model[subject_id]):
        file = f"{idx: 12}.nii.gz".replace(" ", "0")
        os.symlink(src=files[subject], dst=os.path.join(path_analysis.name, file))

    BWAS_run_full_analysis(
        result_dir,
        image_dir,
        mask_file,
        toolbox_path,
        targets_file,
        cov_file,
        CDT=CDT,
        memory_limit_per_core=memory_limit_per_core,
        ncore=ncore,
    )

    path_analysis.cleanup()
