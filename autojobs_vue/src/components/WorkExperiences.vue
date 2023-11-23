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
            <br>
            <p>De <time datetime="2016-1-1">{{experience.exp_start_time}}</time> Até <time datetime="2016-1-1">{{exp_end_time}}</time></p>
          </div>
        </div>
        <footer class="card-footer ">
          <button class="button m-3" @click="openEditModal(experience)">Edit</button>
          <button class="button is-danger m-3">Delete</button>
        </footer>
      </div>
      <!-- Modal de Edição -->
      <ChangeInfoModal
        :isOpen="isEditModalOpen"
        :object_instance="object_instance_test"
        :dataToIterate="selectedWorkExperience"
        @submit="handleEditSubmit"
        @close="closeEditModal"
      />
    </div>
</template>

<script>
import axios from 'axios';
//import EditInfo from './EditInfo.vue';
import ChangeInfoModal from './ChangeInfoModal.vue';
//import { ref } from 'vue';

export default {
  components: {
    ChangeInfoModal
  },
  data() {
    return {
      workExperiences: [],
      isEditModalOpen: false,
      object_fields: {
        object_id:0,
        fields: [
            {
            field_name:"exp_type",
            field_title: "Tipo de Experiência",
            field_type: "dropdown",
            field_value: ""
            },
            {
            field_name:"exp_company",
            field_title: "Título da experiência/cargo",
            field_type: "text",
            field_value: ""
            },
            {
            field_name:"exp_description",
            field_title: "Descrição da experiência",
            field_type: "long_text",
            field_value: ""
            },
            {
            field_name:"exp_start_time",
            field_title: "Data de início",
            field_type: "date",
            field_value: ""
            },
            {
            field_name:"exp_end_time",
            field_title: "Data de fim",
            field_type: "date",
            field_value: ""
            }
          ]
      },
      selectedWorkExperience: {},
      object_instance_test:{}
    };
  },
  computed: {
    userId() {
      // Assumindo que você tem um getter na sua store chamado getUserId
      return this.$store.getters.getUserId;
    },
    endpoint() {
      // Construa o endpoint com base no user_id
      return `http://127.0.0.1:8000/users/${this.userId}/work_experiences/`;
    },
    token() {
      // Obtenha o token do Local Storage
      return localStorage.getItem('token');
    },
  },
  mounted() {
    // Certifique-se de ter userId disponível antes de fazer a solicitação
    if (this.userId) {
      this.fetchWorkExperiences();
    }
  },
  methods: {
    openEditModal(experience) {

      //Deep copy of the fields to edit
      const object_fieldsCopy = JSON.parse(JSON.stringify(this.object_fields));

      // Atualize a cópia com os valores da experiência selecionada
      object_fieldsCopy.fields.forEach(campo => {
        campo.field_value = experience[campo.field_name];
      });

      // Atualize os dados no objeto
      this.object_instance_test = {
        object_id: experience.id,
        fields: object_fieldsCopy.fields,
      };
      this.selectedWorkExperience = { ...experience }
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
    fetchWorkExperiences() {
      // Adicione o token ao cabeçalho da solicitação
      const headers = { Authorization: `Token ${this.token}` };

      // Faça a solicitação HTTP com o token no cabeçalho
      axios.get(this.endpoint, { headers })
        .then(response => {
          this.workExperiences = response.data;
        })
        .catch(error => {
          console.error('Erro ao obter dados da API:', error);
        });
    },
  },
};
</script>
