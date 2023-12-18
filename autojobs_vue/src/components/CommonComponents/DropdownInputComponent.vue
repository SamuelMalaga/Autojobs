<!-- DropdownInputComponent.vue -->
<template>
  <div class="m-2">
    <p>{{ title }}</p>
    <div class="select is-info">
      <select v-model="inputValue">
        <option v-for="option in options" :value="option.field_value">{{ option.field_name }}</option>
      </select>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    title: String,
    options: Array,
  },
  data() {
    return {
      inputValue: null,
    };
  },
  methods: {
    getValue() {
      return this.inputValue;
    },
  },
};
</script>
