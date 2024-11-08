'''
plot_location.py

This module helps plot the input city location using its latitude and longitude coordinates.

'''

import geopandas as gpd
import matplotlib.pyplot as plt
import contextily as ctx
from shapely.geometry import Point

# Function to plot the latitude and longitude of a city and return the figure
def plot_city_location(lat, lon):
    # Create a GeoDataFrame for the city location
    city = gpd.GeoDataFrame(geometry=[Point(lon, lat)], crs="EPSG:4326")

    # Plot the city on a map with smaller figure size
    fig, ax = plt.subplots(figsize=(4, 4))  # Adjust figsize for a smaller plot
    
    # Remove white background
    fig.patch.set_alpha(0)

    # Plot the city location with a custom marker resembling a location dropper
    city.plot(ax=ax, color='red', marker='v', markersize=100)  # 'v' resembles a location marker

    # Set the limits to zoom out (increase the range around the city)
    ax.set_xlim([lon - 10, lon + 10])  # Zoom out horizontally
    ax.set_ylim([lat - 6, lat + 6])    # Zoom out vertically

    # Add a lightweight OpenStreetMap basemap at a lower zoom
    ctx.add_basemap(ax, zoom=4, source=ctx.providers.OpenStreetMap.Mapnik, crs=city.crs.to_string())

    # Set x and y axis labels with increased font size
    ax.set_xlabel("Longitude", fontsize=6.5)
    ax.set_ylabel("Latitude", fontsize=6.5)

    # Increase the font size of ticks
    ax.tick_params(axis='both', which='major', labelsize=4.5)

    # Add a title with larger font size
    ax.set_title('City Location in America', fontsize=8)

    return fig
