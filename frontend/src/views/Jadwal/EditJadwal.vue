<template>
  <div class="content py-3">
    <div class="row justify-content-center">
      <div class="col-md-8">
        <div class="card shadow-sm">
          <div class="card-header bg-dongker text-white py-3">
            <h4 class="card-title text-center mb-0">Edit Data Jadwal</h4>
          </div>
          <div class="card-body">
            <form @submit.prevent="updateJadwal">
              <div class="mb-3">
                <label class="form-label">Nama Bus</label>
                <input v-model="jadwalEdit.nama_bus" type="text" class="form-control" required />
              </div>

              <div class="mb-3">
                <label class="form-label">Asal</label>
                <input v-model="jadwalEdit.asal" type="text" class="form-control" required />
              </div>

              <div class="mb-3">
                <label class="form-label">Tujuan</label>
                <input v-model="jadwalEdit.tujuan" type="text" class="form-control" required />
              </div>

              <div class="mb-3">
                <label class="form-label">Tanggal Berangkat</label>
                <input v-model="jadwalEdit.tanggal_berangkat" type="date" class="form-control" required />
              </div>

              <div class="mb-3">
                <label class="form-label">Jam Berangkat</label>
                <input v-model="jadwalEdit.jam_berangkat" type="time" class="form-control" required />
              </div>

              <div class="mb-3">
                <label class="form-label">Jam Tiba</label>
                <input v-model="jadwalEdit.jam_tiba" type="time" class="form-control" />
              </div>

              <div class="mb-3">
                <label class="form-label">Harga (IDR)</label>
                <input v-model.number="jadwalEdit.harga" type="number" class="form-control" required />
              </div>

              <div class="mb-3">
                <label class="form-label">Total Kursi</label>
                <input v-model.number="jadwalEdit.total_kursi" type="number" class="form-control" required />
              </div>

              <div class="mb-3">
                <label class="form-label">Kursi Tersedia</label>
                <input v-model.number="jadwalEdit.kursi_tersedia" type="number" class="form-control" required />
              </div>

              <div class="text-center">
                <button type="submit" class="btn btn-dongker" :disabled="isSubmitting">
                  <i class="fas fa-save me-2"></i> Update
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
      jadwalEdit: {
        id: "",
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
    async getJadwalById() {
      const id = this.$route.params.id;
      try {
        const response = await axios.get(`/api/jadwal/${id}`);
        this.jadwalEdit = response.data.data;
      } catch (error) {
        console.error("Error mengambil jadwal:", error);
      }
    },

    async updateJadwal() {
      const id = this.jadwalEdit.id;
      try {
        this.isSubmitting = true;
        await axios.put(`/api/admin/jadwal/${id}`, this.jadwalEdit);
        Swal.fire({
          icon: 'success',
          title: 'Berhasil',
          text: 'Jadwal berhasil diperbarui.',
        });
        this.$router.push("/daftar-jadwal");
      } catch (error) {
        console.error("Error memperbarui jadwal:", error);
        Swal.fire({
          icon: 'error',
          title: 'Gagal',
          text: 'Terjadi kesalahan saat memperbarui data.',
        });
      } finally {
        this.isSubmitting = false;
      }
    },
  },
  mounted() {
    this.getJadwalById();
  },
};
</script>

<style scoped>
.bg-dongker {
  background-color: #2c3e50 !important;
  color: white;
  padding: 20px;
  border-radius: 10px;
  margin-bottom: 20px;
}

.card-body {
  background-color: #f9f9f9;
  border-radius: 10px;
  padding: 20px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.form-control {
  padding: 10px;
  font-size: 1rem;
  border-radius: 5px;
  border: 1px solid #ddd;
  margin-bottom: 10px;
}

.form-label {
  font-weight: bold;
  font-size: 1rem;
  margin-bottom: 8px;
}

button {
  background-color: #34495e;
  color: white;
  padding: 10px 20px;
  font-size: 1rem;
  border-radius: 5px;
  border: none;
  cursor: pointer;
}

button:hover {
  background-color: #2c3e50;
}

button:disabled {
  background-color: #bdc3c7;
  cursor: not-allowed;
}

.card-header h4 {
  text-align: center;
  font-size: 1.5rem;
  font-weight: bold;
}

.mb-3 {
  margin-bottom: 1rem;
}

.text-center {
  text-align: center;
}
</style>
