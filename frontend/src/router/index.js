import { createRouter, createWebHistory } from 'vue-router';

const routes = [
  {
    path: '/',
    name: 'Login',
    component: () => import('../views/LoginView.vue'),
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('../views/RegisterView.vue'),
  },
  {
    path: '/dashboard-admin',
    name: 'DashboardAdmin',
    component: () => import('../views/DashboardAdmin.vue'),
  },
  {
    path: '/daftar-bookingan',
    name: 'DaftarPelanggan',
    component: () => import('../views/DaftarBookingan.vue'),
  },
  {
    path: '/daftar-tiket',
    name: 'DaftarTiket',
    component: () => import('../views/DaftarTiket.vue'),
  },
  {
    path: '/add-tiket',
    name: 'AddTiket',
    component: () => import('../views/AddTiket.vue'),
  },
  {
    path: '/user',
    name: 'UserView',
    component: () => import('../views/UserView.vue'),
  },
  {
    path: '/add-user',
    name: 'AddUser',
    component: () => import('../views/AddUser.vue'),
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;