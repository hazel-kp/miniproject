import pandas as pd
import numpy as np

# --- 1. BACA DATA ---
df = pd.read_excel("tuna-fix.xlsx")

# --- 2. MEMBERSIHKAN DATA KOSONG ---
# Pilih kolom wajib yang tidak boleh kosong
required_cols = ["Year", "State", "NMFS Name", "Pounds", "Metric Tons"]

# Hapus baris yang kosong pada kolom-kolom tersebut
df_clean = df.dropna(subset=required_cols).copy()

# --- 3. CEK DAN PERBAIKI KETIDAKCOCOKAN POUNDS <-> METRIC TONS ---
CONVERSION = 2204.62  # 1 metric ton = 2204.62 pounds

# Hitung pounds hasil konversi
df_clean["Pounds_from_MT"] = df_clean["Metric Tons"] * CONVERSION

# Hitung selisih
df_clean["Diff"] = abs(df_clean["Pounds"] - df_clean["Pounds_from_MT"])

# Tandai data yang tidak sesuai (selisih di atas ambang toleransi)
tolerance = 5  # boleh ubah sesuai kebutuhan
df_clean["Pounds_MT_Mismatch"] = df_clean["Diff"] > tolerance

# --- 4. OPSIONAL: PERBAIKI DATA YANG SALAH ---
# Jika Pounds salah → ganti dengan perhitungan yang benar
df_clean.loc[df_clean["Pounds_MT_Mismatch"], "Pounds"] = (
    df_clean.loc[df_clean["Pounds_MT_Mismatch"], "Metric Tons"] * CONVERSION
)

# Hapus kolom bantu
df_clean = df_clean.drop(columns=["Pounds_from_MT", "Diff"])

# --- 5. SIMPAN HASIL BERSIH ---
df_clean.to_excel("tuna-fix-cleaned.xlsx", index=False)

print("Data berhasil dibersihkan dan disimpan sebagai tuna-fix-cleaned.xlsx")
print(df_clean.head())
