<template>
  <div class="content py-4">
    <div class="card shadow-sm rounded-4 bg-dark-blue">
      <div class="card-header text-white py-3 d-flex justify-content-center">
        <h4 class="card-title mb-0 fw-bold">Booking Tiket Bus</h4>
      </div>

      <!-- Form Pencarian Tiket -->
      <div class="card-body">
        <div class="form-container">
          <div class="form-group">
            <label for="kotaKeberangkatan">Kota Keberangkatan</label>
            <input type="text" id="kotaKeberangkatan" v-model="kotaKeberangkatan" placeholder="Ketikan Nama Kota" class="form-control" />
          </div>

          <div class="form-group">
            <label for="kotaTujuan">Kota Tujuan</label>
            <input type="text" id="kotaTujuan" v-model="kotaTujuan" placeholder="Ketikan Nama Kota" class="form-control" />
          </div>

          <div class="form-group">
            <label for="tanggalBerangkat">Tanggal Berangkat</label>
            <input type="date" id="tanggalBerangkat" v-model="tanggalBerangkat" class="form-control" />
          </div>

          <div class="form-group">
            <label for="jumlahKursi">Jumlah Kursi</label>
            <input type="number" id="jumlahKursi" v-model="jumlahKursi" placeholder="Ketikan Jumlah Kursi" class="form-control" />
          </div>

          <button @click="cariTiket" class="btn btn-primary">Cari</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap/dist/js/bootstrap.bundle.min.js";
import Swal from "sweetalert2";

export default {
  data() {
    return {
      kotaKeberangkatan: '',
      kotaTujuan: '',
      tanggalBerangkat: '',
      jumlahKursi: ''
    };
  },
  methods: {
    cariTiket() {
      if (!this.kotaKeberangkatan || !this.kotaTujuan || !this.tanggalBerangkat || !this.jumlahKursi) {
        Swal.fire({
          icon: 'warning',
          title: 'Form tidak lengkap',
          text: 'Silakan lengkapi semua field untuk melanjutkan pencarian tiket.',
        });
        return;
      }

      this.$router.push({
        path: '/hasil-pencarian',
        query: {
          kotaKeberangkatan: this.kotaKeberangkatan,
          kotaTujuan: this.kotaTujuan,
          tanggalBerangkat: this.tanggalBerangkat,
          jumlahKursi: this.jumlahKursi
        }
      });
    }
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

.card-header h4 {
  text-align: center;
  font-weight: bold;
}

.card-body {
  background-color: #f9f9f9;
  border-radius: 12px;
  padding: 20px;
}

.form-container {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 15px;
}

.form-group {
  display: flex;
  flex-direction: column;
}

label {
  font-size: 1rem;
  margin-bottom: 8px;
}

input[type="text"],
input[type="date"],
input[type="number"] {
  padding: 10px;
  font-size: 1rem;
  border-radius: 5px;
  border: 1px solid #ccc;
}

button {
  grid-column: span 2;
  padding: 12px;
  background-color: #34495e;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 1rem;
  margin-top: 10px;
}

button:hover {
  background-color: #2c3e50;
}
</style>