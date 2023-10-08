import pandas as pd
import numpy as np
import datetime as dt
import geopandas as gpd
import matplotlib.pyplot as plt
import os

def get_state_coordinates(path,dropnull = False):
    '''
    '''
    try:
        if os.path.exists(path):
            geobrazil_df = gpd.read_file(path,layer = "lim_unidade_federacao_a")
            geobrazil_df.rename({"sigla":"UF_RESIDENCIA"},axis=1,inplace=True)
        else:
            raise NameError("O nome do arquivo ou o caminho informado está errado")
        if dropnull == True:
            clean_geobrazil_df = geobrazil_df.dropna(axis=1)
        else:
            clean_geobrazil_df = geobrazil_df
    except NameError as error:
        print(error)
        return None
    except Exception as e:
        print("Ocorreu um erro, e não é o nome do arquivo. O erro é: ",str(e))
    else:
        return clean_geobrazil_df

def cria_mapa(army_df,height_colname,state_colname,geobrazil_df):
    '''
    '''
    # Linha abaixo é temporária
    army_df = army_df.dropna(subset=[height_colname])
    try:
        for valor in army_df[height_colname]:
            assert isinstance(valor,(int,float)), f"Erro, elementos da coluna {height_colname} não são números"
            assert valor != 0, "Erro, altura não pode ser zero"
            assert valor > 0, "Erro, altura deve ser maior que zero."
    except AssertionError as error:
        print(error)
        return None
    except Exception as e:
        print("Ocorreu um erro. O erro é: ",str(e))
    else:
        tmp_df = army_df.groupby(state_colname)[height_colname].mean().reset_index()
        tmp_df.columns = [state_colname, height_colname]
        tmp_df = tmp_df[tmp_df[state_colname] != 'KK'] # O estado não existe
        army_height = geobrazil_df.merge(tmp_df,on = state_colname,how= 'right')
        return army_height