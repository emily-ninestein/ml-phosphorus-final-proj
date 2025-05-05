# Plot imputed data
# Emily Ninestein

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Import original excel
df = pd.read_excel('merged_data_with_day_of_year.xlsx')

# Import imputed data
df_imputed = pd.read_excel('imputed_temperature_columns_by_day_poly_lasso_cv_diy.xlsx')

# Plot temperature vs. day of year
plt.figure(figsize=(10, 6))
plt.scatter(df['day_of_year'], df['Temperature'], color='blue', s=10, label='Original Data Points')
plt.scatter(df_imputed['day_of_year'], df_imputed['Temperature'], s=10, label='Imputed Data', color='red', alpha=0.5)
plt.xlabel('Day of Year')
plt.ylabel('Temperature (tenths of degrees C)')
plt.title('Original and Imputed Temperature Data')
plt.legend()
plt.show()

plt.figure(figsize=(10, 6))
plt.scatter(df['day_of_year'], df['Temperature_1d_ago'], color='blue', s=10, label='Original Data Points')
plt.scatter(df_imputed['day_of_year'], df_imputed['Temperature_1d_ago'], s=10, label='Imputed Data', color='red', alpha=0.5)
plt.xlabel('Day of Year')
plt.ylabel('Temperature 1 day ago (tenths of degrees C)')
plt.title('Original and Imputed Temperature Data')
plt.legend()
plt.show()

plt.figure(figsize=(10, 6))
plt.scatter(df['day_of_year'], df['Temperature_2d_ago'], color='blue', s=10, label='Original Data Points')
plt.scatter(df_imputed['day_of_year'], df_imputed['Temperature_2d_ago'], s=10, label='Imputed Data', color='red', alpha=0.5)
plt.xlabel('Day of Year')
plt.ylabel('Temperature 2 days ago (tenths of degrees C)')
plt.title('Original and Imputed Temperature Data')
plt.legend()
plt.show()

plt.figure(figsize=(10, 6))
plt.scatter(df['day_of_year'], df['Temperature_3d_ago'], color='blue', s=10, label='Original Data Points')
plt.scatter(df_imputed['day_of_year'], df_imputed['Temperature_3d_ago'], s=10, label='Imputed Data', color='red', alpha=0.5)
plt.xlabel('Day of Year')
plt.ylabel('Temperature 3 days ago (tenths of degrees C)')
plt.title('Original and Imputed Temperature Data')
plt.legend()
plt.show()

plt.figure(figsize=(10, 6))
plt.scatter(df['day_of_year'], df['Temperature_4d_ago'], color='blue', s=10, label='Original Data Points')
plt.scatter(df_imputed['day_of_year'], df_imputed['Temperature_4d_ago'], s=10, label='Imputed Data', color='red', alpha=0.5)
plt.xlabel('Day of Year')
plt.ylabel('Temperature 4 days ago (tenths of degrees C)')
plt.title('Original and Imputed Temperature Data')
plt.legend()
plt.show()

plt.figure(figsize=(10, 6))
plt.scatter(df['day_of_year'], df['Temperature_5d_ago'], color='blue', s=10, label='Original Data Points')
plt.scatter(df_imputed['day_of_year'], df_imputed['Temperature_5d_ago'], s=10, label='Imputed Data', color='red', alpha=0.5)
plt.xlabel('Day of Year')
plt.ylabel('Temperature 5 days ago (tenths of degrees C)')
plt.title('Original and Imputed Temperature Data')
plt.legend()
plt.show()