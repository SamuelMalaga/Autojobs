<template>
  <div class="m-2">
    <p>{{ title }}</p>
    <textarea class="input" type="text" :placeholder="placeholder || ''" v-model="inputValue"></textarea>
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
  },
  data() {
    return {
      inputValue: '',
    };
  },
  methods: {
    getValue() {
      return this.inputValue;
    },
  },
};
</script>
