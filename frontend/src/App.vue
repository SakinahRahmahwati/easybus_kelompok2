<template>
  <!-- Halaman login dan register -->
  <div v-if="$route.name === 'Login' || $route.name === 'Register'">
    <router-view />
  </div>

  <!-- Layout utama -->
  <div v-else :class="['wrapper', { 'no-sidebar': $route.meta && $route.meta.noSidebar }]">
    <!-- Sidebar -->
    <div
      class="sidebar"
      data-color="black"
      data-active-color="danger"
      v-if="!($route.meta && $route.meta.noSidebar)"
    >
      <div class="logo">
        <a href="#" class="logo-container">
          <div class="logo-image-small">
            <img src="/assets/img/logo.png" alt="Logo" />
          </div>
          <span class="logo-text">EasyBus</span>
        </a>
      </div>
      <AppSidebar />
    </div>

    <!-- Main panel -->
    <div class="main-panel">
      <AppNav v-if="!($route.meta && $route.meta.noNavbar)" />
      <router-view />
    </div>
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
/* Global layout */
#app {
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  background-color: #ffffff;
  min-height: 100vh;
  margin: 0;
  padding: 0;
}

.wrapper,
.main-panel {
  background-color: #ffffff !important;
}

.card,
.card-body {
  background-color: #ffffff !important;
}

/* Logo */
.logo {
  padding: 10px 0;
  display: flex;
  justify-content: center;
  align-items: center;
  background: #2c3e50;
}

.logo-container {
  display: flex;
  align-items: center;
  text-decoration: none;
}

.logo-image-small img {
  width: 30px;
  height: 30px;
  object-fit: contain;
  margin-right: 7px;
}

.logo-text {
  font-size: 17px;
  font-weight: bold;
  color: #fff;
  letter-spacing: 1px;
}

/* Jika sidebar dinonaktifkan via meta */
.wrapper.no-sidebar .main-panel {
  margin-left: 0 !important;
  width: 100% !important;
}

.wrapper.no-sidebar {
  display: flex;
}

.wrapper.no-sidebar .sidebar {
  display: none;
  width: 0;
}
</style>
