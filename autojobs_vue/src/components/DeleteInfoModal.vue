<template>
  <div v-if="isOpen" class="popup">
    <!-- Campos de Edição -->
    <div class="popup_inner">
      <div class="modal-card">
        <header class="modal-card-head">
          <p class="modal-card-title">Delete {{ object_instance.instance_entity }}</p>
          <button class="delete" aria-label="close" @click="handleClose"></button>
        </header>
        <section class="modal-card-body">
          <h2 class="subtitle">Tem certeza que deseja apagar o seguinte item? </h2>
          <fieldset disabled>
          <div v-for="field in object_instance.fields" :key="field.field_name" :disabled="isDisabled">
            <h2 class="subtitle">{{ field.field_title }} | {{ field.field_type }}</h2>
            <input v-model="field.field_value" class="input is-normal mb-4" type="text" placeholder="Normal input">
          </div>
        </fieldset>
        </section>
        <footer class="modal-card-foot">
          <!-- Botões de Ação -->
          <button class="button is-danger" @click="handleDelete">Delete</button>
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
    object_instance:{
      type: Object,
      required: true,
    },
    deleteEndpoint: {
      type: String,
      required: true,
    },
    isDisabled: {
      type: Boolean,
      required: false,
    }
  },
  data() {
    return {
      deletedData: {},
    };
  },
  methods: {
    handleDelete() {
      // Chame o método para enviar a solicitação de atualização
      this.sendDeleteRequest();
      // Emitir evento para o componente pai com os dados deletados
      this.$emit("delete", this.dadosEditados);

    },
    handleClose() {
      // Emitir evento de fechamento
      this.$emit("close");
    },
    sendDeleteRequest() {
      // Extrair informações necessárias da instância do objeto
      const userId = this.$store.getters.getUserId;
      const objectId = this.object_instance.object_id;

      // Construir o URL de atualização usando a propriedade fornecida pelo pai
      const deleteUrl = `${this.deleteEndpoint}${objectId}/delete`;



      // Adicionar cabeçalhos, se necessário (por exemplo, token de autorização)
      const headers = {
        Authorization: `Token ${localStorage.getItem('token')}`,
      };


      // Enviar solicitação PUT para atualizar os dados
      axios.delete(deleteUrl,{ headers })
        .then(response => {
          console.log('Dados excluídos com sucesso:', response.data);
          this.handleClose()
          // Emitir evento de atualização
          this.$emit("data-deleted");
        })
        .catch(error => {
          console.error('Erro ao excluir dados:', error);
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
