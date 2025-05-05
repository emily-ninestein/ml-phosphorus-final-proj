import pandas as pd

# Define the years and the tests to filter
years = range(1990, 2021)
tests_of_interest = ["Dissolved Phosphorus", "Total Phosphorus"]

# List to collect all filtered dataframes
filtered_dfs = []

# Loop through each file
for year in years:
    file_path = f"phosphorus_data_{year}.xlsx"
    try:
        df = pd.read_excel(file_path)
        filtered_df = df[df["Test"].isin(tests_of_interest)]
        filtered_df["Year"] = year  # Add a column to keep track of the year
        filtered_dfs.append(filtered_df)
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"Error processing {file_path}: {e}")

# Concatenate all filtered dataframes
if filtered_dfs:
    combined_df = pd.concat(filtered_dfs, ignore_index=True)
    output_csv_path = "combined_filtered_phosphorus_data.csv"
    combined_df.to_csv(output_csv_path, index=False)
    print(f"Filtered data saved to {output_csv_path}")
else:
    print("No data was processed.")
