'''
Esse modulo contem as ferramentas necessarias para uma anaise
a cerca dos imcs dos alistados.
'''

from typing import List
import pandas as pd
import os


def read_local_data(path: str, dropnull: bool = False,cols: List[str] = None):
    '''
    Lê um arquivo csv e cria um DataFrame.

    Parameters
    ----------
    path : str
        O caminho do arquivo csv que será lido.
        
    cols : list
        Lista com as colunas desejadas.
    
    dropnull : bool
        Se True, dpropa as linhas nulas, se False, não dropa.

    Returns
    -------
    cleandf : pandas.DataFrame
        Retorna um DataFrame que pode ser utilizado para a análise de algo.

    '''
    try:
        if os.path.exists(path):
            if cols is None:
                df = pd.read_csv(path)
            else:
                df = pd.read_csv(path,usecols=cols)
            if dropnull is True:
                cleandf = df.dropna()
            if dropnull is False:
                cleandf = df
        else:
            raise NameError("O nome do arquivo passado está incorreto.")
    except NameError as erro:
        print(erro)
        return None
    except Exception as e:
        print("Ocorreu um erro, e não é o nome do arquivo. O erro é: ",str(e))       
    else:
        return cleandf


#Importante: Essa função serve apenas para guardar os dataframes em uma lista para facilitar a maniupalção.
def save_data_in_list(dropna: bool = False,cols: List[str] = None):
    '''
    Lê arquivos CSV dos anos de 2007 a 2022 e armazena os DataFrames em uma lista.
    Note que essa funcao apenas serve se o nome dos csvs forem compativeis com o formato
    'sermil{ano}.csv' e todos eles estiverem baixados no repositorio.

    Parameters
    -------
    cols : list
        Lista com as colunas desejadas dos datasets que serão salvos em uma lista.
    
    dropna : bool
        Se True dropa as linhas nulas dos datasets da lista, se False, não dropa. 

    Returns
    -------
    dataframes : list
        Uma lista que contém os DataFrames correspondentes a cada ano.
        Para acessar o DataFrame gerado com os dados do 'sermil2007.csv',
        você pode usar dataframes[0], para 'sermil2008.csv', use dataframes[1],
        e assim por diante.
    '''
    # Lista para armazenar os DataFrames
    dataframes = []
    try:
        # Loop para ler os arquivos CSV e armazenar os DataFrames
        if cols is None:
            for ano in range(2007, 2023):
                arquivo_csv = f'sermil{ano}.csv'
                if dropna is False:
                    df = read_local_data(arquivo_csv)
                    if df is not None:
                        dataframes.append(df)
                if dropna is True:
                    df = read_local_data(arquivo_csv, dropnull=True)
                    if df is not None:
                        dataframes.append(df)                
        else:
            for ano in range(2007, 2023):
                arquivo_csv = f'sermil{ano}.csv'
                df = read_local_data(arquivo_csv, cols=cols)
            
                if df is not None:
                    dataframes.append(df)
    except Exception as e:
        print("O erro é:",str(e))
        return None
    else:
        return dataframes


def df_allyears(data_list: list):
    '''
    Concatena os DataFrames de todos os anos.
    
    Parameters
    ----------
    data_list : list
        Lista com os dataframes.

    Returns
    -------
    df_concatenado : pandas.DataFrame
        DataFrame com dados de todos os anos sobre alistamento militar no Brasil.
    
    Example
    -------
    Exemplo em que concatena dois dataframes com colunas com nomes iguais.
    
    >>> import pandas as pd
    >>> data_list = [pd.DataFrame({'Ano': [2007, 2008], 'Valor': [10, 20]}),
    ...              pd.DataFrame({'Ano': [2009, 2010], 'Valor': [30, 40]})]
    >>> df_allyears(data_list)
       Ano  Valor
    0  2007     10
    1  2008     20
    2  2009     30
    3  2010     40
    '''
    try:        
        colnames = None    
        for df in data_list:
            if colnames is None:
                colnames = df.columns
            
            # Verifica se os nomes das colunas são iguais em todos os DataFrames
            if not (df.columns == colnames).all():
                raise ValueError("Os nomes das colunas dos datasets devem ser iguais.")
        if len(data_list) <= 1:
            raise ValueError("A lista de dataframes precisa de no mínimo dois dataframes.")
    except ValueError as erro:
        print(erro)
        return None
    except Exception as erro:
        print("O erro foi :", str(erro))
        return None
    else:
        df_concatenado = pd.concat(data_list, ignore_index=True)
    return df_concatenado






if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True)