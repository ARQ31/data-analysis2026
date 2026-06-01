import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.ticker as mticker
import seaborn as sns
import numpy as np

# ======================
# CONFIG
# ======================
st.set_page_config(
    page_title="Beijing Air Quality Dashboard",
    page_icon="🌫️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Custom CSS ─────────────────────────────────────────────────────────
st.markdown("""
<style>
/* Import font */
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=DM+Mono:wght@400;500&display=swap');

/* Global */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

/* Hide default header */
#MainMenu, footer, header { visibility: hidden; }

/* Page background */
.stApp {
    background-color: #0f1117;
    color: #e8eaf0;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #161b27;
    border-right: 1px solid #252d3d;
}
[data-testid="stSidebar"] .stMarkdown p,
[data-testid="stSidebar"] label {
    color: #8b95a8 !important;
    font-size: 0.82rem;
    letter-spacing: 0.04em;
    text-transform: uppercase;
}

/* Metric cards */
[data-testid="stMetric"] {
    background: linear-gradient(135deg, #1a2035 0%, #1e2640 100%);
    border: 1px solid #2a3550;
    border-radius: 12px;
    padding: 20px 24px !important;
    transition: border-color 0.2s;
}
[data-testid="stMetric"]:hover {
    border-color: #4a6fa5;
}
[data-testid="stMetricLabel"] {
    color: #7a8599 !important;
    font-size: 0.78rem !important;
    letter-spacing: 0.06em;
    text-transform: uppercase;
}
[data-testid="stMetricValue"] {
    color: #e8eaf0 !important;
    font-size: 2rem !important;
    font-weight: 600 !important;
    font-family: 'DM Mono', monospace !important;
}
[data-testid="stMetricDelta"] { font-size: 0.8rem !important; }

/* Section headers */
h1 { 
    color: #e8eaf0 !important;
    font-weight: 700 !important;
    letter-spacing: -0.02em;
}
h2, h3 {
    color: #c8d0de !important;
    font-weight: 600 !important;
}

/* Info/insight boxes */
[data-testid="stAlert"] {
    background-color: #1a2035 !important;
    border: 1px solid #2a3550 !important;
    border-left: 3px solid #4a7fc1 !important;
    border-radius: 8px !important;
    color: #9baec8 !important;
}

/* Divider */
hr { border-color: #252d3d !important; }

/* Dataframe */
[data-testid="stDataFrame"] {
    border: 1px solid #252d3d;
    border-radius: 8px;
}

/* Section card wrapper */
.section-card {
    background: #161b27;
    border: 1px solid #252d3d;
    border-radius: 14px;
    padding: 24px 28px;
    margin-bottom: 20px;
}
.section-label {
    font-size: 0.72rem;
    color: #4a7fc1;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    font-weight: 600;
    margin-bottom: 4px;
}
.section-title {
    font-size: 1.25rem;
    color: #e8eaf0;
    font-weight: 700;
    margin-bottom: 0px;
}

/* WHO badge */
.who-badge {
    display: inline-block;
    background: #2a1f1f;
    border: 1px solid #8b2020;
    color: #e05c5c;
    font-size: 0.75rem;
    padding: 3px 10px;
    border-radius: 20px;
    font-family: 'DM Mono', monospace;
    margin-left: 8px;
    vertical-align: middle;
}

/* Pill tags */
.pill {
    display: inline-block;
    padding: 2px 10px;
    border-radius: 20px;
    font-size: 0.72rem;
    font-weight: 600;
    margin: 2px;
}

/* Custom multiselect */
[data-testid="stMultiSelect"] > div {
    background-color: #1a2035 !important;
    border-color: #2a3550 !important;
}
</style>
""", unsafe_allow_html=True)

# ======================
# LOAD DATA
# ======================
@st.cache_data
def load_data():
    df = pd.read_csv("main_data.csv")
    return df

df = load_data()

# notes untuk reviewer:
# Pastikan sebelum menjalankan dashboard.py ketikkan perintah 'CD' dengan
# filepath yang sesuai di terminal untuk masuk ke direktori dashboard sebelum
# menjalankan streamlit, contoh: cd "C:\Users\ariqm\...\dashboard"
# Jika tidak dilakukan, main_data.csv tidak akan dapat diload.
# Terimakasih pula kepada reviewer untuk reviewnya yang membangun selama ini.

# ======================
# MATPLOTLIB THEME
# ======================
DARK_BG     = "#0f1117"
CARD_BG     = "#161b27"
GRID_COLOR  = "#252d3d"
TEXT_COLOR  = "#9baec8"
TEXT_BRIGHT = "#e8eaf0"

plt.rcParams.update({
    "figure.facecolor":  DARK_BG,
    "axes.facecolor":    CARD_BG,
    "axes.edgecolor":    GRID_COLOR,
    "axes.labelcolor":   TEXT_COLOR,
    "xtick.color":       TEXT_COLOR,
    "ytick.color":       TEXT_COLOR,
    "text.color":        TEXT_BRIGHT,
    "grid.color":        GRID_COLOR,
    "grid.linewidth":    0.7,
    "axes.grid":         True,
    "axes.spines.top":   False,
    "axes.spines.right": False,
    "font.family":       "sans-serif",
    "figure.dpi":        130,
})

SEASON_COLORS  = {"Winter": "#5B8DB8", "Spring": "#73C374",
                  "Summer": "#F4A22D", "Autumn": "#D06B3B"}
STATION_COLORS = {"Tidak Sehat": "#e05c5c", "Sedang": "#f0a045",
                  "Sangat Baik": "#4caf85"}
WHO_LIMIT      = 75.0

# ======================
# SIDEBAR
# ======================
with st.sidebar:
    st.markdown("""
    <div style='padding:12px 0 20px;'>
        <div style='font-size:1.5rem; font-weight:700; color:#e8eaf0;'>🌫️ AirWatch</div>
        <div style='font-size:0.78rem; color:#4a6fa5; letter-spacing:0.05em;'>Beijing · 2013–2017</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("**FILTER DATA**")

    stations = sorted(df["station"].unique())
    selected_station = st.multiselect(
        "Stasiun", stations, default=stations,
        placeholder="Pilih stasiun..."
    )

    selected_season = st.multiselect(
        "Musim", ["Winter", "Spring", "Summer", "Autumn"],
        default=["Winter", "Spring", "Summer", "Autumn"],
        placeholder="Pilih musim..."
    )

    st.divider()
    st.markdown("""
    <div style='font-size:0.72rem; color:#4a5568; line-height:1.8;'>
        <b style='color:#5a6a80;'>Dataset</b><br>
        Beijing Multi-Site Air Quality<br>
        12 Stasiun Pemantauan<br>
        35.064 jam × 12 stasiun<br><br>
        <b style='color:#5a6a80;'>Sumber Polutan</b><br>
        PM2.5 · PM10 · SO2<br>
        NO2 · CO · O3
    </div>
    """, unsafe_allow_html=True)

filtered_df = df[
    df["station"].isin(selected_station) &
    df["season"].isin(selected_season)
]

# ======================
# HEADER
# ======================
st.markdown("""
<div style='padding: 8px 0 28px;'>
    <div style='font-size:0.75rem; color:#4a7fc1; letter-spacing:0.12em;
                text-transform:uppercase; font-weight:600; margin-bottom:6px;'>
        ANALISIS KUALITAS UDARA
    </div>
    <h1 style='font-size:2.2rem; font-weight:800; color:#e8eaf0;
               letter-spacing:-0.03em; margin:0; line-height:1.1;'>
        Beijing Air Quality Dashboard
    </h1>
    <p style='color:#6b7a99; font-size:0.92rem; margin-top:8px;'>
        Visualisasi distribusi polutan udara dari 12 stasiun pemantauan di Beijing · Maret 2013 – Februari 2017
    </p>
</div>
""", unsafe_allow_html=True)

# ======================
# KPI CARDS
# ======================
avg_pm25    = filtered_df["PM2.5"].mean()
avg_pm10    = filtered_df["PM10"].mean()
avg_co      = filtered_df["CO"].mean()
n_stations  = filtered_df["station"].nunique()
worst_s     = filtered_df.groupby("station")["PM2.5"].mean().idxmax() if n_stations > 0 else "—"
who_exceed  = (filtered_df["PM2.5"] > WHO_LIMIT).mean() * 100

k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("Rata-rata PM2.5", f"{avg_pm25:.1f} µg/m³",
          delta=f"{avg_pm25 - WHO_LIMIT:+.1f} vs WHO limit",
          delta_color="inverse")
k2.metric("Rata-rata PM10",  f"{avg_pm10:.1f} µg/m³")
k3.metric("Rata-rata CO",    f"{avg_co:.0f} µg/m³")
k4.metric("Stasiun Aktif",   f"{n_stations}")
k5.metric("Jam > WHO Limit", f"{who_exceed:.1f}%",
          delta="dari total pengukuran", delta_color="off")

st.divider()

# ======================
# ROW 1  |  Musiman + Tahunan
# ======================
st.markdown("""
<div class='section-label'>Pertanyaan 1</div>
<div class='section-title'>Tren PM2.5 Berdasarkan Waktu &amp; Lokasi</div>
""", unsafe_allow_html=True)
st.markdown("")

col_l, col_r = st.columns([1, 1], gap="large")

with col_l:
    # Bar chart musiman
    season_order = ["Winter", "Spring", "Summer", "Autumn"]
    pm25_season  = (filtered_df.groupby("season")["PM2.5"]
                    .mean().reindex(season_order))

    fig, ax = plt.subplots(figsize=(6, 3.8))
    fig.patch.set_facecolor(DARK_BG)

    bars = ax.bar(pm25_season.index, pm25_season.values,
                  color=[SEASON_COLORS[s] for s in season_order],
                  width=0.55, zorder=3, edgecolor=DARK_BG, linewidth=1.2)
    ax.axhline(WHO_LIMIT, color="#e05c5c", linestyle="--",
               linewidth=1.2, zorder=4, label=f"WHO 24-jam ({WHO_LIMIT} µg/m³)")

    for bar, val in zip(bars, pm25_season.values):
        ax.text(bar.get_x() + bar.get_width() / 2, val + 1.2,
                f"{val:.1f}", ha="center", va="bottom",
                fontsize=9, fontweight="600", color=TEXT_BRIGHT)

    ax.set_title("Rata-rata PM2.5 per Musim", fontsize=11,
                 fontweight="700", color=TEXT_BRIGHT, pad=12)
    ax.set_ylabel("PM2.5 (µg/m³)", fontsize=9, color=TEXT_COLOR)
    ax.set_ylim(0, max(pm25_season.values) * 1.18)
    ax.legend(fontsize=8, facecolor=CARD_BG, edgecolor=GRID_COLOR,
              labelcolor=TEXT_COLOR)
    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)

with col_r:
    # Bar chart per stasiun
    pm25_station = (filtered_df.groupby("station")["PM2.5"]
                    .mean().sort_values(ascending=True))

    bins      = [0, 35, 75, 150, float("inf")]
    cat_labels= ["Sangat Baik", "Sedang", "Tidak Sehat", "Berbahaya"]
    categories= pd.cut(pm25_station.values, bins=bins, labels=cat_labels)
    bar_colors= [STATION_COLORS.get(str(c), "#6b7a99") for c in categories]

    fig, ax = plt.subplots(figsize=(6, 3.8))
    fig.patch.set_facecolor(DARK_BG)
    bars = ax.barh(pm25_station.index, pm25_station.values,
                   color=bar_colors, height=0.6,
                   edgecolor=DARK_BG, linewidth=0.8, zorder=3)
    ax.axvline(WHO_LIMIT, color="#e05c5c", linestyle="--",
               linewidth=1.2, zorder=4)

    for bar, val in zip(bars, pm25_station.values):
        ax.text(val + 0.4, bar.get_y() + bar.get_height() / 2,
                f"{val:.1f}", va="center", fontsize=8.5,
                fontweight="600", color=TEXT_BRIGHT)

    patches = [mpatches.Patch(color=v, label=k)
               for k, v in STATION_COLORS.items()]
    ax.legend(handles=patches, fontsize=7.5, facecolor=CARD_BG,
              edgecolor=GRID_COLOR, labelcolor=TEXT_COLOR)
    ax.set_title("Rata-rata PM2.5 per Stasiun", fontsize=11,
                 fontweight="700", color=TEXT_BRIGHT, pad=12)
    ax.set_xlabel("PM2.5 (µg/m³)", fontsize=9, color=TEXT_COLOR)
    ax.set_xlim(0, pm25_station.max() * 1.15)
    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)

st.info("""
**Insight:**  
Winter secara konsisten memiliki PM2.5 tertinggi (~94 µg/m³) — dipicu penggunaan pemanas batubara.  
Summer paling bersih (~64 µg/m³) berkat hujan dan angin. Stasiun pusat kota (Dongsi, Wanshouxigong)  
selalu di atas rata-rata, sementara Dingling & Huairou relatif lebih bersih sebagai area suburban.
""")

st.divider()

# ======================
# ROW 2  |  Korelasi + Wind
# ======================
st.markdown("""
<div class='section-label'>Pertanyaan 2</div>
<div class='section-title'>Pengaruh Faktor Meteorologi terhadap PM2.5</div>
""", unsafe_allow_html=True)
st.markdown("")

col_a, col_b = st.columns([1.2, 0.8], gap="large")

with col_a:
    corr_cols = ["PM2.5","PM10","SO2","NO2","CO","O3",
                 "TEMP","PRES","DEWP","RAIN","WSPM"]
    corr_matrix = filtered_df[corr_cols].corr()

    fig, ax = plt.subplots(figsize=(7, 5.2))
    fig.patch.set_facecolor(DARK_BG)
    mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
    sns.heatmap(corr_matrix, mask=mask, ax=ax,
                annot=True, fmt=".2f", annot_kws={"size": 8},
                cmap="RdBu_r", center=0, vmin=-1, vmax=1,
                linewidths=0.4, linecolor=DARK_BG,
                cbar_kws={"shrink": 0.8})
    ax.set_title("Heatmap Korelasi Antar Variabel", fontsize=11,
                 fontweight="700", color=TEXT_BRIGHT, pad=12)
    ax.tick_params(axis="x", rotation=45, labelsize=8.5, colors=TEXT_COLOR)
    ax.tick_params(axis="y", labelsize=8.5, colors=TEXT_COLOR)
    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)

with col_b:
    # PM2.5 vs kecepatan angin bin
    if "WSPM" in filtered_df.columns:
        wspm_bin = pd.cut(filtered_df["WSPM"],
                          bins=[0, 1, 2, 4, 6, 15],
                          labels=["0–1", "1–2", "2–4", "4–6", ">6"])
        wspm_pm25 = filtered_df.groupby(wspm_bin, observed=True)["PM2.5"].mean()

        fig, ax = plt.subplots(figsize=(5, 5.2))
        fig.patch.set_facecolor(DARK_BG)

        gradient_colors = ["#d73027","#fc8d59","#fee090","#91bfdb","#4575b4"]
        bars = ax.bar(wspm_pm25.index.astype(str), wspm_pm25.values,
                      color=gradient_colors, width=0.6,
                      edgecolor=DARK_BG, linewidth=1, zorder=3)
        ax.axhline(WHO_LIMIT, color="#e05c5c", linestyle="--",
                   linewidth=1.2, zorder=4,
                   label=f"WHO ({WHO_LIMIT} µg/m³)")

        for bar, val in zip(bars, wspm_pm25.values):
            ax.text(bar.get_x() + bar.get_width() / 2, val + 1,
                    f"{val:.1f}", ha="center", va="bottom",
                    fontsize=9.5, fontweight="700", color=TEXT_BRIGHT)

        ax.set_title("PM2.5 vs Kecepatan Angin\n(r = –0.269)",
                     fontsize=11, fontweight="700", color=TEXT_BRIGHT, pad=12)
        ax.set_xlabel("Kecepatan Angin WSPM (m/s)", fontsize=9, color=TEXT_COLOR)
        ax.set_ylabel("Rata-rata PM2.5 (µg/m³)",    fontsize=9, color=TEXT_COLOR)
        ax.set_ylim(0, wspm_pm25.max() * 1.2)
        ax.legend(fontsize=8, facecolor=CARD_BG, edgecolor=GRID_COLOR,
                  labelcolor=TEXT_COLOR)
        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)

st.info("""
**Insight:**  
**CO** memiliki korelasi terkuat dengan PM2.5 (r ≈ 0.77) — emisi pembakaran sebagai sumber utama.  
**Kecepatan angin (WSPM)** berkorelasi negatif: angin >6 m/s menurunkan PM2.5 dari ~100 → ~27 µg/m³  
(turun 73%). Pada angin >4 m/s, rata-rata PM2.5 sudah di bawah panduan WHO 24 jam.
""")

st.divider()

# ======================
# ROW 3  |  Clustering tabel + ringkasan
# ======================
st.markdown("""
<div class='section-label'>Analisis Lanjutan</div>
<div class='section-title'>Clustering Kualitas Udara per Stasiun</div>
""", unsafe_allow_html=True)
st.markdown("")

station_avg = (filtered_df.groupby("station")["PM2.5"]
               .mean().reset_index())
station_avg.columns = ["Stasiun", "Rata-rata PM2.5 (µg/m³)"]
station_avg["Rata-rata PM2.5 (µg/m³)"] = station_avg["Rata-rata PM2.5 (µg/m³)"].round(2)

bins       = [0, 35, 75, 150, float("inf")]
cat_labels = ["Sangat Baik", "Sedang", "Tidak Sehat", "Berbahaya"]
station_avg["Kategori"] = pd.cut(
    station_avg["Rata-rata PM2.5 (µg/m³)"], bins=bins, labels=cat_labels
)
station_avg = station_avg.sort_values("Rata-rata PM2.5 (µg/m³)", ascending=False)

col_t, col_s = st.columns([1.4, 0.6], gap="large")

with col_t:
    def color_kategori(val):
        colors = {
            "Tidak Sehat": "color: #e05c5c; font-weight:600;",
            "Sedang":      "color: #f0a045; font-weight:600;",
            "Sangat Baik": "color: #4caf85; font-weight:600;",
            "Berbahaya":   "color: #8B0000; font-weight:700;",
        }
        return colors.get(str(val), "")

    def color_pm25(val):
        if val > 75:  return "color: #e05c5c;"
        elif val > 35: return "color: #f0a045;"
        return "color: #4caf85;"

    styled = (station_avg.style
              .applymap(color_kategori, subset=["Kategori"])
              .applymap(color_pm25, subset=["Rata-rata PM2.5 (µg/m³)"])
              .format({"Rata-rata PM2.5 (µg/m³)": "{:.2f}"})
              .set_properties(**{
                  "background-color": "#1a2035",
                  "color": "#c8d0de",
                  "border-color": "#252d3d",
                  "font-size": "13px",
              })
              .set_table_styles([{
                  "selector": "th",
                  "props": [("background-color", "#161b27"),
                             ("color", "#7a8599"),
                             ("font-size", "11px"),
                             ("letter-spacing", "0.05em"),
                             ("text-transform", "uppercase"),
                             ("border-bottom", "1px solid #252d3d")]
              }])
    )
    st.dataframe(styled, use_container_width=True, height=460)

with col_s:
    counts = station_avg["Kategori"].value_counts()
    total  = len(station_avg)
    st.markdown("**Distribusi Kategori**")
    st.markdown("")

    for cat in ["Tidak Sehat", "Sedang", "Sangat Baik", "Berbahaya"]:
        n = counts.get(cat, 0)
        if n == 0:
            continue
        pct  = n / total * 100
        col  = {"Tidak Sehat":"#e05c5c","Sedang":"#f0a045",
                "Sangat Baik":"#4caf85","Berbahaya":"#8B0000"}.get(cat,"#6b7a99")
        st.markdown(f"""
        <div style='margin-bottom:14px;'>
            <div style='display:flex;justify-content:space-between;
                        align-items:center;margin-bottom:5px;'>
                <span style='font-size:0.85rem;font-weight:600;color:{col};'>{cat}</span>
                <span style='font-family:DM Mono,monospace;font-size:0.82rem;
                             color:#6b7a99;'>{n} stasiun</span>
            </div>
            <div style='background:#252d3d;border-radius:4px;height:7px;'>
                <div style='background:{col};width:{pct:.0f}%;
                            height:7px;border-radius:4px;'></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown(f"""
    <div style='font-size:0.8rem; color:#6b7a99; line-height:1.9;'>
        <b style='color:#8b95a8;'>Threshold (US EPA AQI)</b><br>
        🟢 Sangat Baik: 0–35 µg/m³<br>
        🟡 Sedang: 35–75 µg/m³<br>
        🔴 Tidak Sehat: 75–150 µg/m³<br>
        ⚫ Berbahaya: >150 µg/m³
    </div>
    """, unsafe_allow_html=True)

st.divider()

# ======================
# CONCLUSION
# ======================
st.markdown("""
<div class='section-label'>Ringkasan</div>
<div class='section-title'>Kesimpulan &amp; Rekomendasi</div>
""", unsafe_allow_html=True)
st.markdown("")

c1, c2 = st.columns(2, gap="large")

with c1:
    st.markdown("""
    <div style='background:#1a2035;border:1px solid #2a3550;
                border-left:3px solid #5B8DB8;border-radius:10px;padding:20px 22px;'>
        <div style='font-size:0.72rem;color:#5B8DB8;letter-spacing:0.1em;
                    text-transform:uppercase;font-weight:600;margin-bottom:8px;'>
            Pertanyaan 1 — Tren Musiman & Spasial
        </div>
        <p style='color:#c8d0de;font-size:0.88rem;line-height:1.75;margin:0;'>
            <b style='color:#e8eaf0;'>Winter</b> (Nov–Jan) secara konsisten
            menjadi periode terburuk (~94 µg/m³), didorong oleh pemanas batubara.
            <b style='color:#e8eaf0;'>Summer</b> (~64 µg/m³) paling bersih.
            Seluruh 12 stasiun melampaui panduan WHO — 9 stasiun masuk kategori
            <b style='color:#e05c5c;'>Tidak Sehat</b>, 3 stasiun suburban
            (Changping, Huairou, Dingling) dalam kategori
            <b style='color:#f0a045;'>Sedang</b>.
        </p>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div style='background:#1a2035;border:1px solid #2a3550;
                border-left:3px solid #D06B3B;border-radius:10px;padding:20px 22px;'>
        <div style='font-size:0.72rem;color:#D06B3B;letter-spacing:0.1em;
                    text-transform:uppercase;font-weight:600;margin-bottom:8px;'>
            Pertanyaan 2 — Faktor Meteorologi
        </div>
        <p style='color:#c8d0de;font-size:0.88rem;line-height:1.75;margin:0;'>
            <b style='color:#e8eaf0;'>CO</b> berkorelasi paling kuat dengan
            PM2.5 (r = 0.77) — konfirmasi emisi pembakaran sebagai sumber dominan.
            <b style='color:#e8eaf0;'>Kecepatan angin</b> (r = –0.27) adalah
            faktor alam terpenting: angin &gt;6 m/s menurunkan PM2.5 sebesar
            <b style='color:#4caf85;'>73%</b> dari kondisi calms.
        </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("")

r1, r2, r3 = st.columns(3, gap="medium")
rec_style = lambda color: f"""
    background:#1a2035;border:1px solid #2a3550;
    border-top:3px solid {color};border-radius:10px;
    padding:18px 20px;height:100%;
"""

with r1:
    st.markdown(f"""
    <div style='{rec_style("#4a7fc1")}'>
        <div style='font-size:1.4rem;margin-bottom:6px;'>📅</div>
        <b style='color:#e8eaf0;font-size:0.9rem;'>Kebijakan Musiman</b>
        <p style='color:#8b95a8;font-size:0.82rem;line-height:1.7;margin-top:8px;'>
            Perketat pembatasan kendaraan & industri berat
            pada November–Februari. Subsidi konversi pemanas
            batubara ke gas alam.
        </p>
    </div>
    """, unsafe_allow_html=True)

with r2:
    st.markdown(f"""
    <div style='{rec_style("#73C374")}'>
        <div style='font-size:1.4rem;margin-bottom:6px;'>🌬️</div>
        <b style='color:#e8eaf0;font-size:0.9rem;'>Sistem Peringatan Dini</b>
        <p style='color:#8b95a8;font-size:0.82rem;line-height:1.7;margin-top:8px;'>
            Integrasikan prakiraan kecepatan angin ke sistem
            alert kualitas udara. Terbitkan peringatan saat
            angin &lt;2 m/s diprakirakan berlangsung lama.
        </p>
    </div>
    """, unsafe_allow_html=True)

with r3:
    st.markdown(f"""
    <div style='{rec_style("#e05c5c")}'>
        <div style='font-size:1.4rem;margin-bottom:6px;'>🏙️</div>
        <b style='color:#e8eaf0;font-size:0.9rem;'>Prioritas Pusat Kota</b>
        <p style='color:#8b95a8;font-size:0.82rem;line-height:1.7;margin-top:8px;'>
            Fokus intervensi di Dongsi, Wanshouxigong &
            Nongzhanguan: perluasan zona rendah emisi,
            penambahan ruang hijau, dan pembatasan truk.
        </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("")
st.markdown("""
<div style='text-align:center;padding:16px 0;
            color:#3a4558;font-size:0.75rem;letter-spacing:0.05em;'>
    Beijing Air Quality Dashboard · Ariq Marwan Permana · AIC012B6Y0004
</div>
""", unsafe_allow_html=True)
