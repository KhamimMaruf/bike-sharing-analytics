import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Konfigurasi halaman
st.set_page_config(
    page_title="Bike Sharing Dashboard",
    page_icon="🚲",
    layout="wide"
)

sns.set_theme(style="whitegrid")

# Load data bersih
@st.cache_data
def load_data():
    day_df = pd.read_csv("dashboard/day_clean.csv")
    hour_df = pd.read_csv("dashboard/hour_clean.csv")
    day_df["dteday"] = pd.to_datetime(day_df["dteday"])
    hour_df["dteday"] = pd.to_datetime(hour_df["dteday"])
    return day_df, hour_df

day_df, hour_df = load_data()

# --- SIDEBAR (FILTER INTERAKTIF) ---
with st.sidebar:
    st.title("🚲 Bike Sharing Analytics")
    st.markdown("Filter data untuk mengeksplorasi pola penyewaan sepeda.")
    
    min_date = day_df["dteday"].min().date()
    max_date = day_df["dteday"].max().date()
    
    date_range = st.date_input(
        label="Rentang Tanggal",
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )
    
    # Filter musim menggunakan season_label
    all_seasons = ["Spring", "Summer", "Fall", "Winter"]
    selected_seasons = st.multiselect(
        label="Pilih Musim",
        options=all_seasons,
        default=all_seasons
    )

# Terapkan filter tanggal & musim
if len(date_range) == 2:
    start_date, end_date = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])
else:
    start_date, end_date = pd.to_datetime(min_date), pd.to_datetime(max_date)

filtered_day = day_df[
    (day_df["dteday"] >= start_date) & 
    (day_df["dteday"] <= end_date) & 
    (day_df["season_label"].isin(selected_seasons))
]

filtered_hour = hour_df[
    (hour_df["dteday"] >= start_date) & 
    (hour_df["dteday"] <= end_date) & 
    (hour_df["season_label"].isin(selected_seasons))
]

# --- HEADER & METRIK UTAMA ---
st.title("📊 Dashboard Analisis Penyewaan Sepeda (2011–2012)")
st.markdown(f"Menampilkan data dari **{start_date.strftime('%d %b %Y')}** hingga **{end_date.strftime('%d %b %Y')}**")

col1, col2, col3 = st.columns(3)
with col1:
    total_rentals = int(filtered_day["cnt"].sum())
    st.metric("Total Penyewaan", f"{total_rentals:,}")
with col2:
    total_registered = int(filtered_day["registered"].sum())
    st.metric("Total Pengguna Registered", f"{total_registered:,}")
with col3:
    total_casual = int(filtered_day["casual"].sum())
    st.metric("Total Pengguna Casual", f"{total_casual:,}")

st.divider()

# --- PERTANYAAN 1: PENGARUH MUSIM & CUACA ---
st.subheader("1. Pengaruh Musim dan Kondisi Cuaca terhadap Rata-rata Penyewaan")

col_q1_a, col_q1_b = st.columns(2)

with col_q1_a:
    season_order = ["Spring", "Summer", "Fall", "Winter"]
    season_avg = filtered_day.groupby("season_label", as_index=False)["cnt"].mean()
    season_avg["season_label"] = pd.Categorical(
        season_avg["season_label"],
        categories=season_order,
        ordered=True
    )
    season_avg = season_avg.sort_values("season_label").dropna()
    season_avg["season_label"] = season_avg["season_label"].astype(str)

    fig, ax = plt.subplots(figsize=(7, 5))
    colors_season = ["#2B5C8F" if s == "Fall" else "#D3D3D3" for s in season_avg["season_label"]]
    bars = sns.barplot(
        data=season_avg,
        x="season_label",
        y="cnt",
        hue="season_label",
        palette=colors_season,
        legend=False,
        ax=ax
    )
    ax.set_title("Rata-rata Penyewaan Harian per Musim", fontsize=12, fontweight="bold")
    ax.set_xlabel("Musim")
    ax.set_ylabel("Rata-rata Penyewaan (Unit)")
    if bars.containers:
        ax.bar_label(bars.containers[0], fmt="%.0f", padding=3)
    st.pyplot(fig)

with col_q1_b:
    weather_order = [
        "Clear/Partly Cloudy",
        "Mist/Cloudy",
        "Light Snow/Rain",
        "Heavy Rain/Ice"
    ]
    weather_avg = filtered_day.groupby("weather_condition", as_index=False)["cnt"].mean()
    weather_avg["weather_condition"] = pd.Categorical(
        weather_avg["weather_condition"],
        categories=weather_order,
        ordered=True
    )
    weather_avg = weather_avg.sort_values("weather_condition").dropna()
    weather_avg["weather_condition"] = weather_avg["weather_condition"].astype(str)

    fig, ax = plt.subplots(figsize=(7, 5))
    colors_weather = ["#2B5C8F" if w == "Clear/Partly Cloudy" else "#D3D3D3" for w in weather_avg["weather_condition"]]
    bars = sns.barplot(
        data=weather_avg,
        x="weather_condition",
        y="cnt",
        hue="weather_condition",
        palette=colors_weather,
        legend=False,
        ax=ax
    )
    ax.set_title("Rata-rata Penyewaan Harian per Kondisi Cuaca", fontsize=12, fontweight="bold")
    ax.set_xlabel("Kondisi Cuaca")
    ax.set_ylabel("Rata-rata Penyewaan (Unit)")
    plt.xticks(rotation=15)
    if bars.containers:
        ax.bar_label(bars.containers[0], fmt="%.0f", padding=3)
    st.pyplot(fig)

st.divider()

# --- PERTANYAAN 2: POLA JAM SIBUK (CASUAL VS REGISTERED) ---
st.subheader("2. Pola Jam Sibuk Penyewaan: Hari Kerja vs Akhir Pekan/Libur")

hourly_pattern = (
    filtered_hour.groupby(["workingday_label", "hr"], as_index=False)[["casual", "registered"]]
    .mean()
)

col_q2_a, col_q2_b = st.columns(2)

with col_q2_a:
    df_weekend = hourly_pattern[hourly_pattern["workingday_label"] == "Holiday/Weekend"]
    fig, ax = plt.subplots(figsize=(7, 5))
    sns.lineplot(
        data=df_weekend,
        x="hr",
        y="registered",
        label="Registered",
        marker="o",
        linewidth=2.5,
        color="#2B5C8F",
        ax=ax
    )
    sns.lineplot(
        data=df_weekend,
        x="hr",
        y="casual",
        label="Casual",
        marker="s",
        linewidth=2.5,
        color="#E07A5F",
        ax=ax
    )
    ax.set_title("Pola Jam Sibuk: Akhir Pekan & Hari Libur", fontsize=12, fontweight="bold")
    ax.set_xlabel("Jam (0–23)")
    ax.set_ylabel("Rata-rata Penyewaan per Jam")
    ax.set_xticks(range(0, 24, 2))
    ax.legend()
    st.pyplot(fig)

with col_q2_b:
    df_workday = hourly_pattern[hourly_pattern["workingday_label"] == "Working Day"]
    fig, ax = plt.subplots(figsize=(7, 5))
    sns.lineplot(
        data=df_workday,
        x="hr",
        y="registered",
        label="Registered",
        marker="o",
        linewidth=2.5,
        color="#2B5C8F",
        ax=ax
    )
    sns.lineplot(
        data=df_workday,
        x="hr",
        y="casual",
        label="Casual",
        marker="s",
        linewidth=2.5,
        color="#E07A5F",
        ax=ax
    )
    ax.set_title("Pola Jam Sibuk: Hari Kerja (Working Day)", fontsize=12, fontweight="bold")
    ax.set_xlabel("Jam (0–23)")
    ax.set_ylabel("Rata-rata Penyewaan per Jam")
    ax.set_xticks(range(0, 24, 2))
    ax.legend()
    st.pyplot(fig)

st.caption("Sumber Data: Bike Sharing Dataset (2011–2012)")