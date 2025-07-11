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
              </div>

              <div class="mb-3">
                <label for="email" class="form-label label-bold">Email</label>
                <input
                  id="email"
                  v-model="email"
                  class="form-control"
                  type="email"
                  placeholder="Masukkan Email User"
                  required
                />
              </div>

              <div class="mb-3">
                <label for="password" class="form-label label-bold">Password</label>
                <input
                  id="password"
                  v-model="password"
                  class="form-control"
                  type="password"
                  placeholder="Masukkan Password User"
                  required
                />
              </div>

              <div class="mb-3">
                <label for="role" class="form-label label-bold">Role</label>
                <select id="role" v-model="role" class="form-control">
                  <option disabled value="">Pilih Role</option>
                  <option value="admin">Admin</option>
                  <option value="customer">Customer</option>
                </select>
              </div>

              <div class="text-center">
                <button type="submit" class="btn btn-dongker" :disabled="isSubmitting">
                  <i class="fas fa-save me-2"></i> Simpan
                </button>
              </div>

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
import Swal from "sweetalert2";

export default {
  data() {
    return {
      nama: "",
      email: "",
      password: "",
      role: "",
      isSubmitting: false, // Indikator untuk menonaktifkan tombol selama proses submit
      errorMessage: "", // Pesan error jika ada kesalahan
    };
  },
  methods: {
    async simpanUser() {
      // Membuat data user untuk dikirim ke server
      const userData = {
        nama: this.nama,
        email: this.email,
        password: this.password,
        role: this.role,
      };

      this.isSubmitting = true; // Menandakan bahwa proses submit sedang berjalan

      try {
        // Kirim data user ke backend
        await axios.post("/api/add-user", userData);  // Tidak perlu menyimpan `data` dari response

        // Menampilkan pesan sukses menggunakan SweetAlert2
        Swal.fire({
          icon: "success",
          title: "User Berhasil Ditambahkan",
          text: "User baru telah berhasil ditambahkan.",
          timer: 2000,
          showConfirmButton: false,
        });

        // Kembali ke halaman daftar user setelah berhasil
        this.$router.push("/user");
      } catch (error) {
        // Menampilkan pesan error jika terjadi kesalahan
        Swal.fire({
          icon: "error",
          title: "Gagal Menambahkan User",
          text: error.response?.data?.error || "Terjadi kesalahan saat menambah user.",
          confirmButtonText: "Coba Lagi",
        });
      } finally {
        this.isSubmitting = false; // Mengembalikan status submit menjadi false
      }
    },
  },
};
</script>

<style scoped>
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