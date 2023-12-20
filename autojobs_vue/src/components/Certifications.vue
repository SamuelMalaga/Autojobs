<template>
  <div class="tile is-child  box">
      <p class="title">Certifications update</p>
      <div v-for="certification in certifications" :key="certification.id" class="card mb-4">
        <header class="card-header">
          <p class="card-header-title">
            {{certification.cert_institute}}
          </p>
          <button class="card-header-icon" aria-label="more options" @click="openEditModal(certification)">
            <span class="icon" >
              <font-awesome-icon  icon="pen"  />
            </span>
          </button>
          <button class="card-header-icon" aria-label="more options">
            <span class="icon">
              <font-awesome-icon icon="trash" :style="{ color: '#ff0000' }" @click="openDeleteModal(certification)" />
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
      </div>
      <button class="button is-sucess m-3" @click="openCreateModal">Add</button>
      <UpdateCertificationModal
        :isOpen="isEditModalOpen"
        :certification="this.selectedCertification"
        :updateUrl="endpoint"
        @submit="handleEditSubmit"
        @data-updated="handleDataUpdated"
        @close="closeEditModal"
      />
      <DeleteInfoModal
        :isOpen="isDeleteModalOpen"
        :object_instance="certification_instance"
        :deleteEndpoint="endpoint"
        @submit="handleDeleteSubmit"
        @data-deleted="handleDataDeleted"
        @close="closeDeleteModal"
      />
      <CreateCertificationModal
        :isOpen="isCreateModalOpen"
        :createEndpoint="endpoint"
        @submit="handleCreateSubmit"
        @data-created="handleCreated"
        @close="closeCreateModal"
      />
    </div>
</template>
<script>
import axios from 'axios';
import CreateCertificationModal from './ModalComponents/CertificationModals/CreateCertificationModal.vue';
import UpdateCertificationModal from './ModalComponents/CertificationModals/UpdateCertificationModal.vue';
import DeleteInfoModal from './DeleteInfoModal.vue';
// import ChangeInfoModal from './ChangeInfoModal.vue';
// import CreateInfoModal from './CreateInfoModal.vue';

export default {
  components: {
    // ChangeInfoModal,
    DeleteInfoModal,
    // CreateInfoModal,
    CreateCertificationModal,
    UpdateCertificationModal
  },
  data() {
    return {
      certifications: [],
      isEditModalOpen: false,
      isDeleteModalOpen:false,
      isCreateModalOpen:false,
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
      selectedCertification:null,
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
    //<--------------------------------Get Data---------------------------------------->
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
    handleDataUpdated() {
      // Lógica para atualizar os dados no componente pai
      this.fetchCertifications();
    },
    //<--------------------------------Edit Data---------------------------------------->
    openEditModal(certification) {
      //Deep copy of the fields to edit
      const object_fieldsCopy = this.object_fields

      // Atualize a cópia com os valores da experiência selecionada
      object_fieldsCopy.forEach(campo => {
        campo.field_value = certification[campo.field_name];
      });

      // Atualize os dados no objeto
      this.certification_instance = {
        instance_entity:"Certification",
        object_id: certification.id,
        fields: object_fieldsCopy,
      };
      this.selectedCertification = certification
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
    openDeleteModal(certification){
      //Deep copy of the fields to edit
      const object_fieldsCopy = this.object_fields

      // Atualize a cópia com os valores da experiência selecionada
      object_fieldsCopy.forEach(campo => {
        campo.field_value = certification[campo.field_name];
      });

      // Atualize os dados no objeto
      this.certification_instance = {
        instance_entity:"Certification",
        object_id: certification.id,
        fields: object_fieldsCopy,
      };
      this.selectedCertification = { ...certification }
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
      this.fetchCertifications();
    },
    //<--------------------------------Create Data---------------------------------------->
    openCreateModal() {
      const object_fieldsCopy = this.object_fields.map(campo => ({
          ...campo,
          field_value: "", // ou qualquer valor padrão desejado
        }));

      this.certification_instance = {
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
      this.fetchCertifications();
    },
  },
};
</script>
