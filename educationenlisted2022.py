from utils_henrique import take_data, transform_column
from plotfunctions import bar_cluster

#Pegando as colunas desejadas para a análise
data_frame = take_data("sermil2022.csv",["ESCOLARIDADE","DISPENSA"])

#criando dicionário para usar como arg em transform_columns
transform_dict = {
    'Ensino Superior': 'Superior',
    'Ensino Médio': 'Médio',
    'Ensino Fundamental': 'Fundamental',
    "Pós-":"Superior",
    "Mestrado":"Superior",
    "Doutorado":"Superior"
}

# transformando os dados da coluna "ESCOLARIDADE"
data_transf = transform_column(data_frame,"ESCOLARIDADE", transform_dict)
# agora teremos apenas os valores "Analfabeto","Alfabetizado","Fundamental","Médio","Superior"
# Fundamental --> Todos que completaram ou que ainda estão no Ensino Fundamental
# Médio --> Todos que completaram ou que ainda estão no Ensino Médio
# Superio --> Todos que completaram ou estão em algum curso superior, pós-graduação, mestrado, doutarado, pós-doutorado ...

# Agora plotamos
bar_cluster(data_transf)