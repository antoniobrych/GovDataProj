'''
Este módulo contém funções que fornecem análises estatísticas e visualizações gráficas
'''

import pandas as pd
import numpy as np
import datetime as dt
from typing import List
import geopandas as gpd
import matplotlib.pyplot as plt
import seaborn as sns
import os


def get_state_coordinates(path: str, dropnull: bool = False) -> gpd.GeoDataFrame:
    '''
    Lê um arquivo gpkg e cria um GeoDataFrame.

    Parameters
    ----------
    path: str
        O caminho do arquivo gpkg que será lido.
    dropnull : bool
        Caso True, remove as linhas nulas; se False, mantém as linhas com valores nulos.

    Returns
    -------
    gpd.GeoDataFrame
        Um GeoDataFrame contendo informações dos estados brasileiros.

    Raises
    -----
    NameError
        Se o arquivo não existir ou o caminho estiver incorreto.

    Example
    -------
    >>> geobrazil_df = get_state_coordinates("dados/geo_data.gpkg")
    >>> isinstance(geobrazil_df, gpd.GeoDataFrame) or geobrazil_df is None
    True
    '''

    try:
        if os.path.exists(path):
            geobrazil_df = gpd.read_file(path, layer="lim_unidade_federacao_a")
            geobrazil_df.rename({"sigla": "UF_RESIDENCIA"},
                                axis=1, inplace=True)
        else:
            raise NameError(
                "O nome do arquivo ou o caminho informado está errado")

        if dropnull:
            clean_geobrazil_df = geobrazil_df.dropna(axis=1)
        else:
            clean_geobrazil_df = geobrazil_df
    except NameError as error:
        print(error)
        return None
    except Exception as e:
        print("Ocorreu um erro: ", str(e))
        return None
    else:
        return clean_geobrazil_df


def merge_height_geography_df(army_df: pd.DataFrame, height_colname: str, state_colname: str, geobrazil_df: gpd.GeoDataFrame) -> pd.DataFrame:
    '''
    Realiza o merge do DataFrame de alistamento militar com um GeoDataFrame contendo informações geográficas.

    Parameters
    ----------
    army_df: pd.DataFrame
        DataFrame com dados do alistamento militar.
    height_colname : str
        Nome da coluna no DataFrame que representa a altura.
    state_colname : str
        Nome da coluna no DataFrame que representa os estados.
    geobrazil_df : gpd.GeoDataFrame
        GeoDataFrame com dados dos estados brasileiros.

    Returns
    -------
    pd.DataFrame
        Um DataFrame que combina informações de altura com dados geográficos dos estados brasileiros.

    Raises
    -----
    KeyError
        Se as colunas especificadas não existirem no DataFrame fornecido.

    Example
    -------
    >>> army_df = pd.read_csv('dados/sermil2022.csv')
    >>> geobrazil_df = get_state_coordinates("dados/geo_data.gpkg")
    >>> result = merge_height_geography_df(army_df, "ALTURA", "UF_RESIDENCIA", geobrazil_df)
    >>> isinstance(result, pd.DataFrame) or result is None
    True
    '''

    try:
        if height_colname not in army_df.columns:
            raise KeyError(
                "A coluna especificada não existe no DataFrame: ", height_colname)
    except KeyError as ke:
        print("Erro: ", str(ke))
        return None

    try:
        if state_colname not in army_df.columns:
            raise KeyError(
                "A coluna especificada não existe no DataFrame: ", state_colname)
    except KeyError as ke:
        print("Erro: ", str(ke))
        return None
    army_df = army_df.dropna(subset=[height_colname])
    try:
        for val in army_df[height_colname]:
            assert isinstance(
                val, (int, float)), f"Erro, elementos da coluna {height_colname} não são números"
            assert val != 0, "Erro, altura não pode ser zero"
            assert val > 0, "Erro, altura deve ser maior que zero."
    except AssertionError as error:
        print(error)
        return None
    except Exception as e:
        print("Ocorreu um erro: ", str(e))
        return None
    else:
        tmp_df = army_df.groupby(state_colname)[
            height_colname].mean().reset_index()
        tmp_df.columns = [state_colname, height_colname]
        tmp_df = tmp_df[tmp_df[state_colname] != 'KK']  # O estado não existe

        try:
            merged_army_height_df = geobrazil_df.merge(
                tmp_df, on=state_colname, how='right')
        except pd.errors.MergeError as e:
            print('Merge não estabelecido')
            return None
        except KeyError as ke:
            print("Ocorreu um erro: ", str(ke))
            return None

        return merged_army_height_df


def create_height_heatmap(merged_army_height_df: pd.DataFrame, height_colname: str, state_colname: str) -> bool:
    '''
    Cria um mapa de calor brasileiro que representa a diferença entre as médias de altura por estado.

    Parameters
    ----------
    merged_army_height_df : pd.DataFrame
        DataFrame combinando informações de altura com dados geográficos dos estados brasileiros.
    height_colname : str
        Nome da coluna no DataFrame que representa a altura.
    state_colname : str
        Nome da coluna no DataFrame que representa os estados.

    Returns
    -------
    bool
        Retorna True se o gráfico foi criado com sucesso, False caso contrário.

    Example
    -------
    >>> army_df = pd.read_csv('dados/sermil2022.csv')
    >>> geobrazil_df = get_state_coordinates("dados/geo_data.gpkg")
    >>> merged_df = merge_height_geography_df(army_df, "ALTURA", "UF_RESIDENCIA", geobrazil_df)
    >>> result = create_height_heatmap(merged_df, "ALTURA", "UF_RESIDENCIA")
    >>> isinstance(result, bool)
    True
    '''

    try:
        if height_colname not in merged_army_height_df.columns:
            raise KeyError(
                "A coluna especificada não existe no DataFrame: ", height_colname)
    except KeyError as ke:
        print("Erro: ", str(ke))
        return None

    try:
        if state_colname not in merged_army_height_df.columns:
            raise KeyError(
                "A coluna especificada não existe no DataFrame: ", state_colname)
    except KeyError as ke:
        print("Erro: ", str(ke))
        return None
    merged_army_height_df = merged_army_height_df.dropna(
        subset=[height_colname])
    for valor in merged_army_height_df[height_colname]:
        try:
            assert isinstance(
                valor, (int, float)), f"Erro, elementos da coluna {height_colname} não são números"
            assert valor != 0, "Erro, altura não pode ser zero"
            assert valor > 0, "Erro, altura deve ser maior que zero."
        except AssertionError as error:
            print(error)
            return None
    try:
        merged_army_height_df.plot(
            column=height_colname,
            cmap='YlGnBu',
            figsize=(16, 10),
            legend=True,
            edgecolor='black',
            vmin=merged_army_height_df[height_colname].min(),
            vmax=merged_army_height_df[height_colname].max()
        )
        plt.title("Mapa de Calor das Alturas das Pessoas por Estado", fontsize=16)
        plt.axis('off')
        plt.show()
        return True
    except Exception as e:
        print('Um erro aconteceu: ', str(e))
        return False


def get_stats(army_df: pd.DataFrame, numeric_colname: str) -> pd.Series:
    '''
    Realiza análise estatística de uma coluna em um DataFrame.

    Parameters
    ----------
    army_df: pd.DataFrame
        DataFrame com dados do alistamento militar.
    numeric_colname : str
        Nome da coluna no DataFrame com dados numéricos.

    Returns
    -------
    pd.Series
        Uma série com estatísticas da coluna especificada.

    Raises
    -----
    KeyError
        Se a coluna especificada não existir no DataFrame.

    Example
    -------
    >>> army_df = pd.read_csv('dados/sermil2022.csv')
    >>> result = get_stats(army_df, "ALTURA")
    >>> isinstance(result, pd.Series) or result is None
    True
    '''

    army_df = army_df.dropna(subset=[numeric_colname])
    try:
        if numeric_colname not in army_df.columns:
            raise KeyError(
                "A seguinte coluna não existe no DataFrame: ", numeric_colname)
    except KeyError as ke:
        print("Erro: ", str(ke))
        return None

    try:
        for val in army_df[numeric_colname]:
            assert isinstance(
                val, (int, float)), f"Erro, elementos da coluna {numeric_colname} não são números"
            assert val != 0, "Erro, valor não pode ser zero"
            assert val > 0, "Erro, valor deve ser maior que zero."
    except AssertionError as error:
        print(error)
        return None
    except Exception as e:
        print("Ocorreu um erro: ", str(e))
        return None
    else:
        try:
            col_summary = army_df[numeric_colname].describe()
        except Exception as e:
            print('Um erro ocorreu: ', str(e))
            return None
        else:
            return col_summary


def create_correlation_matrix(army_df: pd.DataFrame, hum_measures_list: List[str]) -> bool:
    '''
    Cria uma matriz de correlação para medidas físicas humanas.

    Parameters
    ----------
    army_df: pd.DataFrame
        DataFrame com dados de medidas físicas humanas.
    hum_measures_list : List[str]
        Lista de colunas no DataFrame representando medidas físicas.

    Returns
    -------
    bool
        Retorna True se a matriz de correlação foi criada com sucesso, False caso contrário.

    Example
    -------
    >>> army_df = pd.read_csv('dados/sermil2022.csv')
    >>> result = create_correlation_matrix(army_df, ["ALTURA", "CINTURA"])
    >>> isinstance(result, bool)
    True
    '''

    try:
        for elem in hum_measures_list:
            if elem not in army_df.columns:
                raise KeyError(
                    "A seguinte coluna não existe no DataFrame: ", elem)
    except KeyError as ke:
        print('Erro: ', str(ke))
        return None
    army_df = army_df.dropna(subset=hum_measures_list)
    filtered_army_df = army_df[hum_measures_list]
    for col in hum_measures_list:
        try:
            for val in army_df[col]:
                assert isinstance(
                    val, (int, float)), f"Erro, elementos da coluna {col} não são números"
                assert val != 0, "As medidas físicas humanas não podem ser iguais a zero."
                assert val > 0, "As medidas físicas humanas não podem ser menores ou iguais a zero."
        except AssertionError as error:
            print(error)
            return None
        except Exception as e:
            print("Ocorreu um erro: ", str(e))
            return None
    try:
        corr_matrix = filtered_army_df.corr().round(2)
        cmap = sns.diverging_palette(240, 10, s=150, l=40, n=250)
        fig, ax = plt.subplots(figsize=(12, 10))
        sns.heatmap(
            corr_matrix,
            vmin=-1,
            vmax=1,
            cmap=cmap,
            square=True,
            annot=True,
            fmt=".2f",
            linewidths=0.5
        )
        plt.title("Matriz de Correlação das Medidas Físicas Humanas", fontsize=16)
        plt.xticks(rotation=45, ha="right")
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        plt.tight_layout()
        plt.show()
        return True
    except Exception as e:
        print('O seguinte problema ocorreu: ', str(e))
        return False


def get_age(army_df: pd.DataFrame, birth_date_colname: str) -> pd.DataFrame:
    '''
    Calcula a idade a partir da data de nascimento em um DataFrame.

    Parameters
    ----------
    army_df: pd.DataFrame
        DataFrame com dados do alistamento militar.
    birth_date_colname : str
        Nome da coluna no DataFrame que contém a data de nascimento.

    Returns
    -------
    pd.DataFrame
        Um DataFrame contendo a idade calculada de acordo com a data de nascimento.

    Example
    -------
    >>> army_df = pd.read_csv('dados/sermil2022.csv')
    >>> result = get_age(army_df, "ANO_NASCIMENTO")
    >>> isinstance(result, pd.DataFrame) or result is None
    True
    '''

    current_year = dt.datetime.today().year
    age_list = []
    try:
        for birth_date in army_df[birth_date_colname]:
            assert isinstance(
                birth_date, (int, float)), f"Erro, elementos da coluna {birth_date_colname} não são números"
            assert birth_date > 1920, "Erro, data de nascimento deve ser maior que 1920."
            age_list.append(current_year - birth_date)
    except AssertionError as error:
        print(error)
        return None
    except Exception as e:
        print("Ocorreu um erro: ", str(e))
        return None
    else:
        army_age_df = pd.DataFrame(age_list, columns=['IDADE'])
        return army_age_df


def create_age_histogram(army_age_df: pd.DataFrame) -> bool:
    '''
    Cria um histograma de idade.

    Parameters
    ----------
    army_age_df : pd.Series
        Uma série com dados de idade.

    Returns
    -------
    bool
        Retorna True se o gráfico foi criado com sucesso, False caso contrário.

    Example
    -------
    >>> army_df = pd.read_csv('dados/sermil2022.csv')
    >>> army_age_df = get_age(army_df,"ANO_NASCIMENTO")
    >>> result = create_age_histogram(army_age_df)
    >>> isinstance(result, bool)
    True
    '''

    try:
        for val in army_age_df['IDADE']:
            assert isinstance(
                val, (int, float)), f"Erro, elementos da coluna {'IDADE'} não são números"
            assert val != 0, "A idade não pode ser igual a zero."
            assert val > 0, "A idade deve ser maior que zero."
    except AssertionError as error:
        print(error)
        return None
    except Exception as e:
        print("Ocorreu um erro: ", str(e))
        return None

    min_age = army_age_df['IDADE'].min()
    max_age = army_age_df['IDADE'].quantile(0.98)
    bin_width = 1
    x_range = (min_age, max_age + 2)

    try:
        plt.hist(
            army_age_df['IDADE'],
            bins=np.arange(min_age, max_age + bin_width, bin_width),
            facecolor='#1d91c0',
            edgecolor='black',
            linewidth=1
        )
        ticks = [0, 100000, 300000, 500000, 700000, 900000]
        plt.yticks(ticks)
        plt.xlim(x_range)
        plt.grid(alpha=0.2, linestyle='-', linewidth=0.6, color='black')
        plt.xlabel('Idade')
        plt.ylabel('Frequência')
        plt.title('Distribuição de Idades')
        plt.show()
        return True
    except Exception as e:
        print('Ocorreu um erro: ', str(e))
        return False
