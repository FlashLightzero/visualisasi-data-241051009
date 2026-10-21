"""
Bedah Kasus 1 - Dataset Operasional Penjualan
Generator data sintesis (1000 baris) berdasarkan 2 data contoh di slide:
  Laptop | Elektronik | 8.500.000 | 45  | 01/01/24
  Buku   | Pendidikan | 75.000    | 120 | 02/01/24

NIM  : 241051009
Nama : Muhammad Adrian Oktav Al Fattah
"""
import numpy as np
import pandas as pd

NIM = "241051009"
NAMA = "Muhammad Adrian Oktav Al Fattah"

rng = np.random.default_rng(42)  # seed tetap -> hasil selalu sama

# (produk, kategori, harga dasar Rp, rata-rata jumlah terjual per transaksi)
KATALOG = [
    ("Laptop", "Elektronik", 8_500_000, 45),
    ("Smartphone", "Elektronik", 4_200_000, 60),
    ("Headphone", "Elektronik", 650_000, 90),
    ("Monitor", "Elektronik", 2_100_000, 40),
    ("Buku", "Pendidikan", 75_000, 120),
    ("Alat Tulis", "Pendidikan", 25_000, 200),
    ("Tas Sekolah", "Pendidikan", 180_000, 70),
    ("Kamus", "Pendidikan", 95_000, 50),
    ("Kaos", "Fashion", 85_000, 110),
    ("Jaket", "Fashion", 350_000, 55),
    ("Sepatu", "Fashion", 450_000, 65),
    ("Topi", "Fashion", 60_000, 80),
    ("Kopi Bubuk", "Makanan", 55_000, 150),
    ("Snack Box", "Makanan", 30_000, 220),
    ("Mie Instan", "Makanan", 3_500, 400),
    ("Teh Celup", "Makanan", 18_000, 180),
    ("Blender", "Rumah Tangga", 450_000, 35),
    ("Rice Cooker", "Rumah Tangga", 550_000, 38),
    ("Sapu", "Rumah Tangga", 35_000, 90),
    ("Lampu LED", "Rumah Tangga", 40_000, 130),
]

N = 1000
rows = [
    # 2 data asli dari slide dijadikan baris pertama
    ("Laptop", "Elektronik", 8_500_000, 45, pd.Timestamp("2024-01-01")),
    ("Buku", "Pendidikan", 75_000, 120, pd.Timestamp("2024-01-02")),
]

tanggal_all = pd.date_range("2024-01-01", "2024-12-31")
# Bobot musiman: akhir tahun & tahun ajaran baru (Jul-Aug) lebih ramai, weekend naik
bobot = np.ones(len(tanggal_all))
bulan = tanggal_all.month.values
bobot[np.isin(bulan, [7, 8])] *= 1.3
bobot[np.isin(bulan, [11, 12])] *= 1.5
bobot[tanggal_all.dayofweek.values >= 5] *= 1.25
bobot /= bobot.sum()

while len(rows) < N:
    produk, kategori, harga, rata = KATALOG[rng.integers(len(KATALOG))]
    harga_final = int(round(harga * rng.normal(1.0, 0.08), -2))  # variasi harga ±8%
    jumlah = max(1, int(rng.poisson(rata)))                        # data cacah -> diskrit
    tgl = rng.choice(tanggal_all, p=bobot)
    rows.append((produk, kategori, harga_final, jumlah, pd.Timestamp(tgl)))

df = pd.DataFrame(rows, columns=["Produk", "Kategori", "Harga (Rp)", "Jumlah Terjual", "Tanggal"])
df.to_csv("data_penjualan.csv", index=False)
print(f"[{NIM}] {NAMA}")
print(f"Data sintesis berhasil dibuat: {len(df)} baris -> data_penjualan.csv")
print(df.head())
