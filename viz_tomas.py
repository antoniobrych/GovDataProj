from Utils_tomas import utils_tomas as ut
from Utils_tomas import download_data_tomas as ddt
import pandas as pd


ddt.download_gpkg_local("https://geoftp.ibge.gov.br/cartas_e_mapas/bases_cartograficas_continuas/bcim/versao2016/geopackage/bcim_2016_21_11_2018.gpkg")
geobrazil_df = ut.get_state_coordinates('geo_data.gpkg',True)
army_df = pd.read_csv('Utils_tomas/sermil2022.csv')
merged_army_height_df = ut.merge_height_geography_df(army_df,"ALTURA","UF_RESIDENCIA",geobrazil_df)
age_df = ut.get_age(army_df,"ANO_NASCIMENTO")

ut.create_height_heatmap(merged_army_height_df, "ALTURA", "UF_RESIDENCIA")
ut.create_correlation_matrix(army_df, ["ALTURA", "CINTURA", "CABECA"])
ut.create_age_histogram(age_df)



