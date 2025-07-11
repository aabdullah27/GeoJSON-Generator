import streamlit as st
import requests
import json

st.set_page_config(layout="wide")

st.title("GeoJSON Generator")
st.markdown("Upload a file (CSV, Excel, KML, KMZ, or a zipped SHP file) to generate GeoJSON.")

# API endpoint
API_URL = "http://127.0.0.1:8000/api/v1/generator/generate-geojson"

# File uploader
uploaded_file = st.file_uploader("Choose a file", type=["csv", "xlsx", "kml", "kmz", "zip"])

# Document category selection
if uploaded_file:
    file_extension = uploaded_file.name.split('.')[-1].lower()
    
    # Pre-select category based on file extension
    if file_extension == 'zip':
        doc_category = 'shp'
    elif file_extension in ['csv', 'xlsx', 'kml', 'kmz']:
        doc_category = file_extension
    else:
        doc_category = 'csv' # Default
        
    document_category = st.selectbox(
        "Select the document category",
        ("csv", "xlsx", "kml", "kmz", "shp"),
        index=["csv", "xlsx", "kml", "kmz", "shp"].index(doc_category)
    )

    if st.button("Generate GeoJSON"):
        with st.spinner("Processing file and generating GeoJSON..."):
            files = {'file': (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
            data = {'document_category': document_category}
            
            try:
                response = requests.post(API_URL, files=files, data=data)
                
                if response.status_code == 200:
                    st.success("GeoJSON generated successfully!")
                    
                    # The response from the API is a string, which might contain a JSON object.
                    # We need to clean it up and parse it.
                    try:
                        # The Gemini API might return the JSON wrapped in markdown backticks.
                        cleaned_response = response.text.strip()
                        if cleaned_response.startswith('```json'):
                            cleaned_response = cleaned_response[7:]
                        if cleaned_response.endswith('```'):
                            cleaned_response = cleaned_response[:-3]
                        
                        geojson_data = json.loads(cleaned_response)
                        st.json(geojson_data)
                    except json.JSONDecodeError:
                        st.error("Failed to decode JSON from the response. Showing raw text:")
                        st.text(response.text)
                        
                else:
                    st.error(f"Error from API: {response.status_code}")
                    st.text(response.text)
                    
            except requests.exceptions.RequestException as e:
                st.error(f"Failed to connect to the API. Make sure the backend is running. Error: {e}")

st.info("To run this app, first start the backend server, then run `streamlit run app.py` in your terminal.") 