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
            <p>De <time datetime="2016-1-1">{{education.edu_start_time}}</time> Até <time datetime="2016-1-1">{{education.edu_end_time}}</time></p>
          </div>
        </div>
        <footer class="card-footer ">
          <button class="button m-3" @click="openEditModal(education)">Edit</button>
          <button class="button is-danger m-3">Delete</button>
        </footer>
      </div>
      <ChangeInfoModal
        :isOpen="isEditModalOpen"
        :object_instance="education_experience_instance"
        :updateUrl="endpoint"
        @submit="handleEditSubmit"
        @data-updated="handleDataUpdated"
        @close="closeEditModal"
      />
    </div>
</template>

<script>

import axios from 'axios';
import ChangeInfoModal from './ChangeInfoModal.vue';
export default {
  components: {
    ChangeInfoModal
  },
  data() {
    return {
      educationExperiences: [],
      isEditModalOpen: false,
      object_fields: [
        {
        field_name:"edu_institute",
        field_title: "Instituto",
        field_type: "dropdown",
        field_value: ""
        },
        {
        field_name:"edu_description",
        field_title: "Descrição da formação",
        field_type: "text",
        field_value: ""
        },
        {
        field_name:"edu_start_time",
        field_title: "Data de início",
        field_type: "date",
        field_value: ""
        },
        {
        field_name:"edu_end_time",
        field_title: "Data de fim",
        field_type: "date",
        field_value: ""
        }
      ],
      education_experience_instance:{}
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
    token() {
      // Obtenha o token do Local Storage
      return localStorage.getItem('token');
    },
  },
  mounted() {
    // Certifique-se de ter userId disponível antes de fazer a solicitação
    if (this.userId) {
      this.fetchEducationExperiences();
    }
  },
  methods: {
    openEditModal(education) {

     //Deep copy of the fields to edit
      const object_fieldsCopy = this.object_fields

      // Atualize a cópia com os valores da experiência selecionada
      object_fieldsCopy.forEach(campo => {
        campo.field_value = education[campo.field_name];
      });

      // Atualize os dados no objeto
      this.education_experience_instance = {
        instance_entity:"Education",
        object_id: education.id,
        fields: object_fieldsCopy,
      };
      this.selectedEducation = { ...education }
      this.isEditModalOpen = true;
    },
    closeEditModal() {
      this.isEditModalOpen = false;
    },
    handleEditSubmit(dadosEditados) {
      // Lógica para enviar dados editados ao backend
      console.log("Dados Editados:", dadosEditados);
      // Feche o modal
      this.closeEditModal();
    },
    handleDataUpdated() {
      // Lógica para atualizar os dados no componente pai
      this.fetchEducationExperiences();
    },
    fetchEducationExperiences() {

      const headers = { Authorization: `Token ${this.token}` };
      axios.get(this.endpoint, { headers })
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
