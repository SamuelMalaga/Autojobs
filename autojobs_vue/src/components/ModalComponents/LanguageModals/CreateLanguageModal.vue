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
          <TextInputComponent ref="lngName" title="Language Name" placeholder="Type the name of the Institution"/>
          <TextInputComponent ref="lngCountry" title="Language Country Name" placeholder="Type the name/title of the education/course" />
          <DropdownInputComponent ref="lngProficiencyLevel" title="Language Proficiency Level" :options="languageProficiencyOptions" />
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
import DropdownInputComponent from '../../CommonComponents/DropdownInputComponent.vue';
export default {
  components:{
    TextInputComponent,
    DropdownInputComponent
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
      languageProficiencyOptions:[
      { field_name: "Basic", field_value: "A1" },
      { field_name: "Intermediate", field_value: "B1" },
      { field_name: "Advanced", field_value: "C1" },
    ]
    };
  },
  methods: {
    handleSubmit() {
      this.sendCreateRequest();
      this.$emit("submit", this.dadosEditados);
    },
    handleClose() {
      this.$emit("close");
    },
    sendCreateRequest() {
      const createUrl = `${this.createEndpoint}create/`;
      const requestBody = {
        "edu_description":this.$refs.eduDescriptionInput.getValue(),
        "edu_institute":this.$refs.eduInstitutionNameInput.getValue()
      };
      const headers = {
        Authorization: `Token ${localStorage.getItem('token')}`,
      };

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
