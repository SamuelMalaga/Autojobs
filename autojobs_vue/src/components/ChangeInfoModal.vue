<template>
  <div v-if="isOpen" class="popup">
    <!-- Campos de Edição -->
    <div class="popup_inner">
      <div class="modal-card">
        <header class="modal-card-head">
          <p class="modal-card-title">Edit {{ object_instance.instance_entity }}</p>
          <button class="delete" aria-label="close" @click="handleClose"></button>
        </header>
        <section class="modal-card-body">
          <!-- <h2 class="subtitle">ID Obj: {{ object_instance.object_id }}</h2> -->
          <div v-for="field in object_instance.fields" :key="field.field_name">
            <h2 class="subtitle">{{ field.field_title }} | {{ field.field_type }}</h2>
            <input v-model="field.field_value" class="input is-normal mb-4" type="text" placeholder="Normal input">
          </div>
        </section>
        <footer class="modal-card-foot">
          <!-- Botões de Ação -->
          <button class="button is-success" @click="handleSubmit">Save changes</button>
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
    isUser: {
      type: Boolean,
      required: false,
    },
    fields: {
      type: Array,
      required: false,
    },
    object_instance:{
      type: Object,
      required: true,
    },
    updateUrl: {
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
      this.sendUpdateRequest();
      // Emitir evento para o componente pai com os dados editados
      this.$emit("submit", this.dadosEditados);

    },
    handleClose() {
      // Emitir evento de fechamento
      this.$emit("close");
    },
    sendUpdateRequest() {
      // Extrair informações necessárias da instância do objeto
      const userId = this.$store.getters.getUserId;
      const objectId = this.object_instance.object_id;

      let updateUrl =''


      if(this.object_instance.instance_entity==='User'){
        updateUrl = `${this.updateUrl}/update`
        console.log('é tipo user')
        console.log(updateUrl)
      } else {
        // Construir o URL de atualização usando a propriedade fornecida pelo pai
        console.log('não é tipo user')
        updateUrl = `${this.updateUrl}${objectId}/update`;
        console.log(updateUrl)
      }

      //console.log(this.object_instance.instance_entity)

      //const testUrl = updateUrl

      console.log('testUrl')
      //console.log(testUrl)

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
      axios.put(updateUrl, requestBody, { headers })
        .then(response => {
          // console.log('Dados atualizados com sucesso:', response.data);
          // Emitir evento de atualização
          if(this.object_instance.instance_entity==='User'){
            console.log(requestBody)
            this.$store.dispatch('updatePartialUserInfo',
            { bio: requestBody.bio,
              country: requestBody.country,
              city: requestBody.city,
            });
          }
          this.$emit("data-updated");
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
