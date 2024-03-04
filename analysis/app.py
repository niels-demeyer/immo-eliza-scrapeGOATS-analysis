import streamlit as st
import geopandas as gpd
import pandas as pd
import os
import json 
from plotly import express as px

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

def plot_most_expensive_houses_average(data):
    # get the average price per municipality
    avg_price = data.groupby('city').price.mean().reset_index()
    # plot the average price per municipality on a map
    fig = px.choropleth_mapbox(avg_price, geojson=geojson, locations='city', featureidkey="properties.NAME_4",
                               color='price',
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
    plot_most_expensive_houses_average(houses_data)
    
def main():
    streamlit_app()
    
if __name__ == '__main__':
    main()
    