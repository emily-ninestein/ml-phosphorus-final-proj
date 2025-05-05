import requests
import pandas as pd
from datetime import datetime, timedelta
import time
from collections import defaultdict

# NOAA API endpoint and token
url = "https://www.ncei.noaa.gov/cdo-web/api/v2/data"
API_TOKEN = "GvzzpMCrHwOLgbXOzAQEqwFTNehegaVN"
headers = {"token": API_TOKEN}

# Load filtered station list
filtered_stations = pd.read_csv("noaa_filtered_stations.csv").to_dict("records")

# Get past 7 days: yesterday and 6 days before
today = datetime.utcnow().date()
dates = [(today - timedelta(days=i)).isoformat() for i in range(1, 8)]
dates.reverse()  # Oldest to newest

# Store results by date and data type
daily_averages = {date: {"Temperature": [], "Precipitation": [], "Windspeed": []} for date in dates}

# Pull data from NOAA API for each station
for station in filtered_stations:
    for date in dates:
        params = {
            "datasetid": "GHCND",
            "startdate": date,
            "enddate": date,
            "stationid": station["id"],
            "datatypeid": ["TAVG", "PRCP", "AWND"],
            "limit": 1000,
            "includemetadata": "false",
        }

        try:
            response = requests.get(url, headers=headers, params=params)
            if response.status_code == 200:
                results = response.json().get("results", [])
                for r in results:
                    if r["datatype"] == "TAVG":
                        daily_averages[date]["Temperature"].append(r["value"] / 10)  # tenths of °C to °C
                    elif r["datatype"] == "PRCP":
                        daily_averages[date]["Precipitation"].append(r["value"] / 10)  # tenths of mm to mm
                    elif r["datatype"] == "AWND":
                        daily_averages[date]["Windspeed"].append(r["value"])  # m/s
            else:
                print(f"Error {response.status_code} for station {station['id']} on {date}")
        except Exception as e:
            print(f"Request failed for station {station['id']} on {date}: {e}")

        time.sleep(0.5)  # avoid rate limiting

# Find most recent date with full data
valid_reference_index = None
for i in reversed(range(len(dates))):
    day_data = daily_averages[dates[i]]
    if all(day_data[key] for key in ["Temperature", "Precipitation", "Windspeed"]):
        valid_reference_index = i
        break

if valid_reference_index is None or valid_reference_index < 5:
    raise ValueError("Not enough recent days with complete data for temperature, precipitation, and windspeed.")

# Build final output row
ref_date = dates[valid_reference_index]
row = {
    "date": ref_date,
    "Dissolved_Phosphorus": "",
    "Total_Phosphorus": "",
}

# Current day
T = daily_averages[ref_date]["Temperature"]
P = daily_averages[ref_date]["Precipitation"]
W = daily_averages[ref_date]["Windspeed"]
row["Temperature"] = sum(T)/len(T)
row["Precipitation"] = sum(P)/len(P)
row["Windspeed"] = sum(W)/len(W)

# 1 to 5 days ago
for offset in range(1, 6):
    past_date = dates[valid_reference_index - offset]
    T = daily_averages[past_date]["Temperature"]
    P = daily_averages[past_date]["Precipitation"]
    W = daily_averages[past_date]["Windspeed"]
    row[f"Temperature_{offset}d_ago"] = sum(T)/len(T) if T else None
    row[f"Precipitation_{offset}d_ago"] = sum(P)/len(P) if P else None
    row[f"Windspeed_{offset}d_ago"] = sum(W)/len(W) if W else None

# Add day of year
row["day_of_year"] = datetime.strptime(ref_date, "%Y-%m-%d").timetuple().tm_yday

# Create and save Excel file
df_out = pd.DataFrame([row])
df_out.to_excel("weather_6_day_avg_output.xlsx", index=False)
print(f"Exported weather data ending on {ref_date} to Excel.")
