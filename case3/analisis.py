"""
Bedah Kasus 3 - Analisis Detail Dataset Pengamatan Cuaca
NIM  : 241051009
Nama : Muhammad Adrian Oktav Al Fattah
"""
import pandas as pd

NIM = "241051009"
NAMA = "Muhammad Adrian Oktav Al Fattah"

df = pd.read_csv("data_cuaca.csv")
line = "=" * 70
print(line)
print(f"ANALISIS DATASET PENGAMATAN CUACA | NIM {NIM} | {NAMA}")
print(line)

print("\n1. STRUKTUR DATA")
print(df.dtypes)
print(f"Jumlah baris: {len(df)} | Missing value: {int(df.isna().sum().sum())} | Duplikat: {int(df.duplicated().sum())}")

print("\n2. DIAGNOSTIK TIPE DATA (sesuai slide)")
diag = pd.DataFrame({
    "Kolom": ["Kota", "Suhu (°C)", "Kelembaban (%)", "Kondisi"],
    "Tipe Utama": ["Kategorik", "Numerik", "Numerik", "Kategorik"],
    "Skala": ["Nominal", "Interval", "Rasio", "Nominal"],
    "Alasan": ["Label tanpa urutan", "Tidak ada nol absolut", "0% = tidak ada kelembaban (nol absolut)", "Label tanpa urutan"],
})
print(diag.to_string(index=False))

print("\n3. BUKTI: SUHU CELSIUS = INTERVAL (rasio tidak berlaku)")
c1, c2 = 10, 20
print(f"20°C / 10°C = {c2/c1:.2f}  (tampak '2x lebih panas')")
print(f"Dalam Kelvin: {c2+273.15:.2f} K / {c1+273.15:.2f} K = {(c2+273.15)/(c1+273.15):.3f}  -> ternyata hanya ~1.04x")
print("Kesimpulan: rasio pada Celsius menyesatkan; hanya selisih (+, -) yang bermakna.")

print("\n4. FREKUENSI KOTA & KONDISI")
print(df["Kota"].value_counts().to_string())
print()
print(df["Kondisi"].value_counts().to_string())

print("\n5. STATISTIK DESKRIPTIF")
print(df[["Suhu (°C)", "Kelembaban (%)"]].describe().round(2).to_string())
print(f"Skewness suhu: {df['Suhu (°C)'].skew():.2f} | Skewness kelembaban: {df['Kelembaban (%)'].skew():.2f}")

print("\n6. RATA-RATA PER KOTA")
print(df.groupby("Kota")[["Suhu (°C)", "Kelembaban (%)"]].mean().round(2).sort_values("Suhu (°C)", ascending=False).to_string())

print("\n7. RATA-RATA PER KONDISI")
print(df.groupby("Kondisi")[["Suhu (°C)", "Kelembaban (%)"]].mean().round(2).to_string())

print("\n8. TABEL SILANG KOTA x KONDISI (%)")
print((pd.crosstab(df["Kota"], df["Kondisi"], normalize="index") * 100).round(1).to_string())

print("\n9. OUTLIER (metode IQR)")
for col in ["Suhu (°C)", "Kelembaban (%)"]:
    q1, q3 = df[col].quantile([.25, .75])
    i = q3 - q1
    n = int(((df[col] < q1 - 1.5 * i) | (df[col] > q3 + 1.5 * i)).sum())
    print(f"{col}: {n} outlier")

print("\n10. KORELASI Suhu vs Kelembaban")
print(f"Pearson : {df['Suhu (°C)'].corr(df['Kelembaban (%)']):.3f}")
print(f"Spearman: {df['Suhu (°C)'].corr(df['Kelembaban (%)'], method='spearman'):.3f}")
print("(negatif = semakin panas, kelembaban relatif cenderung turun)")
