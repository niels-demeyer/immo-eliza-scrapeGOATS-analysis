from analysis.streamlit.TheClass import StreamLitClass

# Create an instance of the StreamLitClass and load the data
streamlit_app = StreamLitClass()

# Print unique provinces from houses_data
print(streamlit_app.houses_data["province"].unique())

# Print unique provinces from geojson_provinces
print(streamlit_app.geojson_provinces["province"].unique())
