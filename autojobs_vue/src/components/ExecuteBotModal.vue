<template>
  <div class="popup">
    <!-- Campos de Edição -->
    <div class="popup_inner">
      <div class="modal-card">
        <header class="modal-card-head">
          <p class="modal-card-title">Add new Job via link </p>
          <button class="delete" aria-label="close" @click="closeModal"></button>
        </header>
        <section class="modal-card-body">
          <p>Job Link</p>
          <input class="input is-link" type="text" placeholder="Link input">
        </section>
        <footer class="modal-card-foot">
          <!-- Botões de Ação -->
          <button class="button is-success" @click="handleSubmit">Save changes</button>
          <button class="button" @click="closeModal">Cancel</button>
        </footer>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  methods: {
    closeModal() {
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
