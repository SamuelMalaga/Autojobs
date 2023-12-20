<template>
  <div v-if="isOpen" class="popup">
    <!-- Campos de Edição -->
    <div class="popup_inner">
      <div class="modal-card">
        <header class="modal-card-head">
          <p class="modal-card-title">Edit Educational Experience new Modal</p>
          <button class="delete" aria-label="close" @click="handleClose"></button>
        </header>
        <section class="modal-card-body">
          <TextInputComponent ref="eduInstitutionNameInput" title="Education Institute Name" placeholder="Type the name of the Institution" :default-value="EducationalExperience.edu_institute"/>
          <TextInputComponent ref="eduDescriptionInput" title="Education Description" placeholder="Type the name/title of the education/course" :default-value="EducationalExperience.edu_description"/>
          <p>Start time</p>
          <p>End time</p>
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
    EducationalExperience:{
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
      const EducationalExperienceId = this.EducationalExperience.id;
      const updateEducationalExperienceUrl = `${this.updateUrl}${EducationalExperienceId}/update`
      const requestBody = {
        //Add more fields as needed
        "edu_description":this.$refs.eduDescriptionInput.getValue(),
        "edu_institute":this.$refs.eduInstitutionNameInput.getValue()
      };
      const headers = {
        Authorization: `Token ${localStorage.getItem('token')}`,
      };
      console.log(requestBody)
      axios.put(updateEducationalExperienceUrl, requestBody, { headers })
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
