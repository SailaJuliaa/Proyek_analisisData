import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('D:\\DBS_coding\\penyewaan_sepeda\\all_data (1).csv')

df['yr'] = df['yr'].astype(int)
df['mnth'] = df['mnth'].astype(int)
df['date'] = df[['yr', 'mnth']].astype(str).agg('-'.join, axis=1)

df['dteday'] = pd.to_datetime(df['dteday']) 

# Sidebar
st.sidebar.header("Filter Data")
year_options = ["Semua Tahun"] + sorted(df['yr'].unique().tolist())
selected_year = st.sidebar.selectbox("Pilih Tahun:", year_options)

month_options = ["Semua Bulan"] + list(range(1, 13))
selected_month = st.sidebar.selectbox("Pilih Bulan:", month_options)

# Filter Data
filtered_df = df.copy()
if selected_year != "Semua Tahun":
    filtered_df = filtered_df[filtered_df['yr'] == selected_year]
if selected_month != "Semua Bulan":
    filtered_df = filtered_df[filtered_df['mnth'] == selected_month]

st.title("Dashboard Bike by saila Julia ")

# Tren Peminjaman Sepeda
total_per_day = filtered_df.groupby('dteday')['cnt'].sum().reset_index()
st.subheader("Tren Peminjaman Sepeda (2011-2012)")
fig, ax = plt.subplots(figsize=(15, 6))
sns.lineplot(data=total_per_day, x='dteday', y='cnt', marker='o', ax=ax, color='blue', label="Total Rentals")
ax.set_title("Total Peminjaman Sepeda dari 2011 hingga 2012", fontsize=15)
ax.set_xlabel("Tanggal")
ax.set_ylabel("Jumlah Peminjaman")
plt.xticks(rotation=45)
st.pyplot(fig)

# Peminjaman per Bulan
total_per_month = df.groupby(['mnth'])['cnt'].sum().reset_index()

total_per_month = total_per_month.sort_values(by=['mnth'])
month_labels = ["Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul", "Agu", "Sep", "Okt", "Nov", "Des"]

st.subheader("Peminjaman Sepeda per Bulan")
fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(data=total_per_month, x='mnth', y='cnt', palette='flare', ax=ax, errorbar=None)
ax.set_title("Total Peminjaman Sepeda per Bulan", fontsize=15)
ax.set_xlabel("Bulan")
ax.set_ylabel("Jumlah Peminjaman")
ax.set_xticklabels(month_labels)  
st.pyplot(fig)

# Informasi Bulan dengan Peminjaman Tertinggi dan Terendah
if selected_month != "Semua Bulan":
    max_rentals = filtered_df['cnt'].max()
    min_rentals = filtered_df['cnt'].min()
    st.subheader(f"Statistik Bulan {selected_month}")
    st.write(f"Jumlah penyewaan sepeda tertinggi bulan ini: {max_rentals}")
    st.write(f"Jumlah penyewaan sepeda terendah bulan ini: {min_rentals}")

st.info("Data dapat berubah sesuai bulan dan tahun.")
