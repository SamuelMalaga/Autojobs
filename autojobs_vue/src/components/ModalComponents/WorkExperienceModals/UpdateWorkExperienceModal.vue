<template>
  <div v-if="isOpen" class="popup">
    <!-- Campos de Edição -->
    <div class="popup_inner">
      <div class="modal-card">
        <header class="modal-card-head">
          <p class="modal-card-title">Update Experience new Modal</p>
          <button class="delete" aria-label="close" @click="handleClose"></button>
        </header>
        <section class="modal-card-body">
          <TextInputComponent ref="expCompany" title="Company Name" placeholder="Type the name of the Institution" :default-value="Experience.exp_company"/>
          <TextInputComponent ref="expName" title="Experience title" placeholder="Type the name/title of the education/course" :default-value="Experience.exp_title"/>
          <LongTextInputComponent ref="expDesc" title="Experience description" placeholder="Description of your experience" :default-value="Experience.exp_description"/>
          <div class="field has-addons">
            <DateInputComponent class="control is-expanded" ref="expStart" title="Experience start time" :default-value="Experience.exp_start_time"/>
            <DateInputComponent class="control is-expanded" ref="expEnd" title="Experience end time" :default-value="Experience.exp_end_time"/>
          </div>
          <!-- <DropdownInputComponent ref="lngProficiencyLevel" title="Language Proficiency Level" :options="languageProficiencyOptions" /> -->
        </section>
        <footer class="modal-card-foot">
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
import DropdownInputComponent from '../../CommonComponents/DropdownInputComponent.vue'
import LongTextInputComponent from '@/components/CommonComponents/LongTextInputComponent.vue';
import DateInputComponent from '@/components/CommonComponents/DateInputComponent.vue';

export default {
  components: {
    TextInputComponent,
    DropdownInputComponent,
    LongTextInputComponent,
    DateInputComponent
},
  props: {
    isOpen: {
      type: Boolean,
      required: true,
    },
    Experience:{
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
      languageProficiencyOptions:[
      { field_name: "Basic", field_value: "A1" },
      { field_name: "Intermediate", field_value: "B1" },
      { field_name: "Advanced", field_value: "C1" },
    ]
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
      const experienceId = this.Experience.id;
      const updateExperienceUrl = `${this.updateUrl}${experienceId}/update`
      const requestBody = {
        //Add more fields as needed
        "exp_company": this.$refs.expCompany.getValue(),
        "exp_description":  this.$refs.expDesc.getValue(),
        "exp_title": this.$refs.expName.getValue(),
        "exp_start_time": this.$refs.expStart.getValue(),
        "exp_end_time": this.$refs.expEnd.getValue(),
      };
      const headers = {
        Authorization: `Token ${localStorage.getItem('token')}`,
      };
      console.log(requestBody)
      axios.put(updateExperienceUrl, requestBody, { headers })
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
