import pandas as pd
import os

# Directory containing the .xls files

input_directory = f"phosphorus data files"
output_directory = "converted phosphorus files"
os.makedirs(output_directory, exist_ok=True)

for filename in os.listdir(input_directory):
    if filename.endswith(".xls"):
        input_path = os.path.join(input_directory, filename)
        output_filename = filename.replace(".xls", ".xlsx")
        output_path = os.path.join(output_directory, output_filename)
        
        try:
            with open(input_path, "rb") as f:
                header = f.read(8)
                is_html = header.startswith(b'\r\n') or b'<!DOCTYPE html' in header.lower()

            if is_html:
                print(f"Parsing HTML: {filename}")
                tables = pd.read_html(input_path)  # May return multiple tables
                df = tables[0]  # Assume the first one is the main table
            else:
                print(f"Parsing Excel: {filename}")
                df = pd.read_excel(input_path, engine='xlrd')

            df.to_excel(output_path, index=False, engine='openpyxl')
            print(f"Converted: {filename} -> {output_filename}")
        
        except Exception as e:
            print(f"Failed to convert {filename}: {e}")
