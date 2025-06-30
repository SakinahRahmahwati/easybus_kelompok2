<template>
  <div class="background-container">
    <div class="login-container">
      <h1>Login</h1>
      <form @submit.prevent="handleLogin">
        <!-- Form Email -->
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

        <!-- Form Password -->
        <div class="mb-3">
          <label for="password" class="form-label label-bold">Password</label>
          <input
            type="password"
            id="password"
            v-model="password"
            class="form-control input-large"
            placeholder="Masukkan Password"
            required
          />
        </div>

        <!-- Button Login -->
        <div class="text-center mt-4">
          <button class="btn btn-gray btn-lg" type="submit">
            <i class="fas fa-sign-in-alt me-2"></i> Login
          </button>
        </div>
      </form>

      <!-- Link ke Register -->
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
import Swal from 'sweetalert2'

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
      this.$router.push("/register"); // Navigasi ke halaman Register
    },
    async handleLogin() {
      try {
        // Mengirim request login ke backend
        const { data } = await axios.post("/api/login", {
          email: this.email,
          password: this.password,
        });

        const user = data.user;

        // Menyimpan data pengguna dan token di localStorage
        localStorage.setItem("user_id", user.id_user || user.id);  // Menyimpan ID pengguna
        localStorage.setItem("nama", user.nama);  // Menyimpan nama pengguna
        localStorage.setItem("role", user.role);  // Menyimpan role pengguna
        if (data.token) localStorage.setItem("token", data.token);  // Menyimpan token akses

        // Menampilkan SweetAlert untuk memberitahukan login berhasil
        await Swal.fire({
          icon: 'success',
          title: 'Selamat Datang',
          timer: 2000,
          showConfirmButton: false,
        });

        // Redirect ke dashboard setelah login sukses
        this.$router.push("/dashboard-admin");
      } catch (error) {
        console.error(error);

        // Menampilkan SweetAlert untuk memberitahukan login gagal
        await Swal.fire({
          icon: 'error',
          title: 'Maaf!',
          text: 'Login anda gagal, periksa kembali email dan password anda!',
          confirmButtonText: 'Coba Lagi',
        });

        // Menampilkan pesan error
        if (error.response?.data?.error) {
          this.errorMessage = error.response.data.error;
        } else {
          this.errorMessage = "Login anda gagal, periksa kembali email dan password anda!";
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