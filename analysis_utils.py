"""
Principal objetivo deste módulo:

Fornecer funções para facilitar a análise do dataset.

Em especial, análise de séries temporais, 

onde se deseja estudar a mudança ao longo do tempo.
 
"""
import pandas as pd
import doctest
def yearly_mean(df:pd.DataFrame)->pd.DataFrame:
    """
    Função que cálcula a média anual de variáveis numéricas

    no dataset SERMIL (Concatenado ou não.).

    Exclusivamente para uso com este dataset.

    Returns:
    -------
    pandas.DataFrame:
        Dataframe que contém as médias anuais.

    Example:
    --------
    >>> requested_columns = ['PESO','ALTURA','CALCADO','CABECA','CINTURA','VINCULACAO_ANO']
    >>> df = pd.read_csv('data_concat//SERMIL_5_ANOS.csv',usecols=requested_columns)
    >>> df.shape[0]>0
    True
    >>> yearly_mean_df = yearly_mean(df)
    >>> yearly_mean_df.shape[0] > 0
    True
    >>> print(yearly_mean_df.head())
                      CINTURA       PESO      ALTURA     CABECA
    VINCULACAO_ANO                                             
    2007            80.155392  67.364551  173.655000  57.005780
    2008            79.969176  67.569952  173.361765  56.989328
    2009            80.076656  68.011941  173.784207  56.927371
    2010            80.097404  68.522337  173.709347  57.003246
    2011            79.899922  68.839196  173.632318  56.865574
    """
    
    selected_df = df[['VINCULACAO_ANO', 'CINTURA', 'PESO', 'ALTURA','CABECA']]
    #droping NaN values
    selected_df = selected_df.dropna(axis='index')
    selected_df = selected_df.set_index('VINCULACAO_ANO')
    
    # Grouping the data year by year, and calculating the mean afterwwards
    selected_df = selected_df.groupby(level='VINCULACAO_ANO').mean()
    # Return the resulting DataFrame, which contains the yearly mean values.
    return selected_df

def yearly_aggregate(df:pd.DataFrame)->pd.DataFrame:
    """
    Função que cálcula totais de registros em um ano,

    no dataset SERMIL (Concatenado ou não.).

    Exclusivamente para uso com este dataset.

    Returns:
    -------
    pandas.DataFrame:
        Dataframe que contém todos os registros em um determinado ano.

    Example:
    --------
    >>> requested_columns = ['PESO','ALTURA','CALCADO','CABECA','CINTURA','VINCULACAO_ANO','SEXO']
    >>> df = pd.read_csv('data_concat//SERMIL_5_ANOS.csv',usecols=requested_columns)
    >>> df.shape[0]>0
    True
    >>> yearly_aggregate_df = yearly_aggregate(df)
    >>> yearly_aggregate_df.shape[0] > 0
    True
    >>> print(yearly_aggregate_df.head())
                    CINTURA    PESO  ALTURA    TOTAL
    VINCULACAO_ANO                                  
    2007             344305  304614  311951  1615993
    2008             326025  317338  319645  1725059
    2009             328006  327890  327961  1542705
    2010             340473  340447  340493  1695573
    2011             362280  362266  362315  1785369
    """

    synthetic_df = df.copy()
    synthetic_df['TOTAL'] = synthetic_df['VINCULACAO_ANO'].copy()
    synthetic_df = synthetic_df[['VINCULACAO_ANO','CINTURA','PESO','ALTURA','TOTAL']].set_index('VINCULACAO_ANO')
    synthetic_df = synthetic_df.groupby(level='VINCULACAO_ANO').count()
    # Return the resulting DataFrame, which contains the yearly mean values.
    return synthetic_df

if __name__ == "__main__":
    doctest.testmod(verbose=True)