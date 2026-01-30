import streamlit as st
import requests
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.title("Dog Breed Statistics")

API_KEY = st.secrets["DOG_API_KEY"]
URL = "https://api.thedogapi.com/v1/breeds"

headers = {"x-api-key": API_KEY}
data = requests.get(URL, headers=headers).json()
df = pd.DataFrame(data)
sns.set_theme(style="dark")

# How many breeds have in every breed group? #

group_counts = (
    df["breed_group"]
    .dropna()
    .value_counts()
    .reset_index()
)

group_counts.columns = ["breed_group", "count"]

fig, ax = plt.subplots(figsize=(6, 4))

sns.barplot(
    data=group_counts,
    x="count",
    y="breed_group",
    ax=ax,
    color="#8ecae6"

)

ax.set_title("Number of Breeds per Group", color="white", fontsize=12)
ax.set_xlabel("")
ax.set_ylabel("")

ax.tick_params(colors="white")
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["left"].set_color("#666666")
ax.spines["bottom"].set_color("#666666")

fig.patch.set_alpha(0)
ax.set_facecolor("none")

st.pyplot(fig, use_container_width=False)
