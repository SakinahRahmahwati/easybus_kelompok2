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
                <label for="namaBus" class="form-label label-bold">Nama Bus</label>
                <input
                  id="namaBus"
                  v-model="jadwalEdit.nama_bus"
                  class="form-control"
                  type="text"
                  placeholder="Masukkan Nama Bus"
                  required
                />
              </div>

              <!-- Add other form fields here -->

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

export default {
  data() {
    return {
      jadwalEdit: {
        id_jadwal: "",
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
      const id = this.jadwalEdit.id_jadwal;
      try {
        this.isSubmitting = true;
        await axios.put(`/api/admin/jadwal/${id}`, this.jadwalEdit);
        this.$router.push("/jadwal"); // Redirect setelah berhasil
      } catch (error) {
        console.error("Error memperbarui jadwal:", error);
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
/* Styling untuk card header */
.bg-dongker {
  background-color: #2c3e50 !important;
  color: white;
  padding: 20px;
  border-radius: 10px;
  margin-bottom: 20px;
}

/* Styling untuk card body */
.card-body {
  background-color: #f9f9f9;
  border-radius: 10px;
  padding: 20px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

/* Styling untuk input form */
.form-control {
  padding: 10px;
  font-size: 1rem;
  border-radius: 5px;
  border: 1px solid #ddd;
  margin-bottom: 10px;
}

/* Styling untuk label form */
.form-label {
  font-weight: bold;
  font-size: 1rem;
  margin-bottom: 8px;
}

/* Styling untuk button */
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