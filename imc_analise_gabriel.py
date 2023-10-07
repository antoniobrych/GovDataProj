from onedata_downloadlocally import download_alldata
from utils_gabriel import save_data_in_list, cria_imc, df_allyears,filtra, mean, median


#Baixa os dados caso nao estejam baixados localmente (demora pra baixar)
download_alldata(['PESO','ALTURA','DISPENSA'])

# Lista com os dfs de cada ano
dfs = save_data_in_list()

# Data Frame que concatenou todos os anos
df = df_allyears(dfs)

# Novo Data Frame com a coluna imc e a altura em metros
df = cria_imc(df, 'ALTURA', 'PESO')

# Dividiu se em uma tabela para os dispensados e outra para os que nao foram.
dispensados = filtra(df, 'DISPENSA', 'Com dispensa')
recrutados = filtra(df, 'DISPENSA', 'Sem dispensa')

# A fim de explorar os dados calcula-se a media
media_imc_dispensados = mean(dispensados,'IMC')
media_imc_recrutados = mean(recrutados,'IMC')

# A fim de explorar os dados calcula-se a mediana
mediana_imc_dispensados = median(dispensados,'IMC')
mediana_imc_recrutados = median(recrutados,'IMC')

# Duas séries pandas para visualização
serie_dispensados_vis = dispensados.loc[:,'IMC']
serie_recrutados_vis = recrutados.loc[:,'IMC']