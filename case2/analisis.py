"""
Bedah Kasus 2 - Analisis Detail Dataset Profil Mahasiswa
NIM  : 241051009
Nama : Muhammad Adrian Oktav Al Fattah
"""
import pandas as pd

NIM = "241051009"
NAMA = "Muhammad Adrian Oktav Al Fattah"

df = pd.read_csv("data_mahasiswa.csv")
line = "=" * 70
print(line)
print(f"ANALISIS DATASET PROFIL MAHASISWA | NIM {NIM} | {NAMA}")
print(line)

print("\n1. STRUKTUR DATA")
print(df.dtypes)
print(f"Jumlah baris: {len(df)} | Missing value: {int(df.isna().sum().sum())} | Duplikat: {int(df.duplicated().sum())}")

print("\n2. DIAGNOSTIK TIPE DATA (sesuai slide)")
diag = pd.DataFrame({
    "Kolom": ["Jurusan", "Semester", "IPK", "Usia"],
    "Tipe Utama": ["Kategorik", "Kategorik", "Numerik", "Numerik"],
    "Sub-Tipe": ["Nominal", "Ordinal", "Kontinu", "Kontinu"],
    "Visualisasi": ["Bar/Pie Chart", "Bar Chart Berurutan", "Histogram / Box Plot", "Histogram / Box Plot"],
})
print(diag.to_string(index=False))

print("\n3. FREKUENSI JURUSAN (Nominal)")
print(df["Jurusan"].value_counts().to_string())

print("\n4. FREKUENSI SEMESTER (Ordinal, diurutkan 1 -> 8)")
print(df["Semester"].value_counts().sort_index().to_string())
print(f"Median semester (valid untuk ordinal): {df['Semester'].median():.0f}")

print("\n5. STATISTIK DESKRIPTIF IPK & USIA")
print(df[["IPK", "Usia"]].describe().round(3).to_string())
print(f"Skewness IPK: {df['IPK'].skew():.2f} | Skewness Usia: {df['Usia'].skew():.2f}")

print("\n6. IPK PER JURUSAN")
print(df.groupby("Jurusan")["IPK"].agg(["count", "mean", "median", "std"]).round(3).sort_values("mean", ascending=False).to_string())

print("\n7. IPK PER SEMESTER")
print(df.groupby("Semester")["IPK"].agg(["count", "mean"]).round(3).to_string())

print("\n8. OUTLIER IPK (metode IQR)")
q1, q3 = df["IPK"].quantile([.25, .75])
iqr = q3 - q1
lo, hi = q1 - 1.5 * iqr, q3 + 1.5 * iqr
out = df[(df["IPK"] < lo) | (df["IPK"] > hi)]
print(f"Batas bawah {lo:.2f} | batas atas {hi:.2f} | jumlah outlier: {len(out)}")

print("\n9. KORELASI")
print(f"IPK vs Usia (Pearson)      : {df['IPK'].corr(df['Usia']):.3f}")
print(f"IPK vs Semester (Spearman) : {df['IPK'].corr(df['Semester'], method='spearman'):.3f}")
print(f"Usia vs Semester (Spearman): {df['Usia'].corr(df['Semester'], method='spearman'):.3f}")

print("\n10. PROPORSI IPK >= 3.50 (cum laude zone) PER JURUSAN")
print((df.assign(Tinggi=df["IPK"] >= 3.5).groupby("Jurusan")["Tinggi"].mean() * 100).round(1).sort_values(ascending=False).to_string())
