'''
recommendation.py

This module provides functions for recommending skincare products, filtering results, and handling SPF recommendations based on UV index and user preferences. 
It processes and loads data, calculates skin type compatibility, and applies filters for skincare products and sunscreens.

'''

import pandas as pd
from sklearn.preprocessing import LabelEncoder

# Get recommended SPF based on UV index
def get_spf_recommendation(uv_index_max):
    if uv_index_max <= 2:
        return 0
    elif uv_index_max <= 5:
        return 0
    elif uv_index_max <= 7:
        return 30
    elif uv_index_max <= 10:
        return 50
    else:
        return 50

# Load and clean product data
def load_data(file_path):
    df = pd.read_csv(file_path)
    df = df[pd.to_numeric(df['Rating'], errors='coerce').notnull()]
    df['Price'] = df['Price'].astype(float)
    skin_type_columns = ['Combination', 'Dry', 'Normal', 'Oily', 'Sensitive']
    for col in skin_type_columns:
        df[col] = df[col].astype(int)
    return df

# Recommend products based on skin type, product type, and UV index
def recommend_products(df, product_labels, skin_type_suitability, uv_index_max):
    spf_recommended = get_spf_recommendation(uv_index_max)

    label_encoder_product = LabelEncoder()
    df['Label'] = label_encoder_product.fit_transform(df['Label'])

    skin_type_columns = ['Combination', 'Dry', 'Normal', 'Oily', 'Sensitive']
    user_skin_type_binary = [1 if skin_type in skin_type_suitability else 0 for skin_type in skin_type_columns]

    df['Skin Type Match Score'] = df[skin_type_columns].dot(user_skin_type_binary)

    all_filtered_products = pd.DataFrame()

    for product_label in product_labels:
        product_label_encoded = label_encoder_product.transform([product_label])[0]
        filtered_products = df[df['Label'] == product_label_encoded].copy()
        filtered_products = filtered_products[filtered_products['SPF'] >= spf_recommended]
        filtered_products = filtered_products.sort_values(by='Skin Type Match Score', ascending=False)
        filtered_products['Label'] = label_encoder_product.inverse_transform(filtered_products['Label'])
        all_filtered_products = pd.concat([all_filtered_products, filtered_products], ignore_index=True)

    return all_filtered_products

# Filter products based on exact matches for skin type, price range, and skincare improvements
def filter_exact_matches(recommended_df, product_labels, skin_type_suitability, skincare_improvement, price_range, age):
    conditions = [(recommended_df[skin_type] == 1) for skin_type in skin_type_suitability]

    skin_type_condition = conditions[0]
    for condition in conditions[1:]:
        skin_type_condition &= condition

    skincare_columns = ['Acne', 'Brightening', 'Hydration', 'Anti_Aging']

    if skincare_improvement:
        skincare_condition = recommended_df[skincare_columns][skincare_improvement].any(axis=1)
    else:
        skincare_condition = pd.Series([True] * len(recommended_df), index=recommended_df.index)

    # Check if the user is above 30 and adding Anti-aging
    if age > 30:
        anti_aging_condition = recommended_df['Anti_Aging'] == 1
    else:
        anti_aging_condition = pd.Series([True] * len(recommended_df), index=recommended_df.index)

    filtered_products_list = []

    # Filter and recommend products for each product label
    for product_label in product_labels:
        filtered_products = recommended_df[
            (recommended_df['Label'] == product_label) &
            skin_type_condition &
            skincare_condition &
            (recommended_df['Price'] >= price_range[0]) &
            (recommended_df['Price'] <= price_range[1]) &
            anti_aging_condition
        ]

        filtered_products = filtered_products.drop_duplicates(subset='Name')
        filtered_products = filtered_products.sort_values(by='Rating', ascending=False)
        top_5_products = filtered_products.head(5)

        filtered_products_list.append(top_5_products)

    return pd.concat(filtered_products_list, ignore_index=True) if filtered_products_list else pd.DataFrame()

# Recommend sunscreens based on skin type, SPF recommendation, and price range
def recommend_sunscreens(df, user_skin_type_suitability, price_range, uv_index_max):
    spf_recommended = get_spf_recommendation(uv_index_max)

    label_encoder_product = LabelEncoder()
    df['Label'] = label_encoder_product.fit_transform(df['Label'])

    skin_type_columns = ['Combination', 'Dry', 'Normal', 'Oily', 'Sensitive']
    user_skin_type_binary = [1 if skin_type in user_skin_type_suitability else 0 for skin_type in skin_type_columns]
    df['Skin Type Match Score'] = df[skin_type_columns].dot(user_skin_type_binary)

    skin_type_condition = df[skin_type_columns].dot(user_skin_type_binary) > 0
    spf_condition = df['SPF'] >= spf_recommended
    price_condition = (df['Price'] >= price_range[0]) & (df['Price'] <= price_range[1])

    filtered_products = df[skin_type_condition & spf_condition & price_condition]

    filtered_products = filtered_products.drop_duplicates(subset='Name')
    filtered_products = filtered_products.sort_values(by='Rating', ascending=False)

    top_5_products = filtered_products.head(5)
    top_5_products['Label'] = label_encoder_product.inverse_transform(top_5_products['Label'])

    return top_5_products
