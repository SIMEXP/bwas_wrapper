#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os 
import pandas as pd
from nilearn import datasets, plotting
from bwas_wrapper.wrapper import wrapper


# In[2]:


from bwas_wrapper.BWAS import BWAS_cpu


# In[3]:


os.path.dirname(BWAS_cpu.__file__)


# Let's start by downloading a few subjects from the ADHD200 dataset.

# In[4]:


n_subjects = 30
adhd_dataset = datasets.fetch_adhd(n_subjects)
epi_filename = adhd_dataset.func
# Also load a probabilistic grey matter segmentation
mni = datasets.fetch_icbm152_2009()


# Let's load the phenotypic information in a pandas DataFrame and check what variables there are:

# In[5]:


data = pd.DataFrame(adhd_dataset.phenotypic)
data.columns


# We need to select the variables to include in our analyis, and also have a column with the subject IDs:

# In[6]:


model = data[['Subject', 'adhd', 'MeanFD', 'age']]


# let's add sex as well, but this variable is categorical. We need to convert it into a dummy variable first.

# In[7]:


sex = pd.get_dummies(data['sex'], prefix='sex', drop_first=True) # drop_first is applied because the model will include an intercept
model = pd.concat([model, sex], axis=1)


# we can select subjects too. For example, let's filter subjects with excessive motion.

# In[8]:


model = model[model['MeanFD']<0.1]


# Let's add an intercept to the regression model:

# In[9]:


model.insert(0, column='Intercept', value=1)


# Finally, we need to add a dictionary with the file of the preprocessed data for each subject. The IDs of the subject need to correspond to the subject IDs in the data frame. 

# In[10]:


# By checking `adhd_dataset.func`, we can easily pick up the naming patterns of the functional files
# '/home/pbellec/nilearn_data/adhd/data/0010042/0010042_rest_tshift_RPI_voreg_mni.nii.gz'
path_data = os.path.join( os.getenv('HOME'), 'nilearn_data', 'adhd', 'data')
files = {}
for subject in model['Subject']:
    subject_prefix = f'{subject :7}'.replace(' ','0') 
    file = f'{subject_prefix}_rest_tshift_RPI_voreg_mni.nii.gz'
    files[subject] = os.path.join(path_data, f'{subject_prefix}', file)
files


# In[11]:


result_dir = os.path.join(os.getenv('HOME'), 'test_bwas_adhd')
wrapper(model, files, result_dir=result_dir, subject_id="Subject", interest="adhd", ncore=2)


# In[ ]:


model\''


# In[ ]:


plotting.view_img('/tmp/tmpx9iwgjyg/mask.nii.gz')

