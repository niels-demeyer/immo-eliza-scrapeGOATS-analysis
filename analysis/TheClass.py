import streamlit as st
import geopandas as gpd
import pandas as pd
import os
import json
from plotly import express as px
from plotly import graph_objs as go


class StreamLitClass:
    def __init__(self):
        self.houses_data = None
        self.geojson = None
        self.count_houses = None
        self.avg_price = None
        self.provinces = None

        # load the data
        self.load_houses_data_pandas()
        self.load_geojson()

        # get cities per province
        self.provinces = {
            province: self.houses_data[self.houses_data["province"] == province]["city"]
            .unique()
            .tolist()
            for province in self.houses_data["province"].unique()
        }

        # calculate average price
        self.avg_price = self.calculate_average_price("city", "price")

    # Load the houses data
    def load_houses_data_pandas(self):
        script_dir = os.path.dirname(__file__)
        rel_path = "../data/raw/houses_cleaned.csv"
        file_path = os.path.join(script_dir, rel_path)
        self.houses_data = pd.read_csv(file_path)
        self.houses_data["city"] = (
            self.houses_data["city"].str.lower().str.strip()
        )  # convert city names to lowercase and remove whitespaces
        self.count_houses = self.houses_data["city"].value_counts().reset_index()
        self.count_houses.columns = ["city", "count"]

    # Load the geojson file
    def load_geojson(self):
        script_dir = os.path.dirname(__file__)
        rel_path = "../data/raw/BELGIUM_-_Municipalities.geojson"
        file_path = os.path.join(script_dir, rel_path)
        self.geojson = gpd.read_file(file_path)
        self.geojson["Communes"] = (
            self.geojson["Communes"].str.lower().str.strip()
        )  # convert city names to lowercase and remove whitespaces

    # Create a GeoJSON file with the borders of each province
    def create_province_geojson(self):
        # Create a reverse mapping from city to province
        city_to_province = {
            city: province
            for province, cities in self.provinces.items()
            for city in cities
        }

        # Add a 'province' column to the GeoJSON file
        self.geojson["province"] = self.geojson["Communes"].map(city_to_province)

        # Group by the 'province' column and merge the geometries
        gdf_provinces = self.geojson.dissolve(by="province")

        # Save to a new GeoJSON file
        gdf_provinces.to_file("provinces.geojson", driver="GeoJSON")

    def calculate_average_price(self, group_by_column, agg_column):
        return (
            self.houses_data.groupby(group_by_column)[agg_column].mean().reset_index()
        )

    def plot_most_expensive_houses_average(self):
        if self.avg_price is None:
            self.avg_price = self.calculate_average_price("city", "price")
        fig = px.choropleth_mapbox(
            self.avg_price,
            geojson=self.geojson,
            locations="city",
            featureidkey="properties.Communes",
            color="price",
            color_continuous_scale="Plasma",
            range_color=[self.avg_price["price"].min(), 2500000],
            mapbox_style="carto-positron",
            zoom=5,
            center={"lat": 50.8503, "lon": 4.3517},
            opacity=0.5,
            labels={"price": "Average price per municipality"},
        )
        st.plotly_chart(fig, use_container_width=True)

    def plot_count_houses(self):
        fig = px.choropleth_mapbox(
            self.count_houses,
            geojson=self.geojson,
            locations="city",
            featureidkey="properties.Communes",
            color="count",
            color_continuous_scale="Plasma",
            range_color=[self.count_houses["count"].min(), 500],
            mapbox_style="carto-positron",
            zoom=5,
            center={"lat": 50.8503, "lon": 4.3517},
            opacity=0.5,
            labels={"count": "Count of houses per municipality"},
        )
        st.plotly_chart(fig, use_container_width=True)

    def streamlit_app(self):
        st.set_page_config(page_title="Belgium Real Estate Analysis", layout="wide")

        st.title("Belgium Real Estate Analysis")
        st.markdown(
            "This is a simple web app that shows the average price of houses per municipality in Belgium"
        )

        # calculate average price
        if self.avg_price is None:
            self.avg_price = self.calculate_average_price("city", "price")

        # plot the average price of houses per municipality
        st.subheader("Average price of houses per municipality")
        self.plot_most_expensive_houses_average()

        # plot the count of houses per municipality
        st.subheader("Count of houses per municipality")
        self.plot_count_houses()
