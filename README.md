# 🚍 EasyBus - Tiket Pemesanan Bus Online

Proyek ini adalah aplikasi pemesanan tiket bus berbasis **Vue.js (frontend)**, **Flask (backend)** dengan fitur tambahan seperti **Redis**, **RabbitMQ**, **MySQL**, dan **Nginx load balancing**. Dikonfigurasi agar dapat langsung dijalankan dengan **Docker Compose**.

---

## 🧩 Arsitektur

- **Frontend**: Vue.js (build dist)
- **Backend**: Flask (3 instance untuk load balancing)
- **Load Balancer**: Nginx (port `8081`)
- **Database**: MySQL
- **Queue**: RabbitMQ
- **Cache**: Redis
- **Logging**: Worker logging async via queue

---

## 🚀 Cara Menjalankan

### 1. Clone proyek

```bash
git clone 
cd easybus
