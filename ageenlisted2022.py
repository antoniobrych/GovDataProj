from utils_henrique import take_data, calculate_age
from plotfunctions import top_ages_histogram

df = take_data("sermil2022.csv",["ANO_NASCIMENTO"])
data = calculate_age(df,"ANO_NASCIMENTO")

top_ages_histogram(data,"Idade",4,colors= ['#123456', '#6d745f', "black","black","black"])
