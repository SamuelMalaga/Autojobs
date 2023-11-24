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
          <button class="button m-3" @click="openEditModal(language)">Edit</button>
          <button class="button is-danger m-3">Delete</button>
        </footer>
      </div>
      <ChangeInfoModal
        :isOpen="isEditModalOpen"
        :object_instance="languages_instance"
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
      languages: [],
      isEditModalOpen: false,
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
      languages_instance:{}
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
    openEditModal(language) {
      //Deep copy of the fields to edit
      const object_fieldsCopy = this.object_fields

      // Atualize a cópia com os valores da experiência selecionada
      object_fieldsCopy.forEach(campo => {
        campo.field_value = language[campo.field_name];
      });

      // Atualize os dados no objeto
      this.languages_instance = {
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
    handleDataUpdated() {
      // Lógica para atualizar os dados no componente pai
      this.fetchLanguages();
    },
  },
};
</script>
