from TheClass import StreamLitClass

# Create an instance of the StreamLitClass
streamlit_app = StreamLitClass()

# Load the data
streamlit_app.load_houses_data_pandas()
streamlit_app.load_geojson()

# Plot the most expensive houses average
streamlit_app.plot_most_expensive_houses_average()
