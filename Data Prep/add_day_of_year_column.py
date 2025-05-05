import pandas as pd

# Load the combined Excel sheet
df = pd.read_excel("merged_data_1990_to_2020.xlsx")

# Convert 'date' column to datetime if it isn't already
df["date"] = pd.to_datetime(df["date"], errors="coerce")

# Drop rows where date conversion failed
df = df.dropna(subset=["date"])

# Add day of year column
df["day_of_year"] = df["date"].dt.dayofyear

# Save the updated DataFrame
df.to_excel("merged_data_with_day_of_year.xlsx", index=False)

print("Day of year column added and saved to 'merged_data_with_day_of_year.xlsx'")
print(df[["date", "day_of_year"]].head())
