import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ======================
# CONFIG
# ======================
st.set_page_config(
    page_title="Beijing Air Quality Dashboard",
    page_icon="🌫️",
    layout="wide"
)

sns.set_style("whitegrid")

# ======================
# LOAD DATA
# ======================
@st.cache_data
def load_data():
    df = pd.read_csv("dashboard\main_data.csv")
    return df

df = load_data()

# ======================
# SIDEBAR
# ======================
st.sidebar.title("Filter Dashboard")

stations = sorted(df["station"].unique())

selected_station = st.sidebar.multiselect(
    "Pilih Stasiun",
    stations,
    default=stations
)

selected_season = st.sidebar.multiselect(
    "Pilih Musim",
    ["Winter", "Spring", "Summer", "Autumn"],
    default=["Winter", "Spring", "Summer", "Autumn"]
)

filtered_df = df[
    (df["station"].isin(selected_station))
    & (df["season"].isin(selected_season))
]

# ======================
# HEADER
# ======================
st.title("🌫️ Beijing Air Quality Dashboard")
st.markdown("""
Dashboard analisis kualitas udara Beijing 2013–2017 berdasarkan
Beijing Multi-Site Air Quality Dataset.
""")

# ======================
# KPI
# ======================
col1, col2, col3 = st.columns(3)

col1.metric(
    "Rata-rata PM2.5",
    f"{filtered_df['PM2.5'].mean():.2f}"
)

col2.metric(
    "Rata-rata PM10",
    f"{filtered_df['PM10'].mean():.2f}"
)

col3.metric(
    "Jumlah Stasiun",
    filtered_df["station"].nunique()
)

st.divider()

# ======================
# Q1
# ======================
st.header("1. Tren PM2.5 Berdasarkan Musim")

season_order = ["Winter", "Spring", "Summer", "Autumn"]

pm25_season = (
    filtered_df.groupby("season")["PM2.5"]
    .mean()
    .reindex(season_order)
)

fig, ax = plt.subplots(figsize=(8,4))
ax.bar(pm25_season.index, pm25_season.values)
ax.set_ylabel("PM2.5")
ax.set_title("Rata-rata PM2.5 per Musim")

st.pyplot(fig)

st.info("""
Insight:
- Winter memiliki PM2.5 tertinggi.
- Summer memiliki kualitas udara terbaik.
""")

# ======================
# PM25 STATION
# ======================
st.header("2. Rata-rata PM2.5 per Stasiun")

pm25_station = (
    filtered_df.groupby("station")["PM2.5"]
    .mean()
    .sort_values(ascending=False)
)

fig, ax = plt.subplots(figsize=(10,5))

ax.bar(pm25_station.index, pm25_station.values)

plt.xticks(rotation=45)

ax.set_ylabel("PM2.5")
ax.set_title("PM2.5 per Stasiun")

st.pyplot(fig)

# ======================
# KORELASI
# ======================
st.header("3. Korelasi Faktor Meteorologi")

corr_cols = [
    "PM2.5","PM10","SO2",
    "NO2","CO","O3",
    "TEMP","PRES",
    "DEWP","RAIN","WSPM"
]

corr_matrix = filtered_df[corr_cols].corr()

fig, ax = plt.subplots(figsize=(10,7))

sns.heatmap(
    corr_matrix,
    cmap="coolwarm",
    center=0,
    ax=ax
)

st.pyplot(fig)

st.info("""
Insight:
- CO memiliki korelasi positif kuat terhadap PM2.5.
- WSPM (kecepatan angin) memiliki korelasi negatif terhadap PM2.5.
""")

# ======================
# CLUSTERING
# ======================
st.header("4. Clustering Kualitas Udara per Stasiun")

station_avg = (
    filtered_df.groupby("station")["PM2.5"]
    .mean()
    .reset_index()
)

bins = [0,35,75,150,float("inf")]
labels = [
    "Sangat Baik",
    "Sedang",
    "Tidak Sehat",
    "Berbahaya"
]

station_avg["Kategori"] = pd.cut(
    station_avg["PM2.5"],
    bins=bins,
    labels=labels
)

st.dataframe(
    station_avg.sort_values(
        "PM2.5",
        ascending=False
    ),
    use_container_width=True
)

# ======================
# CONCLUSION
# ======================
st.header("5. Kesimpulan")

st.markdown("""
### Pertanyaan 1
- Winter memiliki PM2.5 tertinggi.
- Summer memiliki PM2.5 terendah.
- Stasiun pusat kota cenderung lebih tercemar.

### Pertanyaan 2
- Kecepatan angin membantu menurunkan PM2.5.
- CO merupakan indikator kuat sumber polusi PM2.5.
""")
