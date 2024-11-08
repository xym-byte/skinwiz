'''
config.py - Configuration file for setting paths, headers, city data, and API information for the SkinWiz app.
This file centralizes all configuration-related information to make it easier to modify and maintain.

'''


# Paths for datasets
raw_dataset_folder_path = 'datasets/raw'
cleaned_dataset_folder_path = 'datasets/cleaned'
merged_dataset_path = 'datasets/merged/merged_data.csv'

# User's Downloads directory path (change accordingly)
download_dir = '/Users/rishika/Downloads'

# Headers for web scraping to mimic a browser request
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US, en;q=0.5'
}

# Centralized latitude and longitude data for major cities in the US
cities = {
    "New York City, NY": {"latitude": 40.7128, "longitude": -74.0060},
    "Los Angeles, CA": {"latitude": 34.0522, "longitude": -118.2437},
    "Chicago, IL": {"latitude": 41.8781, "longitude": -87.6298},
    "Houston, TX": {"latitude": 29.7604, "longitude": -95.3698},
    "Phoenix, AZ": {"latitude": 33.4484, "longitude": -112.0740},
    "Philadelphia, PA": {"latitude": 39.9526, "longitude": -75.1652},
    "San Antonio, TX": {"latitude": 29.4241, "longitude": -98.4936},
    "San Diego, CA": {"latitude": 32.7157, "longitude": -117.1611},
    "Dallas, TX": {"latitude": 32.7767, "longitude": -96.7970},
    "Pittsburgh, PA": {"latitude": 40.4406, "longitude": -79.9959}
}

# Base URL for the weather API used to fetch weather data
api_url = "https://api.open-meteo.com/v1/forecast"

