<template>
  <div class="wrapper">
    <NavBar/>
    <section class="section">
      <router-view/>
    </section>
    <footer class="footer">
      <p class="has-text-centered">Versão inicial do jobTracker</p>
    </footer>
  </div>
</template>

<script>
import NavBar from '@/components/NavBar.vue';
export default{
  components: {
    NavBar,
  },
  data(){
    return{
      showMobileMenu:false,
    }
  }
}
</script>

<style lang="scss">
@import '../node_modules/bulma';
</style>
