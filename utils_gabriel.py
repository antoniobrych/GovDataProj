'''
Esse modulo contem as ferramentas necessarias para uma analise
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
    
    Raises
    ------
    NameError
        Se o nome do arquivo passado nao existir no repositorio.
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
    
    Raises
    ------
    ValueError
        Se os nomes das colunas dos dataframes forem diferentes, ou o tamanho da 
        lista de dataframes for menor que dois.
    
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


def create_imc(df, height_colname: str, weight_colname: str):
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
    >>> df = create_imc(df, 'Altura(cm)', 'Peso(kg)')
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


def filtra_equal(df, col: str, valor):
    '''
    Serve para pegar uma parte do dataset que satisfaca uma condicao de igualdade.

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
    dados_filtrados_reset : pandas.DataFrame
        Dataset sem as linhas que nao satisfazem a condicao com os index resetados.
    
    Raises
    ------
    KeyError
        Se o nome da coluna nao estiver no dataframe.
    
    Example
    -------
    Exemplo em que filtra corretamente a tabela.
    
    >>> data = {'Nome': ['Alice', 'Bob', 'Charlie', 'David'],
    ...         'Idade': [25, 30, 22, 35],
    ...         'Cidade': ['NY', 'LA', 'NY', 'SF']}
    >>> df = pd.DataFrame(data)
    >>> filtra_equal(df, 'Cidade', 'NY')
          Nome  Idade Cidade
    0    Alice     25     NY
    1  Charlie     22     NY  
    '''
    try:
        if col not in df.columns:
            raise KeyError(f"Coluna '{col}' não encontrada no DataFrame.")
    except KeyError as erro:
        print(erro)
        return None
    except Exception as e:
        print(e)
        return None
    else:
        dados_filtrados = df[df[col] == valor]
        dados_filtrados_reset = dados_filtrados.reset_index(drop=True)
        return dados_filtrados_reset


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
    
    Raises
    ------
    ValueError
        Se o tipo dos elementos da coluna passada forem nao numericos.    
    
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
        if not pd.api.types.is_numeric_dtype(df[col]):
            raise ValueError("Os elementos da coluna não são números.")
    except ValueError as erro:
        print(erro)
        return None
    else:
        media = df[col].mean()        
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

    Raises
    ------
    ValueError
        Se o tipo dos elementos da coluna passada forem nao numericos.

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
        if not pd.api.types.is_numeric_dtype(df[col]):
            raise ValueError("Os elementos da coluna não são números.")
    except ValueError as erro:
        print(erro)
        return None
    else:
        mediana = df[col].median()
        return mediana


def categorize_series(series, bins: list, labels: list):
    '''
    Categoriza uma serie pandas com base em intervalos e rotulos personalizados.
    Usa se essa função para categorizar os intervalos de imc, de acordo com a tabela de imc.

    Parameters
    ----------
    series : pandas.Series
        Serie de valores de dados para categorizar.
    bins : list
        Lista de limites dos intervalos de categorizacao.
    labels : list
        Lista de rotulos correspondentes aos intervalos.

    Returns
    -------
    serie_categorizada : pandas.Series
        Serie de categorias atribuidas aos valores de dados.

    Raises
    ------
    ValueError
        Se o tamanho da lista de bins não for um a mais do que o tamanho da lista de labels.
        Na pratica, isso significa que deve haver o mesmo número de intervalos e de legenda para os intervalos.

    Example
    --------
    >>> import pandas as pd
    >>> dados = pd.Series([22, 27, 31, 18, 29, 24, 35, 21, 26, 28])
    >>> limites_personalizados = [0, 18.5, 24.9, 29.9, 34.9, 39.9, float('inf')]
    >>> rotulos_personalizados = ['Abaixo do peso', 'Peso normal', 'Sobrepeso', 'Obesidade Grau I', 'Obesidade Grau II', 'Obesidade Grau III']
    >>> categorias = categorize_series(dados, limites_personalizados, rotulos_personalizados)
    >>> print(categorias.value_counts())
    Sobrepeso             4
    Peso normal           3
    Abaixo do peso        1
    Obesidade Grau I      1
    Obesidade Grau II     1
    Obesidade Grau III    0
    dtype: int64
    '''    
    try:
        if len(bins)-1 != len(labels):
            raise ValueError("O número de intervalos deve ser o mesmo que o número de rótulos.")
    except ValueError as erro:
        print(erro)
        return None
    except Exception as erro:
        print(erro)
        return None
    else:
        serie_categorizada = pd.cut(series, bins = bins, labels = labels)
        return serie_categorizada


def percentage_value_counts(series):
    '''
    Mostra a porcentagem que cada valor de uma serie panda representa do total.

    Parameters
    ----------
    series : pandas.Series
        Série na qual se quer saber a porcentagem em que aparece cada valor.

    Raises
    ------
    ValueError
        Quando é passada uma série vazia.

    Returns
    -------
    finaldf : pandas.DataFrame
        Retorna um data frame com a coluna PORCENTAGEM, em que os valores sao 
        decimais que representam quantos por cento o index do data frame representa 
        do total de ocorrências da serie panda, os index  do data frame são os elementos da serie panda.
        
    Example
    -------
    >>> import pandas as pd
    >>> dados = pd.Series([1,2,2,2,3,4,4,4,5,5])
    >>> print(percentage_value_counts(dados))
       PORCENTAGEM
    2          0.3
    4          0.3
    5          0.2
    1          0.1
    3          0.1
    '''
    try:
        series_count = series.count()
        if series_count == 0:
            raise ValueError("Deve haver mais de 0 elementos na série passada.")
        else:
            if series.name is None:
                nome = 0
            else:
                nome = series.name        
    except ValueError as erro:
        print(erro)
        return None
    except Exception as erro:
        print(erro)
        return None
    else:
        categories_count = series.value_counts()
        df = pd.DataFrame(categories_count)
        df['PORCENTAGEM'] = df[nome]/series_count
        finaldf = df.drop(nome, axis = 1)
        return finaldf


def percentage_formatter(x, pos):
    """
    Formata um número como uma string de porcentagem sem casas decimais.

    Parameters
    -----------
    x : float
        O valor numérico a ser formatado como porcentagem.
    
    pos : int
        A posição no eixo em que o valor x está sendo usado.

    Returns
    --------
    str
        Uma string formatada representando o valor x como uma porcentagem inteira.

    Example
    --------
    >>> percentage_formatter(0.25, 0)
    '25%'
    >>> percentage_formatter(0.753, 1)
    '75%'
    """
    return f'{x*100:.0f}%'


if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True)