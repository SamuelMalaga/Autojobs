<template>
  <div class="is-child  box">
      <p class="title">Languages</p>
      <div v-for="language in languages" :key="language.id" class="card mb-4">
        <header class="card-header">
          <p class="card-header-title">
            {{language.lng_name}}
          </p>
          <button class="card-header-icon" aria-label="more options" @click="openEditModal(language)">
            <span class="icon" >
              <font-awesome-icon  icon="pen"  />
            </span>
          </button>
          <button class="card-header-icon" aria-label="more options">
            <span class="icon">
              <font-awesome-icon icon="trash" :style="{ color: '#ff0000' }" @click="openDeleteModal(language, 'Language')" />
            </span>
          </button>
        </header>
      </div>
      <button class="button is-sucess m-3" @click="openCreateModal()">Add</button>
      <ChangeInfoModal
        :isOpen="isEditModalOpen"
        :object_instance="object_instance"
        :updateUrl="endpoint"
        @submit="handleEditSubmit"
        @data-updated="handleDataUpdated"
        @close="closeEditModal"
      />
      <DeleteInfoModal
        :isOpen="isDeleteModalOpen"
        :object_instance="object_instance"
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
    CreateInfoModal,
  },
  data() {
    return {
      languages: [],
      isEditModalOpen: false,
      isCreateModalOpen: false,
      isDeleteModalOpen: false,
      object_fields: [
        {
        field_name:"lng_name",
        field_title: "Nome da linguagem",
        field_type: "dropdown",
        field_value: ""
        },
        {
        field_name:"lng_country",
        field_title: "País da linguagem",
        field_type: "text",
        field_value: ""
        },
        {
        field_name:"lng_proficiency_level",
        field_title: "Nível de proficiencia",
        field_type: "date",
        field_value: ""
        }
      ],
      //languages_instance:{}
      object_instance:{}
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
    //<--------------------------------Get Data---------------------------------------->
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
    handleDataUpdated() {
      // Lógica para atualizar os dados no componente pai
      this.fetchLanguages();
    },
    //<--------------------------------Edit Data---------------------------------------->
    openEditModal(language) {
        //Deep copy of the fields to edit
        const object_fieldsCopy = this.object_fields

        // Atualize a cópia com os valores da experiência selecionada
        object_fieldsCopy.forEach(campo => {
          campo.field_value = language[campo.field_name];
        });

        // Atualize os dados no objeto
        this.object_instance = {
          instance_entity:"Language",
          object_id: language.id,
          fields: object_fieldsCopy,
        };
        this.selectedLanguage = { ...language }
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
    openDeleteModal(item, instanceEntity) {
      const object_fieldsCopy = this.object_fields.map(campo => ({
        ...campo,
        field_value: item[campo.field_name],
      }));

      this.delete_instance = {
        instance_entity: instanceEntity,
        object_id: item.id,
        fields: object_fieldsCopy,
      };

      this.selectedDeleteItem = { ...item };
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
      this.fetchLanguages();
    },
    //<--------------------------------Create Data---------------------------------------->
    openCreateModal() {
      const object_fieldsCopy = this.object_fields.map(campo => ({
          ...campo,
          field_value: "", // ou qualquer valor padrão desejado
        }));

      this.object_instance = {
        instance_entity: "Language",
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
      this.fetchLanguages();
    },
  },
};
</script>
