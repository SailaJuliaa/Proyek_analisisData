import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Dashboard Penyewaan Sepeda", layout="wide")
st.title("Dashboard Penyewaan Sepeda")

# ambil dataset utama dan ubah format tanggal
def baca_data():
    df = pd.read_csv("D:\\DBS_coding\\Bike_dashboard\\all_data.csv")  
    df['dteday'] = pd.to_datetime(df['dteday']) 
    return df

data_sepeda = baca_data()

st.sidebar.header("Pilih Tanggal")
tgl_pilihan = st.sidebar.date_input("Pilih tanggal:", data_sepeda['dteday'].min())
data_harian = data_sepeda.query("dteday == @tgl_pilihan")

st.subheader(f"Data Penyewaan - {tgl_pilihan}")
if not data_harian.empty:
    col1, col2 = st.columns(2)
    
    # Total sewa hari itu
    total_sewa = data_harian['cnt'].values[0]
    col1.metric("Total Sewa", total_sewa)

    # info cuaca
    kondisi_cuaca = {1: "Cerah", 2: "Berkabut", 3: "Hujan Ringan", 4: "Hujan Lebat"}
    cuaca = kondisi_cuaca.get(data_harian['weathersit'].values[0], "Tidak Diketahui")
    
    suhu = round(data_harian['temp'].values[0] * 41, 1)  
    kelembaban = round(data_harian['hum'].values[0] * 100, 1)  
    angin = round(data_harian['windspeed'].values[0] * 67, 1)  

    col2.metric("Kondisi Cuaca", cuaca)
    st.info(f"Suhu: {suhu}°C | Kelembaban: {kelembaban}% | Angin: {angin} km/jam")

    st.subheader("Penyewaan Harian")
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.barplot(x=["Casual", "Registered", "Total"], y=[
        data_harian['casual'].values[0],
        data_harian['registered'].values[0],
        total_sewa
    ], palette="coolwarm", ax=ax)
    ax.set_ylabel("Jumlah Penyewaan")
    st.pyplot(fig)

    st.subheader("Tren Penyewaan Sepeda")
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.lineplot(data=data_sepeda, x='dteday', y='cnt', marker='o', label="Total Rentals", ax=ax)
    plt.axvline(pd.to_datetime(tgl_pilihan), color='r', linestyle='--', label="Tanggal Dipilih")
    plt.xticks(rotation=45)
    plt.xlabel("Tanggal")
    plt.ylabel("Total Penyewaan")
    plt.legend()
    st.pyplot(fig)

else:
    st.warning("Data tidak ditemukan untuk tanggal ini. Silakan pilih tanggal lain.")

st.subheader("Hari dengan Penyewaan Terbanyak & Tersedikit")

hari_max = data_sepeda.sort_values(by='cnt', ascending=False).iloc[0]
hari_min = data_sepeda.sort_values(by='cnt').iloc[0]

col1, col2 = st.columns(2)

col1.metric("Penyewaan Tertinggi", f"{hari_max['cnt']} sepeda", f"Pada {hari_max['dteday'].date()}")
col2.metric("Penyewaan Terendah", f"{hari_min['cnt']} sepeda", f"Pada {hari_min['dteday'].date()}")

if __name__ == "__main__":
    st.success("Dashboard Penyewaan Sepeda ")
