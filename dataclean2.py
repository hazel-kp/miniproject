import pandas as pd
import numpy as np

# --- 1. BACA DATA ---
df = pd.read_excel("tuna-fix.xlsx")

# --- 2. MEMBERSIHKAN DATA KOSONG ---
required_cols = ["Year", "State", "NMFS Name", "Pounds", "Metric Tons"]

df_clean = df.dropna(subset=required_cols).copy()

# --- 3. KONVERSI KOLOM MENJADI NUMERIC ---
# jika ada teks seperti '1,234' atau ' 900 ' akan otomatis dibersihkan
df_clean["Pounds"] = pd.to_numeric(df_clean["Pounds"], errors="coerce")
df_clean["Metric Tons"] = pd.to_numeric(df_clean["Metric Tons"], errors="coerce")

# Buang baris yang gagal dikonversi
df_clean = df_clean.dropna(subset=["Pounds", "Metric Tons"])

# --- 4. CEK KEC0C0KAN POUNDS <-> METRIC TONS ---
CONVERSION = 2204.62  # 1 metric ton = 2204.62 pounds

df_clean["Pounds_from_MT"] = df_clean["Metric Tons"] * CONVERSION
df_clean["Diff"] = abs(df_clean["Pounds"] - df_clean["Pounds_from_MT"])

tolerance = 5  # batas toleransi selisih
df_clean["Pounds_MT_Mismatch"] = df_clean["Diff"] > tolerance

# --- 5. PERBAIKI DATA YANG TIDAK SESUAI ---
df_clean.loc[df_clean["Pounds_MT_Mismatch"], "Pounds"] = (
    df_clean.loc[df_clean["Pounds_MT_Mismatch"], "Metric Tons"] * CONVERSION
)

# Hapus kolom bantu
df_clean = df_clean.drop(columns=["Pounds_from_MT", "Diff"])

# --- 6. SIMPAN FILE ---
df_clean.to_excel("tuna-fix-cleaned.xlsx", index=False)

print("Data berhasil dibersihkan dan disimpan sebagai tuna-fix-cleaned.xlsx")
print(df_clean.head())
