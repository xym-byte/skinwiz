'''
weather_api.py

This module handles fetching weather data, including the UV index, and calculating SPF recommendations based on the UV index using external API data.

'''

import requests
from config import cities, api_url

# SPF recommendation logic
def get_spf_recommendation(uv_index_max):
    if uv_index_max <= 2:
        return 0
    elif uv_index_max <= 5:
        return 15
    elif uv_index_max <= 7:
        return 30
    elif uv_index_max <= 10:
        return 50
    else:
        return 50

# Fetch weather data from API for the selected city using its latitude and longitude
def get_weather_data(selected_city):
    latitude = cities[selected_city]['latitude']
    longitude = cities[selected_city]['longitude']
    
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current_weather": "true",
        "daily": "uv_index_max",
        "timezone": "America/New_York"
    }
    
    response = requests.get(api_url, params=params)
    
    if response.status_code == 200:
        weather_data = response.json()
        current_temperature = weather_data['current_weather']['temperature']
        uv_index_max = weather_data['daily']['uv_index_max'][0]
        recommended_spf = get_spf_recommendation(uv_index_max)
        return current_temperature, uv_index_max, recommended_spf
    else:
        print(f"Failed to get data: {response.status_code}")
        return None, None, None
