from TheClass import StreamLitClass

# Create an instance of the StreamLitClass
streamlit_app = StreamLitClass()

# Load the data
streamlit_app.load_houses_data_pandas()
streamlit_app.load_geojson()

# Get the province for each city
for city in streamlit_app.houses_data["city"].unique():
    streamlit_app.get_province(city)
