import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Konfigurasi halaman dashboard
st.set_page_config(
    page_title="Bike Sharing Analytics Dashboard",
    page_icon="🚲",
    layout="wide"
)

sns.set_style("whitegrid")

@st.cache_data
def load_data():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    day = pd.read_csv(os.path.join(base_dir, "main_day_data.csv"))
    hour = pd.read_csv(os.path.join(base_dir, "main_hour_data.csv"))
    day['date'] = pd.to_datetime(day['date'])
    hour['date'] = pd.to_datetime(hour['date'])
    return day, hour

day_df, hour_df = load_data()

# --- SIDEBAR FILTER ---
st.sidebar.header("🚲 Filter Dashboard")

min_date = day_df['date'].min().date()
max_date = day_df['date'].max().date()

date_range = st.sidebar.date_input(
    label="Rentang Tanggal",
    min_value=min_date,
    max_value=max_date,
    value=[min_date, max_date]
)

if len(date_range) == 2:
    start_date, end_date = date_range
else:
    start_date, end_date = min_date, max_date

selected_seasons = st.sidebar.multiselect(
    label="Pilih Musim (Season)",
    options=['Spring', 'Summer', 'Fall', 'Winter'],
    default=['Spring', 'Summer', 'Fall', 'Winter']
)

# Terapkan filter pada dataframe
filtered_day_df = day_df[
    (day_df['date'].dt.date >= start_date) &
    (day_df['date'].dt.date <= end_date) &
    (day_df['season'].isin(selected_seasons))
]

filtered_hour_df = hour_df[
    (hour_df['date'].dt.date >= start_date) &
    (hour_df['date'].dt.date <= end_date) &
    (hour_df['season'].isin(selected_seasons))
]

# --- HEADER & KPI METRICS ---
st.title("🚲 Bike Sharing Performance & Operational Dashboard")
st.markdown("Analisis pola penyewaan sepeda berdasarkan musim, kondisi cuaca, dan klaster waktu operasional (2011–2012).")

col1, col2, col3, col4 = st.columns(4)
with col1:
    total_rentals = int(filtered_day_df['total_count'].sum())
    st.metric("Total Penyewaan", f"{total_rentals:,}")
with col2:
    avg_daily = round(filtered_day_df['total_count'].mean(), 1) if not filtered_day_df.empty else 0
    st.metric("Rata-rata Harian", f"{avg_daily:,}")
with col3:
    total_registered = int(filtered_day_df['registered'].sum())
    st.metric("Pengguna Registered", f"{total_registered:,}")
with col4:
    total_casual = int(filtered_day_df['casual'].sum())
    st.metric("Pengguna Casual", f"{total_casual:,}")

st.divider()

# --- VISUALISASI 1: MUSIM & CUACA ---
st.subheader("1. Pengaruh Musim dan Kondisi Cuaca terhadap Penyewaan")

if filtered_day_df.empty:
    st.warning("Tidak ada data untuk kombinasi filter yang dipilih.")
else:
    fig1, axes1 = plt.subplots(1, 2, figsize=(16, 5.5))

    season_order = ['Spring', 'Summer', 'Fall', 'Winter']
    season_melt = filtered_day_df.melt(
        id_vars='season',
        value_vars=['casual', 'registered'],
        var_name='user_type',
        value_name='avg_rentals'
    )
    sns.barplot(
        data=season_melt,
        x='season',
        y='avg_rentals',
        hue='user_type',
        order=[s for s in season_order if s in selected_seasons],
        palette=['#66b3ff', '#1f77b4'],
        errorbar=None,
        ax=axes1[0]
    )
    axes1[0].set_title("Rata-rata Penyewaan Harian per Musim", fontsize=12, fontweight='bold')
    axes1[0].set_xlabel("Musim")
    axes1[0].set_ylabel("Rata-rata Penyewaan")
    axes1[0].legend(title="Tipe Pengguna", labels=["Casual", "Registered"])
    for container in axes1[0].containers:
        axes1[0].bar_label(container, fmt='%.0f', padding=3, fontsize=9)

    weather_order = ['Clear / Partly Cloudy', 'Mist / Cloudy', 'Light Snow / Rain']
    weather_melt = filtered_day_df.melt(
        id_vars='weather_condition',
        value_vars=['casual', 'registered'],
        var_name='user_type',
        value_name='avg_rentals'
    )
    sns.barplot(
        data=weather_melt,
        x='weather_condition',
        y='avg_rentals',
        hue='user_type',
        order=weather_order,
        palette=['#66b3ff', '#1f77b4'],
        errorbar=None,
        ax=axes1[1]
    )
    axes1[1].set_title("Rata-rata Penyewaan Harian per Kondisi Cuaca", fontsize=12, fontweight='bold')
    axes1[1].set_xlabel("Kondisi Cuaca")
    axes1[1].set_ylabel("Rata-rata Penyewaan")
    axes1[1].legend(title="Tipe Pengguna", labels=["Casual", "Registered"])
    for container in axes1[1].containers:
        axes1[1].bar_label(container, fmt='%.0f', padding=3, fontsize=9)

    plt.tight_layout()
    st.pyplot(fig1)

st.divider()

# --- VISUALISASI 2: POLA JAM & CLUSTERING PERIODE WAKTU ---
st.subheader("2. Pola Jam Sibuk & Klaster Periode Waktu (Hari Kerja vs Akhir Pekan)")

if filtered_hour_df.empty:
    st.warning("Tidak ada data per jam untuk filter yang dipilih.")
else:
    fig2, axes2 = plt.subplots(1, 2, figsize=(16, 5.5))

    sns.lineplot(
        data=filtered_hour_df,
        x='hour',
        y='total_count',
        hue='workingday_label',
        palette=['#ff7f0e', '#1f77b4'],
        marker='o',
        linewidth=2.2,
        errorbar=None,
        ax=axes2[0]
    )
    axes2[0].set_title("Tren Penyewaan Sepeda 24 Jam", fontsize=12, fontweight='bold')
    axes2[0].set_xlabel("Jam (00:00 - 23:00)")
    axes2[0].set_ylabel("Rata-rata Penyewaan per Jam")
    axes2[0].set_xticks(range(0, 24))
    axes2[0].legend(title="Tipe Hari")

    period_order = [
        '1. Dini Hari (00-05)',
        '2. Pagi / Komuter (06-10)',
        '3. Siang (11-15)',
        '4. Sore / Pulang Kerja (16-19)',
        '5. Malam (20-23)'
    ]
    sns.barplot(
        data=filtered_hour_df,
        x='time_period',
        y='total_count',
        hue='workingday_label',
        order=period_order,
        palette=['#ff7f0e', '#1f77b4'],
        errorbar=None,
        ax=axes2[1]
    )
    axes2[1].set_title("Rata-rata Penyewaan per Klaster Periode Waktu", fontsize=12, fontweight='bold')
    axes2[1].set_xlabel("Klaster Periode Waktu")
    axes2[1].set_ylabel("Rata-rata Penyewaan per Jam")
    axes2[1].tick_params(axis='x', rotation=15)
    axes2[1].legend(title="Tipe Hari")
    for container in axes2[1].containers:
        axes2[1].bar_label(container, fmt='%.0f', padding=3, fontsize=9)

    plt.tight_layout()
    st.pyplot(fig2)

st.caption("Copyright © 2026 - Proyek Analisis Data Bike Sharing")