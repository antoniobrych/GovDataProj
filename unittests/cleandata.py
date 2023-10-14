'''
Este modulo Python fornece funcoes para realizar solicitacoes HTTP 
para obter dados de uma URL e processar dados CSV. Ele pode ser usado 
para recuperar dados de uma fonte remota e prepara los para analise posterior.
Tambem pode auxiliar na limpeza de um dataset.
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
    data : str
        Os dados CSV como uma string.
    
    dropnull : bool, False by default
        O dropnull permite que tire as linhas com valores nulos da tabela. Por padrão ele é False 
        e nao tira as linhas com valores nulos, mas se for True ele tira as linhas com valores nulos.
    
    desired_columns : list, optional
        Lista com os nomes das colunas desejadas, se nao especificado, todas as colunas serao lidas.
    
    Returns
    -------
    pandas.DataFrame or None
        Um DataFrame do pandas contendo os dados processados se a operacao for bem-sucedida.
        None, se ocorrer uma falha no processamento.
    
    Raises
    ------
    TypeError
        Se o tipo de elementos da lista passada para o parâmetro desired_columns for diferente de str.
    
    Example
    -------
    Exemplo de processamento de dados com colunas inválidas:
    
    >>> dados_teste = '''
    ... Nome,Idade,Sexo
    ... João,30,M
    ... Maria,25,F
    ... Carlos,35,M
    ... Ana,28,F
    ... '''
    >>> colunas_invalidas = ['Nome', 1, 'Idade']
    >>> process_data(dados_teste, desired_columns=colunas_invalidas)
    Erro: Todos os elementos da lista de colunas devem ser strings.
    
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
            # Não permite que o nome das colunas sejam diferentes de strings
            for el in desired_columns:
                if not isinstance(el, str):
                    raise TypeError("Todos os elementos da lista de colunas devem ser strings.")
        else:
            desired_columns = None
        dados = pd.read_csv(io.StringIO(data), usecols=desired_columns, error_bad_lines=False)
        if dropnull:
            cleandados = dados.dropna()
        else:
            cleandados = dados 
        return cleandados
    except TypeError as e:
        print("Erro:", e)
    except Exception as erro:
        print("Ocorreu um erro no processamento dos dados:", str(erro))
        return None


def clean_dataframe(
    df,                
    columns_to_drop: list = None,    
    columns_to_rename: dict = None,  
    numeric_columns: list = None,    
    drop_na: bool = False           
):
    '''
    Faz uma limpeza geral em um dataframe.

    Parameters
    ----------
    df : pandas.DataFrame
        O DataFrame a ser limpo.
    
    columns_to_drop : list, optional
        Lista de colunas a serem removidas. The default is None.
    
    columns_to_rename : dict, optional
        Dicionário de mapeamento de colunas. Chave é o nome da coluna antiga, 
        valor nome da coluna nova. The default is None.
    
    numeric_columns : list, optional
        Lista de colunas em que os elementos são numéricos. The default is None.
    
    drop_na : bool, False by default
        Se True, remove registros com valor NaN.

    Returns
    -------
    cleaned_df : pandas.DataFrame
        O DataFrame limpo.

    Example
    -------
    >>> df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6], 'C': [7, 8, 9]})
    >>> columns_to_drop = ['B']
    >>> columns_to_rename = {'A': 'X', 'C': 'Y'}
    >>> numeric_columns = ['X', 'Y']
    >>> cleaned_df = clean_dataframe(df, columns_to_drop, columns_to_rename, numeric_columns, drop_na=False)
    >>> 'B' in cleaned_df.columns
    False
    >>> 'A' in cleaned_df.columns
    False
    >>> 'X' in cleaned_df.columns
    True
    >>> 'C' in cleaned_df.columns
    False
    >>> 'Y' in cleaned_df.columns
    True    
    
    '''
    
    # Faz uma cópia do DataFrame para evitar alterações no DataFrame original
    cleaned_df = df.copy()

    # Remove colunas especificadas
    if columns_to_drop:
        cleaned_df = cleaned_df.drop(columns_to_drop, axis=1, errors='ignore')

    # Renomea colunas especificadas
    if columns_to_rename:
        cleaned_df = cleaned_df.rename(columns=columns_to_rename)

    # Converte colunas numéricas para tipo numérico
    if numeric_columns:
        for col in numeric_columns:
            cleaned_df[col] = pd.to_numeric(cleaned_df[col], errors='coerce')

    # Remove linhas com valores ausentes se drop_na for True
    if drop_na:
        cleaned_df = cleaned_df.dropna()

    return cleaned_df


if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True)