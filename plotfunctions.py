# Funções que geram os gráficos

def gerar_grafico_barras_agrupadas(df):
    import matplotlib as plt
    import pandas as pd

    plt.figure(figsize=(10, 6))
    
    # crosstab para contar as ocorrências de escolaridade e dispensa
    tabela_contagem = pd.crosstab(df['ESCOLARIDADE'], df['Dispensa'])
    
    tabela_contagem.plot(kind='bar')
    
    plt.title('Escolaridade dos Alistados com e sem dispensa')
    plt.xlabel('Escolaridade')
    plt.ylabel('Número de Pessoas')
    
    plt.show()