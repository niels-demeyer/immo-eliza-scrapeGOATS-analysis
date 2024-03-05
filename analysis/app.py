from TheClass import StreamLitClass
from win11toast import toast

# Create an instance of the StreamLitClass and load the data
streamlit_app = StreamLitClass()

toast("The app is running")

# Create the Streamlit app
streamlit_app.streamlit_app()

toast("The app has been closed")
