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
          <button class="button m-3" @click="openEditModal(certification)">Edit</button>
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
      certifications: [],
      isEditModalOpen: false,
      object_fields: [
        {
        field_name:"cert_name",
        field_title: "Nome do certificado",
        field_type: "dropdown",
        field_value: ""
        },
        {
        field_name:"cert_institute",
        field_title: "Instituto/empresa de emissão do certificado",
        field_type: "text",
        field_value: ""
        },
        {
        field_name:"cert_emmited_at",
        field_title: "Emitido em",
        field_type: "date",
        field_value: ""
        },
        {
        field_name:"cert_valid_until",
        field_title: "Válido até",
        field_type: "date",
        field_value: ""
        }
      ],
      certification_instance:{}
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
    token() {
      // Obtenha o token do Local Storage
      return localStorage.getItem('token');
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

      const headers = { Authorization: `Token ${this.token}` };
      axios.get(this.endpoint, { headers })
        .then(response => {
          this.certifications = response.data;
          //console.log(response.data);
        })
        .catch(error => {
          console.error('Erro ao obter dados da API:', error);
        });
    },
    openEditModal(certification) {
      //Deep copy of the fields to edit
      const object_fieldsCopy = this.object_fields

      // Atualize a cópia com os valores da experiência selecionada
      object_fieldsCopy.forEach(campo => {
        campo.field_value = certification[campo.field_name];
      });

      // Atualize os dados no objeto
      this.languages_instance = {
        instance_entity:"Language",
        object_id: certification.id,
        fields: object_fieldsCopy,
      };
      this.selectedCertification = { ...certification }
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
      this.fetchCertifications();
    },
  },
};
</script>
