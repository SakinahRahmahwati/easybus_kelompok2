<template>
  <div class="sidebar-wrapper">
    <ul class="nav" id="nav">
      <li v-for="item in filteredMenu" :key="item.name" :class="['menu-item', { active: $route.path === item.path }]">
        <router-link :to="item.path">
          <i :class="item.icon"></i>
          <p>{{ item.name }}</p>
        </router-link>
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  data() {
    return {
      userRole: localStorage.getItem('role'), // Ambil role dari localStorage
    };
  },
  computed: {
    // Menu utama berdasarkan role
    filteredMenu() {
      const menuItems = [
        { name: "Dashboard", path: "/dashboard-admin", icon: "nc-icon nc-tv-2", roles: ["admin"] },
        { name: "Daftar Pemesanan", path: "/daftar-pemesanan", icon: "nc-icon nc-calendar-60", roles: ["admin"] },
        { name: "Bukti Pembayaran", path: "/bukti-pembayaran", icon: "nc-icon nc-credit-card", roles: ["admin"] },
        { name: "Daftar Jadwal", path: "/daftar-jadwal", icon: "nc-icon nc-tile-56", roles: ["admin"] },
        { name: "User", path: "/user", icon: "nc-icon nc-badge", roles: ["admin"] },
        { name: "Riwayat Booking", path: "/riwayat-pemesanan", icon: "nc-icon nc-badge", roles: ["customer"] },
        { name: "Cari Tiket", path: "/cari-jadwal", icon: "nc-icon nc-badge", roles: ["customer"] },
      ];

      return menuItems.filter((item) => item.roles.includes(this.userRole)); // Filter menu berdasarkan role pengguna
    },
  }
}
</script>

<style scoped>
/* Wrapper styling */
.sidebar-wrapper {
  background: linear-gradient(135deg, #2c3e50, #34495e);
  padding: 15px 20px;
  border-radius: 0px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  height: 100vh; /* Set sidebar height to fill the screen */
  display: flex;
  flex-direction: column;
  overflow-y: auto; /* Allow scrolling if content overflows */
}

/* Menu list styling */
.nav {
  list-style: none;
  padding: 0;
  margin: 0;
  flex-grow: 1; /* Make the list grow to fill available space */
}

/* Menu item styling */
.menu-item {
  margin-bottom: 15px;
  transition: all 0.3s ease;
}

.menu-item a {
  display: flex;
  align-items: center;
  text-decoration: none;
  color: #ecf0f1;
  background: rgba(236, 240, 241, 0.2);
  padding: 10px 15px;
  border-radius: 8px;
  font-size: 16px;
  font-weight: bold;
  transition: background 0.3s ease, color 0.3s ease;
}

/* Hover styling */
.menu-item a:hover {
  background: #f1f0f0;
  color: #2c3e50; /* Warna dongker untuk teks saat hover */
  box-shadow: 0 4px 8px rgba(255, 255, 255, 0.3);
}

.menu-item a:hover i {
  transform: scale(1.2);
  color: #2c3e50; /* Warna dongker untuk ikon saat hover */
}

/* Active menu item styling */
.menu-item.active a {
  background: #f1f0f0;
  color: #2c3e50 !important; /* Warna dongker untuk teks saat aktif */
}

.menu-item.active i {
  color: #2c3e50 !important; /* Warna dongker untuk ikon saat aktif */
}

/* Icon styling */
.menu-item i {
  margin-right: 10px;
  font-size: 20px;
  color: #ecf0f1;
  transition: transform 0.3s ease;
}

/* Text styling */
.menu-item p {
  margin: 0;
}
</style>