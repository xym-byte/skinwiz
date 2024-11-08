'''
banned_skincare_ings_clean.py

Cleans the scraped banned_skincare_ings.csv file

'''

import pandas as pd
import re
import os
from config import raw_dataset_folder_path, cleaned_dataset_folder_path

def clean_banned_skincare_ingredients():
    raw_file_path = os.path.join(raw_dataset_folder_path, 'banned_skincare_ings.csv')
    cleaned_file_path = os.path.join(cleaned_dataset_folder_path, 'banned_skincare_ings.csv')

    # Ensure the cleaned directory exists
    os.makedirs(os.path.dirname(cleaned_file_path), exist_ok=True)

    # Read the file line by line
    with open(raw_file_path, 'r', encoding='utf-8') as f:
        raw_data = f.read()

    # Split the raw data into rows
    rows = raw_data.split("\n")
    
    # Locate the actual start of the data by skipping any irrelevant rows
    start_data_index = 0
    for i, row in enumerate(rows):
        if "Name" in row and "EC No." in row:
            start_data_index = i
            break
    
    # Extract the actual header from the identified row
    header_row = rows[start_data_index].replace('"', '').split("\t")
    
    # Get the actual data starting from the row after the header
    data_rows = rows[start_data_index + 1:]
    
    # Clean the rows by splitting and removing extra quotes
    cleaned_rows = []
    for row in data_rows:
        columns = row.replace('"', '').split("\t")
        if len(columns) == len(header_row):  # Ensure the number of columns matches the headers
            cleaned_rows.append(columns)
    
    # Create DataFrame using the identified header row
    df = pd.DataFrame(cleaned_rows, columns=header_row)
    
    # Drop any rows that are completely empty
    df = df.dropna(how='all')

    # Reset index to ensure it's clean
    df = df.reset_index(drop=True)

    df = df[df['Restriction(s)'].str.startswith('Not permitted for all products', na=False)]

    df.to_csv(cleaned_file_path, index=False)

    print(f"Data cleaned and saved to '{cleaned_file_path}'")