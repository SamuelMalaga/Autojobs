<template>
  <div class="container">
    <p class="title has-text-centered">AutoJobs</p>
    <Login/>
  </div>
</template>

<script>
import Login from '@/components/Login.vue';

export default {
  name: 'HomeView',
  components: {
    Login
  },

}
</script>
