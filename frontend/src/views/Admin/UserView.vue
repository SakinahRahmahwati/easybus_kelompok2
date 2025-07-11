<template>
  <div class="content py-4">
    <div class="card shadow-sm rounded-4 bg-dark-blue">
      <div class="card-header text-white py-3 d-flex justify-content-between align-items-center">
        <h4 class="card-title mb-0 fw-bold">Daftar User</h4>
        <router-link to="/add-user">
          <button class="btn btn-outline-light">
            <i class="fas fa-plus-circle"></i> ADD DATA
          </button>
        </router-link>
      </div>

      <div class="card-body px-4 py-4">
        <div class="table-responsive">
          <table class="table table-striped table-bordered">
            <thead class="text-center text-white">
              <tr>
                <th>No</th>
                <th>Nama User</th>
                <th>Email</th>
                <th>Role</th>
                <th>Aksi</th>
              </tr>
            </thead>
            <tbody>
              <tr v-if="users.length === 0">
                <td colspan="5" class="text-center text-muted">Belum ada data user</td>
              </tr>
              <tr v-for="(user, index) in users" :key="user.id_user">
                <td class="text-center">{{ index + 1 }}</td>
                <td>{{ user.nama }}</td>
                <td>{{ user.email }}</td>
                <td>{{ user.role }}</td>
                <td class="text-center">
                  <button @click="confirmDelete(user)" class="btn btn-sm btn-danger">
                    <i class="fas fa-trash-alt"></i>
                  </button>
                </td>
              </tr>   
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import Swal from "sweetalert2";

export default {
  data() {
    return {
      users: [], // Menyimpan data user
    };
  },
  created() {
    this.getUser();
  },
  methods: {
    // Fungsi untuk mendapatkan daftar user
    getUser() {
      axios.get('/api/user')  // Menggunakan endpoint untuk mendapatkan data user
        .then((response) => {  // Menyimpan data yang diterima ke dalam users
          this.users = response.data;  // Tidak perlu mendestructuring, gunakan langsung response.data
        })
        .catch(error => {
          console.error('Terjadi kesalahan:', error);
        });
    },

    // Fungsi untuk mengonfirmasi penghapusan user
    confirmDelete(user) {
      const userId = localStorage.getItem('user_id');
      
      // Validasi jika user yang sedang login dan user yang ingin dihapus sama
      if (user.id_user === parseInt(userId)) {
        Swal.fire({
          title: 'Apakah Anda yakin?',
          text: `User ${user.nama} akan dihapus!`,
          icon: 'warning',
          showCancelButton: true,
          confirmButtonColor: '#d33',
          cancelButtonColor: '#3085d6',
          confirmButtonText: 'Hapus',
          cancelButtonText: 'Batal',
        }).then((result) => {
          if (result.isConfirmed) {
            this.deleteUser(user.id_user); // Menghapus user berdasarkan id_user
            Swal.fire('Dihapus!', 'User telah berhasil dihapus.', 'success');
          }
        });
      } else {
        Swal.fire('Error', 'Tidak dapat menghapus user yang sedang aktif', 'error');
      }
    },

    // Fungsi untuk menghapus user
    deleteUser(userId) {
      axios.delete(`/api/delete-user/${userId}`)  // Menggunakan endpoint untuk menghapus user
        .then(() => {
          this.getUser();  // Refresh data setelah menghapus
        })
        .catch((error) => {
          console.error('Gagal menghapus user:', error);
        });
    }
  }
};
</script>

<style scoped>
/* Styling remains the same */
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
</style>