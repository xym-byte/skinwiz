'''
process_data.py

Filters and merges all the cleaned datasets into one large dataframe and stores it.

'''

import pandas as pd
import os
from tqdm import tqdm
from config import cleaned_dataset_folder_path, merged_dataset_path
import re

def filter_skincare_ings(skincare_ings, banned_ings):
    # Remove duplicates from both datasets
    banned_ings_cleaned = banned_ings.drop_duplicates()
    skincare_ings_cleaned = skincare_ings.drop_duplicates()

    # Extract relevant banned ingredients and convert to lowercase
    banned_ings_list = banned_ings_cleaned['Name'].dropna().unique()
    banned_ings_list = [ing.lower() for ing in banned_ings_list]

    # Convert the entire dataframe to lowercase for case-insensitive matching
    skincare_ings_cleaned = skincare_ings_cleaned.apply(lambda x: x.astype(str).str.lower())

    # Filter the dataframe to exclude products with banned ingredients
    filtered_skincare_df = skincare_ings_cleaned[~skincare_ings_cleaned['Ingredients'].apply(
        lambda ing: any(banned_ing in ing for banned_ing in banned_ings_list))]

    # Replace "lncme" with "lancome" in the 'Brand' column
    filtered_skincare_df['Brand'] = filtered_skincare_df['Brand'].str.replace('lncme', 'lancome', case=False)

    # Replace any occurrence of 'crme' with 'creme' in all columns (already in lowercase)
    filtered_skincare_df = filtered_skincare_df.replace('crme', 'creme', regex=True)

    return filtered_skincare_df

def extract_spf(text):
    # Regular expression to find 'SPF' followed by a number
    spf_match = re.search(r'spf\s*(\d+)', text, re.IGNORECASE)
    if spf_match:
        # If SPF is found, return the number
        return int(spf_match.group(1))
    else:
        # If no SPF is found, return 0
        return 0
    
def check_ingredients(ingredients, ingredient_list):
    ingredients = ingredients.lower()  # Make the search case-insensitive
    return int(any(ingredient in ingredients for ingredient in ingredient_list))

def process_and_merge_data():
    # Load datasets
    banned_ings = pd.read_csv(os.path.join(cleaned_dataset_folder_path, "banned_skincare_ings.csv"))
    skincare_ings = pd.read_csv(os.path.join(cleaned_dataset_folder_path, "skincare_ingredients.csv"))
    
    skincare_df = filter_skincare_ings(skincare_ings, banned_ings)
    amazon_df = pd.read_csv(os.path.join(cleaned_dataset_folder_path, "amazon_data.csv"))

    # Combine 'Brand' and 'Name' from skincare_df to create a matching field
    skincare_df['Brand_Name'] = skincare_df['Brand'] + " " + skincare_df['Name']

    # Preprocess: tokenize product names and convert to lowercase
    skincare_df['Tokenized'] = skincare_df['Brand_Name'].str.lower().str.split()
    amazon_df['Tokenized'] = amazon_df['Product'].str.lower().str.split()

    # Convert tokenized words to sets
    skincare_df['Tokenized_Set'] = skincare_df['Tokenized'].apply(set)
    amazon_df['Tokenized_Set'] = amazon_df['Tokenized'].apply(set)

    # Use tqdm progress bar for faster processing
    print("Processing matches:")
    matched_rows = []

    # Efficiently perform the matching with apply and set intersections
    for i, skin_row in tqdm(skincare_df.iterrows(), total=skincare_df.shape[0], desc="Skincare Products"):
        skincare_set = skin_row['Tokenized_Set']
        # Create a mask to filter matching rows from amazon_df
        mask = amazon_df['Tokenized_Set'].apply(lambda x: skincare_set.issubset(x))
        matched_amazon_rows = amazon_df[mask]
        
        # If matches are found, combine the rows
        for _, amazon_row in matched_amazon_rows.iterrows():
            combined_row = {**skin_row.to_dict(), **amazon_row.to_dict()}
            matched_rows.append(combined_row)

    # Convert the matched rows into a new dataframe
    matched_df = pd.DataFrame(matched_rows)

    matched_df['Price'] = matched_df['Price'].replace('[\$,]', '', regex=True).astype(float)

    # Sort by 'Product' and 'Price' to get the lowest price per product
    matched_df = matched_df.sort_values(by=['Product', 'Price'])

    # Drop duplicates by keeping the row with the lowest price for each 'Product'
    matched_df = matched_df.drop_duplicates(subset='Product', keep='first')

    matched_df['SPF'] = matched_df.apply(lambda row: max(extract_spf(row['Brand_Name']), extract_spf(row['Product'])), axis=1)

    acne_ingredients = ['salicylic acid', 'benzoyl peroxide', 'retinol']
    brightening_ingredients = ['vitamin c', 'vitamin-c' 'niacinamide', 'alpha-arbutin']
    hydration_ingredients = ['hyaluronic acid', 'glycerin', 'ceramide']
    anti_aging_ingredients = ['retinol', 'peptides', 'vitamin c', 'vitamin-c']

    # Add new columns to the dataframe
    matched_df['Acne'] = matched_df['Ingredients'].apply(lambda x: check_ingredients(x, acne_ingredients))
    matched_df['Brightening'] = matched_df['Ingredients'].apply(lambda x: check_ingredients(x, brightening_ingredients))
    matched_df['Hydration'] = matched_df['Ingredients'].apply(lambda x: check_ingredients(x, hydration_ingredients))
    matched_df['Anti_Aging'] = matched_df['Ingredients'].apply(lambda x: check_ingredients(x, anti_aging_ingredients))

    matched_df = matched_df.drop(columns=['Tokenized', 'Tokenized_Set'], errors='ignore')

    matched_df.to_csv(merged_dataset_path, index=False)
    print(f"Data processed and saved to '{merged_dataset_path}'")

    # Print the shapes of the dataframes
    # print("\nDataframe shapes:")
    # print(f"Skincare DataFrame shape: {skincare_df.shape}")
    # print(f"Amazon DataFrame shape: {amazon_df.shape}")
    # print(f"Merged DataFrame shape: {matched_df.shape}")



