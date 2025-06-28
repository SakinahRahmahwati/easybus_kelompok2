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
.btn-logout {
  color: #ffffff; /* Teks putih */
  background-color: #2c3e50; /* Background biru dongker */
  padding: 3px 8px; 
  border-radius: 4px; 
  text-decoration: none; 
  font-weight: normal; 
  font-size: 10px; 
}

.btn-logout:hover {
  background-color: #34495e; /* Biru dongker lebih gelap untuk efek hover */
}
</style>