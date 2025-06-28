<template>
  <div class="content py-4">
    <!-- Card dengan styling biru dongker -->
    <div class="card shadow-sm rounded-4 bg-dark-blue">
      <div class="card-header text-white py-3 d-flex justify-content-between align-items-center">
        <h4 class="card-title mb-0 fw-bold">Daftar Booking Customer</h4>
        <button @click="exportPDF" class="btn btn-outline-light">
          <i></i> EKSPOR PDF
        </button>
      </div>

      <div class="card-body px-4 py-4">
        <div class="table-responsive">
          <table class="table table-striped table-bordered">
            <thead class="text-center text-primary">
              <tr>
                <th>No</th>
                <th>Nama Penumpang</th>
                <th>Jumlah Tiket</th>
                <th>Total Bayar</th>
                <th>Status Pembayaran</th>
                <th>Aksi</th>
              </tr>
            </thead>
            <tbody>
              <tr v-if="bookings.length === 0">
                <td colspan="6" class="text-center text-muted">Belum ada booking</td>
              </tr>
              <tr v-for="(booking, index) in paginatedData" :key="booking.id_booking">
                <td class="text-center">{{ index + 1 + (currentPage - 1) * pageSize }}</td>
                <td>{{ booking.nama_customer }}</td>
                <td>{{ booking.jenis_service }}</td>
                <td>{{ booking.total_bayar }}</td>
                <td class="text-center">
                  <span :class="statusClass(booking.status)">{{ booking.status }}</span>
                </td>
                <td class="text-center">
                  <button 
                    v-if="booking.status === 'pending'" 
                    @click="updateBooking(booking.id_booking, 'confirmed')" 
                    class="btn btn-sm btn-success me-1">
                    <i class="fas fa-check"></i>
                  </button>
                  <button 
                    v-if="booking.status === 'pending'" 
                    @click="updateBooking(booking.id_booking, 'cancelled')" 
                    class="btn btn-sm btn-warning me-1">
                    <i class="fas fa-times"></i>
                  </button>
                  <button 
                    @click="confirmDelete(booking)" 
                    class="btn btn-sm btn-danger">
                    <i class="fas fa-trash"></i>
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Kontrol Pagination -->
        <div class="d-flex justify-content-between mt-4">
          <button :disabled="currentPage === 1" @click="changePage(currentPage - 1)" class="btn btn-outline-primary">
            Previous
          </button>
          <span>Page {{ currentPage }} of {{ totalPages }}</span>
          <button :disabled="currentPage === totalPages" @click="changePage(currentPage + 1)" class="btn btn-outline-primary">
            Next
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
// Import SweetAlert2
import Swal from 'sweetalert2';

export default {
  data() {
    return {
      bookings: [],
      currentPage: 1,
      pageSize: 10,
    };
  },
  computed: {
    totalPages() {
      return Math.ceil(this.bookings.length / this.pageSize);
    },
    paginatedData() {
      const start = (this.currentPage - 1) * this.pageSize;
      const end = start + this.pageSize;
      return this.bookings.slice(start, end);
    }
  },
  methods: {
    formatDate(date) {
      const d = new Date(date);
      return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}-${String(d.getDate()).padStart(2, "0")} ${String(d.getHours()).padStart(2, "0")}:${String(d.getMinutes()).padStart(2, "0")}`;
    },
    statusClass(status) {
      switch (status) {
        case "confirmed":
          return "text-success";
        case "cancelled":
          return "text-danger";
        default:
          return "text-warning";
      }
    },
    updateBooking(id_booking, newStatus) {
      const token = localStorage.getItem("token");

      fetch(`http://127.0.0.1:5000/update-booking-status/${id_booking}`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${token}`,
        },
        body: JSON.stringify({ status: newStatus }),
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.success) {
            this.bookings = this.bookings.map((booking) =>
              booking.id_booking === id_booking
                ? { ...booking, status: newStatus }
                : booking
            );
          } else {
            Swal.fire({
              icon: 'error',
              title: 'Gagal memperbarui status booking',
              text: 'Terjadi kesalahan saat memperbarui status booking.',
            });
          }
        })
        .catch((error) => {
          console.error("Error:", error);
          Swal.fire({
            icon: 'error',
            title: 'Gagal memperbarui status booking',
            text: 'Terjadi kesalahan saat memperbarui status booking.',
          });
        });
    },
    deleteBooking(id_booking) {
      const token = localStorage.getItem("token");

      fetch(`http://127.0.0.1:5000/delete-booking/${id_booking}`, {
        method: "DELETE",
        headers: {
          "Authorization": `Bearer ${token}`,
        },
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.success) {
            this.bookings = this.bookings.filter(
              (booking) => booking.id_booking !== id_booking
            );
            Swal.fire({
              icon: 'success',
              title: 'Booking berhasil dihapus',
              text: 'Data booking telah dihapus.',
            });
          } else {
            Swal.fire({
              icon: 'error',
              title: 'Gagal menghapus booking',
              text: 'Terjadi kesalahan saat menghapus booking.',
            });
          }
        })
        .catch((error) => {
          console.error("Error:", error);
          Swal.fire({
            icon: 'error',
            title: 'Gagal menghapus booking',
            text: 'Terjadi kesalahan saat menghapus booking.',
          });
        });
    },
    confirmDelete(booking) {
      Swal.fire({
        title: 'Apakah Anda yakin?',
        text: `Booking ${booking.nama_customer} akan dihapus!`,
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#d33',
        cancelButtonColor: '#3085d6',
        confirmButtonText: 'Hapus',
        cancelButtonText: 'Batal',
      }).then((result) => {
        if (result.isConfirmed) {
          this.deleteBooking(booking.id_booking);
          Swal.fire('Dihapus!', 'Booking telah berhasil dihapus.', 'success');
        }
      });
    },
    changePage(page) {
      if (page < 1 || page > this.totalPages) return;
      this.currentPage = page;
    }
  },
  mounted() {
    const token = localStorage.getItem("token");

    if (!token) {
      Swal.fire({
        icon: 'error',
        title: 'Akses ditolak',
        text: 'Anda harus login terlebih dahulu.',
      });
      return;
    }

    fetch("http://127.0.0.1:5000/bookings", {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.error) {
          console.error(data.error);
          Swal.fire({
            icon: 'error',
            title: 'Gagal memuat booking',
            text: 'Terjadi kesalahan saat memuat data booking.',
          });
        } else {
          this.bookings = data;
        }
      })
      .catch((error) => {
        console.error("Error:", error);
        Swal.fire({
          icon: 'error',
          title: 'Gagal memuat booking',
          text: 'Terjadi kesalahan saat memuat data booking.',
        });
      });
  },
};
</script>

<style scoped>
.bg-dark-blue {
  background: linear-gradient(145deg, #34495e, #2c3e50) !important;
  color: #fff !important;
  box-shadow: 0 6px 15px rgba(0, 0, 0, 0.2);
  border-radius: 12px;
  max-width: 900px;
  margin: 0 auto;
}

.card-header {
  padding: 10px 20px;
  font-size: 16px;
}

.card-body {
  background-color: #f9f9f9;
  border-radius: 12px;
  padding: 20px;
}

.table {
  border-collapse: collapse;
  width: 100%;
}

th, td {
  padding: 12px;
  text-align: center;
  border: 1px solid #ddd;
}

th {
  background-color: #f8f9fa;
  color: #333;
}

tbody tr:nth-child(even) {
  background-color: #f2f2f2;
}

tbody tr:hover {
  background-color: #f1f1f1;
  cursor: pointer;
}

.card-title.fw-bold {
  font-weight: bold;
}

.d-flex {
  margin-top: 20px;
  justify-content: space-between;
}

.btn-outline-light {
  font-size: 14px;
  padding: 8px 15px;
}

.btn-outline-light:hover {
  background-color: #8fbca1;
}

.btn-sm {
  font-size: 14px;
  padding: 5px 10px;
}

span {
  font-size: 16px;
  color: #4CAF50;
  font-weight: 600;
}

button:disabled {
  cursor: not-allowed;
}

button {
  margin: 0 5px;
}

.btn-outline-primary {
  color: #007bff;
  border-color: #007bff;
}

.btn-outline-primary:hover {
  background-color: #007bff;
  color: white;
}

/* Tombol Eksport PDF */
.btn-outline-light {
  font-size: 14px; /* Ukuran font tombol */
  padding: 8px 15px; /* Menyesuaikan ukuran tombol */
  border-color: #007bff; /* Warna border biru */
  color: #007bff; /* Warna teks biru */
  background-color: white; /* Warna latar belakang putih */
}

.btn-outline-light:hover {
  background-color: #007bff; /* Warna biru saat hover */
  color: white; /* Warna teks putih saat hover */
}
</style>