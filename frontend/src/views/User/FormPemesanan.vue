<template>
  <div class="content py-4">
    <div class="card shadow-sm rounded-4 bg-dark-blue mb-4">
      <div class="card-header text-white py-3">
        <h4 class="card-title mb-0 text-center">Form Pemesanan Tiket</h4>
      </div>
      <div class="card-body">
        <form @submit.prevent="submitBooking">
          <div class="form-group mb-3">
            <label for="nama">Nama Penumpang</label>
            <input type="text" id="nama" v-model="bookingForm.nama" class="form-control" required />
          </div>

          <div class="form-group mb-3">
            <label for="seatCount">Jumlah Tiket</label>
            <input type="number" id="seatCount" v-model.number="bookingForm.seatCount" class="form-control" min="1" required />
          </div>

          <div class="form-group mb-3">
            <label for="busName">Nama Bus</label>
            <input type="text" id="busName" v-model="selectedBus.nama_bus" class="form-control" readonly />
          </div>

          <div class="form-group mb-3">
            <label for="departureTime">Jam Berangkat</label>
            <input type="text" id="departureTime" v-model="selectedBus.jam_berangkat" class="form-control" readonly />
          </div>

          <div class="form-group mb-3">
            <label for="totalBayar">Total Bayar</label>
            <input type="text" id="totalBayar" :value="totalBayar + ' IDR'" class="form-control" readonly />
          </div>

          <div class="mb-3">
            <label for="paymentProof">Unggah Bukti Pembayaran</label>
            <input type="file" id="paymentProof" accept="image/*" @change="handleFileChange" class="form-control" required />
          </div>

          <div class="text-center">
            <button type="submit" class="btn btn-dongker" :disabled="isSubmitting">
              <i class="fas fa-save me-2"></i> Simpan
            </button>
          </div>
        </form>
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
      selectedBus: this.$route.query.bus ? JSON.parse(this.$route.query.bus) : {},
      bookingForm: {
        nama: "",
        seatCount: 1,
        buktiPembayaran: null
      },
      isSubmitting: false,
    };
  },
  computed: {
    totalBayar() {
      return this.selectedBus.harga * this.bookingForm.seatCount;
    }
  },
  methods: {
    handleFileChange(event) {
      this.bookingForm.buktiPembayaran = event.target.files[0];
    },

    uploadBukti(file) {
      return new Promise((resolve) => {
        // Simulasi upload ke server/file hosting
        const dummyUrl = 'https://your-storage.com/uploads/' + file.name;
        resolve(dummyUrl);
      });
    },

    async submitBooking() {
      this.isSubmitting = true;

      const namaList = Array(this.bookingForm.seatCount).fill(this.bookingForm.nama);

      try {
        const res = await axios.post('/api/pemesanan', {
          id_jadwal: this.selectedBus.id_jadwal,
          nama_penumpang: namaList
        });

        const idPemesanan = res.data.data[0].id_pemesanan;
        const uploadedUrl = await this.uploadBukti(this.bookingForm.buktiPembayaran);

        await axios.post('/api/upload-bukti', {
          id_pemesanan: idPemesanan,
          url: uploadedUrl
        });

        Swal.fire("Berhasil", "Pemesanan berhasil! Menunggu verifikasi.", "success");
        this.$router.push("/riwayat-pemesanan");
      } catch (err) {
        Swal.fire("Gagal", "Terjadi kesalahan saat memesan.", "error");
        console.error(err);
      } finally {
        this.isSubmitting = false;
      }
    }
  }
};
</script>

<style scoped>
.bg-dark-blue {
  background: linear-gradient(145deg, #34495e, #2c3e50) !important;
  color: #fff !important;
  box-shadow: 0 6px 15px rgba(0, 0, 0, 0.2);
  border-radius: 12px;
  max-width: 800px;
  margin: 0 auto;
}

.card-header {
  padding: 10px 20px;
  font-size: 14px;
}

.card-header h4 {
  text-align: center;
  font-weight: bold;
  font-size: 1.5rem;
}

.card-body {
  background-color: #f9f9f9;
  border-radius: 12px;
  padding: 15px;
}

.form-group {
  margin-bottom: 12px;
}

label {
  font-size: 0.9rem;
}

input[type="text"],
input[type="email"],
input[type="number"] {
  padding: 8px;
  font-size: 0.9rem;
  border-radius: 5px;
  border: 1px solid #ccc;
  width: 100%;
}

button {
  background-color: #34495e;
  color: white;
  border: none;
  border-radius: 5px;
  padding: 6px 12px;
  font-size: 0.9rem;
  cursor: pointer;
  font-weight: bold;
}

button:hover {
  background-color: #2c3e50;
}

.text-center {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 20px;
}
</style>