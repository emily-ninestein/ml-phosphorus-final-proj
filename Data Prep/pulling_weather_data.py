import requests
import pandas as pd
from datetime import datetime
import time

# Description: This script pulls weather data from NOAA API for the stations specified in noaa_filtered_stations.csv and saves it to a CSV file.

# NOAA API endpoint
url = "https://www.ncei.noaa.gov/cdo-web/api/v2/data"

# Replace with your valid API token
API_TOKEN = "GvzzpMCrHwOLgbXOzAQEqwFTNehegaVN"

# Define headers
headers = {"token": API_TOKEN}

# Load filtered stations
filtered_stations = pd.read_csv("noaa_filtered_stations.csv").to_dict("records")

# List to store all retrieved data
all_data = []

# Loop over each station and fetch its data
for station in filtered_stations:
    params = {
        "datasetid": "GHCND",
        "startdate": "1990-01-01",
        "enddate": "1990-12-31",
        "stationid": station["id"],  # Use the station's ID
        "datatypeid": ["AWND", "PRCP", "TAVG"], # Average wind speed (m/s), Precipitation (tenths of mm), Average temperature (tenths of degrees C)
        "limit": 1000,  # This is the max records per request
        "includemetadata": "false",
        "offset": 1  # Start at the first record
    }

    while True:
        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200:
            data = response.json().get("results", [])  # Extract results

            if not data:  # Stop when no more data
                break

            all_data.extend(data)  # Add to list
            params["offset"] += 1000  # Move to the next batch

            print(f"Retrieved {len(all_data)} records for station {station['id']}...")

        else:
            print(f"Error retrieving data for station {station['id']}: {response.status_code}")
            break
         
        time.sleep(1) # Delay to avoid hitting the API too hard

# Convert to Pandas DataFrame
df = pd.DataFrame(all_data)

# Save to CSV
csv_filename = "noaa_weather_data_avg_1990.csv"
df.to_csv(csv_filename, index=False)
print(f"Data saved to {csv_filename}")