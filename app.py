import os  # Modul untuk berinteraksi dengan sistem operasi
import pandas as pd  # Modul untuk manipulasi dan analisis data menggunakan DataFrame
import numpy as np  # Modul untuk komputasi numerik
from flask import Flask, render_template, request  # Modul untuk membuat aplikasi web menggunakan Flask
from sklearn.cluster import DBSCAN  # Modul untuk mengimplementasikan algoritma DBSCAN
from sklearn.preprocessing import MinMaxScaler  # Modul untuk melakukan normalisasi data menggunakan MinMaxScaler

from sklearn.preprocessing import MinMaxScaler

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

def perform_clustering(file_path):
    # Membaca file csv menggunakan pandas
    driver = pd.read_csv(file_path, delimiter=";")

    # Menghapus kolom yang tidak diperlukan
    driver_x = driver.drop(["Nomor_KK", "Nama_KK", "Alamat_Asli"], axis=1)

    # Mengubah data menjadi array numpy
    x_array = np.array(driver_x)

    # Normalisasi data menggunakan MinMaxScaler
    scaler = MinMaxScaler()
    x_scaled = scaler.fit_transform(x_array)

    # Melakukan klastering menggunakan DBSCAN
    db = DBSCAN(eps=0.1, min_samples=3)
    db.fit(x_scaled)

    # Mendapatkan label klaster dan jumlah klaster yang terbentuk
    labels = db.labels_
    n_raw = len(labels)
    n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)

    # Menambahkan kolom klaster pada DataFrame
    driver["Kluster"] = db.labels_

    # Mengkonversi hasil klastering menjadi list
    result = driver.values.tolist()

    return result, n_clusters_

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)

            # Melakukan klastering pada file yang diunggah
            result, n_clusters = perform_clustering(file_path)

            # Menampilkan hasil klastering pada halaman HTML menggunakan template index.html
            return render_template('index.html', data=result, n_clusters=n_clusters)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
