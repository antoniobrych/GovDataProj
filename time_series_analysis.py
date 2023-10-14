"""
Analysis: Change of SERMIL statistics over time.

"""

from analysis_utils import *
from data_utils import *

# Aattemp to read the concatenated file
try:
    df = pd.read_csv("data_concat//SERMIL_5_ANOS.csv")
except FileNotFoundError:
    # If the full dataset is not there, concatenate it.
    print("Error! Full Dataset not found, concatenating all years dataset ")
    try:
        df = concatenate_last_n_csv_files('data','data_concat')
    except OSError:
        print('Destiny Folder not Defined.')
print(yearly_mean(df).info())
print(yearly_mean(df).describe())
print(yearly_aggregate(df))
