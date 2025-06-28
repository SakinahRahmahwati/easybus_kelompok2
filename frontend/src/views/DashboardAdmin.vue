<template>
    <div class="content">
      <div class="row">
        <div class="col-lg-3 col-md-6 col-sm-6" v-for="card in cards" :key="card.title">
          <div class="card card-stats">
            <div class="card-body">
              <div class="row">
                <!-- Ikon Card -->
                <div class="col-5 col-md-4">
                  <div class="icon-big text-center icon-warning">
                    <i :class="card.icon"></i>
                  </div>
                </div>
                <!-- Informasi Card -->
                <div class="col-7 col-md-8">
                  <div class="numbers">
                    <p class="card-category">{{ card.category }}</p>
                    <p class="card-title">{{ card.value }}</p>
                  </div>
                </div>
              </div>
            </div>
            <!-- Footer Card -->
            <div class="card-footer">
              <hr />
              <div class="stats">
                <i :class="card.footerIcon"></i> {{ card.footerText }}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import axios from "axios";
  
  export default {
    data() {
      return {
        cards: [
          {
            title: "Jumlah User",
            value: 0,
            icon: "nc-icon nc-badge text-primary",
            category: "User",
            footerIcon: "fa fa-refresh",
            footerText: "Updated now",
          },
          {
            title: "Jumlah Customer",
            value: 0,
            icon: "nc-icon nc-single-02 text-success",
            category: "Customer",
            footerIcon: "fa fa-refresh",
            footerText: "Updated now",
          },
          {
            title: "Jumlah Tiket",
            value: 0,
            icon: "nc-icon nc-tile-56 text-primary",
            category: "Tiket",
            footerIcon: "fa fa-refresh",
            footerText: "Updated now",
          },
          {
            title: "Jumlah Booking",
            value: 0,
            icon: "nc-icon nc-calendar-60 text-success",
            category: "Booking",
            footerIcon: "fa fa-refresh",
            footerText: "Updated now",
          },
        ],
      };
    },
    methods: {
      async fetchDashboardStats() {
        try {
          const response = await axios.get("http://127.0.0.1:5000/api/dashboard-stats");
          const { user, customer, tiket, booking } = response.data;
          this.cards[0].value = user;
          this.cards[1].value = customer;
          this.cards[2].value = tiket;
          this.cards[3].value = booking;
        } catch (error) {
          console.error("Error fetching dashboard stats:", error);
        }
      },
    },
    mounted() {
      this.fetchDashboardStats();
    },
  };
  </script>
  
  <style scoped>
  .content {
    padding: 20px;
  }
  .card {
    margin: 10px;
    box-shadow: 0px 0px 15px rgba(0, 0, 0, 0.1);
    border-radius: 10px;
  }
  .card-title,
  .card-category {
    font-weight: bold;
  }
  .stats {
    color: #999;
  }
  .row {
    display: flex;
    flex-wrap: wrap; /* Agar responsif pada ukuran layar kecil */
  }
  </style>  