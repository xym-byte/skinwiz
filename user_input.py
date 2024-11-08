'''
user_input.py

This module handles user input collection for the SkinWiz app.
It gathers information such as the user's name, age, location, skin type, skincare goals, and product preferences, and returns them to be used in the recommendation process.

'''

import streamlit as st
from config import cities

# Function to collect and return user input data for the SkinWiz app
def get_user_input():
    name = st.text_input("* Enter your name", "")

    age = st.number_input("* Enter your age", min_value=0, max_value=120, step=1)

    location_name = st.selectbox("* Please select your location", list(cities.keys()), index=9)
    location_data = cities[location_name]

    skin_types = ['Dry', 'Oily', 'Combination', 'Sensitive', 'Normal']
    user_input_skin_type = st.multiselect("* Please select your skin type (You can choose more than one option)", skin_types)

    skincare_improvements_map = {
        'Acne': 'Acne',
        'Brightening': 'Brightening',
        'Hydration': 'Hydration',
        'Anti-Aging': 'Anti_Aging'
    }
    
    user_input_skincare_improvement_display = st.multiselect(
        "* Please select desired skincare improvement (You can choose more than one option)",
        list(skincare_improvements_map.keys())
    )
    
    user_input_skincare_improvement = [skincare_improvements_map[improvement] for improvement in user_input_skincare_improvement_display]

    
    product_labels_map = {
        'Moisturizer': 'moisturizer',
        'Cleanser': 'cleanser',
        'Face Mask': 'face mask',
        'Treatment': 'treatment',
        'Eye Cream': 'eye cream'
    }
    
    user_input_labels_display = st.multiselect(
        "* Please select the type of skincare product (You can choose more than one option)",
        list(product_labels_map.keys())
    )
    
    user_input_labels = [product_labels_map[label] for label in user_input_labels_display]

    max_price = st.number_input("* Enter your budget (in $)", min_value=0.0, value=100.0, step=1.0)
    price_range = [0, max_price]

    return name, age, location_name, location_data, user_input_labels, user_input_skin_type, user_input_skincare_improvement, price_range
