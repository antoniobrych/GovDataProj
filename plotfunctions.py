# Funções que geram os gráficos

def bar_cluster(df, column1, column2, name, xname, yname):
    """
    Gera um gráfico de barras agrupadas com os dados das column1 e column2.

    Parâmetros
    ----------
    df : pandas.core.frame.DataFrame
        O DataFrame que contém os dados.
    column1 : str
        O nome da primeira coluna para agrupamento.
    column2 : str
        O nome da segunda coluna para agrupamento.
    name : str
        O título do gráfico.
    xname : str
        O rótulo do eixo x.
    yname : str
        O rótulo do eixo y.

    Retorna
    -------
    None
        O gráfico é exibido, não há valor de retorno.
    """
    import pandas as pd
    import matplotlib as plt

    plt.figure(figsize=(10, 6))
    
    # crosstab para contar as ocorrências das colunas desejadas
    tabela_contagem = pd.crosstab(df[column1], df[column2])
    
    #criar plot com essas colunas
    tabela_contagem.plot(kind='bar')
    
    plt.title(name)
    plt.xlabel(xname)
    plt.ylabel(yname)
    
    plt.show()
    