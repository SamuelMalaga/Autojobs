<template>
  <div class="m-2">
    <p>{{ title }}</p>
    <input class="input" type="date" :value="formattedDate" @change="updateInputValue">
  </div>
</template>

<script>
export default {
  props: {
    title: {
      type: String,
      required: true,
    },
    defaultValue: {
      type: String,
      default: '',
    },
  },
  data() {
    return {
      inputValue: this.convertDatabaseFormatToInputValue(this.defaultValue),
    };
  },
  computed: {
    formattedDate() {
      return this.inputValue || '';
    },
  },
  methods: {
    updateInputValue(event) {
      this.inputValue = event.target.value;
    },
    getValue() {
      return this.inputValue ? this.convertInputValueToDatabaseFormat(this.inputValue) : '';
    },
    convertDatabaseFormatToInputValue(databaseValue) {
      if (!databaseValue) {
        return '';
      }
      // Converte o formato do banco de dados para o formato de entrada do usuário (apenas data)
      const date = new Date(databaseValue);
      return date.toISOString().split('T')[0];
    },
    convertInputValueToDatabaseFormat(inputValue) {
      if (!inputValue) {
        return '';
      }
      // Adiciona uma hora padrão à entrada do usuário antes de enviar ao backend
      const datetimeValue = `${inputValue}T00:00:00`;
      return datetimeValue;
    },
  },
};
</script>
