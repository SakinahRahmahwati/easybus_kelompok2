<template>
  <div class="content py-4">
    <div class="card shadow-sm rounded-4 bg-dark-blue">
      <div class="card-header text-white py-3 d-flex justify-content-center">
        <h4 class="card-title mb-0 fw-bold">Detail Jadwal Bus</h4>
      </div>

      <div class="card-body detail-body">
        <div v-if="jadwal">
          <h5 class="text-dark">{{ jadwal.nama_bus }}</h5>
          <p class="text-dark"><strong>Kota Keberangkatan:</strong> {{ jadwal.asal }}</p>
          <p class="text-dark"><strong>Kota Tujuan:</strong> {{ jadwal.tujuan }}</p>
          <p class="text-dark"><strong>Tanggal Berangkat:</strong> {{ jadwal.tanggal }}</p>
          <p class="text-dark"><strong>Jam Berangkat:</strong> {{ jadwal.jam_berangkat }}</p>
          <p class="text-dark"><strong>Jam Tiba:</strong> {{ jadwal.jam_tiba || 'Belum tersedia' }}</p>
          <p class="text-dark"><strong>Harga:</strong> IDR {{ jadwal.harga.toLocaleString() }}</p>
          <p class="text-dark"><strong>Total Kursi:</strong> {{ jadwal.total_kursi }}</p>
          <p class="text-dark"><strong>Kursi Tersedia:</strong> {{ jadwal.kursi_tersedia }}</p>
          <div class="text-center mt-4">
            <button class="btn btn-primary" @click="pilihJadwal">Pilih</button>
          </div>
        </div>
        <div v-else>
          <p>Loading...</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import Swal from 'sweetalert2'; 

export default {
  data() {
    return {
      jadwal: null,
    };
  },
  methods: {
    async ambilJadwal() {
      const id = this.$route.params.id;
      try {
        const response = await axios.get(`/api/jadwal/${id}`);
        this.jadwal = response.data.data;
      } catch (error) {
        console.error("Error mengambil detail jadwal:", error);
        Swal.fire({
          icon: 'error',
          title: 'Terjadi kesalahan',
          text: 'Gagal mengambil detail jadwal. Coba lagi nanti.'
        });
      }
    },
    pilihJadwal() {
      // Kirim data jadwal ke form pemesanan via query string
      this.$router.push({
        path: '/form-pemesanan',
        query: { bus: JSON.stringify(this.jadwal) }
      });
    }
  },
  mounted() {
    this.ambilJadwal();
  },
};
</script>

<style scoped>
/* Styling untuk bagian detail jadwal */
.bg-dark-blue {
  background: linear-gradient(145deg, #34495e, #2c3e50) !important;
  color: #fff !important;
  box-shadow: 0 6px 15px rgba(0, 0, 0, 0.2);
  border-radius: 12px;
  max-width: 900px;
  margin: 0 auto;
}

.card-header {
  padding: 10px 20px;
  font-size: 16px;
}

.detail-body {
  background-color: #f9f9f9;
  border-radius: 12px;
  padding: 20px;
}

.text-dark {
  color: #222 !important;
}

h5 {
  font-weight: bold;
}

p {
  font-size: 1rem;
}
</style>