import streamlit as st
import pandas as pd
import plotly.express as px

#memuat dataset
@st.cache_data
def muat_data():
    lokasi_file = "https://raw.githubusercontent.com/SailaJuliaa/Proyek_analisisData/refs/heads/main/Dashboard/all_data%20(2).csv"
    data = pd.read_csv(lokasi_file, parse_dates=["dteday"])
    
    # Menambahkan fitur waktu yang relevan
    data['tahun'] = data['dteday'].dt.year
    data['bulan'] = data['dteday'].dt.month
    data['minggu'] = data['dteday'].dt.isocalendar().week
    
    return data

def utama():
    st.set_page_config(page_title="Dashboard Penyewaan Sepeda", layout="wide")
    
    st.title("Dashboard penyewaan sepeda(2011-2012)")
    data = muat_data()
    
    # Filter di sidebar
    st.sidebar.header("Filter Dashboard")
    
    with st.sidebar.expander("Opsi Filter", expanded=True):
        # Pilihan tahun
        pilihan_tahun = ['Semua Tahun'] + sorted(data["tahun"].unique().tolist())
        tahun_terpilih = st.selectbox("Pilih Tahun", options=pilihan_tahun, index=0)
        
        # Pilihan minggu
        pilihan_minggu = ['Semua Minggu'] + sorted(data["minggu"].unique().tolist())
        minggu_terpilih = st.selectbox("Pilih Minggu", options=pilihan_minggu, index=0)
    
    # Menerapkan filter tahun
    if tahun_terpilih != 'Semua Tahun':
        data = data[data["tahun"] == tahun_terpilih]
    
    # Menerapkan filter minggu
    if minggu_terpilih != 'Semua Minggu':
        data = data[data["minggu"] == minggu_terpilih]
    
    # Tampilan metrik utama
    kol1, kol2, kol3 = st.columns(3)
    with kol1:
        st.metric("Total Penyewaan", f"{data['cnt'].sum():,}")
    with kol2:
        st.metric("Rata-rata Penyewaan Harian", f"{data['cnt'].mean():.2f}")
    with kol3:
        st.metric("Maksimum Penyewaan dalam Sehari", f"{data['cnt'].max():,}")
    
    # Grafik
    kol4, kol5 = st.columns(2)
    
    with kol4:
        st.subheader("Total Penyewaan per Bulan (2011-2012)")
        penyewaan_bulanan = data.groupby(["tahun", "bulan"])['cnt'].sum().reset_index()
        penyewaan_bulanan['bulan_tahun'] = penyewaan_bulanan['tahun'].astype(str) + '-' + penyewaan_bulanan['bulan'].astype(str)
        
        grafik1 = px.bar(penyewaan_bulanan, x="bulan_tahun", y="cnt", color="tahun", 
                         title="Total Penyewaan per Bulan", labels={'cnt': 'Total Penyewaan'})
        st.plotly_chart(grafik1, use_container_width=True)
    
    with kol5:
        st.subheader("Total Penyewaan per Minggu")
        penyewaan_mingguan = data.groupby("minggu")["cnt"].sum().reset_index()
        
        grafik2 = px.bar(penyewaan_mingguan, x="minggu", y="cnt", title="Total Penyewaan per Minggu")
        st.plotly_chart(grafik2, use_container_width=True)
    
    # Menampilkan data mentah
    st.subheader("Data Mentah")
    st.dataframe(data)

if __name__ == "__main__":
    utama()

