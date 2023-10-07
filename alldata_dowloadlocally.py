'''
Esse módulo tem o objetivo de baixar os datasets contidos no dados.gov de todos os anos 
sobre alistamento militar, de modo personalizado para cada análise de cada integrante.
(demora um tempo considerável até baixar todos) 
'''

from onedata_downloadlocally import download_csv_local
import os
from typing import List

def download_alldata(desired_columns: List[str]): 
    '''
    A função baixa os dados dos anos 2007 a 2022 do 
    alistamento militar disponíveis no site dados.gov.
    Percebe-se que a função só baixa as colunas desejadas, 
    as quais devem ser especificadas.

    Parameters
    ----------
    desired_columns : List[str]
        As colunas que serão necessárias para a análise de cada integrante.

    Returns
    -------
    None, ela apenas baixa os csvs sobre alistamento militar para o repositório local.

    '''
    try:
        for i in range(2007,2023):
            if os.path.exists(f'sermil{i}.csv'):
                raise Exception
    
    except:
        print("Os dados já estão baixados devidamente no seu local de trabalho.")
        pass
    
    else:
        for i in range(2007,2023):        
                url_repositorio = f'https://dadosabertos.eb.mil.br/arquivos/sermil/sermil{i}.csv'
                download_csv_local(url_repositorio,local_file=f'sermil{i}.csv',dropna=True,columns=desired_columns)