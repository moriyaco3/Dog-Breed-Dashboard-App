import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="Data", layout="wide")

st.title("Dog Breeds Data")
st.write("Raw data from TheDogAPI")

API_KEY = st.secrets["DOG_API_KEY"]
URL = "https://api.thedogapi.com/v1/breeds"
HEADERS = {"x-api-key": API_KEY}

@st.cache_data
def load_data():
    response = requests.get(URL, headers=HEADERS)
    response.raise_for_status()
    return pd.DataFrame(response.json())


df = load_data()
st.dataframe(
    df,
    use_container_width=True,
    height=600
)