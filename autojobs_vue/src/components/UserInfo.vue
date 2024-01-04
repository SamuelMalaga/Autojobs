<template>
  <div class="card">
  <header class="card-header">
    <p class="card-header-title">
      Personal Information
    </p>
    <button class="card-header-icon" aria-label="more options" @click="openEditModal(this.user)">
      <span class="icon" >
            <font-awesome-icon  icon="pen"  />
        </span>
    </button>
  </header>
  <div class="card-content">
    <div class="content">
      <div v-if="user">
        <p><strong>Name:</strong> {{ user.firstName }}</p>
        <p><strong>Sobrenome:</strong> {{ user.lastName }}</p>
        <p><strong>Email:</strong> {{ user.email }}</p>
        <p><strong>Cidade:</strong> {{ user.city }}, {{ user.country }}</p>
        <p><strong>Bio:</strong> {{ user.bio }}</p>
      </div>
      <div v-else>
        <p>No user information available.</p>
      </div>
    </div>
  </div>
  </div>
  <ChangeUserInfoModal
        :isOpen="isEditModalOpen"
        :-user-info="this.user"
        :updateUrl="endpoint"
        @submit="handleEditSubmit"
        @data-updated="handleDataUpdated"
        @close="closeEditModal"
      />
  <!-- <ChangeInfoModal
  :isOpen="isEditModalOpen"
  :object_instance="object_instance"
  :updateUrl="endpoint"
  @submit="handleEditSubmit"
  @data-updated="handleDataUpdated"
  @close="closeEditModal"
  /> -->
</template>
<script>
import axios from 'axios';
import ChangeInfoModal from './ChangeInfoModal.vue';
import ChangeUserInfoModal from './ModalComponents/UserInfoModals/ChangeUserInfoModal.vue';

export default {
  components: {
    ChangeInfoModal,
    ChangeUserInfoModal
  },
  data() {
    return {
      certifications: [],
      isEditModalOpen: false,
      object_fields: [
        {
        field_name:"bio",
        field_title: "Cidade",
        field_type: "text",
        field_value: ""
        },
        {
        field_name: "country",
        field_title:"País do usuário",
        field_type: "text",
        field_value: ""
        },
        {
        field_name:"city",
        field_title: "Bio",
        field_type: "text",
        field_value: ""
        }
      ],
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
      return `http://127.0.0.1:8000/users/${this.userId}/myProfile`;
    },
    token() {
      // Obtenha o token do Local Storage
      return localStorage.getItem('token');
    },
    user() {
      return this.$store.getters.getFullUserInfo;
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
    openEditModal(user) {
        // Abra o modal de edição
        this.isEditModalOpen = true;
    },
    closeEditModal() {
      this.isEditModalOpen = false;
    },
    handleEditSubmit(dadosEditados) {
      // Feche o modal
      this.closeEditModal();
    }
  },
};
</script>

