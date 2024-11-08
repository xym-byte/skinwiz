'''
skincare_ings_scrape.py

Uses Selenium to scrape and download a skincare ingredients dataset from OpenML and moves the downloaded file to the appropriate raw dataset directory.

'''

from selenium import webdriver
from selenium.webdriver.common.by import By
import os
import time
from config import download_dir, raw_dataset_folder_path

def scrape_skincare_ingredients_dataset():
    
    chrome_options = webdriver.ChromeOptions()
    prefs = {"download.default_directory": download_dir}
    chrome_options.add_experimental_option("prefs", prefs)

    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        driver.get("https://www.openml.org/search?type=data&status=active&id=43481&sort=runs")
        time.sleep(3)
        download_button = driver.find_element(By.CSS_SELECTOR, "a[href*='download/22102306/dataset']")
        download_button.click()
        time.sleep(5)

       # Look for the file named 'dataset' in the download directory
        latest_file_path = os.path.join(download_dir, "dataset")
        new_file_path =  os.path.join(raw_dataset_folder_path, "openml_dataset_43481.csv")
        
        if os.path.exists(latest_file_path):
            os.rename(latest_file_path, new_file_path)
            print(f"Dataset has been downloaded and renamed to '{new_file_path}'")
        else:
            print(f"No file named 'dataset' found in the download directory.")
        
    finally:
        driver.quit()

