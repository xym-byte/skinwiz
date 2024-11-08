'''
demo_amazon_data_scrape.py

Same as amazon_data_scrape.py but just for the purpose of demoing the scraping on the Streamlit app since the actual scraping takes ~4 hours.

'''

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
from tqdm import tqdm
import os
from config import HEADERS, raw_dataset_folder_path

# Function to scrape Amazon product data
def demo_scrape_amazon_products():
    print("Starting the scraping process...")

    # Load and clean the skincare ingredients dataset
    skincare_ings_file_path = os.path.join(raw_dataset_folder_path, 'openml_dataset_43481.csv')
    skincare_ings_df = pd.read_csv(skincare_ings_file_path, skiprows=23, on_bad_lines='skip')

    # Clean column names and create product search list
    skincare_ings_df.columns = skincare_ings_df.columns.str.strip().str.replace("'", "")
    skincare_ings_df.dropna(subset=['LA MER', 'Crme de la Mer'], inplace=True)
    skincare_ings_df['brand_product'] = skincare_ings_df['LA MER'].astype(str) + ' ' + skincare_ings_df['Crme de la Mer'].astype(str)
    product_search_list = skincare_ings_df['brand_product'].unique().tolist()

    # Select 5 products to scrape for the demo
    product_search_list = product_search_list[2:7]

    print(product_search_list)

    # Configure Chrome options for the web driver
    chrome_options = Options()
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument(f"user-agent={HEADERS['User-Agent']}")

    driver = webdriver.Chrome(options=chrome_options)

    # Prepare a list to collect data across all pages
    all_data = []

    # Function to scrape data from each page
    def scrape_page():
        """Function to scrape product data from the current page."""
        html_content = driver.page_source
        soup = BeautifulSoup(html_content, 'html.parser')

        # Find all relevant <a> and <i> tags
        a_tags = soup.find_all('a', class_=["a-size-base-plus", "a-color-base", "a-text-normal", "s-underline-text"])
        i_tags = soup.find_all('i', class_=["a-icon", "a-icon-star-small", "a-star-small-4", "aok-align-bottom"])

        # Extract ratings from <i> tags
        ratings = [i.find('span', class_='a-icon-alt').text.strip() if i.find('span', 'a-icon-alt') else None for i in
                   i_tags]

        # Ensure both tag lengths are the same
        min_length = min(len(a_tags), len(i_tags))

        # Prepare data by combining text, rating, and hyperlink
        return [{'Link Text': a_tags[i].text.strip(), 'Rating': ratings[i], 'URL': f"https://www.amazon.com{a_tags[i]['href']}"} 
                for i in range(min_length)]


    # Function to search Amazon for a product and scrape the results
    def search_and_scrape(search_term):
        """Search for a product on Amazon and scrape the results."""
        # Remove quotes and special characters from the search term
        search_term = search_term.replace("'", "").replace('"', "").replace("&", "and")
        
        # Replace spaces with '+' to make the query valid
        search_term = search_term.lower().replace(" ", "+")
        
        search_url = f'https://www.amazon.com/s?k={search_term}'
        print(f"Searching Amazon: {search_url}")
        driver.get(search_url)

        time.sleep(random.uniform(3, 6))

        # Scrape the current page
        return scrape_page()


    # Iterate through each 'brand name + product name' and scrape data
    for search_term in tqdm(product_search_list, desc="Scraping Products", unit="product"):
        search_term = search_term.lower()
        print(f"Searching for: {search_term}")

        try:
            product_data = search_and_scrape(search_term)

            if product_data:
                all_data.extend(product_data)
            else:
                print(f"No data returned for search: {search_term}")

        except Exception as e:
            print(f"Error encountered while searching for '{search_term}': {e}")
            print("Saving collected data before exiting...")
            break

        time.sleep(random.uniform(5, 10))

    # Save data in a csv
    if all_data:
        skincare_ings_df = pd.DataFrame(all_data)
        filename = "demo_amazon_data.csv"
        output_path = os.path.join(raw_dataset_folder_path, filename)
        skincare_ings_df.to_csv(output_path, index=False)
        print("Scraping complete! Data saved to 'demo_amazon_data.csv'.")

    driver.quit()

