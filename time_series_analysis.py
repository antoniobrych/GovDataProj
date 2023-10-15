"""
Analysis: Change of SERMIL statistics over time.

"""

from analysis_utils import *
from data_utils import *

# Aattemp to read the concatenated file
df = concatenate_last_n_csv_files('data','data_concat',n=20)
print(yearly_mean(df).info())
print(yearly_mean(df).describe())
print(yearly_aggregate(df))
import matplotlib.pyplot as plt
import numpy as np
synthetic_df = yearly_mean(synthetic_df)
df2_agg_total = yearly_aggregate(df)['TOTAL']
# Create some data for the plots
x = synthetic_df.index
y1 = synthetic_df['CINTURA']
y2 = synthetic_df['PESO']
y3 = synthetic_df['ALTURA']
y4 = df2_agg_total['TOTAL']
# Create a single figure
big_figure = plt.figure(figsize=(12, 8))  # Adjust the figure size as needed

# Create subplots for each of the original figures
subplot1 = big_figure.add_subplot(221)  # 2x2 grid, 1st position
subplot2 = big_figure.add_subplot(222)  # 2x2 grid, 2nd position
subplot3 = big_figure.add_subplot(223)  # 2x2 grid, 3rd position
subplot4 = big_figure.add_subplot(224)  # 2x2 grid, 4th position

# Plot the data on the subplots
subplot1.plot(x, y1)
subplot1.set_title('Largura da Cintura ao longo dos anos')

subplot2.plot(x, y2)
subplot2.set_title('Evolução do Peso ao longo dos anos')

subplot3.plot(x, y3)
subplot3.set_title('Evolução da Altura ao longo dos anos')

subplot4.plot(x, y4)
subplot4.set_title('Total de Alistados ao longo dos anos')

# Add spacing between subplots
plt.tight_layout()

# Show the big figure
plt.show()
