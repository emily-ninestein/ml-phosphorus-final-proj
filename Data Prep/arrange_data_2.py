import pandas as pd

# Load the phosphorus data
phosphorus_df = pd.read_csv("combined_filtered_phosphorus_data.csv", parse_dates=["Date"])

# Load the weather data
weather_df = pd.read_csv("combined_weather_data.csv", parse_dates=["date"])

# Rename phosphorus 'Date' column to match weather data
phosphorus_df.rename(columns={"Date": "date"}, inplace=True)

# Transform weather dataframe to have columns: date, temperature, precipitation, and wind speed
weather_pivot = weather_df.pivot_table(
    index="date", 
    columns="datatype", 
    values="value", 
    aggfunc="mean"  # Average values for each date
).reset_index()

# Rename columns for clarity
weather_pivot.columns.name = None  # Remove MultiIndex column names
weather_pivot.rename(columns={"PRCP": "Precipitation", "TAVG": "Temperature", "AWND": "Windspeed"}, inplace=True)

# Ensure missing weather columns are added (in case any type is missing)
for col in ["Temperature", "Precipitation", "Windspeed"]:
    if col not in weather_pivot.columns:
        weather_pivot[col] = None

# Create lagged weather columns (1 to 5 days prior)
for lag in range(1, 6):
    weather_pivot[f"Temperature_{lag}d_ago"] = weather_pivot["Temperature"].shift(lag)
    weather_pivot[f"Precipitation_{lag}d_ago"] = weather_pivot["Precipitation"].shift(lag)
    weather_pivot[f"Windspeed_{lag}d_ago"] = weather_pivot["Windspeed"].shift(lag)

# Transform phosphorus dataframe to have columns: date, total phosphorus, dissolved phosphorus
phosphorus_pivot = phosphorus_df.pivot_table(
    index="date", 
    columns="Test", 
    values="Result", 
    aggfunc="mean"  # Average values for each date
).reset_index()

# Rename columns for clarity
phosphorus_pivot.columns.name = None
phosphorus_pivot.rename(columns={"Total Phosphorus": "Total_Phosphorus", "Dissolved Phosphorus": "Dissolved_Phosphorus"}, inplace=True)

# Merge the two dataframes on the date column
merged_df = pd.merge(phosphorus_pivot, weather_pivot, on="date", how="left")

# Define the correct column order
column_order = ["date", "Dissolved_Phosphorus", "Total_Phosphorus"]

# Add the weather columns in the desired order
column_order += ["Temperature", "Precipitation", "Windspeed"]

# Add the lagged columns in the same order as the main weather variables
for lag in range(1, 6):
    column_order += [f"Temperature_{lag}d_ago", f"Precipitation_{lag}d_ago", f"Windspeed_{lag}d_ago"]

# Reorder the dataframe
merged_df = merged_df[column_order]

# Save the dataframe to Excel
merged_df.to_excel("merged_data_with_lags_reordered.xlsx", index=False)

print("Data successfully merged and saved to 'merged_data_with_lags_reordered.xlsx'")
print(merged_df.head())
