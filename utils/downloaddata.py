'''
Esse modulo tem o objetivo de baixar csvs localmente.
Para isso foi criada uma funcao que baixa um unico arquivo csv.
E outra que baixa todos os csvs necessarios para anlise. 
'''

import os
from .cleandata import process_data,make_http_request
from typing import List

def download_csv_local(url: str,dropna:bool = False, local_file:str = None ,columns: List[str] = None):
    '''
    Serve para baixar o CSV localmente de uma URL.
    Permite que voce baixe colunas selecionadas, ou
    seja, nao baixe todo o csv. Utiliza funcoes criadas
    no modulo cleandata.

    Parameters
    ----------
    url : str
        A URL que aponta para o conjunto de dados a ser lido.
    
    dropna : bool
        Argumento para tirar ou nao linhas com valores nulos.
    
    local_file : str, optional
        Nome do arquivo onde sera salvo o csv. Por padrão o nome sera
        'dados.csv'.
    
    columns : list, optional
        Lista com os nomes das colunas desejadas, se nao especificado, todas as colunas serao lidas.
    
    Returns
    -------
    None
        Esta funcao baixa o CSV para o seu diretorio local.
    '''
    try:
        # Chama a função que faz uma solicitação HTTP na URL e retorna o CSV em formato de texto
        textcsv = make_http_request(url)

        if textcsv is not None:
            # Cria um DataFrame com o CSV em formato de texto
            df = process_data(textcsv, dropna,columns)
            
            if df is not None:
                if local_file is not None:
                    # Salva o DataFrame no diretório local como a string passada pra local_file
                    df.to_csv(local_file, index=False)
                    print("CSV baixado e salvo localmente com sucesso.")
                else:
                    # Salva o DataFrame no diretório local como dados.csv
                    df.to_csv("dados.csv", index=False)
                    print("CSV baixado e salvo localmente com sucesso e com o nome default.")
            else:
                print("Falha ao processar os dados CSV, apos ter feito o acesso a url.")
        else:
            print("Falha ao obter o CSV da URL.")
    except Exception as e:
        print("Ocorreu um erro durante o processo:", str(e))
        
def download_alldata(desired_columns: List[str]):
    '''
    Apenas baixa todos os csvs dos anos dispniveis no ambiente local.
    Note que essa funcao so funciona pro caso especifico do tema do trabalho.

    Parameters
    ----------
    desired_columns : List[str]
        Lista com as colunas que o usuario deseja baixar.

    Returns
    -------
    None.

    '''
    for i in range(2007, 2023):
        if not os.path.exists(f'sermil{i}.csv'):
            url_repositorio = f'https://dadosabertos.eb.mil.br/arquivos/sermil/sermil{i}.csv'
            download_csv_local(url_repositorio, local_file=f'sermil{i}.csv', dropna=True, columns=desired_columns)
        else:
            print(f'O arquivo sermil{i}.csv ja existe no seu local de trabalho.')