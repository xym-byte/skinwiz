'''
run_cleaners.py

This module coordinates running all the cleaning functions for the scraped skincare ingredient data,
banned ingredient data, and Amazon product data. 

'''

from processing.skincare_ings_clean import clean_skincare_ingredients
from processing.banned_skincare_ings_clean import clean_banned_skincare_ingredients
from processing.amazon_data_clean import clean_amazon_data

def run_all_cleaners():
    clean_skincare_ingredients()
    clean_banned_skincare_ingredients()
    clean_amazon_data()

if __name__ == "__main__":
    run_all_cleaners()
