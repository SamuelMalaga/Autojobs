<template>
  <div class="popup">
    <!-- Campos de Edição -->
    <div class="popup_inner">
      <div class="modal-card">
        <header class="modal-card-head">
          <p class="modal-card-title">Apply to {{this.TargetJob.job_title}}?</p>
          <button class="delete" aria-label="close" @click="closeCreateApplicationModal"></button>
        </header>
        <section class="modal-card-body">
          <p>Do you want to create a application to the following job?</p>
          <div class="box">
            {{this.TargetJob.job_title}} at {{ this.TargetJob.company_name }}
          </div>
        </section>
        <footer class="modal-card-foot">
          <!-- Botões de Ação -->
          <button class="button is-success" @click="handleSubmit">Apply</button>
          <button class="button" @click="closeCreateApplicationModal">Cancel</button>
        </footer>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  props: {
    TargetJob: {
      type: Object,
      required: true
    }
  },
  methods: {
    closeCreateApplicationModal() {
      this.$emit('close');
    },
    async handleSubmit() {
      try {
        const createApplicationUrl = `${this.$store.getters.getBaseURL}users/${this.$store.getters.getUserId}/applications/create/`

        console.log(this.TargetJob)

        const headers = {
          Authorization: `Token ${localStorage.getItem('token')}`,
        };
        const requestBody = {
          "appl_job_id": this.TargetJob.id,
          "appl_user": this.$store.getters.getUserId
        }

        // const response = await axios.post(createApplicationUrl, {
        //   appl_job_id: this.TargetJob.id,
        //   appl_user: this.$store.getters.getUserId
        // },{ headers });

        axios.post(createApplicationUrl, requestBody, { headers })
        .then(response => {
          console.log('Dados criados com sucesso:', response.data);
          // Emitir evento de atualização
          this.closeCreateApplicationModal();
        })
        .catch(error => {
          console.error('Erro ao atualizar dados:', error);
        });

      } catch (error) {
        console.error('Error:', error.message);
      }
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
