<template>
  <div class="content py-4">
    <div class="card shadow-sm rounded-4 bg-dark-blue">
      <div class="card-header text-white py-3 d-flex justify-content-between align-items-center">
        <h4 class="card-title mb-0 fw-bold">Daftar Data Jadwal Bus</h4>
        <router-link to="/add-jadwal">
          <button class="btn btn-outline-light">
            <i class="fas fa-plus-circle"></i> TAMBAH DATA
          </button>
        </router-link>
      </div>

      <div class="card-body px-4 py-4">
        <div class="table-responsive">
          <table class="table table-striped table-bordered">
            <thead class="text-center text-white">
              <tr>
                <th>No</th>
                <th>Nama Bus</th>
                <th>Kota Keberangkatan</th>
                <th>Kota Tujuan</th>
                <th>Tanggal Keberangkatan</th>
                <th>Jam Keberangkatan</th>
                <th>Jam Tiba</th>
                <th>Harga</th>
                <th>Total Kursi</th>
                <th>Kursi Tersedia</th>
                <th>Aksi</th>
              </tr>
            </thead>
            <tbody>
              <tr v-if="jadwals.length === 0">
                <td colspan="11" class="text-center text-muted">Belum ada data jadwal</td>
              </tr>
              <tr v-for="(jadwal, index) in jadwals" :key="jadwal.id_jadwal">
                <td class="text-center">{{ index + 1 }}</td>
                <td>{{ jadwal.nama_bus }}</td>
                <td>{{ jadwal.asal }}</td>
                <td>{{ jadwal.tujuan }}</td>
                <td>{{ jadwal.tanggal }}</td>
                <td>{{ jadwal.jam_berangkat }}</td>
                <td>{{ jadwal.jam_tiba }}</td>
                <td>{{ jadwal.harga.toLocaleString() }} IDR</td>
                <td>{{ jadwal.total_kursi }}</td>
                <td>{{ jadwal.kursi_tersedia }}</td>
                <td class="text-center">
                  <router-link :to="{ name: 'edit-jadwal', params: { id: jadwal.id_jadwal } }">
                    <button class="btn btn-sm btn-warning">
                      <i class="fas fa-edit"></i> Edit
                    </button>
                  </router-link>
                  <button @click="hapusJadwal(jadwal.id_jadwal)" class="btn btn-sm btn-danger">
                    <i class="fas fa-trash-alt"></i> Hapus
                  </button>
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
import axios from "axios";
import Swal from "sweetalert2";

export default {
  data() {
    return {
      jadwals: [],
    };
  },
  methods: {
    async ambilJadwals() {
      try {
        const response = await axios.get("/api/admin/jadwal");
        this.jadwals = response.data.data;
      } catch (error) {
        Swal.fire({
          icon: 'error',
          title: 'Gagal Memuat Jadwal',
          text: 'Terjadi kesalahan saat mengambil data jadwal.',
        });
      }
    },

    async hapusJadwal(id) {
      try {
        await axios.delete(`/api/admin/jadwal/${id}`);
        this.ambilJadwals();
        Swal.fire({
          icon: 'success',
          title: 'Jadwal Berhasil Dihapus',
          text: 'Data jadwal berhasil dihapus.',
        });
      } catch (error) {
        Swal.fire({
          icon: 'error',
          title: 'Gagal Menghapus Jadwal',
          text: 'Terjadi kesalahan saat menghapus jadwal.',
        });
      }
    }
  },
  mounted() {
    this.ambilJadwals();
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