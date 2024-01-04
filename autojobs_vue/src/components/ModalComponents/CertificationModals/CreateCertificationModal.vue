<template>
  <div v-if="isOpen" class="popup">
    <!-- Campos de Edição -->
    <div class="popup_inner">
      <div class="modal-card">
        <header class="modal-card-head">
          <p class="modal-card-title">Create Certification New Modal</p>
          <button class="delete" aria-label="close" @click="handleClose"></button>
        </header>
        <section class="modal-card-body">
          <TextInputComponent ref="certNameInput" title="Certification Name" placeholder="Type the name/title of the certification"/>
          <TextInputComponent ref="certInstitutionNameInput" title="Institution Name" placeholder="Type the name of the Institution"/>
          <div class="field has-addons">
            <DateInputComponent class="control is-expanded" ref="certEmmission" title="Certification emmission date" />
            <DateInputComponent class="control is-expanded" ref="certExpiration" title="Certification expiration date" />
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
import TextInputComponent from '../../CommonComponents/TextInputComponent.vue';
import DateInputComponent from '../../CommonComponents/DateInputComponent.vue';

export default {
  components:{
    TextInputComponent,
    DateInputComponent
  },
  props: {
    isOpen: {
      type: Boolean,
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
      const createUrl = `${this.createEndpoint}create/`;

      // Construir o corpo da solicitação com os dados editados
      const requestBody = {
        //Add more fields as needed
        "cert_name":this.$refs.certNameInput.getValue(),
        "cert_institute":this.$refs.certInstitutionNameInput.getValue(),
        "cert_emmited_at" :this.$refs.certEmmission.getValue(),
        "cert_valid_until":this.$refs.certExpiration.getValue()
      };

      const headers = {
        Authorization: `Token ${localStorage.getItem('token')}`,
      };

      axios.post(createUrl, requestBody, { headers })
        .then(response => {
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
