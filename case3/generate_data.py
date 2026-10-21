"""
Bedah Kasus 3 - Dataset Pengamatan Cuaca
Generator data sintesis (1000 baris) berdasarkan 2 data contoh di slide:
  Jakarta | 32.5 | 75 | Cerah
  Bandung | 24.0 | 85 | Hujan

NIM  : 241051009
Nama : Muhammad Adrian Oktav Al Fattah
"""
import numpy as np
import pandas as pd

NIM = "241051009"
NAMA = "Muhammad Adrian Oktav Al Fattah"
rng = np.random.default_rng(42)

# kota : (suhu dasar C, peluang [Cerah, Berawan, Hujan])
KOTA = {
    "Jakarta": (32.0, [0.40, 0.30, 0.30]),
    "Bandung": (25.5, [0.25, 0.30, 0.45]),
    "Surabaya": (32.5, [0.50, 0.30, 0.20]),
    "Medan": (31.0, [0.35, 0.30, 0.35]),
    "Semarang": (31.5, [0.45, 0.30, 0.25]),
    "Yogyakarta": (29.5, [0.40, 0.30, 0.30]),
    "Makassar": (31.5, [0.50, 0.25, 0.25]),
    "Denpasar": (30.5, [0.50, 0.30, 0.20]),
}
KONDISI = ["Cerah", "Berawan", "Hujan"]
EFEK_SUHU = {"Cerah": 1.0, "Berawan": 0.0, "Hujan": -2.5}    # hujan menurunkan suhu
BASE_RH = {"Cerah": 68, "Berawan": 76, "Hujan": 88}            # hujan menaikkan kelembaban

N = 1000
rows = [("Jakarta", 32.5, 75, "Cerah"), ("Bandung", 24.0, 85, "Hujan")]   # 2 data asli slide
kota_list = list(KOTA)
while len(rows) < N:
    k = rng.choice(kota_list)
    base, p = KOTA[k]
    kond = rng.choice(KONDISI, p=p)
    suhu = round(float(base + EFEK_SUHU[kond] + rng.normal(0, 1.2)), 1)
    rh = int(np.clip(round(BASE_RH[kond] - 1.5 * (suhu - base) + rng.normal(0, 5)), 30, 100))
    rows.append((k, suhu, rh, kond))

df = pd.DataFrame(rows, columns=["Kota", "Suhu (°C)", "Kelembaban (%)", "Kondisi"])
df.to_csv("data_cuaca.csv", index=False, encoding="utf-8-sig")
print(f"[{NIM}] {NAMA}")
print(f"Data sintesis berhasil dibuat: {len(df)} baris -> data_cuaca.csv")
print(df.head())
