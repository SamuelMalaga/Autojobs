<template>
  <div class="popup">
    <!-- Campos de Edição -->
    <div class="popup_inner">
      <div class="modal-card">
        <header class="modal-card-head">
          <p class="modal-card-title">Run Job Scraper </p>
          <button class="delete" aria-label="close" @click="closeRunJobScraperOnDemandModal"></button>
        </header>
        <section class="modal-card-body">
          <TextInputComponent ref="jobNameInput" title="Job Name" placeholder="Type the name of the job position" />
          <TextInputComponent ref="workLocationInput" title="Work Location" placeholder="Type the job location" />
          <DropdownInputComponent ref="workTypeDropdown" title="Job Type" :options="jobTypeOptions" />

        </section>
        <footer class="modal-card-foot">
          <!-- Botões de Ação -->
          <button class="button is-success" @click="handleSubmit">Add Job</button>
          <button class="button" @click="closeRunJobScraperOnDemandModal">Cancel</button>
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
  data() {
    return {
      jobTypeOptions: [
        { field_name: "On-site", field_value: "1" },
        { field_name: "Hybrid", field_value: "2" },
        { field_name: "Remote", field_value: "3" },
      ],
    };
  },
  components:{
    TextInputComponent,
    DropdownInputComponent
  },
  methods: {
    closeRunJobScraperOnDemandModal() {
      this.$emit('close');
    },
    async handleSubmit() {
      try {
        // Obtenha os valores dos campos do formulário
        const jobName = this.$refs.jobNameInput.getValue();
        const workLocation = this.$refs.workLocationInput.getValue();
        const workType = this.$refs.workTypeDropdown.getValue();

        const headers = {
          Authorization: `Token ${localStorage.getItem('token')}`,
        };

        // Construa a URL para a chamada da API
        const apiUrl = `http://127.0.0.1:8000/execute_full_scraper/`;

        // Faça a chamada para o backend
        const response = await axios.post(apiUrl,{
            job_name: jobName,
            job_location: workLocation,
            job_type: workType,
        },{headers});

        // Lide com a resposta, se necessário
        //console.log(apiUrl);

        // Feche o modal após o sucesso
        this.closeRunJobScraperOnDemandModal();
      } catch (error) {
        // Lide com erros, se necessário
        console.error(error);
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
