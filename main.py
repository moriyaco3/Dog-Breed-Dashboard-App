import streamlit as st
import requests

API_KEY = st.secrets["DOG_API_KEY"]
URL = "https://api.thedogapi.com/v1/breeds"
HEADERS = {"x-api-key": API_KEY}

st.set_page_config(page_title="Dog Breed Dashboard", layout="wide")


def get_breeds():
    response = requests.get(URL, headers=HEADERS)
    response.raise_for_status()
    return response.json()


def show_gallery(breeds):
    st.title("🐶 Dog Breed Dashboard")
    st.write("Browse dog breeds and click for details")

    # --- NEW: search box ---
    query = st.text_input("Search breed by name", "").strip().lower()

    if query:
        breeds = [b for b in breeds if query in (b.get("name", "").lower())]

    if not breeds:
        st.warning("No breeds found. Try a different search.")
        return

    cols = st.columns(4)

    for i, breed in enumerate(breeds):
        col = cols[i % 4]

        name = breed.get("name", "Unknown")
        image_url = None
        if breed.get("image"):
            image_url = breed["image"].get("url")

        with col:
            if image_url:
                st.image(image_url, use_container_width=True)
            else:
                st.info("No image available")

            st.markdown(f"**{name}**")

            if st.button("Details", key=f"details_{breed.get('id', i)}"):
                st.session_state["selected_breed_id"] = breed.get("id")
                st.rerun()


def show_details(breed):
    if st.button("<- Back to gallery"):
        st.session_state.pop("selected_breed_id", None)
        st.rerun()

    st.title(breed.get("name", "Dog"))

    if breed.get("image"):
        st.image(breed["image"].get("url"), width=400)

    st.subheader("General information")
    st.write("Breed group:", breed.get("breed_group"))
    st.write("Temperament:", breed.get("temperament"))
    st.write("Origin:", breed.get("origin"))
    st.write("Life span:", breed.get("life_span"))

    weight = breed.get("weight", {})
    height = breed.get("height", {})

    st.subheader("Size")
    st.write("Weight (kg):", weight.get("metric"))
    st.write("Height (cm):", height.get("metric"))

    st.subheader("Purpose & history")
    st.write("Bred for:", breed.get("bred_for"))
    st.write("History:", breed.get("history"))
    st.write("Description:", breed.get("description"))


try:
    breeds = get_breeds()
except Exception:
    st.error("Failed to load data from TheDogAPI")
    st.stop()

selected_id = st.session_state.get("selected_breed_id")

if selected_id is None:
    show_gallery(breeds)
else:
    selected_breed = next((b for b in breeds if b.get("id") == selected_id), None)

    if selected_breed is None:
        st.warning("Breed not found")
        st.session_state.pop("selected_breed_id", None)
        st.rerun()
    else:
        show_details(selected_breed)