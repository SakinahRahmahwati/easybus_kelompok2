<template>
  <div class="content py-4">
    <div class="card shadow-sm rounded-4 bg-dark-blue">
      <div class="card-header text-white py-3">
        <h4 class="card-title mb-0 text-center fw-bold">Riwayat Pemesanan Tiket</h4>
      </div>
      <div class="card-body px-4 py-4">
        <div class="table-responsive">
          <table class="table table-striped table-bordered">
            <thead class="text-center text-primary">
              <tr>
                <th>No</th>
                <th>Nama Penumpang</th>
                <th>Jadwal Bus</th>
                <th>Total Bayar</th>
                <th>Status</th>
                <th>Aksi</th>
              </tr>
            </thead>
            <tbody>
              <tr v-if="bookings.length === 0">
                <td colspan="6" class="text-center text-muted">Belum ada pemesanan</td>
              </tr>
              <tr v-for="(booking, index) in bookings" :key="booking.id_pemesanan">
                <td>{{ index + 1 }}</td>
                <td>{{ booking.nama_penumpang }}</td>
                <td>{{ booking.jadwal.asal }} - {{ booking.jadwal.tujuan }} | {{ booking.jadwal.tanggal }} {{
                  booking.jadwal.jam }}</td>
                <td>{{ booking.total_bayar }} IDR</td>
                <td>
                  <span :class="statusClass(booking.status)">{{ booking.status }}</span>
                </td>
                <td>
                  <div v-if="booking.status === 'diterima'" class="d-flex flex-column gap-1">
                    <router-link :to="{ name: 'CetakTiket', params: { id: booking.id_pemesanan } }">
                      <button class="btn btn-sm btn-primary w-100">Lihat e-Tiket</button>
                    </router-link>
                  </div>
                  <span v-else class="text-muted">-</span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      bookings: [],
    };
  },
  methods: {
    fetchBookings() {
      axios.get('/api/histori')
        .then(res => {
          this.bookings = res.data.riwayat;
        })
        .catch(err => {
          console.error("Gagal mengambil histori:", err);
        });
    },
    statusClass(status) {
      return {
        'text-success': status === 'diterima',
        'text-danger': status === 'ditolak',
        'text-warning': status === 'pending'
      };
    },
    cetakTiket(id_pemesanan) {
      const url = this.$router.resolve({ name: 'CetakTiket', params: { id: id_pemesanan } }).href;
      window.open(url, '_blank');
    }
  },
  created() {
    this.fetchBookings();
  }
};
</script>

<style scoped>
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

.card-body {
  background-color: #f9f9f9;
  border-radius: 12px;
  padding: 20px;
}

.table {
  border-collapse: collapse;
  width: 100%;
}

th,
td {
  padding: 12px;
  text-align: center;
  border: 1px solid #ddd;
}

th {
  background-color: #f8f9fa;
  color: #333;
}

tbody tr:nth-child(even) {
  background-color: #f2f2f2;
}

tbody tr:hover {
  background-color: #f1f1f1;
  cursor: pointer;
}

.card-title.fw-bold {
  font-weight: bold;
}

.d-flex {
  margin-top: 20px;
  justify-content: space-between;
}

.btn-outline-light {
  font-size: 14px;
  padding: 8px 15px;
}

.btn-outline-light:hover {
  background-color: #8fbca1;
}

.btn-sm {
  font-size: 14px;
  padding: 5px 10px;
}

span {
  font-size: 16px;
  color: #4CAF50;
  font-weight: 600;
}

button:disabled {
  cursor: not-allowed;
}

button {
  margin: 0 5px;
}

.btn-outline-primary {
  color: #007bff;
  border-color: #007bff;
}

.btn-outline-primary:hover {
  background-color: #007bff;
  color: white;
}
</style>