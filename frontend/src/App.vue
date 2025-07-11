<template>
  <!-- Tambahkan v-if untuk mengecek kondisi selain Login dan Register -->
  <div class="wrapper" v-if="$route.name !== 'Login' && $route.name !== 'Register'">
    <div class="sidebar" data-color="black" data-active-color="danger">
      <div class="logo" style="background-color: #2c3e50; color: #ecf0f1; display: flex; align-items: center; justify-content: center;">
        <a class="simple-text logo-mini">
          <div class="logo-image-small">
            <img src="assets/img/logo.png" />
          </div>
        </a>
        <a class="simple-text logo-bold">
          EasyBus
        </a>
      </div>
      <AppSidebar />
    </div>
    <div class="main-panel">
      <AppNav />
      <router-view />
    </div>
  </div>
  <!-- Hanya tampilkan router-view untuk Login atau Register -->
  <div v-else>
    <router-view />
  </div>
</template>

<script>
import AppNav from './components/AppNav.vue';
import AppSidebar from './components/AppSidebar.vue';

export default {
  name: 'App',
  components: {
    AppNav,
    AppSidebar,
  },
};
</script>

<style scoped>
#app {
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  background-color: #ffffff;  /* Menambahkan latar belakang putih di sini */
  min-height: 100vh;  /* Memastikan tinggi halaman penuh */
  margin: 0;
  padding: 0;
}
/* Memastikan latar belakang tetap putih di wrapper dan konten utama */
.wrapper, .main-panel {
  background-color: #ffffff !important; /* Memastikan latar belakang putih */
}

.card, .card-body {
  background-color: #ffffff !important; /* Mengubah card menjadi putih */
}

.logo {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 10px;
}

.logo-mini {
  display: inline-block;
}

.logo-image-small img {
  width: 40px;  /* Ukuran logo */
  height: auto;
}

.logo-bold {
  font-weight: bold;
  font-size: 1.5rem;
  color: #ecf0f1;
  margin-left: 10px;  /* Memberikan jarak antara logo dan teks */
}
</style>