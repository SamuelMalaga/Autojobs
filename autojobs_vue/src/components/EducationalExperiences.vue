<template>
  <div class="tile is-child  box">
      <p class="title">Education</p>
      <div v-for="education in educationExperiences" :key="education.id" class="card mb-4">
        <header class="card-header">
          <p class="card-header-title">
            {{education.edu_institute}}
          </p>
          <button class="card-header-icon" aria-label="more options">
            <span class="icon">
              <i class="fas fa-angle-down" aria-hidden="true"></i>
            </span>
          </button>
        </header>
        <div class="card-content">
          <div class="content">
            {{education.edu_description}}
            <a href="#">@bulmaio</a>. <a href="#">#css</a> <a href="#">#responsive</a>
            <br>
            <p>De <time datetime="2016-1-1">{{education.edu_start_time}}</time> Até <time datetime="2016-1-1">{{edu_end_time}}</time></p>
          </div>
        </div>
        <footer class="card-footer ">
          <button class="button m-3">Edit</button>
          <button class="button is-danger m-3">Delete</button>
        </footer>
      </div>
    </div>
</template>
<!--     {
        "id": 4,
        "edu_institute": "teste Outro",
        "edu_description": "Teste 12312312",
        "edu_start_time": "2023-12-31T17:00:00Z",
        "edu_end_time": "2023-12-31T17:00:00Z",
        "edu_user": 2
    } -->
<script>
import axios from 'axios';

export default {
  data() {
    return {
      educationExperiences: [],
    };
  },
  computed: {
    userId() {
      // Assumindo que você tem um getter na sua store chamado getUserId
      return this.$store.getters.getUserId;
    },
    endpoint() {
      // Construa o endpoint com base no user_id
      return `http://127.0.0.1:8000/users/${this.userId}/educations/`;
    },
  },
  mounted() {
    // Certifique-se de ter userId disponível antes de fazer a solicitação
    if (this.userId) {
      this.fetchEducationExperiences();
    }
  },
  methods: {
    fetchEducationExperiences() {
      axios.get(this.endpoint)
        .then(response => {
          this.educationExperiences = response.data;
          //console.log(response.data);
        })
        .catch(error => {
          console.error('Erro ao obter dados da API:', error);
        });
    },
  },
};
</script>
