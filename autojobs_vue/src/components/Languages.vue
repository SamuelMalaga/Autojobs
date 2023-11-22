<template>
  <div class="tile is-child  box">
      <p class="title">Languages</p>
      <div v-for="language in languages" :key="language.id" class="card mb-4">
        <header class="card-header">
          <p class="card-header-title">
            {{language.lng_name}}
          </p>
          <button class="card-header-icon" aria-label="more options">
            <span class="icon">
              <i class="fas fa-angle-down" aria-hidden="true"></i>
            </span>
          </button>
        </header>
        <footer class="card-footer ">
          <button class="button m-3">Edit</button>
          <button class="button is-danger m-3">Delete</button>
        </footer>
      </div>
    </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      languages: [],
    };
  },
  computed: {
    userId() {
      // Assumindo que você tem um getter na sua store chamado getUserId
      return this.$store.getters.getUserId;
    },
    endpoint() {
      // Construa o endpoint com base no user_id
      return `http://127.0.0.1:8000/users/${this.userId}/languages/`;
    },
    token() {
      // Obtenha o token do Local Storage
      return localStorage.getItem('token');
    },
  },
  mounted() {
    // Certifique-se de ter userId disponível antes de fazer a solicitação
    if (this.userId) {
      this.fetchLanguages();
    }
  },
  methods: {
    fetchLanguages() {

      const headers = { Authorization: `Token ${this.token}` };

      axios.get(this.endpoint, { headers })
        .then(response => {
          this.languages = response.data;
          //console.log(response.data);
        })
        .catch(error => {
          console.error('Erro ao obter dados da API:', error);
        });
    },
  },
};
</script>
