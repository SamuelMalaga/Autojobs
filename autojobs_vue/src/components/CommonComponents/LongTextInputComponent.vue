<template>
  <div class="m-2">
    <p>{{ title }}</p>
    <textarea class="input textarea" type="text" :placeholder="placeholder || ''" v-model="inputValue"></textarea>
  </div>
</template>

<script>
export default {
  props: {
    title: {
      type: String,
      required: true,
    },
    placeholder: String,
    defaultValue: {
      type: String,
      default: '',
    },
  },
  data() {
    return {
      inputValue: this.defaultValue,
    };
  },
  methods: {
    getValue() {
      return this.inputValue;
    },
  },
};
</script>
