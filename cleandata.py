'''
Este modulo Python fornece funcoes para realizar solicitacoes HTTP 
para obter dados de uma URL e processar dados CSV. Ele pode ser usado 
para recuperar dados de uma fonte remota e prepara los para analise posterior.
'''

import io
import requests
import pandas as pd
from typing import List

def make_http_request(url: str):
    """
    Faz uma solicitacao HTTP para obter dados a partir de uma URL.
    Note que a HTTP tem que levar diretamente aos dados csv.

    Parameters
    ----------
    url : str
        A URL que aponta para o conjunto de dados a ser lido.

    Returns
    -------
    str or None
        O conteudo da resposta como texto se a solicitacao for bem sucedida.
        None, se ocorrer uma falha na solicitacao HTTP.
    """
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            print("Falha ao recuperar dados. Codigo de status:", response.status_code)
            return None
    except Exception as erro:
        print("Ocorreu um erro:", str(erro))
        return None

def process_data(data: str, dropnull: bool = False, desired_columns: List[str] = None):
    """
    Le e limpa dados CSV os transformando em pandas.DataFrame.

    Parameters
    ----------
    dados_csv : str
        Os dados CSV como uma string.
    
    dropnull : bool
        O dropnull permite que tire as linhas com valores nulos da tabela. Por padrão ele é False 
        e nao tira as linhas com valores nulos, mas se for True ele tira as linhas com valores nulos.
    
    desired_columss : list, optional
        Lista com os nomes das colunas desejadas, se nao especificado, todas as colunas serao lidas.
    
    Returns
    -------
    pandas.DataFrame or None
        Um DataFrame do pandas contendo os dados processados se a operacao for bem-sucedida.
        None, se ocorrer uma falha no processamento.
    
    Example
    -------
    Exemplo de processamento de dados com colunas invalidas:
    
    >>> # Exemplo de dados CSV como uma string
    >>> dados_teste = '''
    ... Nome,Idade,Sexo
    ... João,30,M
    ... Maria,25,F
    ... Carlos,35,M
    ... Ana,28,F
    ... '''
    >>> colunas_invalidas = ['Nome', 1, 'Idade']
    >>> process_data(dados_teste, colunas_invalidas)
    As colunas passadas não estão no formato adequado
    
    Exemplo de processamento bem-sucedido de dados:
    
    >>> dados_teste = '''
    ... Nome,Idade,Sexo
    ... João,30,M
    ... Maria,25,F
    ... Carlos,35,M
    ... Ana,28,F
    ... '''
    >>> resultado = process_data(dados_teste)
    >>> resultado.head()
         Nome  Idade Sexo
    0    João     30    M
    1   Maria     25    F
    2  Carlos     35    M
    3     Ana     28    F
    
    """
    try:
        if desired_columns is not None:
            #Não permite que o nome das colunas sejam diferentes de strings
            for el in desired_columns:
                if type(el) != str:
                    raise TypeError
            dados = pd.read_csv(io.StringIO(data), usecols=desired_columns, error_bad_lines=False)
        else:
            dados = pd.read_csv(io.StringIO(data), error_bad_lines=False)

        if dropnull is True:
            cleandados = dados.dropna()
        if dropnull is False:
            cleandados = dados
            
        return cleandados
    except TypeError:
        print("As colunas passadas não estão no formato adequado")
    except Exception as erro:
        print("Ocorreu um erro no processamento dos dados:", str(erro))
        return None

if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True)