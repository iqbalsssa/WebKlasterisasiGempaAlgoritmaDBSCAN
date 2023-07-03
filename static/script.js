// Mendapatkan referensi elemen input file
const fileInput = document.getElementById('file');

// Menambahkan event listener untuk perubahan nilai pada input file
fileInput.addEventListener('change', function() {
    // Mendapatkan nama file yang dipilih
    const fileName = fileInput.value.split('\\').pop();

    // Mendapatkan elemen label terkait dengan input file
    const label = document.querySelector('label[for="file"]');

    // Mengubah teks label menjadi nama file yang dipilih
    label.innerText = fileName;
});

// Melakukan permintaan HTTP menggunakan fetch ke endpoint '/chart-data'
fetch('/chart-data')
  .then(response => response.json())
  .then(data => {
    // Mengubah data yang diterima menjadi format yang sesuai dengan Plotly
    const chartData = data.map(row => ({
      x: row['Longitude'],
      y: row['Latitude'],
      mode: 'markers',
      type: 'scatter',
      marker: {
        color: row['Kluster']
      }
    }));

    // Mengatur layout untuk grafik
    const layout = {
      title: 'Grafik Klastering',
      xaxis: { title: 'Longitude' },
      yaxis: { title: 'Latitude' }
    };

    // Membuat grafik menggunakan Plotly dengan data dan layout yang telah ditentukan
    Plotly.newPlot('chart', chartData, layout);
  })
  .catch(error => {
    // Menangani kesalahan jika terjadi
    console.error('Error:', error);
});
