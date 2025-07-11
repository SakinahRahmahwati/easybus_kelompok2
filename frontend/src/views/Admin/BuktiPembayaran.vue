<template>
  <div class="content py-4">
    <div class="card shadow-sm rounded-4 bg-dark-blue">
      <div class="card-header text-white py-3 d-flex justify-content-between align-items-center">
        <h4 class="card-title mb-0 fw-bold">Bukti Pembayaran</h4>
      </div>
      <div class="card-body px-4 py-4">
        <div class="table-responsive">
          <table class="table table-striped table-bordered">
            <thead class="text-center text-primary">
              <tr>
                <th>No</th>
                <th>Nama Penumpang</th>
                <th>Kode Tiket</th>
                <th>File Pembayaran</th>
                <th>Status Pembayaran</th>
              </tr>
            </thead>
            <tbody>
              <tr v-if="buktiPembayaran.length === 0">
                <td colspan="5" class="text-center text-muted">Belum ada bukti pembayaran</td>
              </tr>
              <tr v-for="(item, index) in buktiPembayaran" :key="item.id_pemesanan">
                <td class="text-center">{{ index + 1 }}</td>
                <td>{{ item.nama_penumpang }}</td>
                <td>{{ item.kode_tiket }}</td>
                <td><a :href="item.file_url" target="_blank">Lihat Bukti</a></td>
                <td>{{ item.status_pembayaran }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import Swal from 'sweetalert2';

export default {
  data() {
    return {
      buktiPembayaran: [],
    };
  },
  mounted() {
    this.getBuktiPembayaran();
  },
  methods: {
    async getBuktiPembayaran() {
      try {
        const response = await axios.get("/api/admin/bukti");
        this.buktiPembayaran = response.data.data;
      } catch (error) {
        Swal.fire({
          icon: 'error',
          title: 'Gagal Mengambil Bukti Pembayaran',
          text: 'Terjadi kesalahan saat mengambil bukti pembayaran.',
          confirmButtonText: 'Coba Lagi',
        });
        console.error("Error fetching bukti pembayaran:", error);
      }
    },
  },
};
</script>

<style scoped>
.bg-dark-blue {
  background: linear-gradient(145deg, #2c3e50, #34495e) !important;
  color: #fff !important;
  box-shadow: 0 6px 15px rgba(0, 0, 0, 0.2);
  border-radius: 12px;
  max-width: 900px;
  margin: 0 auto;
}

.card-header {
  padding: 10px 20px;
  font-size: 16px;
  background-color: #2c3e50;
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

th, td {
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
</style>