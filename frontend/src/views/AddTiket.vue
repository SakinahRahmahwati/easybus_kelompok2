<template>
  <div class="content py-3">
    <div class="row justify-content-center">
      <div class="col-md-8">
        <div class="card shadow-sm">
          <div class="card-header bg-dongker text-white py-3">
            <h4 class="card-title text-center mb-0">Tambah Data Tiket</h4>
          </div>
          <div class="card-body">
            <form @submit.prevent="simpanTicket">
              <!-- Nama Bus -->
              <div class="mb-3">
                <label for="namaBus" class="form-label label-bold">Nama Bus</label>
                <input
                  id="namaBus"
                  v-model="newTicket.nama_bus"
                  class="form-control"
                  type="text"
                  placeholder="Masukkan Nama Bus"
                  required
                />
              </div>

              <!-- Kota Keberangkatan -->
              <div class="mb-3">
                <label for="kotaKeberangkatan" class="form-label label-bold">Kota Keberangkatan</label>
                <input
                  id="kotaKeberangkatan"
                  v-model="newTicket.kota_keberangkatan"
                  class="form-control"
                  type="text"
                  placeholder="Masukkan Kota Keberangkatan"
                  required
                />
              </div>

              <!-- Kota Tujuan -->
              <div class="mb-3">
                <label for="kotaTujuan" class="form-label label-bold">Kota Tujuan</label>
                <input
                  id="kotaTujuan"
                  v-model="newTicket.kota_tujuan"
                  class="form-control"
                  type="text"
                  placeholder="Masukkan Kota Tujuan"
                  required
                />
              </div>

              <!-- Jam Keberangkatan -->
              <div class="mb-3">
                <label for="jamKeberangkatan" class="form-label label-bold">Jam Keberangkatan</label>
                <input
                  id="jamKeberangkatan"
                  v-model="newTicket.jam_keberangkatan"
                  class="form-control"
                  type="time"
                  required
                />
              </div>

              <!-- Jam Tiba -->
              <div class="mb-3">
                <label for="jamTiba" class="form-label label-bold">Jam Tiba</label>
                <input
                  id="jamTiba"
                  v-model="newTicket.jam_tiba"
                  class="form-control"
                  type="time"
                  required
                />
              </div>

              <!-- Harga -->
              <div class="mb-3">
                <label for="harga" class="form-label label-bold">Harga</label>
                <input
                  id="harga"
                  v-model="newTicket.harga"
                  class="form-control"
                  type="number"
                  placeholder="Masukkan Harga"
                  required
                />
              </div>

              <!-- Total Kursi -->
              <div class="mb-3">
                <label for="totalKursi" class="form-label label-bold">Total Kursi</label>
                <input
                  id="totalKursi"
                  v-model="newTicket.total_kursi"
                  class="form-control"
                  type="number"
                  placeholder="Masukkan Total Kursi"
                  required
                />
              </div>

              <!-- Kursi Tersedia -->
              <div class="mb-3">
                <label for="kursiTersedia" class="form-label label-bold">Kursi Tersedia</label>
                <input
                  id="kursiTersedia"
                  v-model="newTicket.kursi_tersedia"
                  class="form-control"
                  type="number"
                  placeholder="Masukkan Kursi Tersedia"
                  required
                />
              </div>

              <!-- Tombol Simpan -->
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

export default {
  data() {
    return {
      newTicket: {
        nama_bus: "",
        kota_keberangkatan: "",  // Kolom Kota Keberangkatan
        kota_tujuan: "",          // Kolom Kota Tujuan
        jam_keberangkatan: "",
        jam_tiba: "",
        harga: 0,
        total_kursi: 0,
        kursi_tersedia: 0,
      },
    };
  },
  methods: {
    simpanTicket() {
      const ticketData = {
        nama_bus: this.newTicket.nama_bus,
        kota_keberangkatan: this.newTicket.kota_keberangkatan,
        kota_tujuan: this.newTicket.kota_tujuan,
        jam_keberangkatan: this.newTicket.jam_keberangkatan,
        jam_tiba: this.newTicket.jam_tiba,
        harga: this.newTicket.harga,
        total_kursi: this.newTicket.total_kursi,
        kursi_tersedia: this.newTicket.kursi_tersedia,
      };

      axios
        .post("http://127.0.0.1:5000/add-tiket", ticketData)
        .then((response) => {
          console.log(response.data);
          this.$router.push("/tiket"); // Redirect to the ticket list page after saving
        })
        .catch((error) => {
          console.error("Terjadi kesalahan:", error);
        });
    },
  },
};
</script>

<style>
/* Warna dongker untuk card header */
.bg-dongker {
  background-color: #2c3e50 !important; /* Ganti dengan warna dongker yang diinginkan */
}

/* Warna dongker untuk tombol simpan */
.btn-dongker {
  background-color: #2c3e50; /* Ganti dengan warna dongker yang diinginkan */
  color: #fff; /* Teks tombol putih */
}

.btn-dongker:hover {
  background-color: #34495e; /* Warna dongker sedikit lebih terang saat dihover */
}
</style>