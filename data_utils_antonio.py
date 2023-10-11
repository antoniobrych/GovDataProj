"""
Module containing the main functions
used by me in the project
"""

import pandas as pd
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt
import seaborn as sns
import datetime as dt
import os
import doctest
import glob

def concatenate_last_10_csv_files(folder, destination_folder):
    """
    Parameters
    ----------
    folder : str
        Diretório da pasta que contém todos os arquivos CSV.

    destination_folder : str
        Diretório da pasta destino dos arquivos concatenados.

    Returns
    -------
    pd.DataFrame
        Único DataFrame Pandas com todos os registros dos arquivos.

    Example
    -------
    >>> result = concatenate_last_10_csv_files('data', 'data_concat')
    >>> result.shape[0] > 0
    True
    """
    # Get a list of all files in the folder
    all_files = os.listdir(folder)
    
    # Filter files to only get CSV files and sort them by modification date
    csv_files = [f for f in all_files if f.endswith('.csv')]
    sorted_filenames = sorted(csv_files, key=lambda x: int(x[6:10]))
    
    # Get the last 5 CSV files
    last_10_csv_files = sorted_filenames[5:]
    
    # Initialize an empty DataFrame to store the concatenated data
    concatenated_data = pd.DataFrame()
    # Concatenate the CSV files
    counter = 0
    for csv_file in last_10_csv_files:
        file_path = os.path.join(folder, csv_file)
        data = pd.read_csv(file_path, encoding='latin1')
        data['COLLECTION_YEAR'] = int(last_10_csv_files[counter][6:10])
        concatenated_data = pd.concat([concatenated_data, data], ignore_index=True)
        counter += 1

    concatenated_data.to_csv(os.path.join(destination_folder, 'SERMIL_5_ANOS.csv'))
    return concatenated_data

# Run tests with doctest
if __name__ == "__main__":
    doctest.testmod()
