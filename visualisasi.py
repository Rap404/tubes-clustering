import pandas as pd
import matplotlib.pyplot as plt
import re

from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score

# =========================
# FUNGSI MEMBERSIHKAN ANGKA
# =========================

def clean_number(value):
    value = str(value).lower()

    # Ambil semua angka
    numbers = re.findall(r'\d+\.?\d*', value)

    if len(numbers) == 0:
        return 0

    # Jika format range seperti 3-5
    if len(numbers) >= 2:
        nums = [float(n) for n in numbers]
        return sum(nums) / len(nums)

    return float(numbers[0])

# =========================
# LOAD CSV TANPA HEADER
# =========================

df = pd.read_csv(
    "data_kmeans_mahasiswa.csv",
    header=None
)

# Tambahkan nama kolom manual
df.columns = [
    "timestamp",
    "email",
    "nama",
    "universitas",
    "angkatan",
    "organisasi",
    "belajar",
    "hobi"
]

# =========================
# MEMBERSIHKAN DATA
# =========================

df["organisasi"] = df["organisasi"].apply(clean_number)
df["belajar"] = df["belajar"].apply(clean_number)
df["hobi"] = df["hobi"].apply(clean_number)

# =========================
# FITUR CLUSTERING
# =========================

fitur = df[[
    "organisasi",
    "belajar",
    "hobi"
]]

# =========================
# NORMALISASI
# =========================

scaler = MinMaxScaler()

data_normal = scaler.fit_transform(fitur)

# =========================
# K-MEANS
# =========================

kmeans = KMeans(
    n_clusters=3,
    random_state=42
)

cluster = kmeans.fit_predict(data_normal)

df["cluster"] = cluster

# =========================
# EVALUASI MODEL
# =========================

score = silhouette_score(
    data_normal,
    cluster
)

print("\n===== EVALUASI MODEL =====")
print("Silhouette Score :", round(score, 3))

# =========================
# PCA
# =========================

pca = PCA(n_components=2)

pca_result = pca.fit_transform(data_normal)

df["PCA1"] = pca_result[:, 0]
df["PCA2"] = pca_result[:, 1]

# =========================
# SCATTER PLOT PCA
# =========================

plt.figure(figsize=(8, 6))

for i in range(3):
    cluster_data = df[df["cluster"] == i]

    plt.scatter(
        cluster_data["PCA1"],
        cluster_data["PCA2"],
        label=f"Cluster {i+1}"
    )

plt.title("Scatter Plot PCA Hasil Clustering")
plt.xlabel("PCA Component 1")
plt.ylabel("PCA Component 2")
plt.legend()

plt.show()

# =========================
# BAR CHART DISTRIBUSI
# =========================

jumlah_cluster = (
    df["cluster"]
    .value_counts()
    .sort_index()
)

plt.figure(figsize=(6, 5))

plt.bar(
    [f"Cluster {i+1}" for i in jumlah_cluster.index],
    jumlah_cluster.values
)

plt.title("Distribusi Jumlah Mahasiswa per Cluster")
plt.xlabel("Cluster")
plt.ylabel("Jumlah Mahasiswa")

plt.show()

# =========================
# MENAMPILKAN HASIL
# =========================

print("\n===== HASIL CLUSTERING =====")

for i in range(3):
    print(f"\n--- CLUSTER {i+1} ---")

    anggota = df[df["cluster"] == i]

    for nama in anggota["nama"]:
        print("-", nama)