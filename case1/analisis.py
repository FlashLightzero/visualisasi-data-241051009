"""
Bedah Kasus 1 - Analisis Detail Dataset Operasional Penjualan
NIM  : 241051009
Nama : Muhammad Adrian Oktav Al Fattah
"""
import pandas as pd
import numpy as np

NIM = "241051009"
NAMA = "Muhammad Adrian Oktav Al Fattah"

df = pd.read_csv("data_penjualan.csv", parse_dates=["Tanggal"])
df["Pendapatan (Rp)"] = df["Harga (Rp)"] * df["Jumlah Terjual"]
df["Bulan"] = df["Tanggal"].dt.to_period("M").astype(str)

line = "=" * 70
print(line)
print(f"ANALISIS DATASET PENJUALAN | NIM {NIM} | {NAMA}")
print(line)

print("\n1. STRUKTUR DATA")
print(df[["Produk", "Kategori", "Harga (Rp)", "Jumlah Terjual", "Tanggal"]].dtypes)
print(f"Jumlah baris: {len(df)} | Missing value: {int(df.isna().sum().sum())} | Duplikat: {int(df.duplicated().sum())}")

print("\n2. DIAGNOSTIK TIPE DATA (sesuai slide)")
diag = pd.DataFrame({
    "Kolom": ["Produk", "Kategori", "Harga (Rp)", "Jumlah Terjual", "Tanggal"],
    "Tipe Utama": ["Kategorik", "Kategorik", "Numerik", "Numerik", "Waktu"],
    "Sub-Tipe": ["Nominal", "Nominal", "Kontinu", "Diskrit", "Interval"],
    "Skala": ["Nominal", "Nominal", "Rasio", "Rasio", "Interval"],
    "Visualisasi": ["Bar/Pie Chart", "Bar/Pie Chart", "Histogram", "Histogram/Bar Chart", "Line Chart"],
})
print(diag.to_string(index=False))

print("\n3. STATISTIK DESKRIPTIF")
print(df[["Harga (Rp)", "Jumlah Terjual", "Pendapatan (Rp)"]].describe().round(2).to_string())
print(f"Skewness harga: {df['Harga (Rp)'].skew():.2f} | Skewness jumlah: {df['Jumlah Terjual'].skew():.2f}")

print("\n4. FREKUENSI KATEGORI")
print(df["Kategori"].value_counts().to_string())

print("\n5. PENDAPATAN PER KATEGORI")
kat = df.groupby("Kategori").agg(
    Transaksi=("Produk", "count"),
    Unit=("Jumlah Terjual", "sum"),
    Pendapatan=("Pendapatan (Rp)", "sum"),
).sort_values("Pendapatan", ascending=False)
kat["Kontribusi %"] = (kat["Pendapatan"] / kat["Pendapatan"].sum() * 100).round(1)
print(kat.to_string())

print("\n6. TOP 5 PRODUK (PENDAPATAN)")
print(df.groupby("Produk")["Pendapatan (Rp)"].sum().nlargest(5).to_string())

print("\n7. TREN BULANAN")
tren = df.groupby("Bulan")["Pendapatan (Rp)"].sum()
print(tren.to_string())
print(f"Bulan tertinggi: {tren.idxmax()} | terendah: {tren.idxmin()}")

print("\n8. OUTLIER HARGA (metode IQR)")
q1, q3 = df["Harga (Rp)"].quantile([.25, .75])
iqr = q3 - q1
out = df[(df["Harga (Rp)"] > q3 + 1.5 * iqr)]
print(f"Batas atas: Rp{q3 + 1.5 * iqr:,.0f} | Jumlah outlier: {len(out)} (didominasi: {', '.join(out['Produk'].value_counts().head(3).index)})")

print("\n9. KORELASI Harga vs Jumlah Terjual")
print(f"Pearson: {df['Harga (Rp)'].corr(df['Jumlah Terjual']):.3f}  (negatif = barang mahal cenderung terjual lebih sedikit)")
print(f"Spearman: {df['Harga (Rp)'].corr(df['Jumlah Terjual'], method='spearman'):.3f}")

print("\n10. POLA HARI")
hari = df.groupby(df["Tanggal"].dt.dayofweek)["Pendapatan (Rp)"].mean().round(0)
hari.index = ["Sen", "Sel", "Rab", "Kam", "Jum", "Sab", "Min"]
print(hari.to_string())
