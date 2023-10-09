import pandas as pd
import numpy as np
import datetime as dt
import geopandas as gpd
import matplotlib.pyplot as plt
import seaborn as sns
import datetime as dt
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
        return None
    else:
        return clean_geobrazil_df

def merge_height_geography_df(army_df,height_colname,state_colname,geobrazil_df):
    '''
    '''
    # Linha abaixo é temporária
    army_df = army_df.dropna(subset=[height_colname])
    try:
        for val in army_df[height_colname]:
            assert isinstance(val,(int,float)), f"Erro, elementos da coluna {height_colname} não são números"
            assert val != 0, "Erro, altura não pode ser zero"
            assert val > 0, "Erro, altura deve ser maior que zero."
    except AssertionError as error:
        print(error)
        return None
    except Exception as e:
        print("Ocorreu um erro. O erro é: ",str(e))
    else:
        tmp_df = army_df.groupby(state_colname)[height_colname].mean().reset_index()
        tmp_df.columns = [state_colname, height_colname]
        tmp_df = tmp_df[tmp_df[state_colname] != 'KK'] # O estado não existe
        try:
            merged_army_height_df = geobrazil_df.merge(tmp_df,on = state_colname,how= 'right')
        except pd.errors.MergeError as e:
            print('Merge não estabelecido')
        return merged_army_height_df

def create_height_heatmap(merged_army_height_df):
    '''
    '''
    # código abaixo temporário
    merged_army_height_df = merged_army_height_df.dropna(subset=['ALTURA'])
    try:
        for valor in merged_army_height_df['ALTURA']:
                try:
                    assert isinstance(valor, (int, float)), f"Erro, elementos da coluna {'ALTURA'} não são números"
                    assert valor != 0, "Erro, altura não pode ser zero"
                    assert valor > 0, "Erro, altura deve ser maior que zero."
                except AssertionError as error:
                    print(error)
                    return None
    except KeyError as ke:
        print("A seguinte coluna não existe no Dataframe fornecido: ",str(ke))
        return None

    try:
        for val in merged_army_height_df['UF_RESIDENCIA']:
            try:
                assert isinstance(val,(str)), f"Erro, elementos da coluna {'ALTURA'} não são do tipo str"
            except AssertionError as error:
                print(error)
                return None
    except KeyError as ke:
        print("A seguinte coluna não existe no Dataframe fornecido: ",str(ke))
        return None        

    try:
        merged_army_height_df.plot(
            column = 'ALTURA',
            cmap = 'YlGnBu',
            figsize = (16,10),
            legend = True,
            edgecolor = 'black',
            vmin=merged_army_height_df['ALTURA'].min(),
            vmax=merged_army_height_df['ALTURA'].max(),
        )
        plt.title("Mapa de Calor das Alturas das Pessoas por Estado", fontsize=16)
        plt.axis('off')
        plt.show()
    except Exception as e:
        print('Um erro aconteceu: ',str(e))
        return None
    

def get_stats(army_df,numeric_colname):
    '''
    '''
    # código temporário
    army_df = army_df.dropna(subset=[numeric_colname])
    try:
        for val in army_df[numeric_colname]:
            assert isinstance(val,(int,float)), f"Erro, elementos da coluna {numeric_colname} não são números"
            assert val != 0, "As medidas físicas humanas não podem ser iguais a zero."
            assert val > 0, "As medidas físicas humanas não podem menores ou iguais a zero."
    except AssertionError as error:
        print(error)
        return None
    except Exception as e:
        print("Ocorreu um erro. O erro é: ",str(e))
        return None
    else:
        try:    
            col_summary = army_df[numeric_colname].describe()
        except Exception as e:
            print('Um erro ocorreu: ',str(e))
            return None
        else:   
            return col_summary
        
def create_correlation_matrix(army_df,hum_measures_list):
    '''
    '''
    #código temporário
    army_df = army_df.dropna(subset=hum_measures_list)
    filtered_army_df = army_df[hum_measures_list]
    for col in hum_measures_list:
        try:
            for val in army_df[col]:
                assert isinstance(val,(int,float)), f"Erro, elementos da coluna {col} não são números"
                assert val != 0, "As medidas físicas humanas não podem ser iguais a zero."
                assert val > 0, "As medidas físicas humanas não podem menores ou iguais a zero."
        except AssertionError as error:
            print(error)
            return None
        except Exception as e:
            print("Ocorreu um erro. O erro é: ",str(e))
            return None
    # Não sei como melhorar essa try - except para gráficos
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
        plt.title("Matrix de correlação dos atributos físicos", fontsize=16)
        plt.xticks(rotation=45, ha="right")
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        plt.tight_layout()
        plt.show()
    except Exception as e:
        print('O seguinte problema ocorreu: ',str(e))
        return None

def get_age(army_df,birth_date_colname):
    '''
    '''
    # Tem que fazer o tartamento dos dados para ver 
    current_year = dt.datetime.today().year
    age_list = []
    try:
        for birth_date in army_df[birth_date_colname]:
            assert isinstance(birth_date,(int,float)), f"Erro, elementos da coluna {birth_date_colname} não são números"
            assert birth_date > 1920, "Erro, data de nascimento deve ser maior que 1920."
            age_list.append(current_year - birth_date)
    except AssertionError as error:
        print(error)
        return None
    except Exception as e:
        print("Ocorreu um erro, e não é o nome do arquivo. O erro é: ",str(e))
        return None
    else:
        army_age_df = pd.DataFrame(age_list,columns=['IDADE'])
        return army_age_df
    
def create_age_histogram(army_age_df):
    '''
    '''
    try:
        for val in army_age_df['IDADE']:
            assert isinstance(val,(int,float)), f"Erro, elementos da coluna {'IDADE'} não são números"
            assert val != 0, "A idade não podem ser iguais a zero."
            assert val > 0, "As medidas físicas humanas não podem menores ou iguais a zero."
    except AssertionError as error:
        print(error)
        return None
    except Exception as e:
        print("Ocorreu um erro. A seguinte coluna não pertence ao Dataframe: ",str(e))
        return None
    min_age = army_age_df['IDADE'].min()
    max_age = army_age_df['IDADE'].quantile(0.98)
    bin_width = 1    
    x_range = (min_age, max_age + 2)

    try:
        plt.hist(
            army_age_df['IDADE'],
            bins=np.arange(min_age, max_age + bin_width, bin_width),  # Define custom bin edges
            facecolor='#1d91c0',
            edgecolor='black',
            linewidth=1
        )
        ticks = [0, 100000, 300000,500000, 700000, 900000]
        plt.yticks(ticks)
        plt.xlim(x_range)
        plt.grid(alpha=0.2,linestyle='-', linewidth=0.6,color= 'black')
        plt.xlabel('Idade')
        plt.ylabel('Frequência')
        plt.title('Distribuição de idades')
        plt.show()
    except Exception as e:
        print('ocorreu um erro: ',str(e))
