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
df = df.loc[:, ["name", "breed_group", "life_span", "temperament", "origin", "weight", "height", "image"]]
sns.set_theme(style="dark")

##############################
# Number of Breeds per Group #
##############################

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

#######################################
# Average Life Span per Group (years) #
#######################################

# convert life span to average
def split_range(text):
    if pd.isna(text):
        return None, None

    min_range, max_range = text.split("-")

    return float(min_range), float(max_range)


df["life_min"], df["life_max"] = zip(
    *df["life_span"].apply(split_range)
)

df["life_avg"] = (df["life_min"] + df["life_max"]) / 2


fig, ax = plt.subplots(figsize=(6, 3))

sns.boxplot(
    data=df.dropna(subset=["breed_group", "life_avg"]),
    x="life_avg",
    y="breed_group",
    ax=ax,
    color="#b8e1dd"
)

ax.set_title("Life Span Distribution by Breed Group (years)", color="white", fontsize=12)
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

###################################################
# Average Weight per Breed Group – Male vs Female #
###################################################

def get_metric(w):
    if isinstance(w, dict):
        return w.get("metric")
    return None


df["weight_kg"] = df["weight"].apply(get_metric)

# extract "min-max" ranges for each sex

df["male_range"] = df["weight_kg"].str.extract(r"Male:\s*([\d\.]+-[\d\.]+)")
df["female_range"] = df["weight_kg"].str.extract(r"Female:\s*([\d\.]+-[\d\.]+)")

# use the split_range function
df["male_min"], df["male_max"] = zip(*df["male_range"].apply(split_range))
df["female_min"], df["female_max"] = zip(*df["female_range"].apply(split_range))

# averages
df["male_avg_kg"] = (df["male_min"] + df["male_max"]) / 2
df["female_avg_kg"] = (df["female_min"] + df["female_max"]) / 2

weight_group = (
    df[["breed_group", "male_avg_kg", "female_avg_kg"]]
    .dropna(subset=["breed_group"])
    .groupby("breed_group", as_index=False)
    .mean()
    .round(1)
)

weight_group = weight_group.sort_values(
    by=["male_avg_kg", "female_avg_kg"],
    ascending=False
)

fig, ax = plt.subplots(figsize=(6, 3))

y = range(len(weight_group))

ax.barh(
    y,
    weight_group["male_avg_kg"],
    height=0.4,
    label="Male",
    color="#4ea8de"
)

ax.barh(
    [i + 0.4 for i in y],
    weight_group["female_avg_kg"],
    height=0.4,
    label="Female",
    color="#f28482"
)

ax.set_yticks([i + 0.2 for i in y])
ax.set_yticklabels(weight_group["breed_group"], color="white")

ax.set_title("Average Weight per Breed Group (kg)", color="white", fontsize=12)
ax.legend()

ax.tick_params(colors="white")
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["left"].set_color("#666666")
ax.spines["bottom"].set_color("#666666")

fig.patch.set_alpha(0)
ax.set_facecolor("none")

st.pyplot(fig, use_container_width=False)

#################################
# Scatter: Weight vs Life Span  #
#################################

df["avg_weight_kg"] = df[["male_avg_kg", "female_avg_kg"]].mean(axis=1)

scatter_df = df.dropna(subset=["avg_weight_kg", "life_avg"])

fig, ax = plt.subplots(figsize=(6, 3))

sns.regplot(
    data=scatter_df,
    x="avg_weight_kg",
    y="life_avg",
    ax=ax,
    scatter_kws={"alpha": 0.6, "color": "#4ea8de"},
    line_kws={"color": "white"}
)

ax.set_title("Weight vs Life Span", color="white", fontsize=12)
ax.set_xlabel("Average Weight (kg)")
ax.set_ylabel("Average Life Span (years)")

ax.tick_params(colors="white")
ax.xaxis.label.set_color("white")
ax.yaxis.label.set_color("white")
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["left"].set_color("#666666")
ax.spines["bottom"].set_color("#666666")

fig.patch.set_alpha(0)
ax.set_facecolor("none")

st.pyplot(fig, use_container_width=False)

#############################################
# Average Height per Breed Group – Male vs Female #
#############################################

df["height_cm"] = df["height"].apply(get_metric)

# extract "min-max" ranges for each sex
df["h_male_range"] = df["height_cm"].str.extract(r"Male:\s*([\d\.]+-[\d\.]+)")
df["h_female_range"] = df["height_cm"].str.extract(r"Female:\s*([\d\.]+-[\d\.]+)")

# use the split_range function
df["h_male_min"], df["h_male_max"] = zip(*df["h_male_range"].apply(split_range))
df["h_female_min"], df["h_female_max"] = zip(*df["h_female_range"].apply(split_range))

# averages
df["h_male_avg_cm"] = (df["h_male_min"] + df["h_male_max"]) / 2
df["h_female_avg_cm"] = (df["h_female_min"] + df["h_female_max"]) / 2

height_group = (
    df[["breed_group", "h_male_avg_cm", "h_female_avg_cm"]]
    .dropna(subset=["breed_group"])
    .groupby("breed_group", as_index=False)
    .mean()
    .round(1)
)

height_group = height_group.sort_values(
    by=["h_male_avg_cm", "h_female_avg_cm"],
    ascending=False
)

fig, ax = plt.subplots(figsize=(6, 3))

y = range(len(height_group))

ax.barh(
    y,
    height_group["h_male_avg_cm"],
    height=0.4,
    label="Male",
    color="#4ea8de"
)

ax.barh(
    [i + 0.4 for i in y],
    height_group["h_female_avg_cm"],
    height=0.4,
    label="Female",
    color="#f28482"
)

ax.set_yticks([i + 0.2 for i in y])
ax.set_yticklabels(height_group["breed_group"], color="white")

ax.set_title("Average Height per Breed Group (cm)", color="white", fontsize=12)
ax.legend()

ax.tick_params(colors="white")
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["left"].set_color("#666666")
ax.spines["bottom"].set_color("#666666")

fig.patch.set_alpha(0)
ax.set_facecolor("none")

st.pyplot(fig, use_container_width=False)

#################################
# Scatter: Height vs Life Span  #
#################################
df["height_avg_cm"] = df[["h_male_avg_cm", "h_female_avg_cm"]].mean(axis=1)

scatter_df2 = df.dropna(subset=["height_avg_cm", "life_avg"])

fig, ax = plt.subplots(figsize=(6, 3))

sns.regplot(
    data=scatter_df2,
    x="height_avg_cm",
    y="life_avg",
    ax=ax,
    scatter_kws={"alpha": 0.6, "color": "#90dbf4"},
    line_kws={"color": "white"},
    fit_reg=False
)

ax.set_title("Height vs Life Span", color="white", fontsize=12)
ax.set_xlabel("Average Height (cm)", color="white")
ax.set_ylabel("Average Life Span (years)", color="white")

ax.tick_params(colors="white")
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["left"].set_color("#666666")
ax.spines["bottom"].set_color("#666666")

fig.patch.set_alpha(0)
ax.set_facecolor("none")

st.pyplot(fig, use_container_width=False)

######################################
# Show breeds by a temperament trait #
######################################

# --- Trait graph ---
# take all temperament strings
all_temp = df["temperament"].dropna()

# split by comma
traits = all_temp.str.split(",")

traits = traits.explode()
traits = traits.str.strip()
traits = traits.dropna()

traits_clean = (
    traits.dropna()
          .astype(str)
          .str.strip()
          .str.lower()
          .str.replace(r"\s+", " ", regex=True)
)

unique_traits = sorted(traits_clean.unique())

st.markdown("## Choose a Temperament Trait")
trait = st.selectbox(
    label="",
    options=unique_traits,
    label_visibility="collapsed"
)

temp = df[["breed_group", "temperament"]].dropna(subset=["breed_group", "temperament"]).copy()

# per breed: does temperament contain this trait?
temp["has_trait"] = temp["temperament"].str.contains(fr"\b{trait}\b", case=False, na=False)

# percent of breeds in each group that have the trait
stats = (
    temp.groupby("breed_group")["has_trait"]
        .mean()
        .mul(100)
        .reset_index()
        .rename(columns={"has_trait": "percent"})
        .sort_values("percent", ascending=False)
)


fig, ax = plt.subplots(figsize=(6, 3))

sns.barplot(
    data=stats,
    x="percent",
    y="breed_group",
    ax=ax,
    color="#bde0fe"
)

ax.set_title(f"Breed groups with trait: {trait}", color="white", fontsize=12)
ax.set_xlabel("Percent of breeds (%)")
ax.set_ylabel("")
ax.set_xlim(0, 100)

ax.tick_params(colors="white")
ax.xaxis.label.set_color("white")

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["left"].set_color("#666666")
ax.spines["bottom"].set_color("#666666")

fig.patch.set_alpha(0)
ax.set_facecolor("none")

st.pyplot(fig, use_container_width=False)