import pandas as pd
import os

# Folder containing the weather CSV files
weather_folder = "weather data files"

# List to hold individual dataframes
weather_dfs = []

# Loop through each CSV file in the folder
for filename in os.listdir(weather_folder):
    if filename.endswith(".csv"):
        filepath = os.path.join(weather_folder, filename)
        print(f"Reading {filename}...")
        df = pd.read_csv(filepath, parse_dates=["date"])
        weather_dfs.append(df)

# Combine all weather data into a single DataFrame
combined_weather_df = pd.concat(weather_dfs, ignore_index=True)

# Optional: sort by date
combined_weather_df.sort_values("date", inplace=True)

# Save to a single CSV file
output_path = "combined_weather_data.csv"
combined_weather_df.to_csv(output_path, index=False)

print(f"Combined weather data saved to '{output_path}'")
print(combined_weather_df.head())
