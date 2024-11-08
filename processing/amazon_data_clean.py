'''
amazon_data_clean.py

Cleans the scraped amazon_data.csv file

'''

import pandas as pd
import numpy as np
import os
from config import raw_dataset_folder_path, cleaned_dataset_folder_path

def clean_amazon_data():
    
    raw_file_path = os.path.join(raw_dataset_folder_path, 'amazon_data.csv')
    cleaned_file_path = os.path.join(cleaned_dataset_folder_path, 'amazon_data.csv')

    # Read the raw CSV file
    df = pd.read_csv(raw_file_path)

    # Create a table containing Link Text and URL
    df_link_text = df[['Link Text', 'URL']].copy()  # Copy Link Text and URL columns

    # Remove unwanted rows based on specific keywords
    unwanted_phrases = [
        'new offer', 'Learn more', 'Visit the help section', 'contact us', 
        'Remove', 'Leave ad feedback', 'Refresh Your BeautyRefresh Your Beauty',
        'CleansersCleansers', 'Best SellersBest Sellers', 'MasksMasks'
    ]
    for phrase in unwanted_phrases:
        df_link_text = df_link_text[~df_link_text['Link Text'].str.contains(phrase, na=False)]

    # Initialize a list to store the transposed data
    transposed_data = []
    i = 0  # Initialize the index to 0

    # Iterate over the DataFrame until all rows are processed
    while i < len(df_link_text):
        product, review_count, price, url = None, np.nan, np.nan, None

        # Extract product, review count, and price in groups of 3
        if i < len(df_link_text):
            product = df_link_text.iloc[i]['Link Text']
        if i + 1 < len(df_link_text):
            review_count_value = df_link_text.iloc[i + 1]['Link Text']
            if pd.notna(review_count_value) and str(review_count_value).replace(',', '').isdigit():
                review_count = review_count_value.replace(',', '')  # Clean commas in review count
        if i + 2 < len(df_link_text):
            price_value = df_link_text.iloc[i + 2]['Link Text']
            if pd.notna(price_value) and str(price_value).startswith('$'):
                price = price_value.split('(')[0]  # Remove nested details in parentheses
                price = '$' + price.split('$')[1] if '$' in price else price  # Keep only one price
                url = df_link_text.iloc[i + 2]['URL'].split('?')[0]  # Clean URL to remove query parameters

                # Fix for malformed URLs
                if pd.notna(url):
                    if url.count('https://') > 1:
                        url = url[url.find('https://', url.find('https://') + 1):]  # Keep the second part of malformed URL

        # Append the transposed data
        transposed_data.append([product, review_count, price, url])

        # Move to the next group of rows
        next_group_size = 3 if pd.notna(review_count) and pd.notna(price) else 2 if pd.isna(review_count) or pd.isna(price) else 1
        i += next_group_size

    # Convert the transposed data to a DataFrame
    transposed_df = pd.DataFrame(transposed_data, columns=['Product', 'Review Count', 'Price', 'URL'])

    # Clean the Rating column
    df_rating = df[['Rating']].copy().dropna().reset_index(drop=True)
    df_rating['Rating'] = df_rating['Rating'].apply(lambda x: x.split(' ')[0] if pd.notna(x) else x)  # Extract numeric rating

    # Ensure both transposed_df and df_rating have the same number of rows
    if len(transposed_df) > len(df_rating):
        transposed_df = transposed_df.iloc[:len(df_rating)]
    elif len(df_rating) > len(transposed_df):
        df_rating = df_rating.iloc[:len(transposed_df)]

    # Combine the two DataFrames
    final_df = pd.concat([transposed_df.reset_index(drop=True), df_rating.reset_index(drop=True)], axis=1).dropna()

    # Save the cleaned data to a new CSV file
    final_df.to_csv(cleaned_file_path, index=False)
    print(f"Data cleaned and saved to '{cleaned_file_path}'")
