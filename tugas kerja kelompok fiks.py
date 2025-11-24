# ==============================================
# PROGRAM ANALISIS DATA WISUDAWAN (FINAL + NAMA)
# ==============================================
# Dibuat oleh: Muhammad Rizqi Ardiansyah
# Bahasa: Python
# ==============================================
# Fitur:
# 1. Membaca data wisudawan dari Excel
# 2. Menentukan Grade dan Predikat kelulusan
# 3. Menampilkan hasil (Nama, Prodi, IPK, Grade, Predikat)
# 4. Menghitung rata-rata IPK per Prodi
# 5. Menampilkan grafik batang & pie chart
# 6. Menyimpan hasil analisis ke file Excel baru
# ==============================================

import pandas as pd
import matplotlib.pyplot as plt

# -----------------------------------------------------------
# Membaca file Excel berisi data wisudawan
# -----------------------------------------------------------
data = pd.read_excel("hasil_data_wisudawan_fiks.xlsx")

# -----------------------------------------------------------
# Normalisasi nama kolom menjadi huruf kecil tanpa spasi
# agar program tetap jalan walau nama kolom berbeda
# -----------------------------------------------------------
data.columns = data.columns.str.strip().str.lower()

# -----------------------------------------------------------
# Deteksi otomatis kolom penting
# -----------------------------------------------------------
col_nama = next((c for c in data.columns if "nama" in c), None)
col_ipk = next((c for c in data.columns if "ipk" in c), None)
col_prodi = next((c for c in data.columns if "prodi" in c or "program" in c), None)
col_studi = next((c for c in data.columns if "lama" in c or "semester" in c), None)

# -----------------------------------------------------------
# Pastikan semua kolom penting ditemukan
# -----------------------------------------------------------
if not all([col_nama, col_ipk, col_prodi, col_studi]):
    print("❌ Kolom tidak ditemukan! Pastikan file Excel memiliki kolom Nama, IPK, Prodi, dan Lama Studi.")
    print("Kolom yang ditemukan:", data.columns.tolist())
    exit()

# -----------------------------------------------------------
# Fungsi menentukan Grade berdasarkan IPK
# -----------------------------------------------------------
def tentukan_grade(ipk):
    if 3.75 <= ipk <= 4.00:
        return "A"
    elif 3.50 <= ipk < 3.75:
        return "B+"
    elif 3.00 <= ipk < 3.50:
        return "B"
    elif 2.50 <= ipk < 3.00:
        return "C"
    else:
        return "D"

# -----------------------------------------------------------
# Fungsi menentukan Predikat Wisuda berdasarkan IPK & Lama Studi
# -----------------------------------------------------------
def tentukan_predikat(ipk, lama_studi):
    if ipk >= 3.75 and lama_studi <= 8:
        return "Cumlaude (Dengan Pujian)"
    elif ipk >= 3.50 and lama_studi <= 10:
        return "Sangat Memuaskan"
    elif ipk >= 3.00:
        return "Memuaskan"
    else:
        return "Cukup"

# -----------------------------------------------------------
# Tambahkan kolom baru untuk Grade dan Predikat
# -----------------------------------------------------------
data["grade"] = data[col_ipk].apply(tentukan_grade)
data["predikat"] = data.apply(lambda x: tentukan_predikat(x[col_ipk], x[col_studi]), axis=1)

# -----------------------------------------------------------
# Tampilkan hasil analisis ke terminal
# -----------------------------------------------------------
print("\n=== HASIL ANALISIS DATA WISUDAWAN ===")
print("--------------------------------------------------------------")
print(f"{'Nama':25} {'Prodi':20} {'IPK':5} {'Grade':6} {'Predikat'}")
print("--------------------------------------------------------------")

# Menampilkan setiap baris data hasil analisis
for i, row in data.iterrows():
    print(f"{row[col_nama]:25} {row[col_prodi]:20} {row[col_ipk]:<5.2f} {row['grade']:<6} {row['predikat']}")

print("--------------------------------------------------------------")

# -----------------------------------------------------------
# Menghitung rata-rata IPK per Prodi
# -----------------------------------------------------------
rata_ipk = data.groupby(col_prodi)[col_ipk].mean().reset_index()

print("\n=== RATA-RATA IPK PER PRODI ===")
for i, row in rata_ipk.iterrows():
    print(f"{row[col_prodi]:20}: {row[col_ipk]:.2f}")

# -----------------------------------------------------------
# Grafik batang jumlah wisudawan per program studi
# -----------------------------------------------------------
plt.figure(figsize=(8,5))
plt.bar(data[col_prodi].value_counts().index, data[col_prodi].value_counts().values)
plt.title("Jumlah Wisudawan per Program Studi")
plt.xlabel("Program Studi")
plt.ylabel("Jumlah Wisudawan")
plt.xticks(rotation=30)
plt.tight_layout()
plt.show()

# -----------------------------------------------------------
# Grafik lingkaran (pie chart) distribusi predikat kelulusan
# -----------------------------------------------------------
predikat_count = data["predikat"].value_counts()

# Daftar warna berbeda untuk setiap predikat
# Warna Cumlaude dibuat paling mencolok (kuning terang)
warna_map = {
    "Cumlaude (Dengan Pujian)": "red",  # mencolok
    "Sangat Memuaskan": "skyblue",
    "Memuaskan": "lightcoral",
    "Cukup": "plum",
}

# Jika ada predikat di luar daftar, beri warna default
warna_khusus = [warna_map.get(label, "lightgray") for label in predikat_count.index]

plt.figure(figsize=(6,6))
plt.pie(
    predikat_count,
    labels=predikat_count.index,
    autopct='%1.1f%%',
    startangle=90,
    colors=warna_khusus,
    shadow=True,  # efek bayangan agar tampil menonjol
    textprops={'fontsize': 10}
)
plt.title("Distribusi Predikat Kelulusan (Cumlaude Berwarna Mencolok)")
plt.show()

# -----------------------------------------------------------
# Grafik perbandingan rata-rata IPK antar program studi
# -----------------------------------------------------------
plt.figure(figsize=(8,5))
plt.bar(rata_ipk[col_prodi], rata_ipk[col_ipk], color='skyblue')
plt.title("Perbandingan Rata-Rata IPK Antar Program Studi")
plt.xlabel("Program Studi")
plt.ylabel("Rata-Rata IPK")
plt.xticks(rotation=30)
plt.tight_layout()
plt.show()

# -----------------------------------------------------------
# Simpan hasil analisis ke file Excel baru
# -----------------------------------------------------------
data.to_excel("hasil_analisis_wisudawan.xlsx", index=False)
print("\n✅ File 'hasil_analisis_wisudawan.xlsx' berhasil dibuat!")
