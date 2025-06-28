<template>
  <div class="content py-3">
    <div class="row justify-content-center">
      <div class="col-md-8">
        <div class="card shadow-sm">
          <div class="card-header bg-dongker text-white py-3">
            <h4 class="card-title text-center mb-0">Tambah Daftar User</h4>
          </div>
          <div class="card-body">
            <form @submit.prevent="simpanUser">
              <div class="mb-3">
                <label for="nama" class="form-label label-bold">Nama</label>
                <input
                  id="nama"
                  v-model="nama"
                  class="form-control"
                  type="text"
                  placeholder="Masukkan Nama User"
                  required
                />
                <div v-if="errorMessage && !nama" class="text-danger">Nama user wajib diisi.</div>
              </div>

              <div class="mb-3">
                <label for="email" class="form-label label-bold">Email</label>
                <input
                  id="email"
                  v-model="email"
                  class="form-control"
                  type="text"
                  placeholder="Masukkan Email User"
                  required
                />
                <div v-if="errorMessage && !email" class="text-danger">Email user wajib diisi.</div>
              </div>

              <div class="mb-3">
                <label for="password" class="form-label label-bold">Password</label>
                <input
                  id="password"
                  v-model="password"
                  class="form-control"
                  type="text"
                  placeholder="Masukkan Password User"
                  required
                />
                <div v-if="errorMessage && !password" class="text-danger">Password user wajib diisi.</div>
              </div>

              <div class="mb-3">
                <label for="role" class="form-label label-bold">Role</label>
                <select id="role" v-model="role" class="form-control">
                  <option disabled value="">Pilih Role</option>
                  <option value="Admin">Admin</option>
                  <option value="Customer">Customer</option>
                </select>
                <div v-if="errorMessage && !role" class="text-danger">Role user wajib dipilih.</div>
              </div>

              <div class="text-center">
                <button type="submit" class="btn btn-dongker" :disabled="isSubmitting">
                  <i class="fas fa-save me-2"></i> Simpan
                </button>
              </div>

              <!-- Menampilkan pesan error umum jika ada -->
              <div v-if="errorMessage" class="text-danger mt-3">{{ errorMessage }}</div>
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
      nama: "",
      email: "",
      password: "",
      role: "",
    };
  },
  methods: {
    simpanUser() {
      const userData = {
        nama: this.nama,
        email: this.email,
        password: this.password, // Anda bisa mengubah ini untuk memakai password default di backend
        role: this.role,
      };

      axios
        .post('http://127.0.0.1:5000/add-user', userData)
        .then((response) => {
          console.log(response.data);
          // Redirect or inform user
          this.$router.push('/user'); // Kembali ke daftar user setelah berhasil
        })
        .catch((error) => {
          console.error('Terjadi kesalahan:', error);
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