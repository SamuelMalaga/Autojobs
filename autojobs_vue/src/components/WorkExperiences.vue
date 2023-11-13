<template>
  <div class="tile is-child  box">
      <p class="title">Work Experiences</p>
      <div v-for="experience in workExperiences" :key="experience.id" class="card mb-4">
        <header class="card-header">
          <p class="card-header-title">
            {{experience.exp_company}}
          </p>
          <button class="card-header-icon" aria-label="more options">
            <span class="icon">
              <i class="fas fa-angle-down" aria-hidden="true"></i>
            </span>
          </button>
        </header>
        <div class="card-content">
          <div class="content">
            {{experience.exp_description}}
            <a href="#">@bulmaio</a>. <a href="#">#css</a> <a href="#">#responsive</a>
            <br>
            <p>De <time datetime="2016-1-1">{{experience.exp_start_time}}</time> Até <time datetime="2016-1-1">{{exp_end_time}}</time></p>
          </div>
        </div>
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
      workExperiences: [],
    };
  },
  mounted() {
    axios.get('http://127.0.0.1:8000/work_experiences/')
      .then(response => {
        this.workExperiences = response.data;
      })
      .catch(error => {
        console.error('Erro ao obter dados da API:', error);
      });
  },
};
</script>
