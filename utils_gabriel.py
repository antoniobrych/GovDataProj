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


def cria_imc(df, height_colname: str, weight_colname: str):
    '''
    Cria a coluna imc para uma tabela. Lembrando que o IMC 
    calcula se pelo peso(kg)/altura(m)**2.
    
    Parameters
    ----------
    df : pandas.DataFrame
        Tabela que tenha colunas de altura e peso.
    
    height_colname : str
        Nome da coluna do DataFrame que representa a altura.
    
    weight_colname : str
        Nome da coluna do DataFrame que representa o peso.

    Returns
    -------
    df : pandas.DataFrame or None
        Retorna uma tabela que contenha a coluna IMC. Retorna None
        se alguma das exeções forem encontradas.
        
    Example
    -------
    Exemplo em que cria a coluna imc com sucesso.
    
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


def filtra(df, col: str, valor):
    '''
    Serve para pega uma parte do dataset que satisfaca uma condicao de igualdade.

    Parameters
    ----------
    df : pandas.DataFrame
        Dataset que vai ser filtrado.
    
    col : str
        Coluna que vai ser filtrada.
    
    valor : str,float,int
        Valor que vai filtrar.

    Returns
    -------
    filtered_df : pandas.DataFrame
        Dataset sem as linhas que nao satisfazem a condicao.
    
    Example
    -------
    Exemplo em que filtra corretamente a tabela.
    
    >>> data = {'Nome': ['Alice', 'Bob', 'Charlie', 'David'],
    ...         'Idade': [25, 30, 22, 35],
    ...         'Cidade': ['NY', 'LA', 'NY', 'SF']}
    >>> df = pd.DataFrame(data)
    >>> filtra(df, 'Cidade', 'NY')
       Nome  Idade Cidade
    0  Alice     25     NY
    2 Charlie     22     NY    
    '''
    try:
        dados_filtrados = df[df[col] == valor]
        return dados_filtrados
    except KeyError as e:
        raise KeyError(f"Coluna '{col}' não encontrada no DataFrame.") from e
    except Exception as e:
        raise e


def mean(df, col: str):
    '''
    Funcao para calcular a media de uma coluna de um pandas.DataFrame.

    Parameters
    ----------
    df : pandas.DataFrame
        Dados que contem a coluna na qual vai ser calculada a media.
    col : str
        Nome da coluna.

    Returns
    -------
    float,int
        A media aritimetica de uma coluna.
    
    Examples
    --------
    >>> import pandas as pd
    >>> data = {'Valor': [1, 2, 3, 4, 5]}
    >>> df = pd.DataFrame(data)
    >>> media = mean(df, 'Valor')
    >>> isinstance(media, (int, float))
    True
    >>> media
    3.0
    '''
    try:
        if df[col].dtype in [int,float]:
            media = df[col].mean()
        else:
            raise ValueError("Os elementos da coluna não são números.")
    except ValueError as erro:
        print(erro)
        return None
    else:        
        return media


def median(df, col: str):
    '''
    Funcao para calcular a mediana de uma coluna de um pandas.DataFrame.

    Parameters
    ----------
    df : pandas.DataFrame
        Dados que contem a coluna na qual vai ser calculada a mediana.
    col : str
        Nome da coluna.

    Returns
    -------
    float,int
        A mediana da coluna.

    Examples
    --------
    >>> import pandas as pd
    >>> data = {'Valor': [1, 2, 3, 4, 5]}
    >>> df = pd.DataFrame(data)
    >>> mediana = median(df, 'Valor')
    >>> mediana
    3.0
    '''
    try:
        if df[col].dtype in [int, float]:
            mediana = df[col].median()
        else:
            raise ValueError("Os elementos da coluna não são números.")
    except ValueError as erro:
        print(erro)
        return None
    else:
        return mediana



if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True)