<template>
  <div class="popup">
    <!-- Campos de Edição -->
    <div class="popup_inner">
      <div class="modal-card">
        <header class="modal-card-head">
          <p class="modal-card-title">Create application via link</p>
          <button class="delete" aria-label="close" @click="closeCreateApplicationAndJobModal"></button>
        </header>
        <section class="modal-card-body">
          <p>Paste the job link below</p>
          <TextInputComponent title="Job Link" placeholder="Digite o link do trabalho" />
        </section>
        <footer class="modal-card-foot">
          <!-- Botões de Ação -->
          <button class="button is-success" >Apply</button>
          <button class="button" @click="closeCreateApplicationAndJobModal" >Cancel</button>
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
    TextInputComponent
  },
  props: {
  },
  methods: {
    closeCreateApplicationAndJobModal() {
      this.$emit('close');
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
