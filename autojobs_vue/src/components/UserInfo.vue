<template>
  <div>
    <h2>User Information</h2>
    <div v-if="user">
      <p><strong>Name:</strong> {{ user.firstName }}</p>
      <p><strong>Sobrenome:</strong> {{ user.lastName }}</p>
      <p><strong>Email:</strong> {{ user.email }}</p>
      <p><strong>Cidade:</strong> {{ user.city }}<strong> Pais:</strong> {{ user.country }}</p>
      <p><strong>Bio:</strong> {{ user.bio }}</p>
      <!-- Adicione outros campos conforme necessário -->
    </div>
    <div v-else>
      <p>No user information available.</p>
    </div>
  </div>
</template>
<script>
export default {
  computed: {
    user() {
      return this.$store.getters.getFullUserInfo;
    },
  },
};
</script>
