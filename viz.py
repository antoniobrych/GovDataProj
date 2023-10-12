"""

Data Viz
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

requested_columns = ['PESO','ALTURA','CALCADO','CABECA','CINTURA']    

df = pd.read_csv("data_concat//SERMIL_5_ANOS.csv",usecols=requested_columns)


