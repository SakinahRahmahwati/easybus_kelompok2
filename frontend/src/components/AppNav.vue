<template>
  <nav class="navbar navbar-expand-lg navbar-absolute fixed-top navbar-transparent">
    <div class="container-fluid">
      <div class="collapse navbar-collapse justify-content-end" id="navigation">
        <ul class="navbar-nav">
          <!-- Tombol Logout -->
          <li class="nav-item">
            <a class="nav-link btn-logout" href="javascript:;" @click="logout">
              <p>
                Logout
              </p>
            </a>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>

<script>
export default {
  methods: {
    logout() {
      // Hapus token dan role dari localStorage
      localStorage.removeItem('token');
      localStorage.removeItem('role');
      
      // Redirect ke halaman login
      this.$router.push('/');
    }
  }
}
</script>

<style scoped>
.navbar {
  min-height: 38px !important;
  height: 48px !important;
  padding-top: 0 !important;
  padding-bottom: 0 !important;
  background: #fff !important;
  border-bottom: 1px solid #e0e0e0;
  box-shadow: none;
  display: flex;
  align-items: center;
}

.navbar .container-fluid {
  padding-left: 0;
  padding-right: 0;
}

.navbar .navbar-nav {
  margin-top: 0;
  margin-bottom: 0;
}

.btn-logout {
  color: #ffffff;
  background-color: #2c3e50;
  padding: 1px 5px;
  border-radius: 3px;
  text-decoration: none;
  font-weight: normal;
  font-size: 8px;
  line-height: 1.2;
  min-width: 40px;
  min-height: 22px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.btn-logout:hover {
  background-color: #34495e;
}
</style>