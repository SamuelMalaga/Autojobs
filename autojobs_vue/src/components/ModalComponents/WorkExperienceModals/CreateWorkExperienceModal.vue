<template>
  <div v-if="isOpen" class="popup">
    <!-- Campos de Edição -->
    <div class="popup_inner">
      <div class="modal-card">
        <header class="modal-card-head">
          <p class="modal-card-title">Create Work Experience New Modal</p>
          <button class="delete" aria-label="close" @click="handleClose"></button>
        </header>
        <section class="modal-card-body">
          <TextInputComponent ref="expCompany" title="Company Name" placeholder="Type the name of the Institution" />
          <TextInputComponent ref="expName" title="Experience title" placeholder="Type the name/title of the education/course" />
          <LongTextInputComponent ref="expDesc" title="Experience description" placeholder="Description of your experience" />
          <DropdownInputComponent ref="expType" title="Type of work experience" :options="WorkExperienceType" />
          <div class="field has-addons">
            <DateInputComponent class="control is-expanded" ref="expStart" title="Experience start time" />
            <DateInputComponent class="control is-expanded" ref="expEnd" title="Experience end time"/>
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
import DropdownInputComponent from '../../CommonComponents/DropdownInputComponent.vue';
import LongTextInputComponent from '../../CommonComponents/LongTextInputComponent.vue';
import DateInputComponent from '@/components/CommonComponents/DateInputComponent.vue';
export default {
  components:{
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
    createEndpoint: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      dadosEditados: {},
      WorkExperienceType:[
      { field_name: "Work", field_value: "work" },
      { field_name: "Volunteer", field_value: "volunteer" },
      { field_name: "Project", field_value: "project" },
    ]
    };
  },
  methods: {
    formatDateForSubmit(dateString) {
      if (!dateString) {
        return '';
      }
      const date = new Date(dateString);
      // Retorna a data formatada no formato "YYYY-MM-DDTHH:mm:ss.sssZ"
      return date.toISOString();
    },
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
        "exp_company": this.$refs.expCompany.getValue(),
        "exp_description": this.$refs.expDesc.getValue(),
        "exp_start_time": this.$refs.expStart.getValue(),
        "exp_end_time": this.$refs.expEnd.getValue(),
        "exp_type": this.$refs.expType.getValue(),
        "exp_title": this.$refs.expName.getValue()
      };
      const headers = {
        Authorization: `Token ${localStorage.getItem('token')}`,
      };
      console.log(requestBody)

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
