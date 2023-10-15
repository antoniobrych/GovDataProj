from utils import utils_henrique as uh
from utils import plotfunctions as pf

df = uh.take_data("sermilH2022.csv",["ANO_NASCIMENTO"])
data = uh.calculate_age(df,"ANO_NASCIMENTO")

pf.top_ages_histogram(data,"Idade",4,colors= ['#123456', '#6d745f', "black","black","black"])
