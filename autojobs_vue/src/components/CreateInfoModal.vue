<template>
  <div v-if="isOpen" class="popup">
    <!-- Campos de Edição -->
    <div class="popup_inner">
      <div class="modal-card">
        <header class="modal-card-head">
          <p class="modal-card-title">Create {{ object_instance.instance_entity }}</p>
          <button class="delete" aria-label="close" @click="handleClose"></button>
        </header>
        <section class="modal-card-body">
          <div v-for="field in object_instance.fields" :key="field.field_name">
            <h2 class="subtitle">{{ field.field_title }} | {{ field.field_type }}</h2>
            <input v-model="field.field_value" class="input is-normal mb-4" type="text" placeholder="Normal input">
          </div>
        </section>
        <footer class="modal-card-foot">
          <!-- Botões de Ação -->
          <button class="button is-success" @click="handleSubmit">Create</button>
          <button class="button" @click="handleClose">Cancel</button>
        </footer>
      </div>
    </div>
  </div>
</template>

<script>

import axios from 'axios';

export default {
  props: {
    isOpen: {
      type: Boolean,
      required: true,
    },
    fields: {
      type: Array,
      required: false,
    },
    object_instance:{
      type: Object,
      required: true,
    },
    createEndpoint: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      dadosEditados: {},
    };
  },
  methods: {
    handleSubmit() {
      // Chame o método para enviar a solicitação de atualização
      this.sendCreateRequest();
      // Emitir evento para o componente pai com os dados editados
      this.$emit("submit", this.dadosEditados);

    },
    handleClose() {
      // Emitir evento de fechamento
      this.$emit("close");
    },
    sendCreateRequest() {
      // Extrair informações necessárias da instância do objeto
      // const userId = this.$store.getters.getUserId;
      // const objectId = this.object_instance.object_id;

      // Construir o URL de atualização usando a propriedade fornecida pelo pai
      const createUrl = `${this.createEndpoint}create/`;

      // Construir o corpo da solicitação com os dados editados
      const requestBody = {};
      this.object_instance.fields.forEach(field => {
        requestBody[field.field_name] = field.field_value;
      });

      // Adicionar cabeçalhos, se necessário (por exemplo, token de autorização)
      const headers = {
        Authorization: `Token ${localStorage.getItem('token')}`,
      };

      // Enviar solicitação PUT para atualizar os dados
      axios.post(createUrl, requestBody, { headers })
        .then(response => {
          console.log('Dados criados com sucesso:', response.data);
          // Emitir evento de atualização
          this.$emit("data-created");
        })
        .catch(error => {
          console.error('Erro ao atualizar dados:', error);
        });
    },

  },
};
</script>

<style lang="scss" scoped>
.popup{
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 99;
  background-color: rgba(0,0,0,0.2);
  display: flex;
  align-items: center;
  justify-content: center;

}
</style>
