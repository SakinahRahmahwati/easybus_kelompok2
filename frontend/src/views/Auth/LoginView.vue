<template>
  <div class="background-container">
    <div class="login-container">
      <h1>Masuk</h1>
      <form @submit.prevent="handleLogin">
        <div class="mb-3">
          <label for="email" class="form-label label-bold">Email</label>
          <input
            type="email"
            id="email"
            v-model="email"
            class="form-control input-large"
            placeholder="Masukkan Email"
            required
          />
        </div>

        <div class="mb-3">
          <label for="password" class="form-label label-bold">Kata Sandi</label>
          <input
            type="password"
            id="password"
            v-model="password"
            class="form-control input-large"
            placeholder="Masukkan Kata Sandi"
            required
          />
        </div>

        <div class="text-center mt-4">
          <button class="btn btn-gray btn-lg" type="submit">
            <i class="fas fa-sign-in-alt me-2"></i> Masuk
          </button>
        </div>
      </form>

      <p class="text-center mt-3">
        Belum punya akun? <a href="#" @click="goToRegister">Daftar di sini</a>
      </p>

      <!-- Error Message -->
      <p v-if="errorMessage" class="error text-center">{{ errorMessage }}</p>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import Swal from 'sweetalert2';

export default {
  name: "LoginView",
  data() {
    return {
      email: "",
      password: "",
      errorMessage: "",
    };
  },
  methods: {
    goToRegister() {
      this.$router.push("/register");
    },
    async handleLogin() {
      try {
        const { data } = await axios.post("/api/login", {
          email: this.email,
          password: this.password,
        });

        const user = data.user;
        localStorage.setItem("user_id", user.id_user);
        localStorage.setItem("nama", user.nama);
        localStorage.setItem("role", user.role);
        if (data.token) localStorage.setItem("token", data.token);

        await Swal.fire({
          icon: 'success',
          title: 'Selamat Datang',
          timer: 2000,
          showConfirmButton: false,
        });

        if (user.role === 'admin') {
          this.$router.push("/dashboard-admin");
        } else {
          this.$router.push("/cari-jadwal");
        }
      } catch (error) {
        Swal.fire({
          icon: 'error',
          title: 'Login Gagal',
          text: 'Periksa kembali email dan kata sandi Anda!',
          confirmButtonText: 'Coba Lagi',
        });
        if (error.response?.data?.error) {
          this.errorMessage = error.response.data.error;
        } else {
          this.errorMessage = "Login gagal, coba periksa kembali email dan kata sandi Anda!";
        }
      }
    },
  },
};
</script>

<style scoped>
body,
html {
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

.login-container {
  max-width: 400px;
  width: 100%;
  padding: 30px;
  background-color: rgba(255, 255, 255, 0.9);
  border-radius: 10px;
  box-shadow: 0px 6px 10px rgba(0, 0, 0, 0.15);
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
  background-color: #2c3e50; /* Warna abu-abu gelap */
  color: white;
  border: none;
  width: 100%;
  font-size: 16px;
  padding: 10px;
}

.btn-gray:hover {
  background-color: #1818cf; /* Warna lebih terang saat hover */
  border-color: #1818cf;
}

.text-center {
  text-align: center;
}

.error {
  color: red;
  margin-top: 10px;
  font-size: 14px;
}
</style>