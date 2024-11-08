'''
skincare_ings_clean.py

Cleans the scraped openml_dataset_4341.csv which has skincare ingredients data.

'''

import pandas as pd
import re
import os
from config import raw_dataset_folder_path, cleaned_dataset_folder_path

def clean_skincare_ingredients():
    raw_file_path = os.path.join(raw_dataset_folder_path, 'openml_dataset_43481.csv')
    cleaned_file_path = os.path.join(cleaned_dataset_folder_path, 'skincare_ingredients.csv')
    
    # Ensure the cleaned directory exists
    os.makedirs(os.path.dirname(cleaned_file_path), exist_ok=True)

    # Read the file line by line
    with open(raw_file_path, 'r') as file:
        lines = file.readlines()

    # Find the @DATA line (where actual data starts)
    data_start = lines.index('@DATA\n') + 1

    # Extract only the data part (skip metadata)
    data_lines = lines[data_start:]

    # Convert the data into a list of lists, handling quotes and commas properly
    cleaned_data = []
    for line in data_lines:
        # Split on commas but respect quoted substrings
        row = re.findall(r"(?:'[^']*'|[^,]+)", line.strip())
        # Remove quotes around string values
        row = [re.sub(r"^'|'$", '', item.strip()) for item in row]
        cleaned_data.append(row)

    # Define the column names based on the @ATTRIBUTE section
    columns = [
        "Label", "Brand", "Name", "Price", "Rank", "Ingredients",
        "Combination", "Dry", "Normal", "Oily", "Sensitive"
    ]

    # Ensure that only rows with 11 columns are processed
    cleaned_data = [row for row in cleaned_data if len(row) == len(columns)]

    # Create a DataFrame from the cleaned data
    df = pd.DataFrame(cleaned_data, columns=columns)

    # Convert data types
    df['Price'] = pd.to_numeric(df['Price'], errors='coerce')
    df['Rank'] = pd.to_numeric(df['Rank'], errors='coerce')
    df[['Combination', 'Dry', 'Normal', 'Oily', 'Sensitive']] = df[
        ['Combination', 'Dry', 'Normal', 'Oily', 'Sensitive']].apply(pd.to_numeric, errors='coerce')

    # Handle missing values (fill NaN with empty strings or appropriate values)
    df.fillna('', inplace=True)

    # Save the cleaned data
    df.to_csv(cleaned_file_path, index=False)

    print(f"Data cleaned and saved to '{cleaned_file_path}'")
