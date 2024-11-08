'''
plot_stats.py

This module helps plot visualizations to display some skincare statistics.

'''

import pandas as pd
import matplotlib.pyplot as plt
from config import merged_dataset_path

# Function to plot Top 10 Most Highly Rated and Reviewed Products
def plot_top_rated_reviewed():
    df = pd.read_csv(merged_dataset_path)

    df['Review Count'] = pd.to_numeric(df['Review Count'], errors='coerce')
    df['Rating'] = pd.to_numeric(df['Rating'], errors='coerce')

    df['Brand_Name'] = df['Brand_Name'].str.title()

    top_10_products = df.sort_values(by=['Rating', 'Review Count'], ascending=[False, False]).head(10)

    fig, ax = plt.subplots(figsize=(10, 6), facecolor='none')

    ax.barh(top_10_products['Brand_Name'], top_10_products['Review Count'], color='lightblue', label='Review Count')

    for index, value in enumerate(top_10_products['Rating']):
        ax.text(top_10_products['Review Count'].iloc[index] + 1, index, f'Rating: {value:.1f}', va='center', fontsize=10, color='black')

    ax.set_xlabel('Review Count')
    ax.set_ylabel('Product Name')

    ax.set_title('Top 10 Most Highly Rated and Reviewed Products')
    ax.legend()
    plt.tight_layout()

    return fig

# Function to plot Boxplot of Price for Each Product Type
def plot_price_dist_product_types():
    df = pd.read_csv(merged_dataset_path)

    df['Label'] = df['Label'].str.title()

    fig, ax = plt.subplots(figsize=(10, 6), facecolor='none')

    df.boxplot(column='Price', by='Label', grid=False, vert=False, patch_artist=True,
               ax=ax, boxprops=dict(facecolor='pink'),
               flierprops=dict(marker='o', color='red', markersize=6))

    ax.set_title('Boxplot of Price for Each Product Type')
    ax.set_xlabel('Price (in $)')
    ax.set_ylabel('Product Type')
    plt.suptitle('')
    plt.tight_layout()

    return fig
