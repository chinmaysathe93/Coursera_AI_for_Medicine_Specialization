
# coding: utf-8

# ## AI for Medicine Course 1 Week 1 lecture exercises

# # Patient Overlap and Data Leakage
# 
# Patient overlap in medical data is a part of a more general problem in machine learning called **data leakage**.  To identify patient overlap in this week's graded assignment, you'll check to see if a patient's ID appears in both the training set and the test set. You should also verify that you don't have patient overlap in the training and validation sets, which is what you'll do here.
# 
# Below is a simple example showing how you can check for and remove patient overlap in your training and validations sets.

# In[13]:


# Import necessary packages
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
import os
import seaborn as sns
sns.set()


# ### Read in the data from a csv file
# 
# First, you'll read in your training and validation datasets from csv files. Run the next two cells to read these csvs into `pandas` dataframes.

# In[14]:


# Read csv file containing training data
train_df = pd.read_csv("nih/train-small.csv")
# Print first 5 rows
print(f'There are {train_df.shape[0]} rows and {train_df.shape[1]} columns in the training dataframe')
train_df.head()


# In[15]:


# Read csv file containing validation data
valid_df = pd.read_csv("nih/valid-small.csv")
# Print first 5 rows
print(f'There are {valid_df.shape[0]} rows and {valid_df.shape[1]} columns in the validation dataframe')
valid_df.head()


# ### Extract and compare the PatientId columns from the train and validation sets
# By running the next four cells you will do the following:
# 1. Extract patient IDs from the train and validation sets
# 2. Convert these arrays of numbers into `set()` datatypes for easy comparison
# 3. Identify patient overlap in the intersection of the two sets

# In[16]:


# Extract patient id's for the training set
ids_train = train_df.PatientId.values
# Extract patient id's for the validation set
ids_valid = valid_df.PatientId.values


# In[17]:


# Create a "set" datastructure of the training set id's to identify unique id's
ids_train_set = set(ids_train)
print(f'There are {len(ids_train_set)} unique Patient IDs in the training set')
# Create a "set" datastructure of the validation set id's to identify unique id's
ids_valid_set = set(ids_valid)
print(f'There are {len(ids_valid_set)} unique Patient IDs in the validation set')


# In[18]:


# Identify patient overlap by looking at the intersection between the sets
patient_overlap = list(ids_train_set.intersection(ids_valid_set))
n_overlap = len(patient_overlap)
print(f'There are {n_overlap} Patient IDs in both the training and validation sets')
print('')
print(f'These patients are in both the training and validation datasets:')
print(f'{patient_overlap}')


# ### Identify rows (indices) of overlapping patients and remove from either the train or validation set
# Run the next two cells to do the following:
# 1. Create lists of the overlapping row numbers in both the training and validation sets. 
# 2. Drop the overlapping patient records from the validation set (could also choose to drop from train set)

# In[19]:


train_overlap_idxs = []
valid_overlap_idxs = []
for idx in range(n_overlap):
    train_overlap_idxs.extend(train_df.index[train_df['PatientId'] == patient_overlap[idx]].tolist())
    valid_overlap_idxs.extend(valid_df.index[valid_df['PatientId'] == patient_overlap[idx]].tolist())
    
print(f'These are the indices of overlapping patients in the training set: ')
print(f'{train_overlap_idxs}')
print(f'These are the indices of overlapping patients in the validation set: ')
print(f'{valid_overlap_idxs}')


# In[20]:


# Drop the overlapping rows from the validation set
valid_df.drop(valid_overlap_idxs, inplace=True)


# ### Check that everything worked as planned by rerunning the patient ID comparison between train and validation sets.
# 
# When you run the next two cells you should see that there are now fewer records in the validation set and that the overlap problem has been removed!

# In[21]:


# Extract patient id's for the validation set
ids_valid = valid_df.PatientId.values
# Create a "set" datastructure of the validation set id's to identify unique id's
ids_valid_set = set(ids_valid)
print(f'There are {len(ids_valid_set)} unique Patient IDs in the validation set')


# In[22]:


# Identify patient overlap by looking at the intersection between the sets
patient_overlap = list(ids_train_set.intersection(ids_valid_set))
n_overlap = len(patient_overlap)
print(f'There are {n_overlap} Patient IDs in both the training and validation sets')


# ### Congratulations! You removed overlapping patients from the validation set! 
# 
# You could have just as well removed them from the training set. 
# 
# Always be sure to check for patient overlap in your train, validation and test sets.
