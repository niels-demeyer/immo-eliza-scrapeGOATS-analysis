import streamlit as st
import geopandas as gpd
import pandas as pd
import os
import json 

# Load the houses data
def load_houses_data_pandas():
    file_path = './data/raw/houses_cleaned.csv'  # replace with your actual file path
    data = pd.read_csv(file_path)
    return data

# Load the geojson file
def load_geojson():
    file_path = './data/raw/BELGIUM_-_Municipalities.geojson'
    data = gpd.read_file(file_path)
    return data

houses = load_houses_data_pandas()
print(houses)