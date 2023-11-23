<template>
  <div v-if="isOpen" class="popup">
    <!-- Campos de Edição -->
    <div class="popup_inner">
      <div class="modal-card">
        <header class="modal-card-head">
          <p class="modal-card-title">Edit Work Experience</p>
          <button class="delete" aria-label="close" @click="handleClose"></button>
        </header>
        <section class="modal-card-body">
          <div v-for="field in object_instance.fields" :key="field.field_name">
            <h2 class="subtitle">{{ field.field_title }} | {{ field.field_type }}</h2>
            <input v-model="field.field_value" class="input is-normal mb-4" type="text" placeholder="Normal input">
          </div>
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

export default {
  props: {
    isOpen: {
      type: Boolean,
      required: true,
    },
    fields: {
      type: Array,
      required: false,
    },
    dataToIterate: {
      type: Object,
      required: false,
    },
    object_instance:{
      type: Object,
      required: true,
    }
  },
  data() {
    return {
      dadosEditados: {},
    };
  },
  methods: {
    handleSubmit() {
      // Emitir evento para o componente pai com os dados editados
      this.$emit("submit", this.dadosEditados);
    },
    handleClose() {
      // Emitir evento de fechamento
      this.$emit("close");
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
