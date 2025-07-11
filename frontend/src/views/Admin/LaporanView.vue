<template>
  <div class="content py-4">
    <div class="card shadow-sm rounded-4 bg-dark-blue">
      <div class="card-header text-white py-3 d-flex justify-content-between align-items-center">
        <h4 class="card-title mb-0 fw-bold">Laporan</h4>
      </div>
      <div class="card-body px-4 py-4">
        <div class="row">
          <div class="col-md-3">
            <div class="card">
              <div class="card-body">
                <h5 class="card-title">Total Pemesanan</h5>
                <p class="card-text">{{ laporan.total_pemesanan }}</p>
              </div>
            </div>
          </div>
          <div class="col-md-3">
            <div class="card">
              <div class="card-body">
                <h5 class="card-title">Tiket Diterima</h5>
                <p class="card-text">{{ laporan.tiket_diterima }}</p>
              </div>
            </div>
          </div>
          <div class="col-md-3">
            <div class="card">
              <div class="card-body">
                <h5 class="card-title">Total Customer</h5>
                <p class="card-text">{{ laporan.total_user }}</p>
              </div>
            </div>
          </div>
          <div class="col-md-3">
            <div class="card">
              <div class="card-body">
                <h5 class="card-title">Pendapatan</h5>
                <p class="card-text">{{ laporan.pendapatan }} IDR</p>
              </div>
            </div>
          </div>
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
      laporan: {},
    };
  },
  mounted() {
    this.getLaporan();
  },
  methods: {
    async getLaporan() {
      try {
        const response = await axios.get("/api/admin/laporan");
        this.laporan = response.data;
      } catch (error) {
        Swal.fire({
          icon: 'error',
          title: 'Gagal Mengambil Laporan',
          text: 'Terjadi kesalahan saat mengambil laporan.',
          confirmButtonText: 'Coba Lagi',
        });
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

.card {
  margin: 10px;
}

.card-title {
  font-weight: bold;
}

.card-text {
  font-size: 18px;
}

.d-flex {
  margin-top: 20px;
  justify-content: space-between;
}
</style>