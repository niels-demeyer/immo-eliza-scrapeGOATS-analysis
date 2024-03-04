from TheClass import StreamLitClass

# Create an instance of the StreamLitClass
streamlit_app = StreamLitClass()
houses = streamlit_app.load_houses_data_pandas()
print(houses.head())
