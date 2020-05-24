import os
from shutil import rmtree
import tempfile
from bwas_wrapper.BWAS import BWAS_cpu
from nilearn.input_data import NiftiMasker

def wrapper(
    model,
    files,
    result_dir,
    subject_id,
    interest,
    delete_tmp=False,
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
    :parameter result_dir: where to save the results of the analysis.
    :type output_folder: string.
    :parameter subject_id: the name of the column in model containing subject IDs
    :type subject_id: string
    :parameter interest: the name of the column of interest in model.
    This would be for example a dummy variable with 0s and 1s for a group
    comparison. The other columns will be used as confonds in the analysis.
    :type interest: string
    :parameter ncore: Number of CPU to use for this analysis.
    :type ncore: int, optional
    :parameter memory_limit_per_core: The maximum memory limits per CPU (GB)
    :type memory_limit_per_core: int, optional
    :parameter CDT: Cluster defining threshold (z-value), better >= 4.5 for whole brain analysis.
    :type CDT: float, optional
    :parameter delete_tmp: turn on/off the deletion of the temporary folder for the analysis
    :type delete_tmp: boolean, optional

    :return path_analysis: the temporary folder used to run the analysis. This
        folder may be automatically deleted on exit (see ``delete_tmp``).
    :type path_analysis: string.
    Note
    ----
    The files need to point to *fully preprocessed* 4D nifti files. No detrending or smoothing can be applied.

    The analysis mask is automatically generated using nilearn.
    User-specified mask is not currently supported.
    """
    # Create temporary file name structure with sym links
    # BWAS uses the alphabetical order in files to make a match with the model variables
    # This is a risky strategy: any discrepancy between the model row order and
    # files will result in a catastrophic (silent) failure.
    # To address this issue, bwas_wrapper uses a python dictionary to list files
    # and creates a collection of symlinks that matches the model order just for
    # the analysis
    path_analysis = tempfile.mkdtemp()
    print("Creating sym links in the following temporary folder: {0}".format(path_analysis))
    imgs = []
    for idx, subject in enumerate(model[subject_id]):
        file = f"{idx: 12}.nii.gz".replace(" ", "0")
        imgs.append(os.path.join(path_analysis, file))
        print("linking {0} with {1}".format(files[subject], imgs[-1]))
        os.symlink(src=files[subject], dst=imgs[-1])

    # Create the output folder if it does not exist
    if not os.path.exists(result_dir):
        os.makedirs(result_dir)
        print(f"Result directory {result_dir} created.")
    else:
        print(f"Storing results in {result_dir} (already exists).")

    # Create a mask, if not specified
    mask_file = os.path.join(path_analysis, 'mask.nii.gz')
    print(f"Generating a brain mask for the analysis in {mask_file}")
    masker = NiftiMasker()
    masker.fit(imgs)
    mask = masker.mask_img_
    mask.to_filename(mask_file)

    # dump the target in a numpy file
    targets_file = os.path.join(path_analysis, 'targets.npy')
    np.save(targets_file, model[interest].to_numpy())

    # dump the covariates in a numpy file
    cov_file = os.path.join(path_analysis, 'covariates.npy')
    labels = models.columns
    cov = labels[[item not in [interest, subject_id] for item in labels]]
    np.save(cov_file, model[cov].to_numpy())

    # dump the
    # Run BWAS
    print("Running BWAS")
    BWAS_cpu.BWAS_run_full_analysis(
        result_dir=result_dir,
        image_dir=path_analysis,
        mask_file=mask_file,
        toolbox_path=os.path.dirname(BWAS_cpu.__file__),
        targets_file=targets_file,
        cov_file=cov_file,
        CDT=CDT,
        memory_limit_per_core=memory_limit_per_core,
        ncore=ncore,
    )

    if delete_tmp:
        rmtree(path_analysis)

    return path_analysis
