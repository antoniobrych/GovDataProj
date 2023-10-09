from downloaddata import download_alldata
from utils_gabriel import save_data_in_list, create_imc, df_allyears, filtra_equal, mean, median, categorize_series,\
percentage_value_counts, percentage_formatter
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

# Baixa os dados caso nao estejam baixados localmente (demora pra baixar).
download_alldata(['PESO','ALTURA','DISPENSA'])

# Lista com os dfs de cada ano.
dfs = save_data_in_list()

# Data Frame que concatenou todos os anos.
df = df_allyears(dfs)

# Novo Data Frame com a coluna imc e a altura em metros.
df = create_imc(df, 'ALTURA', 'PESO')

# Dividiu se em uma tabela para os dispensados e outra para os que nao foram.
dispensados = filtra_equal(df, 'DISPENSA', 'Com dispensa')
recrutados = filtra_equal(df, 'DISPENSA', 'Sem dispensa')

# A fim de explorar os dados calcula-se a media.
media_imc_dispensados = mean(dispensados,'IMC')
media_imc_recrutados = mean(recrutados,'IMC')

# A fim de explorar os dados calcula-se a mediana.
mediana_imc_dispensados = median(dispensados,'IMC')
mediana_imc_recrutados = median(recrutados,'IMC')

# Duas séries pandas para visualização.
serie_dispensados = dispensados.loc[:,'IMC']
serie_recrutados = recrutados.loc[:,'IMC']

# De acordo com a tabela de IMC ha 6 grupos diferentes de IMCs.
intervalo = [0, 18.5, 24.9, 29.9, 34.9, 39.9, float('inf')]
rotulos = ['Abaixo do peso', 'Peso normal', 'Sobrepeso', 'Obesidade grau I', 'Obesidade grau II', 'Obesidade grau III']

# Serie panda que substitui o valor do imc pela categoria que ele se encontra.
dispensados_categorizado_imc = categorize_series(serie_dispensados, intervalo, rotulos)
recrutados_categorizado_imc = categorize_series(serie_recrutados, intervalo, rotulos)

# Conta os valores em cada categoria e ve a porcentagem em relação ao total de dispensados e recrutados respectivamente.
contagem_intervalos_dispensados = percentage_value_counts(dispensados_categorizado_imc)
contagem_intervalos_recrutados = percentage_value_counts(recrutados_categorizado_imc)

# Coloca a serie na ordem da tabela de IMC
contagem_intervalos_dispensados_reordenado =contagem_intervalos_dispensados.reindex(rotulos)
contagem_intervalos_recrutados_reordenado =contagem_intervalos_recrutados.reindex(rotulos)

# GRÁFICO DISPENSADOS
categorias_dispensados = contagem_intervalos_dispensados_reordenado.index

porcentagens_dispensados = contagem_intervalos_dispensados_reordenado['PORCENTAGEM']

plt.bar(categorias_dispensados,porcentagens_dispensados,color='green')
plt.title("Dispensados")
plt.xticks(rotation=45)
plt.ylim(0,1)
plt.gca().yaxis.set_major_formatter(FuncFormatter(percentage_formatter))
plt.tight_layout()
plt.show()

# GRÁFICO RECRUTADOS
categorias_recrutados = contagem_intervalos_recrutados_reordenado.index

porcentagens_recrutados = contagem_intervalos_recrutados_reordenado['PORCENTAGEM']

plt.bar(categorias_recrutados,porcentagens_recrutados,color='blue')
plt.title("Recrutados")
plt.xticks(rotation=45)
plt.ylim(0,1)
plt.gca().yaxis.set_major_formatter(FuncFormatter(percentage_formatter))
plt.tight_layout()
plt.show()