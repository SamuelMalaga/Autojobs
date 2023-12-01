<template>
  <JobList/>
</template>

<script>
import JobList from '@/components/JobList.vue';

export default {
  name: 'Jobs',
  components: {
    JobList
  },
  created() {
    // Exemplo: Se as informações do usuário não estiverem disponíveis, redirecione para outra página
    if (!this.$store.getters.isLoggedIn) {
      this.$router.push('/'); // ou qualquer outra página
    }
  },
}
</script>
