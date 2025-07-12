<template>
  <div class="background-container">
    <div class="register-container">
      <h1>Daftar</h1>
      <form @submit.prevent="handleRegister">
        <div class="mb-3">
          <label for="nama" class="form-label label-bold">Nama</label>
          <input
            id="nama"
            type="text"
            v-model="registerNama"
            class="form-control input-large"
            placeholder="Masukkan Nama Anda"
            required
          />
        </div>

        <div class="mb-3">
          <label for="email" class="form-label label-bold">Email</label>
          <input
            id="email"
            type="email"
            v-model="registerEmail"
            class="form-control input-large"
            placeholder="Masukkan Email Anda"
            required
          />
        </div>

        <div class="mb-3">
          <label for="password" class="form-label label-bold">Kata Sandi</label>
          <input
            id="password"
            type="password"
            v-model="registerPassword"
            class="form-control input-large"
            placeholder="Masukkan Kata Sandi Anda"
            required
          />
        </div>

        <div class="mb-3">
          <label for="confirmPassword" class="form-label label-bold">Konfirmasi Kata Sandi</label>
          <input
            id="confirmPassword"
            type="password"
            v-model="registerConfirmPassword"
            class="form-control input-large"
            placeholder="Konfirmasi Kata Sandi Anda"
            required
          />
        </div>

        <div class="text-center mt-4">
          <button class="btn btn-gray btn-lg" type="submit">
            Daftar
          </button>
        </div>
      </form>

      <p class="text-center mt-3">
        Sudah punya akun? 
        <a href="#" @click.prevent="goToLogin" class="text-register">Login di sini</a>
      </p>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import Swal from 'sweetalert2';

export default {
  data() {
    return {
      registerNama: "",
      registerEmail: "",
      registerPassword: "",
      registerConfirmPassword: "",
    };
  },
  methods: {
    async handleRegister() {
      if (this.registerPassword !== this.registerConfirmPassword) {
        Swal.fire({
          icon: 'error',
          title: 'Password Tidak Sama',
          text: 'Password dan konfirmasi password harus sama!',
          confirmButtonText: 'Coba Lagi',
        });
        return;
      }

      try {
        const response = await axios.post("/api/register", {
          nama: this.registerNama,
          email: this.registerEmail,
          password: this.registerPassword,
          confirmPassword: this.registerConfirmPassword,
        });

        if (response.status === 200) {
          Swal.fire({
            icon: 'success',
            title: 'Registrasi Berhasil',
            text: 'Akun Anda telah berhasil dibuat.',
            timer: 2000,
            showConfirmButton: false,
          }).then(() => {
            this.$router.push('/');
          });
        }
      } catch (err) {
        Swal.fire({
          icon: 'error',
          title: 'Gagal Registrasi',
          text: err.response?.data?.error || 'Terjadi kesalahan saat mendaftar.',
          confirmButtonText: 'Coba Lagi',
        });
      }
    },
    goToLogin() {
      this.$router.push("/"); // Navigasi ke halaman login
    },
  },
};
</script>

<style scoped>
body, html {
  margin: 0;
  padding: 0;
  height: 100%;
  width: 100%;
  overflow: auto;
}

.background-container {
  width: 100vw;
  height: 100vh;
  background-image: url("/public/assets/img/login.jpg");
  background-size: cover;
  background-position: center;
  display: flex;
  justify-content: center;
  align-items: center;
}

.register-container {
  max-width: 400px;
  width: 100%;
  padding: 30px;
  background-color: rgba(255, 255, 255, 0.9);
  border-radius: 10px;
  box-shadow: 0 6px 10px rgba(0, 0, 0, 0.15);
}

h1 {
  font-size: 28px;
  font-weight: bold;
  color: #333;
  text-align: center;
  margin-bottom: 20px;
}

.label-bold {
  font-weight: bold;
  font-size: 16px;
}

.input-large {
  height: 45px;
  font-size: 15px;
  padding: 10px;
  width: 100%;
  box-sizing: border-box;
}

.btn-gray {
  background-color: #2c3e50; /* Hijau pastel lembut */
  color: #fff;
  border: none;
  width: 100%;
  font-size: 16px;
  padding: 10px;
  transition: background-color 0.3s ease;
  cursor: pointer;
}

.btn-gray:hover {
  background-color: #1818cf; /* Warna lebih terang saat hover */
  border-color: #1818cf;
}

.text-center {
  text-align: center;
}

.mt-4 {
  margin-top: 1.5rem;
}

.mt-3 {
  margin-top: 1rem;
}
</style>