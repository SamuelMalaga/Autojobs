<template>
  <div class="tile is-child  box">
      <p class="title">Education</p>
      <div v-for="education in educationExperiences" :key="education.id" class="card mb-4">
        <header class="card-header">
          <p class="card-header-title">
            {{education.edu_institute}}
          </p>
          <button class="card-header-icon" aria-label="more options" @click="openEditModal(education)">
            <span class="icon" >
              <font-awesome-icon  icon="pen"  />
            </span>
          </button>
          <button class="card-header-icon" aria-label="more options">
            <span class="icon">
              <font-awesome-icon icon="trash" :style="{ color: '#ff0000' }" @click="openDeleteModal(education)" />
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
      </div>
      <button class="button is-sucess m-3" @click="openCreateModal">Add</button>
      <ChangeInfoModal
        :isOpen="isEditModalOpen"
        :object_instance="education_experience_instance"
        :updateUrl="endpoint"
        @submit="handleEditSubmit"
        @data-updated="handleDataUpdated"
        @close="closeEditModal"
      />
      <DeleteInfoModal
        :isOpen="isDeleteModalOpen"
        :object_instance="education_experience_instance"
        :deleteEndpoint="endpoint"
        @submit="handleDeleteSubmit"
        @data-deleted="handleDataDeleted"
        @close="closeDeleteModal"
      />
      <CreateInfoModal
        :isOpen="isCreateModalOpen"
        :fields="object_fields"
        :createEndpoint="endpoint"
        @submit="handleCreateSubmit"
        @data-created="handleCreated"
        @close="closeCreateModal"
        :object_instance="object_instance"
      />
    </div>
</template>

<script>

import axios from 'axios';
import ChangeInfoModal from './ChangeInfoModal.vue';
import DeleteInfoModal from './DeleteInfoModal.vue';
import CreateInfoModal from './CreateInfoModal.vue';

export default {
  components: {
    ChangeInfoModal,
    DeleteInfoModal,
    CreateInfoModal
  },
  data() {
    return {
      educationExperiences: [],
      isEditModalOpen: false,
      isDeleteModalOpen: false,
      isCreateModalOpen:false,
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
    //<--------------------------------Get Data---------------------------------------->
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
    handleDataUpdated() {
      // Lógica para atualizar os dados no componente pai
      this.fetchEducationExperiences();
    },
    //<--------------------------------Edit Data---------------------------------------->
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
    //<--------------------------------Delete Data---------------------------------------->
    openDeleteModal(education){
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
      this.isDeleteModalOpen = true;

    },
    closeDeleteModal() {
      this.isDeleteModalOpen = false;
    },
    handleDeleteSubmit(dadosEditados) {
      // Lógica para enviar dados editados ao backend
      console.log("Dados Deletados:", deletedData);
      // Feche o modal
      this.closeEditModal();
    },
    handleDataDeleted(){
      // Lógica para atualizar os dados no componente pai
      this.fetchEducationExperiences();
    },
    //<--------------------------------Create Data---------------------------------------->
    openCreateModal() {
      const object_fieldsCopy = this.object_fields.map(campo => ({
          ...campo,
          field_value: "", // ou qualquer valor padrão desejado
        }));

      this.object_instance = {
        instance_entity: "Education",
        object_id: null, // ou qualquer valor padrão desejado
        fields: object_fieldsCopy,
      };

      this.isCreateModalOpen = true;
    },
    closeCreateModal() {
      this.isCreateModalOpen = false;
    },
    handleCreateSubmit(dadosEditados) {
      // Lógica para enviar dados editados ao backend
      console.log("Dados Criados:");
      // Feche o modal
      this.closeCreateModal();
    },
    handleCreated(){
      // Lógica para atualizar os dados no componente pai
      this.fetchEducationExperiences();
    },
  },
};
</script>
