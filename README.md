# Bike Sharing Analytics Dashboard 🚲

Dashboard interaktif ini dibuat menggunakan **Streamlit** sebagai bagian dari Proyek Akhir *Belajar Fundamental Analisis Data* (Dicoding Indonesia). Dashboard ini menyajikan hasil analisis pola penyewaan sepeda berdasarkan musim, kondisi cuaca, tren jam operasional, serta klaster periode waktu (*Time Period Clustering*).

## Struktur Direktori

- `dashboard/dashboard.py`: File utama aplikasi Streamlit dashboard.
- `dashboard/main_day_data.csv`: Dataset harian hasil pembersihan (*cleaned data*).
- `dashboard/main_hour_data.csv`: Dataset per jam hasil pembersihan (*cleaned data*).
- `data/day.csv`: Dataset mentah penyewaan sepeda harian.
- `data/hour.csv`: Dataset mentah penyewaan sepeda per jam.
- `notebook.ipynb`: Jupyter Notebook berisi seluruh proses analisis data.
- `README.md`: Dokumentasi proyek dan panduan menjalankan dashboard.
- `requirements.txt`: Daftar library Python yang dibutuhkan.
- `url.txt`: Tautan publik dashboard yang sudah di-deploy di Streamlit Cloud.

## Setup Environment & Cara Menjalankan Dashboard

### 1. Setup Virtual Environment
Buka terminal dan arahkan ke direktori utama proyek, lalu buat dan aktifkan *virtual environment*:

**Menggunakan `venv` (Windows):**
    python -m venv venv
    venv\Scripts\activate

**Menggunakan `venv` (macOS/Linux):**
    python3 -m venv venv
    source venv/bin/activate

**Atau menggunakan `conda`:**
    conda create --name main-ds python=3.11
    conda activate main-ds

### 2. Instalasi Dependensi (Library)
Setelah *virtual environment* aktif, instal seluruh *library* yang dibutuhkan melalui berkas `requirements.txt`:

    pip install -r requirements.txt

### 3. Menjalankan Aplikasi Streamlit
Jalankan berkas `dashboard.py` yang berada di dalam folder `dashboard/` dengan perintah berikut:

    streamlit run dashboard/dashboard.py

Aplikasi dashboard akan otomatis terbuka pada browser di alamat `http://localhost:8501`.