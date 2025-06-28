<template>
  <div class="content py-4">
    <!-- Card dengan styling biru dongker -->
    <div class="card shadow-sm rounded-4 bg-dark-blue">
      <div class="card-header text-white py-3 d-flex justify-content-between align-items-center">
        <h4 class="card-title mb-0 fw-bold">Daftar Data Tiket Bus</h4>
        <!-- Tombol untuk membuka form tambah data -->
        <router-link to="/add-tiket">
          <button class="btn btn-outline-light">
            <i class="fas fa-plus-circle"></i>  ADD DATA
          </button>
        </router-link>      
      </div>

      <!-- Form tambah data tiket -->
      <div v-if="isAddFormVisible" class="add-data-form">
        <div class="card-body">
          <h5>Tambah Data Tiket</h5>
          <form @submit.prevent="addTicket">
            <div class="mb-3">
              <label for="namaBus" class="form-label">Nama Bus</label>
              <input type="text" id="namaBus" v-model="newTicket.nama_bus" class="form-control" placeholder="Masukkan Nama Bus" required />
            </div>
            <!-- Tambahan Kolom Kota Keberangkatan dan Kota Tujuan setelah Nama Bus -->
            <div class="mb-3">
              <label for="kotaKeberangkatan" class="form-label">Kota Keberangkatan</label>
              <input type="text" id="kotaKeberangkatan" v-model="newTicket.kota_keberangkatan" class="form-control" placeholder="Masukkan Kota Keberangkatan" required />
            </div>
            <div class="mb-3">
              <label for="kotaTujuan" class="form-label">Kota Tujuan</label>
              <input type="text" id="kotaTujuan" v-model="newTicket.kota_tujuan" class="form-control" placeholder="Masukkan Kota Tujuan" required />
            </div>
            <div class="mb-3">
              <label for="jamKeberangkatan" class="form-label">Jam Keberangkatan</label>
              <input type="time" id="jamKeberangkatan" v-model="newTicket.jam_keberangkatan" class="form-control" required />
            </div>
            <div class="mb-3">
              <label for="jamTiba" class="form-label">Jam Tiba</label>
              <input type="time" id="jamTiba" v-model="newTicket.jam_tiba" class="form-control" required />
            </div>
            <div class="mb-3">
              <label for="harga" class="form-label">Harga</label>
              <input type="number" id="harga" v-model="newTicket.harga" class="form-control" placeholder="Masukkan Harga" required />
            </div>
            <div class="mb-3">
              <label for="totalKursi" class="form-label">Total Kursi</label>
              <input type="number" id="totalKursi" v-model="newTicket.total_kursi" class="form-control" placeholder="Masukkan Total Kursi" required />
            </div>
            <div class="mb-3">
              <label for="kursiTersedia" class="form-label">Kursi Tersedia</label>
              <input type="number" id="kursiTersedia" v-model="newTicket.kursi_tersedia" class="form-control" placeholder="Masukkan Kursi Tersedia" required />
            </div>
            <button type="submit" class="btn btn-success">Simpan</button>
            <button @click="toggleAddDataForm" type="button" class="btn btn-danger ms-2">Batal</button>
          </form>
        </div>
      </div>

      <!-- Table Daftar Tiket -->
      <div class="card-body px-4 py-4">
        <div class="table-responsive">
          <table class="table table-striped table-bordered">
            <thead class="text-center text-white">
              <tr>
                <th>No</th>
                <th>Nama Bus</th>
                <th>Kota Keberangkatan</th>
                <th>Kota Tujuan</th>
                <th>Jam Keberangkatan</th>
                <th>Jam Tiba</th>
                <th>Harga</th>
                <th>Total Kursi</th>
                <th>Kursi Tersedia</th>
                <th>Aksi</th>
              </tr>
            </thead>
            <tbody>
              <!-- Jika belum ada data tiket -->
              <tr v-if="tickets.length === 0">
                <td colspan="10" class="text-center text-muted">Belum ada data tiket</td>
              </tr>
              <!-- Daftar tiket yang ada -->
              <tr v-for="(ticket, index) in tickets" :key="ticket.id_tiket">
                <td class="text-center">{{ index + 1 }}</td>
                <td>{{ ticket.nama_bus }}</td>
                <td>{{ ticket.kota_keberangkatan }}</td>
                <td>{{ ticket.kota_tujuan }}</td>
                <td>{{ ticket.jam_keberangkatan }}</td>
                <td>{{ ticket.jam_tiba }}</td>
                <td>{{ ticket.harga.toLocaleString() }} IDR</td>
                <td>{{ ticket.total_kursi }}</td>
                <td>{{ ticket.kursi_tersedia }}</td>
                <td class="text-center">
                  <button @click="deleteTicket(ticket.id_tiket)" class="btn btn-sm btn-danger">
                    <i class="fas fa-trash-alt"></i>
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Pagination Controls -->
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
import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap/dist/js/bootstrap.bundle.min.js";

export default {
  data() {
    return {
      tickets: [],
      currentPage: 1,
      pageSize: 10,
      isAddFormVisible: false, // Menyembunyikan form add data
      newTicket: {
        nama_bus: '',
        kota_keberangkatan: '',   // Kolom Kota Keberangkatan
        kota_tujuan: '',           // Kolom Kota Tujuan
        jam_keberangkatan: '',
        jam_tiba: '',
        harga: 0,
        total_kursi: 0,
        kursi_tersedia: 0
      }
    };
  },
  computed: {
    totalPages() {
      return Math.ceil(this.tickets.length / this.pageSize);
    },
    paginatedData() {
      const start = (this.currentPage - 1) * this.pageSize;
      const end = start + this.pageSize;
      return this.tickets.slice(start, end);
    }
  },
  mounted() {
    this.fetchTickets();
  },
  methods: {
    fetchTickets() {
      // Fetch data tiket dari API
      this.tickets = [
        { id_tiket: 1, nama_bus: 'Gumarang Jaya', kota_keberangkatan: 'Jakarta', kota_tujuan: 'Bandung', jam_keberangkatan: '09:30', jam_tiba: '17:30', harga: 490000, total_kursi: 25, kursi_tersedia: 10 },
        { id_tiket: 2, nama_bus: 'Kencana', kota_keberangkatan: 'Surabaya', kota_tujuan: 'Yogyakarta', jam_keberangkatan: '08:30', jam_tiba: '16:30', harga: 400000, total_kursi: 30, kursi_tersedia: 15 }
      ];
    },

    toggleAddDataForm() {
      this.isAddFormVisible = !this.isAddFormVisible; // Toggle form add data
    },

    addTicket() {
      const newTicket = { ...this.newTicket, id_tiket: this.tickets.length + 1 };
      this.tickets.push(newTicket);
      this.newTicket = { nama_bus: '', kota_keberangkatan: '', kota_tujuan: '', jam_keberangkatan: '', jam_tiba: '', harga: 0, total_kursi: 0, kursi_tersedia: 0 };
      this.toggleAddDataForm(); // Close the form after adding
    },

    deleteTicket(id_tiket) {
      this.tickets = this.tickets.filter(ticket => ticket.id_tiket !== id_tiket);
    },

    changePage(page) {
      if (page < 1 || page > this.totalPages) return;
      this.currentPage = page;
    }
  }
};
</script>

<style scoped>
.bg-dark-blue {
  background: linear-gradient(145deg, #34495e, #2c3e50) !important;  /* Warna biru dongker */
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

.add-data-form {
  background-color: #fff;
  padding: 20px;
  border-radius: 10px;
  margin-bottom: 20px;
}

.add-data-form form {
  width: 100%;
}

.add-data-form input {
  margin-bottom: 10px;
}

.add-data-form button {
  margin-top: 10px;
}
</style>