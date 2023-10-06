import pandas as pd
import os

def le_csv_local(path: str):
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
    df : pandas.DataFrame
        Retorna uma tabela que contenha a coluna IMC.

    '''
    df['ALTURA(m)'] = df[height_colname]/100
    df['IMC'] = df[weight_colname]/(df['ALTURA(m)'])**2
    df = df.drop(height_colname,axis=1)
    return df
