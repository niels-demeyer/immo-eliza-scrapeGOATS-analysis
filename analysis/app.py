import streamlit as st
import geopandas as gpd
import pandas as pd
import os
import json 
from plotly import express as px

# Load the houses data
def load_houses_data_pandas():
    script_dir = os.path.dirname(__file__)
    rel_path = "../data/raw/houses_cleaned.csv"
    file_path = os.path.join(script_dir, rel_path)
    data = pd.read_csv(file_path)
    data['city'] = data['city'].str.lower().str.strip()  # convert city names to lowercase and remove whitespaces
    return data

# Load the geojson file
def load_geojson():
    script_dir = os.path.dirname(__file__)
    rel_path = "../data/raw/BELGIUM_-_Municipalities.geojson"
    file_path = os.path.join(script_dir, rel_path)
    data = gpd.read_file(file_path)
    data['Communes'] = data['Communes'].str.lower().str.strip()  # convert city names to lowercase and remove whitespaces
    return data

def calculate_average_price(data, group_by_column, agg_column):
    return data.groupby(group_by_column)[agg_column].mean().reset_index()

def plot_most_expensive_houses_average(data, geojson):
    avg_price = calculate_average_price(data, 'city', 'price')
    plot_map(avg_price, geojson, 'city', "properties.Communes", 'price')

def plot_map(avg_price, geojson, locations, featureidkey, color):
    fig = px.choropleth_mapbox(avg_price, geojson=geojson.__geo_interface__, locations=locations, featureidkey=featureidkey,
                               color=color,
                               color_continuous_scale="YlOrRd",  # use the YlOrRd color scale
                               range_color=(0, 2500000),  # set the min and max values of the legend
                               mapbox_style="carto-positron",
                               zoom=5, center = {"lat": 50.8503, "lon": 4.3517},
                               opacity=0.5,
                               labels={'price':'Average price per municipality'}
                              )
    st.plotly_chart(fig, use_container_width=True)  # display the plot in the Streamlit app
    
def streamlit_app():
    st.set_page_config(page_title='Belgium Real Estate Analysis', layout='wide')
    
    st.title('Belgium Real Estate Analysis')
    st.markdown('This is a simple web app that shows the average price of houses per municipality in Belgium')
    
    # load the data
    houses_data = load_houses_data_pandas()
    geojson = load_geojson()
    
    # avg_price = calculate_average_price(houses_data, 'city', 'price')
    # st.write(avg_price)
    
    # plot the average price per municipality
    plot_most_expensive_houses_average(houses_data, geojson)
    
def main():
    streamlit_app()
    
if __name__ == '__main__':
    main()