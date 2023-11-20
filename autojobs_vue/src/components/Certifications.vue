<template>
  <div class="tile is-child  box">
      <p class="title">Certifications</p>
      <div v-for="certification in certifications" :key="certification.id" class="card mb-4">
        <header class="card-header">
          <p class="card-header-title">
            {{certification.cert_institute}}
          </p>
          <button class="card-header-icon" aria-label="more options">
            <span class="icon">
              <i class="fas fa-angle-down" aria-hidden="true"></i>
            </span>
          </button>
        </header>
        <div class="card-content">
          <div class="content">
            {{certification.cert_name}}
            <a href="#">@bulmaio</a>. <a href="#">#css</a> <a href="#">#responsive</a>
            <br>
            <p>De <time datetime="2016-1-1">{{certification.cert_emmited_at}}</time> Até <time datetime="2016-1-1">{{certification.cert_valid_until}}</time></p>
          </div>
        </div>
        <footer class="card-footer ">
          <button class="button m-3">Edit</button>
          <button class="button is-danger m-3">Delete</button>
        </footer>
      </div>
    </div>
</template>
<!--         {
        "id": 3,
        "cert_name": "Teate",
        "cert_institute": "Teste Institute",
        "cert_emmited_at": "2023-12-31T17:00:00Z",
        "cert_valid_until": "2023-12-31T17:00:00Z",
        "cert_user": 2
    }
    } -->
<script>
import axios from 'axios';

export default {
  data() {
    return {
      certifications: [],
    };
  },
  computed: {
    userId() {
      // Assumindo que você tem um getter na sua store chamado getUserId
      return this.$store.getters.getUserId;
    },
    endpoint() {
      // Construa o endpoint com base no user_id
      return `http://127.0.0.1:8000/users/${this.userId}/certifications/`;
    },
  },
  mounted() {
    // Certifique-se de ter userId disponível antes de fazer a solicitação
    if (this.userId) {
      this.fetchCertifications();
    }
  },
  methods: {
    fetchCertifications() {
      axios.get(this.endpoint)
        .then(response => {
          this.certifications = response.data;
          //console.log(response.data);
        })
        .catch(error => {
          console.error('Erro ao obter dados da API:', error);
        });
    },
  },
};
</script>
