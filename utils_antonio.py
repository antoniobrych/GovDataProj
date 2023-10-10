"""

Módulo que contém as principais funções

utilizadas por mim no projeto

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
def concatenar_ultimos_10_arquivos_csv(pasta,pasta_destino):
    """
    Concatena os últimos 5 arquivos CSV na pasta especificada e retorna o DataFrame resultante.

    Args:
    pasta (str): O caminho para a pasta contendo os arquivos CSV.
    pasta_destino (str): Destino para os arquivos CSV concatenados

    Returns:
    pd.DataFrame: Um DataFrame contendo os dados concatenados dos últimos 5 arquivos CSV.
    
    Exemplo:
    >>> resultado = concatenar_ultimos_10_arquivos_csv('data','data_concat')
    >>> resultado.shape[0] > 0
    True
    """
    # Obtém uma lista de todos os arquivos na pasta
    todos_os_arquivos = os.listdir(pasta)
    
    # Filtra os arquivos para pegar apenas os CSV e os ordena por data de modificação
    arquivos_csv = [f for f in todos_os_arquivos if f.endswith('.csv')]
    sorted_filenames = sorted(arquivos_csv, key=lambda x: int(x[6:10]))
    # Pega os últimos 5 arquivos CSV
    ultimos_10_arquivos_csv = sorted_filenames[5:]
    
    # Inicializa um DataFrame vazio para armazenar os dados concatenados
    dados_concatenados = pd.DataFrame()
    # Concatena os arquivos CSV
    counter = 0
    for arquivo_csv in ultimos_10_arquivos_csv:
        caminho_arquivo = os.path.join(pasta, arquivo_csv)
        dados = pd.read_csv(caminho_arquivo,encoding='latin1')
        dados['ANO_COLETA'] = int(ultimos_10_arquivos_csv[counter][6:10])
        dados_concatenados = pd.concat([dados_concatenados, dados], ignore_index=True)
        counter +=1

    dados_concatenados.to_csv(os.path.join(pasta_destino,'SERMIL_5_ANOS.csv'))
    return dados_concatenados

# Executa os testes com doctest
if __name__ == "__main__":
    resultado = concatenar_ultimos_10_arquivos_csv('data','data_concat')
    print(resultado.head())
    doctest.testmod()
