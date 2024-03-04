import streamlit as st
import geopandas as gpd
import pandas as pd
import os
import json
from plotly import express as px


class StreamLitClass:
    def __init__(self):
        self.houses_data = None
        self.geojson = None

    # Load the houses data
    def load_houses_data_pandas(self):
        script_dir = os.path.dirname(__file__)
        rel_path = "../data/raw/houses_cleaned.csv"
        file_path = os.path.join(script_dir, rel_path)
        self.houses_data = pd.read_csv(file_path)
        self.houses_data["city"] = (
            self.houses_data["city"].str.lower().str.strip()
        )  # convert city names to lowercase and remove whitespaces

    # Load the geojson file
    def load_geojson(self):
        script_dir = os.path.dirname(__file__)
        rel_path = "../data/raw/BELGIUM_-_Municipalities.geojson"
        file_path = os.path.join(script_dir, rel_path)
        self.geojson = gpd.read_file(file_path)
        self.geojson["Communes"] = (
            self.geojson["Communes"].str.lower().str.strip()
        )  # convert city names to lowercase and remove whitespaces

    def calculate_average_price(self, group_by_column, agg_column):
        return (
            self.houses_data.groupby(group_by_column)[agg_column].mean().reset_index()
        )

    def plot_most_expensive_houses_average(self):
        avg_price = self.calculate_average_price("city", "price")
        self.plot_map(avg_price, "city", "properties.Communes", "price")

    def plot_count_houses(self):
        count_houses = self.houses_data["city"].value_counts().reset_index()
        count_houses.columns = ["city", "count"]
        self.plot_map(count_houses, "city", "properties.Communes", "count")

    def plot_map(self, avg_price, locations, featureidkey, color):
        fig = px.choropleth_mapbox(
            avg_price,
            geojson=self.geojson.__geo_interface__,
            locations=locations,
            featureidkey=featureidkey,
            color=color,
            color_continuous_scale="RdYlBu",  # use the RdYlBu color scale
            range_color=(0, 2500000),  # set the min and max values of the legend
            mapbox_style="carto-positron",
            zoom=5,
            center={"lat": 50.8503, "lon": 4.3517},
            opacity=0.5,
            labels={"price": "Average price per municipality"},
        )
        st.plotly_chart(
            fig, use_container_width=True
        )  # display the plot in the Streamlit app

    def streamlit_app(self):
        st.set_page_config(page_title="Belgium Real Estate Analysis", layout="wide")

        st.title("Belgium Real Estate Analysis")
        st.markdown(
            "This is a simple web app that shows the average price of houses per municipality in Belgium"
        )

        # load the data
        self.load_houses_data_pandas()
        self.load_geojson()

        # Create a sidebar selectbox for the plot selection
        plot_option = st.sidebar.selectbox(
            "Select a plot",
            ("Average Price per Municipality", "Count of Houses per Municipality"),
        )

        # Display the selected plot
        if plot_option == "Average Price per Municipality":
            self.plot_most_expensive_houses_average()
        elif plot_option == "Count of Houses per Municipality":
            self.plot_count_houses()
