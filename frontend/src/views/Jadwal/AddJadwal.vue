<template>
  <div class="content py-3">
    <div class="row justify-content-center">
      <div class="col-md-8">
        <div class="card shadow-sm">
          <div class="card-header bg-dongker text-white py-3">
            <h4 class="card-title text-center mb-0">Tambah Data Jadwal</h4>
          </div>
          <div class="card-body">
            <form @submit.prevent="simpanJadwal">
              <div class="mb-3">
                <label for="namaBus" class="form-label label-bold">Nama Bus</label>
                <input
                  id="namaBus"
                  v-model="jadwalBaru.nama_bus"
                  class="form-control"
                  type="text"
                  placeholder="Masukkan Nama Bus"
                  required
                />
              </div>

              <div class="mb-3">
                <label for="asal" class="form-label label-bold">Kota Keberangkatan</label>
                <input
                  id="asal"
                  v-model="jadwalBaru.asal"
                  class="form-control"
                  type="text"
                  placeholder="Masukkan Kota Keberangkatan"
                  required
                />
              </div>

              <div class="mb-3">
                <label for="tujuan" class="form-label label-bold">Kota Tujuan</label>
                <input
                  id="tujuan"
                  v-model="jadwalBaru.tujuan"
                  class="form-control"
                  type="text"
                  placeholder="Masukkan Kota Tujuan"
                  required
                />
              </div>

              <div class="mb-3">
                <label for="tanggalBerangkat" class="form-label label-bold">Tanggal Keberangkatan</label>
                <input
                  id="tanggalBerangkat"
                  v-model="jadwalBaru.tanggal_berangkat"
                  class="form-control"
                  type="date"
                  required
                />
              </div>

              <div class="mb-3">
                <label for="jamBerangkat" class="form-label label-bold">Jam Keberangkatan</label>
                <input
                  id="jamBerangkat"
                  v-model="jadwalBaru.jam_berangkat"
                  class="form-control"
                  type="time"
                  required
                />
              </div>

              <div class="text-center">
                <button type="submit" class="btn btn-dongker" :disabled="isSubmitting">
                  <i class="fas fa-save me-2"></i> Simpan
                </button>
              </div>
            </form>
          </div>
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
      jadwalBaru: {
        nama_bus: "",
        asal: "",
        tujuan: "",
        tanggal_berangkat: "",
        jam_berangkat: "",
        jam_tiba: "",
        harga: 0,
        total_kursi: 0,
        kursi_tersedia: 0,
      },
      isSubmitting: false,
    };
  },
  methods: {
    async simpanJadwal() {
      const dataJadwal = { ...this.jadwalBaru };

      try {
        this.isSubmitting = true;
        await axios.post("/api/admin/jadwal", dataJadwal);
        this.$router.push("/jadwal"); // Redirect ke halaman daftar jadwal setelah berhasil
        Swal.fire({
          icon: 'success',
          title: 'Jadwal Berhasil Ditambahkan',
          text: 'Jadwal bus berhasil ditambahkan.',
        });
      } catch (error) {
        Swal.fire({
          icon: 'error',
          title: 'Gagal Menambahkan Jadwal',
          text: 'Terjadi kesalahan saat menambah jadwal. Coba lagi nanti.',
        });
      } finally {
        this.isSubmitting = false;
      }
    },
  },
};
</script>

<style scoped>
.bg-dongker {
  background-color: #2c3e50 !important;
}

.btn-dongker {
  background-color: #2c3e50;
  color: #fff;
  border: none;
  padding: 5px 15px;
  font-size: 16px;
  border-radius: 5px;
}

.btn-dongker:hover {
  background-color: #34495e;
  color: #fff;
}
</style>