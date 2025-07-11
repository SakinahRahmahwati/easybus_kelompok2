<template>
  <div class="content py-4">
    <div class="card shadow-sm rounded-4 bg-dark-blue mb-4">
      <div class="card-header text-white py-3">
        <h4 class="card-title mb-0 text-center">Form Pemesanan Tiket</h4>
      </div>
      <div class="card-body">
        <form @submit.prevent="submitBooking">
          <!-- Input Jumlah Kursi -->
          <div class="form-group mb-3">
            <label for="seatCount">Jumlah Kursi</label>
            <input type="number" id="seatCount" v-model.number="bookingForm.seatCount" class="form-control" min="1"
              @change="generatePassengerFields" required />
          </div>

          <!-- Input Nama Penumpang -->
          <div v-for="(nama, index) in bookingForm.nama_penumpang" :key="index" class="form-group mb-3">
            <label :for="'nama-' + index">Nama Penumpang {{ index + 1 }}</label>
            <input type="text" class="form-control" v-model="bookingForm.nama_penumpang[index]" required />
          </div>

          <!-- Input Info Jadwal (Readonly) -->
          <div class="form-group mb-3">
            <label>Nama Bus</label>
            <input type="text" class="form-control" :value="selectedBus.nama_bus" readonly />
          </div>

          <div class="form-group mb-3">
            <label>Jam Berangkat</label>
            <input type="text" class="form-control" :value="selectedBus.jam_berangkat" readonly />
          </div>

          <div class="form-group mb-3">
            <label>Total Bayar</label>
            <input type="text" class="form-control" :value="totalBayar + ' IDR'" readonly />
          </div>

          <!-- Upload Bukti Pembayaran -->
          <div class="mb-3">
            <label for="paymentProof">Unggah Bukti Pembayaran (Nama File akan dikirim)</label>
            <input type="file" id="paymentProof" accept="image/*" @change="handleFileChange" class="form-control"
              required />
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
import { supabase } from "@/supabase";

export default {
  data() {
    return {
      selectedBus: this.$route.query.bus ? JSON.parse(this.$route.query.bus) : {},
      bookingForm: {
        seatCount: 1,
        nama_penumpang: [""],
        buktiPembayaran: null,
      },
      isSubmitting: false,
    };
  },
  computed: {
    totalBayar() {
      return this.selectedBus.harga * this.bookingForm.seatCount;
    },
  },
  methods: {
    generatePassengerFields() {
      this.bookingForm.nama_penumpang = Array.from({ length: this.bookingForm.seatCount }, (_, i) => this.bookingForm.nama_penumpang[i] || "");
    },
    handleFileChange(event) {
      this.bookingForm.buktiPembayaran = event.target.files[0];
    },
    async submitBooking() {
      this.isSubmitting = true;

      try {
        const token = localStorage.getItem("token");
        // 1. Kirim data pemesanan ke backend dulu
        const resPemesanan = await axios.post("/api/pemesanan", {
          id_jadwal: this.selectedBus.id_jadwal || this.selectedBus.id,
          nama_penumpang: this.bookingForm.nama_penumpang,
        },
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          });

        const id_pemesanan = resPemesanan.data.data[0].id_pemesanan;

        // 2. Upload ke Supabase Storage
        const file = this.bookingForm.buktiPembayaran;
        const filePath = `public/bukti-${Date.now()}-${file.name}`;

        const { error } = await supabase.storage
          .from("easybusbuktiupload")
          .upload(filePath, file);

        if (error) throw error;

        // 3. Dapatkan public URL file
        const { data } = supabase.storage
          .from("easybusbuktiupload")
          .getPublicUrl(filePath);

        const fileUrl = data.publicUrl;


        // 4. Kirim URL ke backend
        await axios.post("/api/upload-bukti", {
          id_pemesanan: id_pemesanan,
          url: fileUrl,
        },
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          });

        Swal.fire("Berhasil", "Pemesanan berhasil! Menunggu verifikasi pembayaran.", "success");
        this.$router.push("/riwayat-pemesanan");

      } catch (error) {
        console.error(error);
        Swal.fire("Gagal", "Terjadi kesalahan saat pemesanan.", "error");
      } finally {
        this.isSubmitting = false;
      }
    }

  },
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