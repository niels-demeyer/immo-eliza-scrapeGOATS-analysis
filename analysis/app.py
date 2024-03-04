import streamlit as st
from streamlit import sidebar
import geopandas as gpd
import pandas as pd
import os
import json 
from plotly import express as px

# Load the houses data
def load_houses_data_pandas():
    # Get the directory of the current script
    script_dir = os.path.dirname(__file__)
    # Create the relative path
    rel_path = "../data/raw/houses_cleaned.csv"
    # Join the script directory with the relative path
    file_path = os.path.join(script_dir, rel_path)
    data = pd.read_csv(file_path)
    return data

# Load the geojson file
def load_geojson():
    # Get the directory of the current script
    script_dir = os.path.dirname(__file__)
    # Create the relative path
    rel_path = "../data/raw/BELGIUM_-_Municipalities.geojson"
    # Join the script directory with the relative path
    file_path = os.path.join(script_dir, rel_path)
    data = gpd.read_file(file_path)
    return data

def calculate_average_price(data, group_by_column, agg_column):
    return data.groupby(group_by_column)[agg_column].mean().reset_index()

def plot_most_expensive_houses_average(data, geojson):
    avg_price = calculate_average_price(data, 'city', 'price')
    plot_map(avg_price, geojson, 'city', "properties.NAME_4", 'price')



def plot_map(avg_price, geojson, locations, featureidkey, color):
    fig = px.choropleth_mapbox(avg_price, geojson=geojson, locations=locations, featureidkey=featureidkey,
                               color=color,
                               color_continuous_scale="Viridis",  # use the Viridis color scale
                               range_color=(avg_price[color].min(), avg_price[color].max()),  # adjust the legend based on the max average price
                               mapbox_style="carto-positron",
                               zoom=6, center = {"lat": 50.8503, "lon": 4.3517},
                               opacity=0.5,
                               labels={'price':'Average price per municipality'}
                              )
    fig.show()

# make the streamlit app
def streamlit_app():
    st.title('Belgium Real Estate Analysis')
    st.write('This is a simple web app that shows the average price of houses per municipality in Belgium')
    
    # load the data
    houses_data = load_houses_data_pandas()
    geojson = load_geojson()
    
    # plot the average price per municipality
    plot_most_expensive_houses_average(houses_data, geojson)
    
def main():
    streamlit_app()
    
if __name__ == '__main__':
    main()