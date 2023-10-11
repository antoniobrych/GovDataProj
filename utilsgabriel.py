'''
Esse modulo contem as ferramentas necessarias para uma analise
a cerca dos imcs dos alistados.
'''

from typing import List
import pandas as pd
import os
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import numpy as np
import downloaddata as dd


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
    ----------
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
        # Loop para ler os arquivos CSV e armazenar os DataFrames especicos do trabalho.
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


#Pasta com os arquivos para esta vis está adicionada no GitHub.
def bar_plot_imc():
    '''
    Funcao que cria a visualizacao para a analise do IMC.
    '''
    # Baixa os dados caso nao estejam baixados localmente(demora pra baixar).
    dd.download_alldata(['PESO','ALTURA','DISPENSA'])

    # Lista com os dfs de cada ano.
    dfs = save_data_in_list()

    # Data Frame que concatenou todos os anos.
    df = df_allyears(dfs)

    # Novo Data Frame com a coluna imc e a altura em metros.
    df = create_imc(df, 'ALTURA', 'PESO')

    # Dividiu se em uma tabela para os dispensados e outra para os que nao foram.
    dispensados = df[df['DISPENSA'] == 'Com dispensa']
    recrutados = df[df['DISPENSA'] == 'Sem dispensa']

    # Duas séries pandas para visualização.
    serie_dispensados = dispensados.loc[:,'IMC']
    serie_recrutados = recrutados.loc[:,'IMC']

    # De acordo com a tabela de IMC ha 6 grupos diferentes de IMCs.
    intervalo = [0, 18.5, 24.9, 29.9, 34.9, 39.9, float('inf')]
    rotulos = ['Abaixo do peso', 'Peso normal', 'Sobrepeso', 'Obesidade grau I', 'Obesidade grau II', 'Obesidade grau III']

    # Serie panda que substitui o valor do imc pela categoria que ele se encontra.
    dispensados_categorizado_imc = pd.cut(serie_dispensados, bins=intervalo, labels=rotulos)
    recrutados_categorizado_imc = pd.cut(serie_recrutados, bins=intervalo, labels=rotulos)

    # Conta os valores em cada categoria e ve a porcentagem em relação ao total de dispensados e recrutados respectivamente.
    contagem_intervalos_dispensados = percentage_value_counts(dispensados_categorizado_imc)
    contagem_intervalos_recrutados = percentage_value_counts(recrutados_categorizado_imc)

    # Coloca a serie na ordem da tabela de IMC
    contagem_intervalos_dispensados_reordenado =contagem_intervalos_dispensados.reindex(rotulos)
    contagem_intervalos_recrutados_reordenado =contagem_intervalos_recrutados.reindex(rotulos)

    # Os valores da coluna PORCENTAGEM de cada data frame já ordenado
    porcentagens_dispensados = contagem_intervalos_dispensados_reordenado['PORCENTAGEM']
    porcentagens_recrutados = contagem_intervalos_recrutados_reordenado['PORCENTAGEM']

    # Largura das barras do gráfico
    largura_barra = 0.23

    # Calcule as posições das barras para recrutados e dispensados
    posicoes = np.arange(len(rotulos))
    posicoes_recrutados = posicoes - largura_barra / 2
    posicoes_dispensados = posicoes + largura_barra / 2

    # As barras do gráfico, verde para os dados dos Recrutados e cinza para os dados dos Dispensados
    plt.bar(x=posicoes_recrutados,width=largura_barra, label='Recrutados',height=porcentagens_recrutados,color='green',alpha=0.8)
    plt.bar(x=posicoes_dispensados,width=largura_barra, label='Dispensados',height=porcentagens_dispensados,color='gray',alpha=0.4)

    # Configurando o gráfico
    plt.xticks(rotation=45)
    plt.ylim(0,1)
    plt.gca().yaxis.set_major_formatter(FuncFormatter(percentage_formatter))
    plt.xticks(posicoes, rotulos, rotation=45)
    plt.legend()
    plt.tight_layout()

    # Mostra o gráfico no output
    plt.show()


if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True)