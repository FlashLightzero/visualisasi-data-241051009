"""
Bedah Kasus 1 - Dashboard Dataset Operasional Penjualan (Streamlit)
NIM  : 241051009
Nama : Muhammad Adrian Oktav Al Fattah

Jalankan: streamlit run app.py
"""
import pandas as pd
import plotly.express as px
import streamlit as st
from pathlib import Path

BASE = Path(__file__).parent

NIM = "241051009"
NAMA = "Muhammad Adrian Oktav Al Fattah"

st.set_page_config(page_title="Dashboard Penjualan | Kasus 1", page_icon="📊", layout="wide")


@st.cache_data
def load_data():
    df = pd.read_csv(BASE / "data_penjualan.csv", parse_dates=["Tanggal"])
    df["Pendapatan (Rp)"] = df["Harga (Rp)"] * df["Jumlah Terjual"]
    df["Bulan"] = df["Tanggal"].dt.to_period("M").dt.to_timestamp()
    return df


def rp(x):
    if x >= 1e9:
        return f"Rp {x/1e9:,.2f} M"
    if x >= 1e6:
        return f"Rp {x/1e6:,.1f} Jt"
    return f"Rp {x:,.0f}"


df = load_data()

# ---------- Header (NIM & NAMA wajib) ----------
st.title("📊 Dashboard Operasional Penjualan")
st.caption("Visualisasi Data • Pertemuan 2 • Bedah Kasus 1")
st.info(f"**NIM:** {NIM}  |  **Nama:** {NAMA}")

# ---------- Sidebar filter ----------
st.sidebar.header("Filter Data")
st.sidebar.markdown(f"**{NAMA}**  \nNIM {NIM}")
kategori = st.sidebar.multiselect("Kategori", sorted(df["Kategori"].unique()), default=sorted(df["Kategori"].unique()))
produk_opsi = sorted(df[df["Kategori"].isin(kategori)]["Produk"].unique())
produk = st.sidebar.multiselect("Produk", produk_opsi, default=produk_opsi)
tgl = st.sidebar.date_input("Rentang Tanggal", (df["Tanggal"].min(), df["Tanggal"].max()),
                            min_value=df["Tanggal"].min(), max_value=df["Tanggal"].max())
if len(tgl) != 2:
    st.warning("Pilih tanggal awal dan akhir.")
    st.stop()

f = df[df["Kategori"].isin(kategori) & df["Produk"].isin(produk)
       & (df["Tanggal"] >= pd.Timestamp(tgl[0])) & (df["Tanggal"] <= pd.Timestamp(tgl[1]))]
if f.empty:
    st.warning("Tidak ada data untuk filter ini.")
    st.stop()

# ---------- KPI ----------
k1, k2, k3, k4 = st.columns(4)
k1.metric("Total Transaksi", f"{len(f):,}")
k2.metric("Total Unit Terjual", f"{f['Jumlah Terjual'].sum():,}")
k3.metric("Total Pendapatan", rp(f["Pendapatan (Rp)"].sum()))
k4.metric("Rata-rata Harga", rp(f["Harga (Rp)"].mean()))

tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["🧬 Diagnostik Tipe Data", "📦 Kategorik (Nominal)", "🔢 Numerik", "📈 Tren Waktu", "🗂️ Data & Insight"])

# ---------- Tab 1: diagnostik tipe data ----------
with tab1:
    st.subheader("Hasil Diagnostik Tipe Data per Kolom")
    diag = pd.DataFrame({
        "Kolom": ["Produk", "Kategori", "Harga (Rp)", "Jumlah Terjual", "Tanggal"],
        "Tipe Utama": ["Kategorik", "Kategorik", "Numerik", "Numerik", "Waktu"],
        "Sub-Tipe": ["Nominal", "Nominal", "Kontinu", "Diskrit", "Interval"],
        "Skala Stevens": ["Nominal", "Nominal", "Rasio", "Rasio", "Interval"],
        "Alasan": ["Label tanpa urutan", "Label tanpa urutan", "Hasil ukur, punya nol absolut",
                   "Hasil hitung (bilangan bulat), punya nol absolut", "Nol bukan berarti 'tidak ada waktu'"],
        "Visualisasi Terbaik": ["Bar / Pie Chart", "Bar / Pie Chart", "Histogram", "Histogram / Bar Chart", "Line Chart"],
    })
    st.dataframe(diag, width="stretch", hide_index=True)
    st.success("Aturan emas: pilih grafik berdasarkan tipe datanya, bukan berdasarkan apa yang terlihat indah.")

# ---------- Tab 2: kategorik ----------
with tab2:
    c1, c2 = st.columns(2)
    kat = f.groupby("Kategori", as_index=False).agg(Transaksi=("Produk", "count"), Pendapatan=("Pendapatan (Rp)", "sum"))
    with c1:
        fig = px.bar(kat.sort_values("Transaksi", ascending=False), x="Kategori", y="Transaksi",
                     color="Kategori", title="Jumlah Transaksi per Kategori (Bar Chart)", text_auto=True)
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, width="stretch")
    with c2:
        fig = px.pie(kat, names="Kategori", values="Pendapatan", title="Kontribusi Pendapatan per Kategori (Pie Chart)", hole=0.4)
        st.plotly_chart(fig, width="stretch")
    prod = f.groupby("Produk", as_index=False)["Pendapatan (Rp)"].sum().sort_values("Pendapatan (Rp)")
    fig = px.bar(prod, x="Pendapatan (Rp)", y="Produk", orientation="h", title="Pendapatan per Produk (Bar Chart)")
    st.plotly_chart(fig, width="stretch")

# ---------- Tab 3: numerik ----------
with tab3:
    c1, c2 = st.columns(2)
    with c1:
        fig = px.histogram(f, x="Harga (Rp)", nbins=40, title="Distribusi Harga (Numerik Kontinu - Histogram)")
        st.plotly_chart(fig, width="stretch")
    with c2:
        fig = px.histogram(f, x="Jumlah Terjual", nbins=40, title="Distribusi Jumlah Terjual (Numerik Diskrit - Histogram)")
        st.plotly_chart(fig, width="stretch")
    c3, c4 = st.columns(2)
    with c3:
        fig = px.box(f, x="Kategori", y="Harga (Rp)", color="Kategori", log_y=True,
                     title="Sebaran Harga per Kategori (Box Plot, skala log)")
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, width="stretch")
    with c4:
        fig = px.scatter(f, x="Harga (Rp)", y="Jumlah Terjual", color="Kategori", log_x=True, opacity=0.7,
                         title="Harga vs Jumlah Terjual (Scatter Plot)")
        st.plotly_chart(fig, width="stretch")
    corr = f["Harga (Rp)"].corr(f["Jumlah Terjual"], method="spearman")
    st.metric("Korelasi Spearman Harga vs Jumlah Terjual", f"{corr:.3f}")
    st.dataframe(f[["Harga (Rp)", "Jumlah Terjual", "Pendapatan (Rp)"]].describe().round(2), width="stretch")

# ---------- Tab 4: waktu ----------
with tab4:
    tren = f.groupby("Bulan", as_index=False)["Pendapatan (Rp)"].sum()
    fig = px.line(tren, x="Bulan", y="Pendapatan (Rp)", markers=True, title="Tren Pendapatan Bulanan (Line Chart)")
    st.plotly_chart(fig, width="stretch")
    tren_k = f.groupby(["Bulan", "Kategori"], as_index=False)["Jumlah Terjual"].sum()
    fig = px.line(tren_k, x="Bulan", y="Jumlah Terjual", color="Kategori", markers=True,
                  title="Tren Unit Terjual per Kategori (Line Chart)")
    st.plotly_chart(fig, width="stretch")
    hari = f.assign(Hari=f["Tanggal"].dt.day_name()).groupby("Hari", as_index=False)["Pendapatan (Rp)"].mean()
    urut = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    hari["Hari"] = pd.Categorical(hari["Hari"], urut, ordered=True)
    fig = px.bar(hari.sort_values("Hari"), x="Hari", y="Pendapatan (Rp)", title="Rata-rata Pendapatan per Hari")
    st.plotly_chart(fig, width="stretch")

# ---------- Tab 5: data & insight ----------
with tab5:
    st.subheader("Insight Otomatis")
    top_k = kat.sort_values("Pendapatan", ascending=False).iloc[0]
    bln = f.groupby("Bulan")["Pendapatan (Rp)"].sum()
    top_p = f.groupby("Produk")["Pendapatan (Rp)"].sum().idxmax()
    unit_k = f.groupby("Kategori")["Jumlah Terjual"].sum().idxmax()
    st.markdown(f"""
- Kategori **{top_k['Kategori']}** menyumbang pendapatan terbesar ({top_k['Pendapatan']/kat['Pendapatan'].sum()*100:.1f}%).
- Produk dengan pendapatan tertinggi: **{top_p}**.
- Kategori dengan unit terjual terbanyak: **{unit_k}** (volume tinggi tidak selalu berarti pendapatan tinggi).
- Bulan pendapatan tertinggi: **{bln.idxmax():%B %Y}**, terendah: **{bln.idxmin():%B %Y}**.
- Korelasi harga-jumlah terjual negatif ({corr:.2f}): barang mahal cenderung terjual lebih sedikit per transaksi.
- Distribusi harga sangat miring ke kanan (skewness {f['Harga (Rp)'].skew():.2f}), sehingga median lebih representatif daripada rata-rata.
""")
    st.subheader("Data Sintesis (1000 baris)")
    st.dataframe(f.drop(columns="Bulan"), width="stretch", hide_index=True)
    st.download_button("⬇️ Unduh CSV (terfilter)", f.drop(columns="Bulan").to_csv(index=False), "data_penjualan_filtered.csv")

st.divider()
st.caption(f"Dibuat oleh {NAMA} (NIM {NIM}) • Data sintesis berbasis contoh Bedah Kasus 1")
