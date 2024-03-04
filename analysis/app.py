from TheClass import StreamLitClass

# Create an instance of the StreamLitClass
streamlit_app = StreamLitClass()
streamlit_app.load_houses_data_pandas()
streamlit_app.load_geojson()
print(streamlit_app.geojson)
print(streamlit_app.houses_data.head())
