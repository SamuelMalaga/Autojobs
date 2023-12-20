<template>
  <div class="popup">
    <!-- Campos de Edição -->
    <div class="popup_inner">
      <div class="modal-card">
        <header class="modal-card-head">
          <p class="modal-card-title">Add new Job via link </p>
          <button class="delete" aria-label="close" @click="closeAddJobViaLinkModal"></button>
        </header>
        <section class="modal-card-body">
          <TextInputComponent ref="jobLinkInput" title="Job Link" placeholder="Job Link" />
        </section>
        <footer class="modal-card-foot">
          <!-- Botões de Ação -->
          <button class="button is-success" @click="handleSubmit">Add Job</button>
          <button class="button" @click="closeAddJobViaLinkModal">Cancel</button>
        </footer>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import TextInputComponent from '../../CommonComponents/TextInputComponent.vue';

export default {
  components:{
    TextInputComponent,
  },
  methods: {
    closeAddJobViaLinkModal() {
      this.$emit('close');
    },
    async handleSubmit() {
      // Get the input value
      const jobLink = this.$refs.jobLinkInput.getValue();
      const headers = {
          Authorization: `Token ${localStorage.getItem('token')}`,
        };

      // Make a POST request to your Django backend using Axios
      try {
        const response = await axios.post('http://127.0.0.1:8000/execute_link_scraper/', {
          job_link: jobLink,
        },{ headers });

        // Check if the request was successful (status code 2xx)
        if (response.status === 200) {
          // Handle success (e.g., close the modal)
          this.closeAddJobViaLinkModal();
        } else {
          // Handle error (e.g., show an error message)
          console.error('Error:', response.statusText);
        }
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
