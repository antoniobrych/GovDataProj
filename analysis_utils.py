"""
Principal objetivo da minha análise

é estudar a mudança ao longo dos anos nessa base de dados.

Principalmente Peso, Altura, Tam. Cabeça,Cintura etc.

Então, esse módulo contém funções específicas para uma

abordagem de séries temporais nessa base.
"""
import pandas as pd

def yearly_mean(df:pd.DataFrame)->pd.DataFrame:
    """
    Função que cálcula a média anual de variáveis numéricas

    no dataset SERMIL (Concatenado ou não.)   
    Returns:
    -------
    pandas.DataFrame:
        Da
    """
    
    selected_df = df[['VINCULACAO_ANO', 'CINTURA', 'PESO', 'ALTURA']]
    
    selected_df = selected_df.set_index('VINCULACAO_ANO')
    
    # Grouping the data by year, and calculating the mean afterwwards.
    selected_df = selected_df.groupby(level='VINCULACAO_ANO').mean()

    # Return the resulting DataFrame, which contains the yearly mean values.
    return selected_df
