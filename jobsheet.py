import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

file_path = "nilai_mahasiswa.xlsx"
data = pd.read_excel(file_path)

#pembulatan
data['Rata-rata'] = (
    data['Nilai Tugas'] * 0.3 + 
    data['Nilai UTS'] * 0.3 + 
    data['Nilai UAS'] * 0.4
).round(2)

#Status kelulusan
data['Status'] = data['Rata-rata'].apply(
    lambda x: 'Lulus' if x >= 75 else 'Tidak Lulus'
)

#Nilai urut
data_sorted = data.sort_values('Rata-rata', ascending=False)

#Nilai Tertinggi
nilai_tertinggi = data['Rata-rata'].max()
terbaik = data[data['Rata-rata'] == nilai_tertinggi]

#5 mahasiswa dengan nilai tertinggi
top_5 = data_sorted.head(5)

print("=== Data Mahasiswa dengan Nilai Rata-rata (Bobot) ===")
print("Bobot: Tugas (30%), UTS (30%), UAS (40%)")
print(data_sorted)
print("\nMahasiswa dengan Nilai Tertinggi:")
print(terbaik[['NIM', 'Nama Mahasiswa', 'Rata-rata', 'Status']])
print("\n5 Mahasiswa dengan Nilai Tertinggi:")
print(top_5[['NIM', 'Nama Mahasiswa', 'Rata-rata', 'Status']])

output_file = "hasil_mahasiswa.xlsx"
data.to_excel(output_file, index=False)

rekap_file = "rekap_nilai.xlsx"
data_sorted.to_excel(rekap_file, index=False)

print(f"\nFile hasil telah disimpan ke: {output_file}")
print(f"File rekap telah disimpan ke: {rekap_file}")

print("\n=== STATISTIK ===")
print(f"Jumlah mahasiswa: {len(data)}")
print(f"Jumlah lulus: {len(data[data['Status'] == 'Lulus'])}")
print(f"Jumlah tidak lulus: {len(data[data['Status'] == 'Tidak Lulus'])}")
print(f"Nilai tertinggi: {data['Rata-rata'].max():.2f}")
print(f"Nilai terendah: {data['Rata-rata'].min():.2f}")
print(f"Rata-rata kelas: {data['Rata-rata'].mean():.2f}")

print("\n=== MEMBUAT VISUALISASI GRAFIK ===")

# Set style untuk grafik
plt.style.use('seaborn-v0_8')
fig, axes = plt.subplots(1, 3, figsize=(18, 6))
fig.suptitle('ANALISIS NILAI MAHASISWA', fontsize=16, fontweight='bold')

#Distribusi Status Kelulusan
status_counts = data['Status'].value_counts()
colors = ['#2E8B57', '#DC143C']
axes[0].pie(status_counts.values, labels=status_counts.index, autopct='%1.1f%%', 
           colors=colors, startangle=90)
axes[0].set_title('Distribusi Status Kelulusan')

#Perbandingan Nilai Tugas, UTS, UAS
x = np.arange(len(data_sorted))
width = 0.25
axes[1].bar(x - width, data_sorted['Nilai Tugas'], width, label='Tugas', alpha=0.8)
axes[1].bar(x, data_sorted['Nilai UTS'], width, label='UTS', alpha=0.8)
axes[1].bar(x + width, data_sorted['Nilai UAS'], width, label='UAS', alpha=0.8)
axes[1].set_title('Perbandingan Nilai Tugas, UTS, dan UAS')
axes[1].set_xlabel('Mahasiswa')
axes[1].set_ylabel('Nilai')
axes[1].set_xticks(x)
axes[1].set_xticklabels(data_sorted['Nama Mahasiswa'], rotation=45)
axes[1].legend()

#Mahasiswa dengan Nilai Tertinggi
top_5_sorted = top_5.sort_values('Rata-rata', ascending=True)
axes[2].barh(top_5_sorted['Nama Mahasiswa'], top_5_sorted['Rata-rata'], 
         color=['#FFD700', '#C0C0C0', '#CD7F32', '#2E8B57', '#4169E1'])
axes[2].set_title('TOP 5 MAHASISWA DENGAN NILAI TERTINGGI')
axes[2].set_xlabel('Nilai Rata-rata')
axes[2].set_xlim(0, 100)

for i, v in enumerate(top_5_sorted['Rata-rata']):
    axes[2].text(v + 1, i, f'{v:.2f}', va='center', fontweight='bold')

plt.tight_layout()
plt.savefig('visualisasi_nilai_mahasiswa.png', dpi=300, bbox_inches='tight')
plt.show()

print("Visualisasi grafik telah disimpan sebagai:")
print("   - visualisasi_nilai_mahasiswa.png")