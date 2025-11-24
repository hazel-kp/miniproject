import pandas as pd
import matplotlib.pyplot as plt

# --- 1. BACA DATA ---
df = pd.read_excel("tuna-fix-cleaned.xlsx")

# --- 2. MEMBERSIHKAN DATA ---
required_cols = ["Year", "State", "NMFS Name", "Pounds", "Metric Tons"]
df_clean = df.dropna(subset=required_cols).copy()

df_clean["Pounds"] = pd.to_numeric(df_clean["Pounds"], errors="coerce")
df_clean["Metric Tons"] = pd.to_numeric(df_clean["Metric Tons"], errors="coerce")
df_clean = df_clean.dropna(subset=["Pounds", "Metric Tons"])

# -----------------------------
#         GRAFIK 1
#   TOTAL POUNDS PER YEAR
# -----------------------------
plt.figure()
df_clean.groupby("Year")["Pounds"].sum().plot()
plt.title("Total Pounds per Year")
plt.xlabel("Year")
plt.ylabel("Pounds")
plt.tight_layout()
plt.show()

# -----------------------------
#         GRAFIK 2
#   TOTAL METRIC TONS PER STATE
# -----------------------------
plt.figure()
df_clean.groupby("State")["Metric Tons"].sum().plot(kind="bar")
plt.title("Total Metric Tons per State")
plt.xlabel("State")
plt.ylabel("Metric Tons")
plt.tight_layout()
plt.show()

# -----------------------------
#         GRAFIK 3
#   SCATTER POUNDS vs METRIC TONS
# -----------------------------
plt.figure()
plt.scatter(df_clean["Pounds"], df_clean["Metric Tons"])
plt.title("Relationship between Pounds and Metric Tons")
plt.xlabel("Pounds")
plt.ylabel("Metric Tons")
plt.tight_layout()
plt.show()

# -----------------------------
#         GRAFIK 4
#         PIE CHART
# -----------------------------
plt.figure()
state_totals = df_clean.groupby("State")["Pounds"].sum()
plt.pie(state_totals, labels=state_totals.index, autopct="%1.1f%%")
plt.title("Percentage of Total Pounds by State")
plt.tight_layout()
plt.show()
import pandas as pd
import matplotlib.pyplot as plt

# --- 1. BACA DATA ---
df = pd.read_excel("tuna-fix-cleaned.xlsx")

# --- 2. MEMBERSIHKAN DATA ---
required_cols = ["Year", "State", "NMFS Name", "Pounds", "Metric Tons"]
df_clean = df.dropna(subset=required_cols).copy()

df_clean["Pounds"] = pd.to_numeric(df_clean["Pounds"], errors="coerce")
df_clean["Metric Tons"] = pd.to_numeric(df_clean["Metric Tons"], errors="coerce")
df_clean = df_clean.dropna(subset=["Pounds", "Metric Tons"])

# -----------------------------
#         GRAFIK 1
#   TOTAL POUNDS PER YEAR
# -----------------------------
plt.figure()
df_clean.groupby("Year")["Pounds"].sum().plot()
plt.title("Total Pounds per Year")
plt.xlabel("Year")
plt.ylabel("Pounds")
plt.tight_layout()
plt.show()

# -----------------------------
#         GRAFIK 2
#   TOTAL METRIC TONS PER STATE
# -----------------------------
plt.figure()
df_clean.groupby("State")["Metric Tons"].sum().plot(kind="bar")
plt.title("Total Metric Tons per State")
plt.xlabel("State")
plt.ylabel("Metric Tons")
plt.tight_layout()
plt.show()

# -----------------------------
#         GRAFIK 3
#   SCATTER POUNDS vs METRIC TONS
# -----------------------------
plt.figure()
plt.scatter(df_clean["Pounds"], df_clean["Metric Tons"])
plt.title("Relationship between Pounds and Metric Tons")
plt.xlabel("Pounds")
plt.ylabel("Metric Tons")
plt.tight_layout()
plt.show()

# -----------------------------
#         GRAFIK 4
#         PIE CHART
# -----------------------------
plt.figure()
state_totals = df_clean.groupby("State")["Pounds"].sum()
plt.pie(state_totals, labels=state_totals.index, autopct="%1.1f%%")
plt.title("Percentage of Total Pounds by State")
plt.tight_layout()
plt.show()
