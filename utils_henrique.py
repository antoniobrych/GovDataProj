"""
Rascunho:
Gráfico de barras com o nível de escolaridade dos alistados
"""
import pandas as pd
import matplotlib.pyplot as plt

# Usando o csv de 2022 
df = pd.read_csv('sermil2022.csv', encoding='utf-8')
#Criar/usar func que pega de todos os anos

#pegar dados e criar dataframe só com as colunas de ESCOLARIDADE e DISPENSA
novo_df = df.copy() 

#transformar isso em func
novo_df['ESCOLARIDADE'] = novo_df['ESCOLARIDADE'].apply(lambda x: 'Ensino Fundamental' if 'Ensino Fundamental' in x else x)
novo_df['ESCOLARIDADE'] = novo_df['ESCOLARIDADE'].apply(lambda x: 'Ensino Médio' if 'Ensino Médio' in x else x)
novo_df['ESCOLARIDADE'] = novo_df['ESCOLARIDADE'].apply(lambda x: 'Ensino Superior' if 'Ensino Superior' in x else x)
novo_df['ESCOLARIDADE'] = novo_df['ESCOLARIDADE'].apply(lambda x: 'Ensino Superior' if 'Mestrado' in x else x)
novo_df['ESCOLARIDADE'] = novo_df['ESCOLARIDADE'].apply(lambda x: 'Ensino Superior' if 'Doutorado' in x else x)
novo_df['ESCOLARIDADE'] = novo_df['ESCOLARIDADE'].apply(lambda x: 'Ensino Superior' if 'Pós-Graduaç' in x else x)

#transformar em func pra gerar grafico
contagem_escolaridade = novo_df['ESCOLARIDADE'].value_counts()
plt.figure(figsize=(10, 6))  
contagem_escolaridade.plot(kind='bar')
plt.title('Distribuição de Escolaridade')
plt.xlabel('Grau de Escolaridade')
plt.ylabel('Número de Pessoas')

plt.show()
