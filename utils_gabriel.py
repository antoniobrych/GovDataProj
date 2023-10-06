'''
Esse módulo contém as ferramentas necessárias para uma análise
a cerca dos imcs dos alistados.
'''

from typing import List
import pandas as pd
import os


def read_local_data(path: str):
    '''
    Lê um arquivo csv e cria um DataFrame.

    Parameters
    ----------
    path : str
        O caminho do arquivo csv que será lido.

    Returns
    -------
    df : pandas.DataFrame
        Retorna um DataFrame que pode ser utilizado para a análise de algo.

    '''
    try:
        if os.path.exists(path):
            df = pd.read_csv(path)
        else:
            raise NameError("O nome do arquivo passado está incorreto.")
    except NameError as erro:
        print(erro)
        return None
    except Exception as e:
        print("Ocorreu um erro, e não é o nome do arquivo. O erro é: ",str(e))       
    else:
        return df


#Importane: Essa função serve apenas para guardar os dataframes em uma lista para facilitar a maniupalção.
def save_data_in_list():
    '''
    Lê arquivos CSV de anos de 2007 a 2022 e armazena os DataFrames em uma lista.

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
    
    # Loop para ler os arquivos CSV e armazenar os DataFrames
    for ano in range(2007, 2023):
        arquivo_csv = f'sermil{ano}.csv'
        df = read_local_data(arquivo_csv)
        
        if df is not None:
            dataframes.append(df)
    return dataframes


def df_allyears(data_list: List[str]):
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


def cria_imc(df, height_colname: str, weight_colname: str):
    '''
    Cria a coluna imc para uma tabela

    Parameters
    ----------
    df : pandas.DataFrame
        Tabela que tenha colunas de altura e peso.
    
    height_colname : str
        Nome da coluna do antigo DataFrame que representa a altura.
    
    weight_colname : str
        Nome da coluna do antigo DataFrame que representa o peso.

    Returns
    -------
    df : pandas.DataFrame or None
        Retorna uma tabela que contenha a coluna IMC. Retorna None
        se alguma das exeções forem encontradas.
        
    Example
    -------
    >>> import pandas as pd
    >>> dados = {'Altura(cm)': [160, 175, 150, 180],
    ...          'Peso(kg)': [65, 80, 55, 90]}
    >>> df = pd.DataFrame(dados)
    >>> df = cria_imc(df, 'Altura(cm)', 'Peso(kg)')
    >>> df
       Peso(kg)  ALTURA(m)        IMC
    0        65       1.60  25.390625
    1        80       1.75  26.122449
    2        55       1.50  24.444444
    3        90       1.80  27.777778
    '''
    try:
        for valor in df[height_colname]:
            assert isinstance(valor, (int, float)), f"Erro, elementos da coluna {height_colname} não são números."
            assert valor != 0, "Erro, altura não pode ser zero."
            assert valor > 0, "Erro, altura deve ser maior que zero."
        for valor in df[weight_colname]:
            assert isinstance(valor, (int, float)), f"Erro, elementos da {weight_colname} não são números."
            assert valor != 0, "Erro, peso não pode ser zero."
            assert valor > 0, "Erro, peso deve ser maior que zero."
    except AssertionError as erro:
        print(erro)
        return None
    except Exception as e:
        print("Ocorreu um erro. O erro é: ",str(e))
    else:
        df['ALTURA(m)'] = df[height_colname]/100
        df['IMC'] = df[weight_colname]/(df['ALTURA(m)'])**2
        df = df.drop(height_colname,axis=1)
    return df

if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True)