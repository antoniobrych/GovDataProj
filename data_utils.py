"""

Module containing the main functions
used by my analysis in the project

"""

import pandas as pd
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt
import seaborn as sns
import datetime as dt
import os
import doctest

def concatenate_last_n_csv_files(folder:str, destination_folder:str,n:int=10)->pd.DataFrame:
    """
    Função que concatena os n últimos arquivos csv em uma pasta,
    onde n é um número inteiro escolhido pelo usuário,
    se n for um número maior que o de registros disponíveis,
    a função concatena todos os arquivos. 

    Parameters
    ----------
    folder : str
        Diretório da pasta que contém todos os arquivos CSV.

    destination_folder : str
        Diretório da pasta destino dos arquivos concatenados.

    n : int , optional
        n últimos arquivos a serem concatenados, por default n = 10.

    Returns
    -------
    pd.DataFrame
        Único DataFrame Pandas com todos os registros dos arquivos.

    Example
    -------
    >>> result = concatenate_last_n_csv_files('data', 'data_concat',10)
    >>> result.shape[0] > 0
    True
    """
    # Get a list of all files in the folder

    all_files = os.listdir(folder)
    
    # Filter files to only get CSV files and sort them by modification date
    csv_files = [f for f in all_files if f.endswith('.csv')]
    sorted_filenames = sorted(csv_files, key=lambda x: int(x[6:10]))
    
    # Get the last n csv fiLes
    last_n_csv_files = sorted_filenames[n:]
    
    # Initialize empty DataFrame to store concat data
    concatenated_data = pd.DataFrame()
    # Concatenate the CSV files, based on Date
    counter = 0
    for csv_file in last_n_csv_files:
        file_path = os.path.join(folder, csv_file)
        data = pd.read_csv(file_path, encoding='latin1',low_memory=False)
        data['ANO_COLETA'] = int(last_n_csv_files[counter][6:10])
        concatenated_data = pd.concat([concatenated_data, data], ignore_index=True)
        counter += 1
    concatenated_data = concatenated_data.dropna(axis='index')
    concatenated_data.to_csv(os.path.join(destination_folder, 'SERMIL_5_ANOS.csv'),index=False)
    return concatenated_data

def integrity_check(folder:str,begin:int=2012,end:int=2022):
    """
    Função que verifica se todos os arquivos csv de múltiplos
    anos (onde no título ex.: 'sermil2023' do arquivo está escrito o ano), estão
    devidamente presentes. 

    Importante: Esta função funciona somente para arquivos cujo 
    título é do tipo 'sermilYYYY'.

    Parameters
    ----------
    folder : str
        Diretório da pasta que contém todos os arquivos CSV.

    begin : int, optional
        Data de arquivo mais antigo que deveria estar presente na pasta

    end : str , optional
        Data de arquivo mais recente que deveria estar presente na pasta

    Returns
    -------
    bool
        Verdadeiro ou Falso, sucesso do teste de integridade.

    Example
    -------
    >>> integrity_result = integrity_check(folder='data',begin=1999,end=2023)
    >>> integrity_result == False
    True
    >>> integrity_result = integrity_check(folder='data',begin=1882,end=2023)
    >>> integrity_result == False
    True
    >>> integrity_result = integrity_check(folder='data',begin=-12,end=2023)
    >>> integrity_result == False
    True
    >>> integrity_result = integrity_check(folder='data',begin=2010,end=2023)
    >>> integrity_result == False
    True
    """
    # Correct typing mistake
    # Such as, writing begin data as end data.
    if (begin > end):
        end = begin

    # Get a list of all files in the folder
    # important, to counter negative dates,(typing mistake)
    # begin and end are defined as an absolute value
    all_files = os.listdir(folder)
    begin = abs(int(begin))
    end = abs(int(end))
    # Filter files to only get CSV files and sort them by modification date
    # The earlier the date, the first are the positions at the list.
    csv_files = [f for f in all_files if f.endswith('.csv')]
    sorted_filenames_all = sorted(csv_files, key=lambda x: int(x[6:10]))
    sorted_filenames_all[0]
    sorted_filenames = sorted_filenames_all[-(end-begin)-1:]
    # If user wrote an interval that does not exist,
    # Integrity check fails, Function returns False
    if (end-begin)>len(sorted_filenames):
        return False
    # Counter that updates checked files
    for file_name in sorted_filenames:
        if int(file_name[6:10])==begin:
            sorted_filenames = sorted_filenames.remove(file_name)
        begin += 1
    # begin == end, implies that no file is missing, all years were verified.
    if  begin == end:
        return True
    return False
# Run tests with doctest
if __name__ == "__main__":
    doctest.testmod(verbose=True)
