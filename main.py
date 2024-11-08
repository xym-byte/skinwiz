'''
main.py

This file contains the main logic for the SkinWiz app's Streamlit web interface and serves as the entry point to the code.
It imports and calls methods for data scraping, cleaning, processing, getting results of API calls, running recommendation logic, and handling user input and output.

Andrew IDs:
Rishika Dwaraghanath - rthiruve@andrew.cmu.edu
Xinyue Meng - xinyuem@andrew.cmu.edu
Afifa Iqbal - afifai@andrew.cmu.edu
Lydia Abebe - labebe@andrew.cmu.edu

'''

from scrapers.run_scrapers import run_all_scrapers
from processing.run_cleaners import run_all_cleaners
from processing.process_data import process_and_merge_data
import streamlit as st
from user_input import get_user_input
from recommendation import load_data, recommend_products, filter_exact_matches, recommend_sunscreens
from weather_api import get_weather_data
from config import merged_dataset_path, cities
from streamlit_extras.stylable_container import stylable_container
from plots.plot_location import plot_city_location
from plots.plot_stats import plot_top_rated_reviewed, plot_price_dist_product_types

# Page Configuration
st.set_page_config(page_title="Skin Wiz App")

# Custom styles for the background and UI elements
page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] {{
    background-image: url("https://i.imgur.com/bNcJRd0.png");
    background-size: cover;
    background-position: left center;
    background-repeat: no-repeat;
}}

[data-testid="stHeader"] {{
    background: rgba(0,0,0,0);
}}

h1 {{
    color: #000000;
    font-size: 2.75em;
    font-weight: 625;
    text-align: center;
}}

h2 {{
    color: #000000;
    font-size: 1.5em;
}}

[data-testid="stText"] {{
    color: #ffffff;
    font-size: 1.2em;
}}

[data-testid="stCheckbox"] label {{
    font-size: 1.2em;
    color: #ffffff;
}}

button[data-testid="stButton"] {{
    background-color: #0f4c75;
    color: #ffffff;
    font-size: 1.2em;
    border-radius: 8px;
}}

input {{
    background-color: #0f4c75;
    color: #ffffff;
}}

select {{
    background-color: #0f4c75;
    color: #ffffff;
}}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

# Header and Introduction Section
header = st.container()
with header:
    st.title("Welcome to SkinWiz: Your Personalized Skincare Recommender")

# User Input Section
user_input_container = st.container()

with user_input_container:
    st.header("Fill out your information below")

   # Collecting user inputs
    name, age, location_name, location_data, user_input_labels, user_input_skin_type, user_input_skincare_improvement, user_input_price_range = get_user_input()

    # Option to rerun scrapers and cleaners
    run_all_processes = st.checkbox("Run data scrapers and cleaners again?")

    # Button for generating recommendations
    with stylable_container(
        "pink_button",
        css_styles="""
        button {
            background-color: #F4C2C2;
            color: white;
        }""",
    ):
        rec_button = st.button("Click to Get Recommendations!", key="recommend_button")

    # Main Logic for recommendation
    if rec_button:
        if not name:
            st.error("Name is required.")
        elif not user_input_skin_type:
            st.error("Please select at least one skin type.")
        elif not user_input_labels:
            st.error("Please select at least one skincare product type.")
        elif not user_input_skincare_improvement:
            st.error("Please select at least one skincare improvement.")
        else:
            if run_all_processes:
                try:
                    st.write("Scraping and cleaning data from the web. Please wait...")
                    run_all_scrapers()
                    st.write("Scrapers ran successfully.")
                    run_all_cleaners()
                    st.write("Cleaners ran successfully.")
                    process_and_merge_data()
                    st.write("Data merged successfully.")
                except Exception as e:
                    st.write(f"Error running scrapers/cleaners/merge: {e}")

            st.markdown(f"### Hey **{name}**! 😄")
            st.write("Thanks for using Skin Wiz! We've got some awesome skincare recommendations coming your way.")

            # Fetching weather data from API
            try:
                current_temperature, uv_index_max, recommended_spf = get_weather_data(location_name)
            except Exception as e:
                st.write(f"Error fetching weather data: {e}")

            # Recommend products
            try:
                recommended_df = recommend_products(load_data(merged_dataset_path), user_input_labels, user_input_skin_type, uv_index_max)
            except Exception as e:
                st.write(f"Error generating recommendations: {e}")

            # Fetching recommendations
            for label in user_input_labels:
                capitalized_label = label.title()
                st.write(f"**Recommended Products for {capitalized_label}:**")
                try:
                    filtered_products = filter_exact_matches(recommended_df, [label], user_input_skin_type, user_input_skincare_improvement, user_input_price_range, age)
                except Exception as e:
                    st.write(f"Error filtering products: {e}")

                if not filtered_products.empty:
                    st.dataframe(filtered_products[['Product', 'Price', 'Rating', 'Review Count', 'Ingredients', 'URL']])
                else:
                    st.write(f"Oops! It looks like we couldn’t find any products that match your criteria for {capitalized_label} right now. But don’t worry—we’re constantly expanding our datasets to include more options. Check back soon for new recommendations tailored just for you!")
            
            # Display weather information
            if current_temperature is not None:
                st.markdown(f"### <span style='font-size: 0.85em;'>You are from</span> **{location_name}**!", unsafe_allow_html=True)

                if location_name in cities:
                    lat = cities[location_name]["latitude"]
                    lon = cities[location_name]["longitude"]

                    # Plotting the city location
                    fig = plot_city_location(lat, lon)
                    st.pyplot(fig)
                else:
                    st.write(f"Coordinates for {location_name} not found.")

                st.write(f"The current temperature is {current_temperature}°C, and the maximum UV index is {uv_index_max}.")
                st.write(f"Recommended SPF for today: **{recommended_spf}**.")

            # Recommending sunscreen products
            if uv_index_max > 5:
                st.write("It’s sunny out there, so don’t forget your sunscreen! ☀️🧴")
                st.write(f"**Recommended Sunscreen Products:**")
                try:
                    sunscreen_products = recommend_sunscreens(recommended_df, user_input_skin_type, user_input_price_range, uv_index_max)
                except Exception as e:
                    st.write(f"Error generating sunscreen recommendations: {e}")

                if not sunscreen_products.empty:
                    st.dataframe(sunscreen_products[['Product', 'SPF', 'Price', 'Rating', 'Review Count', 'Ingredients', 'URL']])
                else:
                    st.write("Oops! No sunscreen matches for now, but we're adding more options soon. Check back for updated recommendations!")
            else:
                st.write("No need to worry about sunscreen today—your skin is safe from those UV rays! 🌥️")

        # Display stats about products
        st.write("")   
        st.subheader("Check out some popular skincare statistics! ✨")
        st.write("##### Top 10 Most Highly Rated and Reviewed Products on Amazon")
        fig_top_rated = plot_top_rated_reviewed()
        st.pyplot(fig_top_rated)
        st.write("")
        st.write("##### Price Distribution of Skincare products by Type")
        fig_price_dist = plot_price_dist_product_types()
        st.pyplot(fig_price_dist)
