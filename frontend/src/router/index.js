import { createRouter, createWebHistory } from 'vue-router';

const routes = [
  {
    path: '/',
    name: 'Login',
    component: () => import('../views/Auth/LoginView.vue'),
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('../views/Auth/RegisterView.vue'),
  },
  {
    path: '/dashboard-admin',
    name: 'DashboardAdmin',
    component: () => import('../views/Admin/DashboardAdmin.vue'),
  },
  {
    path: '/daftar-pemesanan',
    name: 'DaftarPemesanan',
    component: () => import('../views/Admin/DaftarPemesanan.vue'),
  },
  {
    path: '/user',
    name: 'UserView',
    component: () => import('../views/Admin/UserView.vue'),
  },
  {
    path: '/add-user',
    name: 'AddUser',
    component: () => import('../views/Admin/AddUser.vue'),
  },
  {
    path: '/bukti-pembayaran',
    name: 'BuktiPembayaran',
    component: () => import('../views/Admin/BuktiPembayaran.vue'),
  },
  {
    path: '/laporan',
    name: 'LaporanView',
    component: () => import('../views/Admin/LaporanView.vue'),
  },
  {
    path: '/daftar-jadwal',
    name: 'DaftarJadwal',
    component: () => import('../views/Jadwal/DaftarJadwal.vue'),
  },
  {
    path: '/add-jadwal',
    name: 'AddJadwal',
    component: () => import('../views/Jadwal/AddJadwal.vue'),
  },
  {
    path: '/edit-jadwal/:id',
    name: 'EditJadwal',
    component: () => import('../views/Jadwal/EditJadwal.vue'),
  },
  {
    path: '/cari-jadwal',
    name: 'CariJadwal',
    component: () => import('../views/Jadwal/CariJadwal.vue'),
  },
  {
    path: '/hasil-pencarian',
    name: 'HasilPencarian',
    component: () => import('../views/Jadwal/HasilPencarian.vue'),
  },
  {
  path: '/detail-jadwal/:id',
  name: 'DetailJadwal',
  component: () => import('../views/Jadwal/DetailJadwal.vue'),
  },
  {
    path: '/form-pemesanan',
    name: 'FormPemesanan',
    component: () => import('../views/User/FormPemesanan.vue'),
  },
    {
    path: '/riwayat-pemesanan',
    name: 'RiwayatPemesanan',
    component: () => import('../views/User/RiwayatPemesanan.vue'),
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;