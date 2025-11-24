import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# ============================
# 1. LOAD & CLEAN DATA
# ============================
df = pd.read_excel(r"C:\Users\ADVAN\VS Code Files\miniproject\tuna-fix.xlsx")

required = ["Year", "State", "NMFS Name", "Pounds", "Metric Tons"]
df = df.dropna(subset=required).copy()

df["Pounds"] = pd.to_numeric(df["Pounds"], errors="coerce")
df["Metric Tons"] = pd.to_numeric(df["Metric Tons"], errors="coerce")
df = df.dropna(subset=["Pounds", "Metric Tons"])


# ============================
# 2. AMBIL TOP 5 PER TAHUN (TIDAK DITAMPILKAN)
# ============================
top_per_year = (
    df.sort_values(["Year", "Pounds"], ascending=[True, False])
      .groupby("Year")
      .head(5)
      .reset_index(drop=True)
)

top_per_year["Rank"] = top_per_year.groupby("Year").cumcount() + 1


# ============================
# 3. TOP 5 TAHUN PALING AWAL
# ============================
min_year = df["Year"].min()
first_year_df = top_per_year[top_per_year["Year"] == min_year]

print("\n\n===== TOP 5 TAHUN PALING AWAL =====")
print(f"Tahun: {min_year}")
for _, row in first_year_df.iterrows():
    print(f"{row['Rank']}. {row['State']:<20} {row['Pounds']:.3f}")


# ============================
# 4. TOP 5 TAHUN PALING AKHIR
# ============================
max_year = df["Year"].max()
last_year_df = top_per_year[top_per_year["Year"] == max_year]

print("\n\n===== TOP 5 TAHUN PALING AKHIR =====")
print(f"Tahun: {max_year}")
for _, row in last_year_df.iterrows():
    print(f"{row['Rank']}. {row['State']:<20} {row['Pounds']:.3f}")


# ============================
# 5. TOP 5 ALL-TIME (TOTAL POUNDS + TAHUN AKTIF)
# ============================
state_lifespan = df.groupby("State").agg(
    Total_Pounds=("Pounds", "sum"),
    First_Year=("Year", "min"),
    Last_Year=("Year", "max")
).reset_index()

top_all_time = (
    state_lifespan.sort_values("Total_Pounds", ascending=False)
                  .head(5)
                  .reset_index(drop=True)
)
top_all_time["Rank"] = top_all_time.index + 1

print("\n\n===== TOP 5 STATES ALL-TIME (BY TOTAL POUNDS + TAHUN) =====")
for _, row in top_all_time.iterrows():
    print(f"{row['Rank']}. {row['State']:<20} {row['Total_Pounds']:.3f} Pounds "
          f"(aktif: {row['First_Year']}–{row['Last_Year']})")


# ============================
# 6. TOP 5 TAHUN PRODUKSI TERBANYAK + KOTA TERBANYAK DI TAHUN ITU
# ============================

# Total produksi per tahun
year_totals = (
    df.groupby("Year")["Pounds"]
      .sum()
      .reset_index()
      .sort_values("Pounds", ascending=False)
      .head(5)
      .reset_index(drop=True)
)

# Cari kota terbesar setiap tahun
top_city_each_year = (
    df.groupby(["Year", "State"])["Pounds"]
      .sum()
      .reset_index()
      .sort_values(["Year", "Pounds"], ascending=[True, False])
)

# Ambil kota ranking 1 per tahun
top_city_each_year = top_city_each_year.groupby("Year").first().reset_index()

# Gabungkan
result = year_totals.merge(
    top_city_each_year,
    on="Year",
    suffixes=("_total", "_city")
)

result["Rank"] = result.index + 1

print("\n\n===== TOP 5 TAHUN DENGAN PRODUKSI TERBANYAK =====")
for _, row in result.iterrows():
    print(
        f"{row['Rank']}. {row['Year']} – {row['Pounds_total']:.3f} Pounds "
        f"(kota terbanyak: {row['State']} – {row['Pounds_city']:.3f} Pounds)"
    )


# ============================
# 7. GRAFIK BATANG PER DEKADE
# ============================

df["Decade"] = (df["Year"] // 10) * 10
df["Decade"] = df["Decade"].astype(str) + "s"

pivot_decade = df.pivot_table(
    index="Decade",
    columns="State",
    values="Pounds",
    aggfunc="sum"
)

decades = pivot_decade.index.values
states = pivot_decade.columns
num_states = len(states)

x = np.arange(len(decades))
width = 0.8 / num_states

plt.figure(figsize=(12, 6))

for i, state in enumerate(states):
    plt.bar(
        x + i * width,
        pivot_decade[state].fillna(0),
        width,
        label=state
    )

plt.title("Grafik Batang Penjualan Setiap Kota per Dekade")
plt.xlabel("Dekade")
plt.ylabel("Total Pounds")
plt.xticks(x + width * num_states / 2, decades, rotation=45)

plt.legend(bbox_to_anchor=(1.05, 1), loc="upper left")
plt.tight_layout()
plt.show()
