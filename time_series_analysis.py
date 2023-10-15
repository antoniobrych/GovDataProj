"""
Analysis: Change of SERMIL statistics over time.

"""

from analysis_utils import *
from data_utils import *

# Aattemp to read the concatenated file
df = concatenate_last_n_csv_files('data','data_concat')
print('Destiny Folder not Defined.')
print(yearly_mean(df).info())
print(yearly_mean(df).describe())
print(yearly_aggregate(df))
