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
        self.geojson_cities = None
        self.geojson_provinces = None
        self.count_houses = None
        self.avg_price = None
        self.provinces = None

        # load the data
        self.load_houses_data_pandas()
        self.load_geojson_cities()
        self.load_geojson_provinces()

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

    # Load the geojson files

    def load_geojson_cities(self):
        script_dir = os.path.dirname(__file__)
        rel_path = "../data/raw/BELGIUM_-_Municipalities.geojson"
        file_path = os.path.join(script_dir, rel_path)
        self.geojson_cities = gpd.read_file(file_path)
        self.geojson_cities["Communes"] = (
            self.geojson_cities["Communes"].str.lower().str.strip()
        )  # convert city names to lowercase and remove whitespaces

    def load_geojson_provinces(self):
        script_dir = os.path.dirname(__file__)
        rel_path = "../data/raw/provinces.geojson"
        file_path = os.path.join(script_dir, rel_path)
        self.geojson_provinces = gpd.read_file(file_path)
        self.geojson_provinces["province"] = self.geojson_provinces[
            "province"
        ].str.strip()  # remove leading and trailing whitespaces
        self.geojson_provinces["Communes"] = (
            self.geojson_provinces["Communes"].str.lower().str.strip()
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
        fig = px.choropleth(
            self.avg_price,
            geojson=self.geojson_cities,
            locations="city",
            featureidkey="properties.Communes",
            color="price",
            color_continuous_scale="Plasma",
            range_color=[self.avg_price["price"].min(), 2500000],
            labels={"price": "Average price per municipality"},
            title="Average price per municipality",
        )
        fig.update_geos(
            showcountries=False,
            showcoastlines=True,
            showland=True,
            fitbounds="locations",
        )

        st.plotly_chart(fig, use_container_width=True)

    def plot_count_houses(self):
        fig = px.choropleth_mapbox(
            self.count_houses,
            geojson=self.geojson_cities,
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

    def plot_count_houses_per_province(self):
        # Remove trailing whitespaces from province names
        self.houses_data["province"] = self.houses_data["province"].str.strip()

        # Group the data by 'province' and count the number of houses
        count_houses_per_province = (
            self.houses_data.groupby("province").size().reset_index(name="count")
        )

        fig = px.choropleth(
            count_houses_per_province,
            geojson=self.geojson_provinces,
            locations="province",
            featureidkey="properties.province",
            color="count",
            color_continuous_scale="Plasma",
            range_color=[count_houses_per_province["count"].min(), 500],
            labels={"count": "Count of houses per province"},
            title="Count of houses per province",
        )
        fig.update_geos(
            showcountries=False,
            showcoastlines=True,
            showland=True,
            fitbounds="locations",
        )

    def plot_most_expensive_houses_average_static(self):
        if self.avg_price is None:
            self.avg_price = self.calculate_average_price("city", "price")
        fig = px.choropleth(
            self.avg_price,
            geojson=self.geojson_cities,
            locations="city",
            featureidkey="properties.Communes",
            color="price",
            color_continuous_scale="Plasma",  # Change color scale
            range_color=[self.avg_price["price"].min(), 2500000],
            labels={"price": "Average price per municipality"},
            title="Average price per municipality",
            hover_name="city",  # Add hover name
            hover_data=["price"],  # Add hover data
        )
        fig.update_geos(
            showcountries=False,
            showcoastlines=False,
            showland=False,
            fitbounds="locations",
        )
        fig.update_layout(
            title_text="Average price per municipality",
            title_x=0.5,  # Center the title
            margin={"r": 10, "t": 30, "l": 10, "b": 10},  # Adjust margins
            dragmode=False,  # Disable panning
            hovermode="closest",  # Hover over the closest data
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

        # # # plot the average price of houses per municipality
        # st.subheader("Average price of houses per municipality")
        # self.plot_most_expensive_houses_average()

        # # plot the count of houses per municipality
        # st.subheader("Count of houses per municipality")
        # self.plot_count_houses()

        # plot the count of houses per province
        st.subheader("Count of houses per province")
        self.plot_count_houses_per_province()
