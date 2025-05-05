# Plot imputed data
# Emily Ninestein

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Import original excel
df = pd.read_excel('merged_data_with_day_of_year.xlsx')

# Import imputed data
df_imputed = pd.read_excel('imputed_based_on_temp_and_day.xlsx')

# Create 3 subplots: Precipitation, Windspeed, Temperature
fig, axes = plt.subplots(3, 1, figsize=(12, 12), sharex=True)

# Plot 1 - Precipitation
axes[0].scatter(df['day_of_year'], df['Precipitation'], color='blue', s=10, label='Original Precipitation')
axes[0].set_ylabel('Precipitation')
axes[0].set_title('Precipitation vs. Day of Year')
axes[0].legend()

# Plot 2 - Windspeed
axes[1].scatter(df['day_of_year'], df['Windspeed'], color='blue', s=10, label='Original Windspeed')
axes[1].set_ylabel('Windspeed')
axes[1].set_title('Windspeed vs. Day of Year')
axes[1].legend()

# Plot 3 - Temperature
axes[2].scatter(df['day_of_year'], df['Temperature'], color='blue', s=10, label='Original Temperature')
axes[2].set_xlabel('Day of Year')
axes[2].set_ylabel('Temperature (tenths of °C)')
axes[2].set_title('Temperature vs. Day of Year')
axes[2].legend()

plt.tight_layout()
plt.show()
