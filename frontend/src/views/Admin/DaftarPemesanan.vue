<template>
  <div class="content py-4">
    <div class="card shadow-sm rounded-4 bg-dark-blue">
      <div class="card-header text-white py-3 d-flex justify-content-between align-items-center">
        <h4 class="card-title mb-0 fw-bold">Daftar Pemesanan Customer</h4>
        <button @click="exportPDF" class="btn btn-outline-light">
          <i class="fas fa-file-pdf me-2"></i> EKSPOR PDF
        </button>
      </div>

      <div class="card-body px-4 py-4">
        <div class="table-responsive">
          <table class="table table-striped table-bordered">
            <thead class="text-center text-primary">
              <tr>
                <th>No</th>
                <th>Nama Penumpang</th>
                <th>Kota Keberangkatan</th>
                <th>Kota Tujuan</th>
                <th>Jam Berangkat</th>
                <th>Jam Tiba</th>
                <th>Jumlah Tiket</th>
                <th>Total Bayar</th>
                <th>Status Pembayaran</th>
                <th>Aksi</th>
              </tr>
            </thead>
            <tbody>
              <tr v-if="pemesanan.length === 0">
                <td colspan="10" class="text-center text-muted">Belum ada pemesanan</td>
              </tr>
              <tr v-for="(item, index) in paginatedData" :key="item.id_pemesanan">
                <td class="text-center">{{ index + 1 + (currentPage - 1) * pageSize }}</td>
                <td>{{ item.nama_penumpang }}</td>
                <td>{{ item.asal }}</td>
                <td>{{ item.tujuan }}</td>
                <td>{{ item.jam_berangkat }}</td>
                <td>{{ item.jam_tiba }}</td>
                <td>{{ item.jumlah_tiket }}</td>
                <td>{{ item.total_bayar }}</td>
                <td class="text-center">
                  <span :class="{
                    'text-warning': item.status_pembayaran === 'pending',
                    'text-success': item.status_pembayaran === 'diterima',
                    'text-danger': item.status_pembayaran === 'ditolak'
                  }">{{ item.status_pembayaran }}</span>
                </td>
                <td class="text-center">
                  <button 
                    v-if="item.status_pembayaran === 'pending'" 
                    @click="updateStatusPemesanan(item.id_pemesanan, 'diterima')" 
                    class="btn btn-sm btn-success me-1">
                    <i class="fas fa-check"></i> Terima
                  </button>
                  <button 
                    v-if="item.status_pembayaran === 'pending'" 
                    @click="updateStatusPemesanan(item.id_pemesanan, 'ditolak')" 
                    class="btn btn-sm btn-danger me-1">
                    <i class="fas fa-times"></i> Tolak
                  </button>
                  <button 
                    @click="confirmDelete(item)" 
                    class="btn btn-sm btn-danger">
                    <i class="fas fa-trash"></i> Hapus
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Pagination -->
        <div class="d-flex justify-content-between mt-4">
          <button :disabled="currentPage === 1" @click="changePage(currentPage - 1)" class="btn btn-outline-primary">
            Previous
          </button>
          <span>Page {{ currentPage }} of {{ totalPages }}</span>
          <button :disabled="currentPage === totalPages" @click="changePage(currentPage + 1)" class="btn btn-outline-primary">
            Next
          </button>
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
      pemesanan: [], // Array untuk menyimpan data pemesanan
      currentPage: 1,
      pageSize: 10,
      totalPages: 0,
    };
  },
  computed: {
    // Paginasi data
    paginatedData() {
      const startIndex = (this.currentPage - 1) * this.pageSize;
      return this.pemesanan.slice(startIndex, startIndex + this.pageSize);
    },
  },
  methods: {
    // Mengambil data pemesanan dari backend
    async fetchPemesanan() {
      try {
        const response = await axios.get("/api/admin/pemesanan"); // Endpoint untuk daftar pemesanan
        this.pemesanan = response.data.data; // Simpan data pemesanan
        this.totalPages = Math.ceil(this.pemesanan.length / this.pageSize); // Hitung total halaman
      } catch (error) {
        Swal.fire({
          icon: "error",
          title: "Gagal Memuat Daftar Pemesanan",
          text: "Terjadi kesalahan saat mengambil daftar pemesanan.",
          confirmButtonText: "Coba Lagi",
        });
      }
    },

    // Mengubah status pemesanan
    async updateStatusPemesanan(id_pemesanan, status) {
      try {
        await axios.put(`/api/verifikasi/${id_pemesanan}`, { status });
        const pemesananIndex = this.pemesanan.findIndex(p => p.id_pemesanan === id_pemesanan);
        this.pemesanan[pemesananIndex].status_pembayaran = status;

        Swal.fire({
          icon: "success",
          title: "Status Pemesanan Terupdate",
          text: `Status pemesanan telah diubah menjadi ${status}`,
          timer: 2000,
          showConfirmButton: false,
        });
      } catch (error) {
        Swal.fire({
          icon: "error",
          title: "Gagal Memperbarui Status Pemesanan",
          text: "Terjadi kesalahan saat memperbarui status pemesanan.",
          confirmButtonText: "Coba Lagi",
        });
      }
    },

    // Fungsi untuk mengubah halaman
    changePage(page) {
      if (page < 1 || page > this.totalPages) return;
      this.currentPage = page;
    },

    // Fungsi untuk mengonfirmasi penghapusan pemesanan
    confirmDelete(pemesanan) {
      Swal.fire({
        title: "Apakah Anda Yakin?",
        text: `Anda akan menghapus pemesanan dengan ID ${pemesanan.id_pemesanan}`,
        icon: "warning",
        showCancelButton: true,
        confirmButtonText: "Hapus",
        cancelButtonText: "Batal",
      }).then(async (result) => {
        if (result.isConfirmed) {
          try {
            await axios.delete(`/api/admin/delete-user/${pemesanan.id_pemesanan}`);
            Swal.fire({
              icon: "success",
              title: "Pemesanan Dihapus",
              text: `Pemesanan dengan ID ${pemesanan.id_pemesanan} telah berhasil dihapus.`,
              timer: 2000,
              showConfirmButton: false,
            });

            this.fetchPemesanan(); // Refresh data pemesanan setelah dihapus
          } catch (error) {
            Swal.fire({
              icon: "error",
              title: "Gagal Menghapus Pemesanan",
              text: "Terjadi kesalahan saat menghapus pemesanan.",
              confirmButtonText: "Coba Lagi",
            });
          }
        }
      });
    },

    // Fungsi untuk mengekspor PDF (misalnya, menavigasi ke halaman laporan)
    exportPDF() {
      this.$router.push("/laporan"); // Menavigasi ke halaman LaporanView.vue setelah ekspor PDF
    },
  },
  mounted() {
    this.fetchPemesanan(); // Memuat data pemesanan saat halaman dimuat
  },
};
</script>

<style scoped>
/* Custom Styles */
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

/* Tombol Eksport PDF */
.btn-outline-light {
  font-size: 14px; /* Ukuran font tombol */
  padding: 8px 15px; /* Menyesuaikan ukuran tombol */
  border-color: #007bff; /* Warna border biru */
  color: #007bff; /* Warna teks biru */
  background-color: white; /* Warna latar belakang putih */
}

.btn-outline-light:hover {
  background-color: #007bff; /* Warna biru saat hover */
  color: white; /* Warna teks putih saat hover */
}
</style>