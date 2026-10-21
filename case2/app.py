"""
Bedah Kasus 2 - Dashboard Dataset Profil Mahasiswa (Streamlit)
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

st.set_page_config(page_title="Dashboard Mahasiswa | Kasus 2", page_icon="🎓", layout="wide")


@st.cache_data
def load_data():
    df = pd.read_csv(BASE / "data_mahasiswa.csv")
    df["Semester"] = pd.Categorical(df["Semester"], categories=list(range(1, 9)), ordered=True)
    return df


df = load_data()

st.title("🎓 Dashboard Profil Mahasiswa")
st.caption("Visualisasi Data • Pertemuan 2 • Bedah Kasus 2")
st.info(f"**NIM:** {NIM}  |  **Nama:** {NAMA}")

st.sidebar.header("Filter Data")
st.sidebar.markdown(f"**{NAMA}**  \nNIM {NIM}")
jur = st.sidebar.multiselect("Jurusan", sorted(df["Jurusan"].unique()), default=sorted(df["Jurusan"].unique()))
sem = st.sidebar.slider("Rentang Semester", 1, 8, (1, 8))
ipk_r = st.sidebar.slider("Rentang IPK", 2.0, 4.0, (2.0, 4.0), step=0.05)

f = df[df["Jurusan"].isin(jur) & df["Semester"].astype(int).between(*sem) & df["IPK"].between(*ipk_r)]
if f.empty:
    st.warning("Tidak ada data untuk filter ini.")
    st.stop()

k1, k2, k3, k4 = st.columns(4)
k1.metric("Jumlah Mahasiswa", f"{len(f):,}")
k2.metric("Rata-rata IPK", f"{f['IPK'].mean():.2f}")
k3.metric("Median Usia", f"{f['Usia'].median():.0f} th")
k4.metric("IPK ≥ 3.50", f"{(f['IPK'] >= 3.5).mean()*100:.1f}%")

tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["🧬 Diagnostik Tipe Data", "🏫 Nominal: Jurusan", "📶 Ordinal: Semester", "📈 Numerik: IPK & Usia", "🗂️ Data & Insight"])

with tab1:
    st.subheader("Hasil Diagnostik Tipe Data per Kolom")
    diag = pd.DataFrame({
        "Kolom": ["Jurusan", "Semester", "IPK", "Usia"],
        "Tipe Utama": ["Kategorik", "Kategorik", "Numerik", "Numerik"],
        "Sub-Tipe": ["Nominal", "Ordinal", "Kontinu", "Kontinu"],
        "Alasan": ["Hanya label pembeda", "Ada tingkatan jelas (1 → 2 → 3), jarak belum tentu sama",
                   "Hasil ukur berupa desimal", "Hasil ukur berupa rentang"],
        "Visualisasi Terbaik": ["Bar / Pie Chart", "Bar Chart Berurutan",
                                "Histogram (distribusi) / Box Plot (sebaran & outlier)", "Histogram / Box Plot"],
    })
    st.dataframe(diag, width="stretch", hide_index=True)
    st.success("Aturan emas: pilih grafik berdasarkan tipe datanya, bukan berdasarkan apa yang terlihat indah.")

with tab2:
    c1, c2 = st.columns(2)
    jc = f["Jurusan"].value_counts().reset_index()
    jc.columns = ["Jurusan", "Jumlah"]
    with c1:
        st.plotly_chart(px.bar(jc, x="Jurusan", y="Jumlah", color="Jurusan", text_auto=True,
                               title="Jumlah Mahasiswa per Jurusan (Bar Chart)").update_layout(showlegend=False), width="stretch")
    with c2:
        st.plotly_chart(px.pie(jc, names="Jurusan", values="Jumlah", hole=0.4,
                               title="Proporsi Mahasiswa per Jurusan (Pie Chart)"), width="stretch")
    st.plotly_chart(px.bar(f.groupby("Jurusan", as_index=False)["IPK"].mean().sort_values("IPK"), x="IPK", y="Jurusan",
                           orientation="h", title="Rata-rata IPK per Jurusan").update_xaxes(range=[2.5, 4]), width="stretch")

with tab3:
    sc = f["Semester"].value_counts().sort_index().reset_index()
    sc.columns = ["Semester", "Jumlah"]
    sc["Semester"] = sc["Semester"].astype(str)
    st.plotly_chart(px.bar(sc, x="Semester", y="Jumlah", text_auto=True,
                           title="Jumlah Mahasiswa per Semester (Bar Chart Berurutan)"), width="stretch")
    sm = f.groupby("Semester", observed=True, as_index=False)["IPK"].mean()
    sm["Semester"] = sm["Semester"].astype(str)
    st.plotly_chart(px.bar(sm, x="Semester", y="IPK", text_auto=".2f", title="Rata-rata IPK per Semester").update_yaxes(range=[2.5, 4]),
                    width="stretch")
    st.caption("Semester adalah ordinal: urutannya bermakna, tetapi jaraknya tidak diasumsikan sama. Karena itu median lebih tepat daripada rata-rata untuk ringkasan semester.")

with tab4:
    c1, c2 = st.columns(2)
    with c1:
        st.plotly_chart(px.histogram(f, x="IPK", nbins=30, title="Distribusi IPK (Histogram)"), width="stretch")
    with c2:
        st.plotly_chart(px.histogram(f, x="Usia", nbins=12, title="Distribusi Usia (Histogram)"), width="stretch")
    c3, c4 = st.columns(2)
    with c3:
        st.plotly_chart(px.box(f, x="Jurusan", y="IPK", color="Jurusan", title="Sebaran IPK per Jurusan (Box Plot)")
                        .update_layout(showlegend=False), width="stretch")
    with c4:
        st.plotly_chart(px.box(f, x="Semester", y="Usia", title="Sebaran Usia per Semester (Box Plot)"), width="stretch")
    st.plotly_chart(px.scatter(f, x="Usia", y="IPK", color="Jurusan", opacity=0.6, title="Usia vs IPK (Scatter Plot)"), width="stretch")
    st.dataframe(f[["IPK", "Usia"]].describe().round(3), width="stretch")

with tab5:
    st.subheader("Insight Otomatis")
    best = f.groupby("Jurusan")["IPK"].mean().idxmax()
    top = f["Jurusan"].value_counts().idxmax()
    c_sem = f["IPK"].corr(f["Semester"].astype(int), method="spearman")
    st.markdown(f"""
- Jurusan dengan mahasiswa terbanyak: **{top}**.
- Jurusan dengan rata-rata IPK tertinggi: **{best}** ({f.groupby('Jurusan')['IPK'].mean().max():.2f}).
- Median IPK **{f['IPK'].median():.2f}**, rata-rata **{f['IPK'].mean():.2f}**, simpangan baku **{f['IPK'].std():.2f}**.
- Korelasi IPK vs semester (Spearman): **{c_sem:.2f}**, hubungannya lemah.
- Usia bergerak seiring semester (korelasi Usia-Semester {f['Usia'].corr(f['Semester'].astype(int), method='spearman'):.2f}).
""")
    st.subheader("Data Sintesis (1000 baris)")
    st.dataframe(f, width="stretch", hide_index=True)
    st.download_button("⬇️ Unduh CSV (terfilter)", f.to_csv(index=False), "data_mahasiswa_filtered.csv")

st.divider()
st.caption(f"Dibuat oleh {NAMA} (NIM {NIM}) • Data sintesis berbasis contoh Bedah Kasus 2")
