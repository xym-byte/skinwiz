'''
banned_ings_scrape.py

This module uses Selenium to scrape and download the dataset of banned ingredients from the ECHA website.
The downloaded file is renamed and moved to the raw dataset directory.

'''

from selenium import webdriver
from selenium.webdriver.common.by import By
import os
import time
from config import download_dir, raw_dataset_folder_path

def scrape_banned_ingredients_dataset():
    
    chrome_options = webdriver.ChromeOptions()
    prefs = {"download.default_directory": download_dir}
    chrome_options.add_experimental_option("prefs", prefs)

    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        driver.get("https://www.echa.europa.eu/web/guest/cosmetics-prohibited-substances?p_p_id=eucleflegislationlist_WAR_euclefportlet&p_p_lifecycle=0&p_p_state=normal&p_p_mode=view&_eucleflegislationlist_WAR_euclefportlet_cur=1&_eucleflegislationlist_WAR_euclefportlet_substance_identifier_field_key=&_eucleflegislationlist_WAR_euclefportlet_delta=50&_eucleflegislationlist_WAR_euclefportlet_doSearch=&_eucleflegislationlist_WAR_euclefportlet_deltaParamValue=50&_eucleflegislationlist_WAR_euclefportlet_orderByCol=fld_erc2_maxthres&_eucleflegislationlist_WAR_euclefportlet_orderByType=desc")
        time.sleep(5)
        accept_button = driver.find_element(By.ID, "_viewsubstances_WAR_echarevsubstanceportlet_acceptDisclaimerButton")
        accept_button.click()
        time.sleep(3)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        csv_button = driver.find_element(By.ID, "_eucleflegislationlist_WAR_euclefportlet_exportButtonCSV")
        driver.execute_script("arguments[0].scrollIntoView(true);", csv_button)
        time.sleep(1)
        csv_button.click()
        time.sleep(10)

        latest_file_path = os.path.join(download_dir, "cosmetic-products-regulation--annex-ii---prohibited-substances-export.csv")
        new_file_path =  os.path.join(raw_dataset_folder_path, "banned_skincare_ings.csv")
        
        if os.path.exists(latest_file_path):
            os.rename(latest_file_path, new_file_path)
            print(f"Dataset has been downloaded and renamed to '{new_file_path}'")
        else:
            print(f"No file named 'dataset' found in the download directory.")
        
    finally:
        driver.quit()

