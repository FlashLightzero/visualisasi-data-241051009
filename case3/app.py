"""
Bedah Kasus 3 - Dashboard Dataset Pengamatan Cuaca (Streamlit)
NIM  : 241051009
Nama : Muhammad Adrian Oktav Al Fattah

Jalankan: python -m streamlit run app.py
"""
import pandas as pd
import plotly.express as px
import streamlit as st
from pathlib import Path

BASE = Path(__file__).parent

NIM = "241051009"
NAMA = "Muhammad Adrian Oktav Al Fattah"

st.set_page_config(page_title="Dashboard Cuaca | Kasus 3", page_icon="🌦️", layout="wide")


@st.cache_data
def load_data():
    return pd.read_csv(BASE / "data_cuaca.csv")


df = load_data()

st.title("🌦️ Dashboard Pengamatan Cuaca")
st.caption("Visualisasi Data • Pertemuan 2 • Bedah Kasus 3")
st.info(f"**NIM:** {NIM}  |  **Nama:** {NAMA}")

st.sidebar.header("Filter Data")
st.sidebar.markdown(f"**{NAMA}**  \nNIM {NIM}")
kota = st.sidebar.multiselect("Kota", sorted(df["Kota"].unique()), default=sorted(df["Kota"].unique()))
kond = st.sidebar.multiselect("Kondisi", sorted(df["Kondisi"].unique()), default=sorted(df["Kondisi"].unique()))
smin, smax = float(df["Suhu (°C)"].min()), float(df["Suhu (°C)"].max())
suhu_r = st.sidebar.slider("Rentang Suhu (°C)", smin, smax, (smin, smax), step=0.5)

f = df[df["Kota"].isin(kota) & df["Kondisi"].isin(kond) & df["Suhu (°C)"].between(*suhu_r)]
if f.empty:
    st.warning("Tidak ada data untuk filter ini.")
    st.stop()

k1, k2, k3, k4 = st.columns(4)
k1.metric("Jumlah Pengamatan", f"{len(f):,}")
k2.metric("Rata-rata Suhu", f"{f['Suhu (°C)'].mean():.1f} °C")
k3.metric("Rata-rata Kelembaban", f"{f['Kelembaban (%)'].mean():.1f} %")
k4.metric("Persentase Hujan", f"{(f['Kondisi'] == 'Hujan').mean()*100:.1f}%")

tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["🧬 Diagnostik Tipe Data", "🏙️ Nominal: Kota & Kondisi", "🌡️ Interval: Suhu", "💧 Rasio: Kelembaban", "🗂️ Data & Insight"])

with tab1:
    st.subheader("Hasil Diagnostik Tipe Data per Kolom")
    diag = pd.DataFrame({
        "Kolom": ["Kota", "Suhu (°C)", "Kelembaban (%)", "Kondisi"],
        "Tipe Utama": ["Kategorik", "Numerik", "Numerik", "Kategorik"],
        "Skala Stevens": ["Nominal", "Interval", "Rasio", "Nominal"],
        "Alasan": ["Label teks tanpa urutan", "Jarak antar suhu sama, tetapi 0°C bukan 'tidak ada suhu'",
                   "0% benar-benar tidak ada kelembaban (nol absolut)", "Label teks tanpa urutan"],
        "Operasi yang Valid": ["=, ≠", "+, −", "+, −, ×, ÷", "=, ≠"],
    })
    st.dataframe(diag, width="stretch", hide_index=True)
    st.subheader("Mengapa Celsius bukan Rasio?")
    c1, c2, c3 = st.columns(3)
    c1.metric("20°C ÷ 10°C", "2.00", help="Tampak seperti 2x lebih panas")
    c2.metric("20°C → Kelvin ÷ 10°C → Kelvin", f"{(20+273.15)/(10+273.15):.3f}", help="Kelvin punya nol absolut")
    c3.metric("Kesimpulan", "Bukan 2x", help="Rasio tidak valid pada skala Interval")
    st.success("Aturan emas: pilih grafik berdasarkan tipe datanya, bukan berdasarkan apa yang terlihat indah.")

with tab2:
    c1, c2 = st.columns(2)
    kc = f["Kota"].value_counts().reset_index()
    kc.columns = ["Kota", "Jumlah"]
    cc = f["Kondisi"].value_counts().reset_index()
    cc.columns = ["Kondisi", "Jumlah"]
    with c1:
        st.plotly_chart(px.bar(kc, x="Kota", y="Jumlah", color="Kota", text_auto=True,
                               title="Jumlah Pengamatan per Kota (Bar Chart)").update_layout(showlegend=False), width="stretch")
    with c2:
        st.plotly_chart(px.pie(cc, names="Kondisi", values="Jumlah", hole=0.4, title="Proporsi Kondisi Cuaca (Pie Chart)"),
                        width="stretch")
    ct = (pd.crosstab(f["Kota"], f["Kondisi"], normalize="index") * 100).reset_index().melt(id_vars="Kota", value_name="Persen")
    st.plotly_chart(px.bar(ct, x="Kota", y="Persen", color="Kondisi", barmode="stack", title="Komposisi Kondisi Cuaca per Kota (%)"),
                    width="stretch")

with tab3:
    c1, c2 = st.columns(2)
    with c1:
        st.plotly_chart(px.histogram(f, x="Suhu (°C)", nbins=30, title="Distribusi Suhu (Histogram)"), width="stretch")
    with c2:
        st.plotly_chart(px.box(f, x="Kota", y="Suhu (°C)", color="Kota", title="Sebaran Suhu per Kota (Box Plot)")
                        .update_layout(showlegend=False), width="stretch")
    st.plotly_chart(px.box(f, x="Kondisi", y="Suhu (°C)", color="Kondisi", title="Suhu menurut Kondisi Cuaca"), width="stretch")
    st.caption("Suhu Celsius adalah skala Interval: selisih suhu bermakna (32°C - 24°C = 8°C), tetapi perbandingan rasio tidak.")

with tab4:
    c1, c2 = st.columns(2)
    with c1:
        st.plotly_chart(px.histogram(f, x="Kelembaban (%)", nbins=30, title="Distribusi Kelembaban (Histogram)"), width="stretch")
    with c2:
        st.plotly_chart(px.box(f, x="Kondisi", y="Kelembaban (%)", color="Kondisi", title="Kelembaban menurut Kondisi (Box Plot)"),
                        width="stretch")
    st.plotly_chart(px.scatter(f, x="Suhu (°C)", y="Kelembaban (%)", color="Kondisi", opacity=0.6,
                               title="Suhu vs Kelembaban (Scatter Plot)"), width="stretch")
    st.dataframe(f[["Suhu (°C)", "Kelembaban (%)"]].describe().round(2), width="stretch")

with tab5:
    st.subheader("Insight Otomatis")
    kt = f.groupby("Kota")["Suhu (°C)"].mean()
    kh = f.groupby("Kota")["Kelembaban (%)"].mean()
    rain = f.assign(h=f["Kondisi"] == "Hujan").groupby("Kota")["h"].mean() * 100
    corr = f["Suhu (°C)"].corr(f["Kelembaban (%)"], method="spearman")
    st.markdown(f"""
- Kota terpanas: **{kt.idxmax()}** ({kt.max():.1f} °C); terdingin: **{kt.idxmin()}** ({kt.min():.1f} °C).
- Kota paling lembab: **{kh.idxmax()}** ({kh.max():.1f}%).
- Kota dengan persentase hujan tertinggi: **{rain.idxmax()}** ({rain.max():.1f}%).
- Korelasi suhu vs kelembaban (Spearman): **{corr:.2f}**, suhu naik cenderung diiringi kelembaban turun.
- Selisih suhu rata-rata kota terpanas dan terdingin: **{kt.max() - kt.min():.1f} °C** (selisih valid untuk skala Interval).
""")
    st.subheader("Data Sintesis (1000 baris)")
    st.dataframe(f, width="stretch", hide_index=True)
    st.download_button("⬇️ Unduh CSV (terfilter)", f.to_csv(index=False), "data_cuaca_filtered.csv")

st.divider()
st.caption(f"Dibuat oleh {NAMA} (NIM {NIM}) • Data sintesis berbasis contoh Bedah Kasus 3")
