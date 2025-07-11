<template>
  <div class="content py-4">
    <div class="card shadow-sm rounded-4 bg-dark-blue mb-4">
      <div class="card-body filter-card-body">
        <div class="search-details">
          <div class="row">
            <div class="col-md-3">
              <label for="kotaKeberangkatan">Kota Keberangkatan</label>
              <input type="text" id="kotaKeberangkatan" v-model="kotaKeberangkatan" class="form-control" placeholder="Kota Keberangkatan" readonly />
            </div>
            <div class="col-md-3">
              <label for="kotaTujuan">Kota Tujuan</label>
              <input type="text" id="kotaTujuan" v-model="kotaTujuan" class="form-control" placeholder="Kota Tujuan" readonly />
            </div>
            <div class="col-md-3">
              <label for="tanggalBerangkat">Tanggal Berangkat</label>
              <input type="date" id="tanggalBerangkat" v-model="tanggalBerangkat" class="form-control" readonly />
            </div>
            <div class="col-md-3">
              <label for="jumlahKursi">Jumlah Kursi</label>
              <input type="number" id="jumlahKursi" v-model="jumlahKursi" class="form-control" min="1" placeholder="Jumlah Kursi" readonly />
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Daftar Bus yang Tersedia -->
    <div class="card shadow-sm rounded-4 bg-light">
      <div class="card-body">
        <div class="bus-list">
          <div v-for="bus in buses" :key="bus.id" class="bus-card">
            <div class="bus-info">
              <h5>{{ bus.nama_bus }}</h5>
              <div class="bus-schedule">
                <span class="departure-time">{{ bus.jam_berangkat }} - {{ bus.jam_tiba }}</span>
                <span class="seats">{{ bus.kursi_tersedia }} kursi tersedia</span>
              </div>
            </div>

            <!-- Tombol Lihat Detail -->
            <div class="bus-price">
              <p>IDR {{ bus.harga }} / kursi</p>
              <router-link :to="{ name: 'DetailJadwal', params: { id: bus.id } }">
                <button class="btn btn-primary">Lihat Detail</button>
              </router-link>
            </div>
          </div>
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
      kotaKeberangkatan: this.$route.query.kotaKeberangkatan || '',
      kotaTujuan: this.$route.query.kotaTujuan || '',
      tanggalBerangkat: this.$route.query.tanggalBerangkat || '',
      jumlahKursi: this.$route.query.jumlahKursi || '',
      buses: [],
    };
  },
  methods: {
    async fetchBuses() {
      try {
        const response = await axios.get('/api/jadwal', {
          params: {
            asal: this.kotaKeberangkatan,
            tujuan: this.kotaTujuan,
            tanggal: this.tanggalBerangkat,
          },
        });
        this.buses = response.data.data;

        if (this.buses.length === 0) {
          Swal.fire({
            icon: 'warning',
            title: 'Tidak ada jadwal yang ditemukan',
            text: 'Silakan coba dengan kriteria pencarian lain.',
          });
        }
      } catch (error) {
        console.error("Error mengambil jadwal:", error);
        Swal.fire({
          icon: 'error',
          title: 'Terjadi kesalahan',
          text: 'Gagal mengambil data jadwal. Coba lagi nanti.',
        });
      }
    },
  },
  mounted() {
    this.fetchBuses(); // Mengambil jadwal berdasarkan query parameters saat halaman dimuat
  },
};
</script>

<style scoped>
/* Styling untuk bagian bus list dan filter */
.bg-dark-blue {
  background: linear-gradient(145deg, #34495e, #2c3e50) !important;
  color: #fff !important;
  box-shadow: 0 6px 15px rgba(0, 0, 0, 0.2);
  border-radius: 5px;
  max-width: 900px;
  margin: 0 auto;
}

.bus-card {
  background-color: #f0f0f0;
  padding: 20px;
  border-radius: 12px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 6px 15px rgba(0, 0, 0, 0.1);
}

.bus-info {
  flex-grow: 1;
  margin-right: 20px;
}

.bus-price {
  text-align: right;
}

button {
  background-color: #34495e;
  color: white;
  border: none;
  border-radius: 5px;
  padding: 6px 12px;
  font-size: 0.7rem;
  cursor: pointer;
  font-weight: bold;
}

button:hover {
  background-color: #2c3e50;
}
</style>