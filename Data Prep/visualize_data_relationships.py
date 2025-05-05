import pandas as pd
import matplotlib.pyplot as plt

# Load the Excel file
file_path = 'imputed_temperature_columns_by_day_poly_lasso_cv.xlsx'  # <-- Replace with your actual filename
df = pd.read_excel(file_path)

# Define columns for precipitation, windspeed, and temperature (each day and prior 5 days)
precip_cols = ['Precipitation', 'Precipitation_1d_ago', 'Precipitation_2d_ago',
               'Precipitation_3d_ago', 'Precipitation_4d_ago', 'Precipitation_5d_ago']

wind_cols = ['Windspeed', 'Windspeed_1d_ago', 'Windspeed_2d_ago',
             'Windspeed_3d_ago', 'Windspeed_4d_ago', 'Windspeed_5d_ago']

temp_cols = ['Temperature', 'Temperature_1d_ago', 'Temperature_2d_ago',
             'Temperature_3d_ago', 'Temperature_4d_ago', 'Temperature_5d_ago']

# === Precipitation Figure ===
fig, axs = plt.subplots(2, 3, figsize=(18, 10))
axs = axs.flatten()
for i, col in enumerate(precip_cols):
    axs[i].scatter(df[col], df['Total_Phosphorus'], alpha=0.6, edgecolors='k')
    axs[i].set_xlabel(col)
    axs[i].set_ylabel('Total Phosphorus')
    axs[i].set_title(f'TP vs {col.replace("_", " ")}')
plt.suptitle('Total Phosphorus vs Precipitation (Current + Prior Days)', fontsize=16)
plt.tight_layout()
plt.show()

# === Windspeed Figure ===
fig, axs = plt.subplots(2, 3, figsize=(18, 10))
axs = axs.flatten()
for i, col in enumerate(wind_cols):
    axs[i].scatter(df[col], df['Total_Phosphorus'], alpha=0.6, edgecolors='k')
    axs[i].set_xlabel(col)
    axs[i].set_ylabel('Total Phosphorus')
    axs[i].set_title(f'TP vs {col.replace("_", " ")}')
plt.suptitle('Total Phosphorus vs WindSpeed (Current + Prior Days)', fontsize=16)
plt.tight_layout()
plt.show()

# === Temperature Figure ===
fig, axs = plt.subplots(2, 3, figsize=(18, 10))
axs = axs.flatten()
for i, col in enumerate(temp_cols):
    axs[i].scatter(df[col], df['Total_Phosphorus'], alpha=0.6, edgecolors='k')
    axs[i].set_xlabel(col)
    axs[i].set_ylabel('Total Phosphorus')
    axs[i].set_title(f'TP vs {col.replace("_", " ")}')
plt.suptitle('Total Phosphorus vs Temperature (Current + Prior Days)', fontsize=16)
plt.tight_layout()
plt.show()

# === Total Phosphorus vs Day of Year ===
plt.figure(figsize=(10, 6))
plt.scatter(df['day_of_year'], df['Total_Phosphorus'], alpha=0.6, edgecolors='k')
plt.xlabel('Day of Year')
plt.ylabel('Total Phosphorus')
plt.title('Total Phosphorus vs Day of Year')
plt.grid(True)
plt.show()
