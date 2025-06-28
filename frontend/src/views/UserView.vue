<template>
  <div class="content py-4">
    <!-- Card dengan styling biru dongker -->
    <div class="card shadow-sm rounded-4 bg-dark-blue">
      <div class="card-header text-white py-3 d-flex justify-content-between align-items-center">
        <h4 class="card-title mb-0 fw-bold">Daftar User</h4>
        <!-- Tombol untuk membuka form tambah data -->
        <router-link to="/add-user">
          <button class="btn btn-outline-light">
            <i class="fas fa-plus-circle"></i>  ADD DATA
          </button>
        </router-link>      
      </div>

      <!-- Form tambah data user -->
      <div v-if="isAddFormVisible" class="add-data-form">
        <div class="card-body">
          <h5>Tambah Data User</h5>
          <form @submit.prevent="addUser">
            <div class="mb-3">
              <label for="namaUser" class="form-label">Nama User</label>
              <input type="text" id="namaUser" v-model="newUser.nama" class="form-control" placeholder="Masukkan Nama User" required />
            </div>
            <div class="mb-3">
              <label for="email" class="form-label">Email</label>
              <input type="email" id="email" v-model="newUser.email" class="form-control" placeholder="Masukkan Email" required />
            </div>
            <div class="mb-3">
              <label for="password" class="form-label">Password</label>
              <input type="password" id="password" v-model="newUser.password" class="form-control" placeholder="Masukkan Password" required />
            </div>
            <div class="mb-3">
              <label for="role" class="form-label">Role</label>
              <select id="role" v-model="newUser.role" class="form-control" required>
                <option value="admin">Admin</option>
                <option value="customer">Customer</option>
              </select>
            </div>
            <button type="submit" class="btn btn-success">Simpan</button>
            <button @click="toggleAddDataForm" type="button" class="btn btn-danger ms-2">Batal</button>
          </form>
        </div>
      </div>

      <!-- Table Daftar User -->
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
              <!-- Jika belum ada data user -->
              <tr v-if="users.length === 0">
                <td colspan="5" class="text-center text-muted">Belum ada data user</td>
              </tr>
              <!-- Daftar user yang ada -->
              <tr v-for="(user, index) in users" :key="user.id">
                <td class="text-center">{{ index + 1 }}</td>
                <td>{{ user.nama }}</td>
                <td>{{ user.email }}</td>
                <td>{{ user.role }}</td>
                <td class="text-center">
                  <button 
                    @click="confirmDelete(user)" 
                    class="btn btn-sm btn-danger">
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
import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap/dist/js/bootstrap.bundle.min.js";
import axios from 'axios';

export default {
  data() {
    return {
      users: [],
      isAddFormVisible: false,
      newUser: {
        nama: '',
        email: '',
        password: '',
        role: 'customer'
      },
      showDeleteModal: false, 
      userToDelete: null, 
    };
  },
  created() {
    this.getUser();
  },
  mounted() {
    this.getUser();
  },
  methods: {
    getUser() {
      axios.get('http://127.0.0.1:5000/user')
        .then(response => {
          this.users = response.data;
        })
        .catch(error => {
          console.error('Terjadi kesalahan:', error);
        });
    },
    toggleAddDataForm() {
      this.isAddFormVisible = !this.isAddFormVisible;
    },
    addUser() {
      const newUser = { ...this.newUser };
      axios.post('http://127.0.0.1:5000/add-user', newUser)
        .then(response => {
          this.users.push(response.data);
          this.newUser = { nama: '', email: '', password: '', role: 'customer' };
          this.toggleAddDataForm(); // Close form after adding
        })
        .catch(error => {
          console.error('Terjadi kesalahan:', error);
        });
    },
    confirmDelete(user) {
      this.userToDelete = user;
      this.showDeleteModal = true;
    },
    closeDeleteModal() {
      this.showDeleteModal = false;
      this.userToDelete = null;
    },
    deleteUser() {
      if (this.userToDelete && this.userToDelete.id) {
        axios.delete(`http://127.0.0.1:5000/delete-user/${this.userToDelete.id}`)
          .then(() => {
            this.users = this.users.filter(user => user.id !== this.userToDelete.id);
            this.closeDeleteModal();
          })
          .catch(error => {
            console.error('Gagal menghapus user:', error);
          });
      }
    }
  }
}
</script>

<style scoped>
.bg-dark-blue {
  background: linear-gradient(145deg, #34495e, #2c3e50) !important; /* Warna biru dongker */
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