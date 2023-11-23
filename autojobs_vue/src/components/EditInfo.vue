<!-- Modal.vue -->
<template>
  <div class="popup">
    <div class="popup_inner">
      <div v-for="campo in fields" :key="campo">
        <label>{{ campo }}</label>
        <input v-model="dadosEditados[campo]" />
      </div>
      <!-- <slot/> -->
      <!-- Campos de Edição -->
      <button class="popup_close" @click="closeModal()">
        Close Popup
      </button>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    TogglePopup:{
      type: Function,
      required: true,
    },
    fields: {
      type: Array,
      required: true,
    },
  },
  methods: {
    closeModal() {
      // Chame a função passada do componente pai
      this.TogglePopup();
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
  .popup_inner{
    background: #fff;
    padding:32px;
  }
}
</style>
