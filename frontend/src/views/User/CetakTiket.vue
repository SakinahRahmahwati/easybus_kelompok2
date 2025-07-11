<template>
  <div class="ticket-layout" ref="printArea">
    <div class="ticket-box">
      <div class="ticket-header">
        <div>
          <h3>BUS TICKET</h3>
          <p class="ticket-type">E-TIKET</p>
        </div>
        <div class="ticket-code">{{ tiket.kode_tiket }}</div>
      </div>

      <div class="ticket-body">
        <div class="ticket-row">
          <div class="label">Nama Penumpang</div>
          <div class="value">{{ tiket.nama_penumpang }}</div>
        </div>
        <div class="ticket-row">
          <div class="label">Nama Bus</div>
          <div class="value">{{ tiket.bus }}</div>
        </div>
        <div class="ticket-row">
          <div class="label">Asal</div>
          <div class="value">{{ tiket.asal }}</div>
          <div class="label">Tujuan</div>
          <div class="value">{{ tiket.tujuan }}</div>
        </div>
        <div class="ticket-row">
          <div class="label">Tanggal</div>
          <div class="value">{{ formatTanggal(tiket.tanggal) }}</div>
          <div class="label">Jam</div>
          <div class="value">{{ tiket.jam_berangkat }} - {{ tiket.jam_tiba }}</div>
        </div>
        <div class="ticket-row">
          <div class="label">Total Bayar</div>
          <div class="value">{{ formatRupiah(tiket.total_bayar) }}</div>
        </div>
      </div>
    </div>

    <!-- Tombol Print -->
    <div class="text-center mt-4 no-print">
      <button class="btn btn-primary" @click="printPDF">
        <i class="fas fa-print"></i> Cetak / Simpan PDF
      </button>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      tiket: {}
    };
  },
  mounted() {
    const id = this.$route.params.id;
    axios.get(`/api/etiket/${id}`)
      .then(res => {
        this.tiket = res.data;
      })
      .catch(err => console.error(err));
  },
  methods: {
    printPDF() {
      window.print();
    },
    formatRupiah(value) {
      if (!value && value !== 0) return '-';
      return new Intl.NumberFormat('id-ID', {
        style: 'currency',
        currency: 'IDR',
        minimumFractionDigits: 0
      }).format(value);
    },
    formatTanggal(tanggal) {
      if (!tanggal) return '-';
      const date = new Date(tanggal);
      return date.toLocaleDateString('id-ID', {
        weekday: 'long',
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      });
    }
  }
};
</script>

<style scoped>
.ticket-layout {
  max-width: 700px;
  margin: 100px auto 30px auto; /* agar tidak menabrak navbar */
  color: #2c3e50;
  font-family: 'Segoe UI', sans-serif;
}

.ticket-box {
  border: 2px dashed #2980b9;
  padding: 20px 30px;
  border-radius: 12px;
  background: #ecf0f1;
  position: relative;
}

.ticket-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 2px solid #2980b9;
  padding-bottom: 10px;
  margin-bottom: 20px;
}

.ticket-header h3 {
  margin: 0;
  color: #2980b9;
  font-weight: 700;
}

.ticket-type {
  font-size: 14px;
  color: #7f8c8d;
}

.ticket-code {
  font-size: 18px;
  font-weight: bold;
  color: #e74c3c;
}

.ticket-body {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.ticket-row {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.label {
  font-weight: 600;
  min-width: 100px;
}

.value {
  flex: 1;
}

.ticket-footer {
  margin-top: 30px;
  text-align: center;
  font-size: 14px;
  color: #7f8c8d;
}

/* Hindari mencetak sidebar/navbar/footer */
@media print {
  body * {
    visibility: hidden;
  }

  .ticket-layout,
  .ticket-layout * {
    visibility: visible;
  }

  .ticket-layout {
    position: absolute;
    left: 0;
    top: 0;
    width: 100%;
    margin: 0;
    padding: 0;
  }

  .no-print {
    display: none !important;
  }

  /* Tambahan: pastikan sidebar dan navbar tidak tampil saat cetak */
  .sidebar,
  .navbar,
  .footer,
  #sidebar,
  #navbar,
  #footer {
    display: none !important;
  }
}
</style>
