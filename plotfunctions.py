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
    import matplotlib.pyplot as plt

    plt.figure(figsize=(10, 6))
    
    # crosstab para contar as ocorrências das colunas desejadas
    tabela_contagem = pd.crosstab(df[column1], df[column2])

    # Cores pras barras
    colors = ['#123456', '#6d745f']
    #criar plot com essas colunas
    tabela_contagem.plot(kind='bar', color = colors)
    
    plt.title(name)
    plt.xlabel(xname)
    plt.ylabel(yname)
    
    plt.show()

def top_ages_histogram(data, column_name, num_top_ages=5, colors=None):
    """
    Gera um histograma das idades mais frequentes em um DataFrame.

    Parâmetros
    ----------
    data : pandas.core.frame.DataFrame
        O DataFrame contendo os dados.
    column_name : str
        O nome da coluna que contém as idades.
    num_top_ages : int, opcional
        O número de idades mais frequentes a serem exibidas no histograma. O padrão é 5.
    colors : list, opcional
        Uma lista de cores personalizadas para as barras. O padrão é None.

    Retorna
    -------
    None
        O gráfico de histograma é exibido, não há valor de retorno.

    """

    import matplotlib.pyplot as plt

    top_ages = data[column_name].value_counts().nlargest(num_top_ages)
    
    # Adicionar a categoria "Outros" para idades que não estão no top
    other_ages_count = data.shape[0] - top_ages.sum()
    top_ages['Outros'] = other_ages_count

    # Cores padrão para as barras se não forem fornecidas
    if colors is None:
        colors = ['b', 'g', 'r', 'c', 'm']
    
    top_ages.plot(kind='bar', color=colors)
    plt.title(f'As {num_top_ages} Idades Mais Frequentes')
    plt.xlabel('Idade')
    plt.ylabel('Frequência')
    plt.show()
    