"""
Bedah Kasus 2 - Dataset Profil Mahasiswa
Generator data sintesis (1000 baris) berdasarkan 2 data contoh di slide:
  Sistem Informasi | 3 | 3.85 | 20
  Manajemen        | 1 | 3.50 | 19

NIM  : 241051009
Nama : Muhammad Adrian Oktav Al Fattah
"""
import numpy as np
import pandas as pd

NIM = "241051009"
NAMA = "Muhammad Adrian Oktav Al Fattah"
rng = np.random.default_rng(42)

# jurusan : (bobot populasi, bonus rata-rata IPK)
JURUSAN = {
    "Sistem Informasi": (0.22, 0.05),
    "Manajemen Informatika": (0.15, 0.00),
    "Teknik Informatika": (0.20, -0.05),
    "Manajemen": (0.18, 0.03),
    "Akuntansi": (0.15, 0.08),
    "Desain Komunikasi Visual": (0.10, 0.02),
}
N = 1000
rows = [("Sistem Informasi", 3, 3.85, 20), ("Manajemen", 1, 3.50, 19)]  # 2 data asli slide

nama_j = list(JURUSAN)
bobot_j = np.array([v[0] for v in JURUSAN.values()])
bobot_j /= bobot_j.sum()
bobot_sem = np.array([.17, .15, .15, .14, .12, .11, .09, .07])  # semester 1-8 (mahasiswa tingkat awal lebih banyak)
bobot_sem /= bobot_sem.sum()

while len(rows) < N:
    j = rng.choice(nama_j, p=bobot_j)
    sem = int(rng.choice(np.arange(1, 9), p=bobot_sem))
    ipk = rng.normal(3.20 + JURUSAN[j][1] + 0.02 * sem, 0.35)      # IPK naik tipis seiring semester
    ipk = round(float(np.clip(ipk, 2.00, 4.00)), 2)
    usia = int(round(rng.normal(18 + sem / 2, 0.8)))                # usia ikut semester
    usia = int(np.clip(usia, 17, 28))
    rows.append((j, sem, ipk, usia))

df = pd.DataFrame(rows, columns=["Jurusan", "Semester", "IPK", "Usia"])
df.to_csv("data_mahasiswa.csv", index=False)
print(f"[{NIM}] {NAMA}")
print(f"Data sintesis berhasil dibuat: {len(df)} baris -> data_mahasiswa.csv")
print(df.head())
