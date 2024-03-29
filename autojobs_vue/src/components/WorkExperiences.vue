<template>
  <div class="tile is-child  box">
      <p class="title">Work Experiences</p>
      <div v-for="experience in workExperiences" :key="experience.id" class="card mb-4">
        <header class="card-header">
          <p class="card-header-title">
            {{experience.exp_title}} at {{ experience.exp_company }}
          </p>
          <button class="card-header-icon" aria-label="more options" @click="openEditModal(experience)">
            <span class="icon" >
              <font-awesome-icon  icon="pen"  />
            </span>
          </button>
          <button class="card-header-icon" aria-label="more options">
            <span class="icon">
              <font-awesome-icon icon="trash" :style="{ color: '#ff0000' }" @click="openDeleteModal(experience)" />
            </span>
          </button>
        </header>
        <div class="card-content">
          <div class="content">
            {{experience.exp_description}}
            <br>
            <p>De <time datetime="2016-1-1">{{experience.exp_start_time}}</time> Até <time datetime="2016-1-1">{{experience.exp_end_time}}</time></p>
          </div>
        </div>
      </div>
      <button class="button is-sucess m-3" @click="openCreateModal">Add</button>
      <!-- Modal de Edição -->
      <UpdateWorkExperienceModal
        :isOpen="isEditModalOpen"
        :updateUrl="endpoint"
        :-experience="selectedExperience"
        @submit="handleEditSubmit"
        @data-updated="handleDataUpdated"
        @close="closeEditModal"
      />
      <DeleteInfoModal
        :isOpen="isDeleteModalOpen"
        :object_instance="work_experience_instance"
        :deleteEndpoint="endpoint"
        @submit="handleDeleteSubmit"
        @data-deleted="handleDataDeleted"
        @close="closeDeleteModal"
      />
      <CreateWorkExperienceModal
        :isOpen="isCreateModalOpen"
        :fields="object_fields"
        :createEndpoint="endpoint"
        @submit="handleCreateSubmit"
        @data-created="handleCreated"
        @close="closeCreateModal"
      />
    </div>
</template>

<script>
import axios from 'axios';
import ChangeInfoModal from './ChangeInfoModal.vue';
import DeleteInfoModal from './DeleteInfoModal.vue';
import CreateInfoModal from './CreateInfoModal.vue';
import CreateWorkExperienceModal from './ModalComponents/WorkExperienceModals/CreateWorkExperienceModal.vue';
import UpdateWorkExperienceModal from './ModalComponents/WorkExperienceModals/UpdateWorkExperienceModal.vue';

export default {
  components: {
    ChangeInfoModal,
    DeleteInfoModal,
    //CreateInfoModal,
    CreateWorkExperienceModal,
    UpdateWorkExperienceModal
  },
  data() {
    return {
      workExperiences: [],
      isEditModalOpen: false,
      isDeleteModalOpen: false,
      isCreateModalOpen: false,
      object_fields: [
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
      ],
      work_experience_instance:{},
      selectedExperience:null
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
    //<--------------------------------Get Data---------------------------------------->
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
    handleDataUpdated() {
      // Lógica para atualizar os dados no componente pai
      this.fetchWorkExperiences();
    },
    //<--------------------------------Edit Data---------------------------------------->
    openEditModal(experience) {
      this.selectedExperience = experience
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
    openDeleteModal(experience){
      //Deep copy of the fields to edit
      const object_fieldsCopy = this.object_fields

      // Atualize a cópia com os valores da experiência selecionada
      object_fieldsCopy.forEach(campo => {
        campo.field_value = experience[campo.field_name];
      });

      // Atualize os dados no objeto
      this.work_experience_instance = {
        instance_entity:"Experience",
        object_id: experience.id,
        fields: object_fieldsCopy,
      };
      this.selectedCertification = { ...experience }
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
      this.fetchWorkExperiences();
    },
    //<--------------------------------Create Data---------------------------------------->
    openCreateModal() {
      const object_fieldsCopy = this.object_fields.map(campo => ({
          ...campo,
          field_value: "", // ou qualquer valor padrão desejado
        }));

      this.work_experience_instance = {
        instance_entity: "Certification",
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
      //console.log("Dados Criados:");
      // Feche o modal
      this.closeCreateModal();
    },
    handleCreated(){
      // Lógica para atualizar os dados no componente pai
      this.fetchWorkExperiences();
    },
  },
};
</script>
