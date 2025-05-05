# Description: This script retrieves all weather stations in a bounding box and saves the data to a CSV file.
# The results are saved in noaa_filtered_stations.csv.

import requests
import pandas as pd

# NOAA API endpoint for stations
stations_url = "https://www.ncei.noaa.gov/cdo-web/api/v2/stations"

# Replace with your valid API token
API_TOKEN = "GvzzpMCrHwOLgbXOzAQEqwFTNehegaVN"

# Define headers
headers = {"token": API_TOKEN}

# Define parameters to retrieve stations in the bounding box
params = {
    "datasetid": "GHCND",
    "startdate": "2020-01-01",
    "enddate": "2020-12-31",
    "bbox": "45.2,-74.1,43.4,-72.4", # Bounding box for Lake Champlain Basin -- this doesn't seem to actually work though
    "datatypeid": ["PRCP", "TAVG", "AWND"],  # Ensure relevant stations by specifying desired measurements
    "limit": 1000,
    "includemetadata": "false",
    "offset": 1
}

# List to store all station data
stations = []

while True:
    response = requests.get(stations_url, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json().get("results", [])  # Extract results

        if not data:  # Stop when no more data
            break

        stations.extend(data)  # Add to list
        params["offset"] += 1000  # Move to the next batch

        print(f"Retrieved {len(stations)} stations so far...")

    else:
        print("Error:", response.status_code, response.text)
        break


filtered_stations = [
    s for s in stations
    if 43.4 <= s["latitude"] <= 45.2 and -74.1 <= s["longitude"] <= -72.4
]
print(f"Filtered stations count: {len(filtered_stations)}")

# Convert to Pandas DataFrame
df = pd.DataFrame(filtered_stations)

# Save to CSV
csv_filename = "noaa_filtered_stations.csv"
df.to_csv(csv_filename, index=False)
print(f"Data saved to {csv_filename}")
