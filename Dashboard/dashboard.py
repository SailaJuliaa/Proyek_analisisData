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
        st.subheader("Jumlah Peminjaman Sepeda Per Bulan (2011-2012)")
        penyewaan_bulanan = data.groupby(data['dteday'].dt.to_period("M"))['cnt'].sum().reset_index()
        penyewaan_bulanan['dteday'] = penyewaan_bulanan['dteday'].astype(str)

        grafik1 = px.bar(
            penyewaan_bulanan,
            x="dteday",
            y="cnt",
            labels={"dteday": "Bulan", "cnt": "Jumlah Peminjaman Sepeda"},
            title="Jumlah Peminjaman Sepeda Per Bulan pada Tahun 2011-2012",
            color_discrete_sequence=px.colors.sequential.Viridis
        )
        grafik1.update_layout(
            xaxis_tickangle=45,
            yaxis=dict(gridcolor='lightgray', gridwidth=0.5),
            plot_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(grafik1, use_container_width=True)

    with kol5:
        st.subheader("Pola Peminjaman Sepeda per Minggu (2011 & 2012)")

        # Filter tahun 2011 dan 2012
        data_2011 = data[data['tahun'] == 2011]
        data_2012 = data[data['tahun'] == 2012]

        mingguan_2011 = data_2011.groupby("minggu")["cnt"].sum().reset_index()
        mingguan_2012 = data_2012.groupby("minggu")["cnt"].sum().reset_index()

        grafik2 = px.bar(
            mingguan_2011,
            x="minggu",
            y="cnt",
            labels={"minggu": "Minggu ke-", "cnt": "Jumlah Peminjaman"},
            title="Pola Peminjaman Sepeda per Minggu pada Tahun 2011",
            color_discrete_sequence=px.colors.sequential.Viridis
        )
        grafik2.update_layout(
            xaxis_tickangle=45,
            yaxis=dict(gridcolor='lightgray'),
            plot_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(grafik2, use_container_width=True)

        grafik3 = px.bar(
            mingguan_2012,
            x="minggu",
            y="cnt",
            labels={"minggu": "Minggu ke-", "cnt": "Jumlah Peminjaman"},
            title="Pola Peminjaman Sepeda per Minggu pada Tahun 2012",
            color_discrete_sequence=px.colors.sequential.Viridis
        )
        grafik3.update_layout(
            xaxis_tickangle=45,
            yaxis=dict(gridcolor='lightgray'),
            plot_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(grafik3, use_container_width=True)

if __name__ == "__main__":
    utama()
