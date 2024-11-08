'''
run_scrapers.py

This module coordinates running all the scraping functions for collecting skincare ingredient data,
banned ingredient data, and Amazon product data. 

'''

from scrapers.skincare_ings_scrape import scrape_skincare_ingredients_dataset
from scrapers.banned_ings_scrape import scrape_banned_ingredients_dataset
from scrapers.amazon_data_scrape import scrape_amazon_products
from scrapers.demo_amazon_scrape import demo_scrape_amazon_products

def run_all_scrapers():
    scrape_skincare_ingredients_dataset()
    demo_scrape_amazon_products()
    scrape_banned_ingredients_dataset()
    # scrape_amazon_products() # Uncomment to scrape Amazon data (~4 hours)


if __name__ == "__main__":
    run_all_scrapers()