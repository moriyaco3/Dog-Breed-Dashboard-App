import streamlit as st
import requests

API_KEY = st.secrets["DOG_API_KEY"]
URL = "https://api.thedogapi.com/v1/breeds"
HEADERS = {"x-api-key": API_KEY}

name = st.text_input('Enter your name', '')
if name:
    st.write(f'Hello {name}, welcome to the app!')