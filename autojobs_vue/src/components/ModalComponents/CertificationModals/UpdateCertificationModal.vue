<template>
  <div v-if="isOpen" class="popup">
    <!-- Campos de Edição -->
    <div class="popup_inner">
      <div class="modal-card">
        <header class="modal-card-head">
          <p class="modal-card-title">Edit Certification new Modal</p>
          <button class="delete" aria-label="close" @click="handleClose"></button>
        </header>
        <section class="modal-card-body">
          <TextInputComponent ref="certNameInput" title="Certification Name" placeholder="Type the name/title of the certification" :default-value="certification.cert_name"/>
          <TextInputComponent ref="certInstitutionNameInput" title="Institution Name" placeholder="Type the name of the Institution" :default-value="certification.cert_institute"/>
          <p>Datetime emmited at</p>
          <p>Datetime Valid until</p>
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
import TextInputComponent from '../../CommonComponents/TextInputComponent.vue';

export default {
  components: {
    TextInputComponent,
  },
  props: {
    isOpen: {
      type: Boolean,
      required: true,
    },
    certification:{
      type:Object,
      required: true
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
      this.$emit("close");
    },
    sendUpdateRequest() {
      const userId = this.$store.getters.getUserId;
      const certificationId = this.certification.id;
      const updateCertificationUrl = `${this.updateUrl}${certificationId}/update`
      const requestBody = {
        //Add more fields as needed
        "cert_name":this.$refs.certNameInput.getValue(),
        "cert_institute":this.$refs.certInstitutionNameInput.getValue()
      };
      const headers = {
        Authorization: `Token ${localStorage.getItem('token')}`,
      };
      axios.put(updateCertificationUrl, requestBody, { headers })
        .then(response => {
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
