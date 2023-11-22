<template>
  <p>Dashboard</p>
</template>

<script>
export default {
  name: 'Dashboard',
  components: {
  },
  created() {
    // Exemplo: Se as informações do usuário não estiverem disponíveis, redirecione para outra página
    if (!this.$store.getters.isLoggedIn) {
      this.$router.push('/'); // ou qualquer outra página
    }
  },
}
</script>
