<template>
  <div class="wrapper">
    <nav class="navbar is-dark" role="navigation" aria-label="main navigation">
      <div class="navbar-brand">
        <router-link to="/" class="navbar-item"><strong>Autojobs</strong></router-link>

        <a role="button" class="navbar-burger" aria-label="menu" aria-expanded="false" data-target="navbarBasicExample" @click="showMobileMenu = !showMobileMenu">
          <span aria-hidden="true"></span>
          <span aria-hidden="true"></span>
          <span aria-hidden="true"></span>
        </a>
      </div>

      <div id="navbarBasicExample" class="navbar-menu" v-bind:class="{'is-active' : showMobileMenu}">
        <div class="navbar-start"  v-if="$store.getters.isLoggedIn">
          <router-link to="/myProfile"  class="navbar-item"><a class="has-text-white">My Profile</a></router-link>
          <router-link to="/JobTracker"  class="navbar-item "><a class="has-text-white">Job Tracker</a></router-link>
          <router-link to="/Jobs"  class="navbar-item"><a class="has-text-white">Jobs</a></router-link>
          <router-link to="/Dashboard"  class="navbar-item"><a class="has-text-white">Dashboard</a></router-link>
        </div>

        <div class="navbar-end">
          <div class="navbar-item">
            <div class="buttons">
              <button  v-if="$store.getters.isLoggedIn" class="button is-danger" @click="logout">
                <strong>Logout</strong>
              </button>
              <router-link  v-if="!$store.getters.isLoggedIn" to="/signup" class="button is-primary">
                <strong>Sign up</strong>
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </nav>
  </div>
</template>

<script>
import axios from 'axios';

export default{
  data(){
    return{
      showMobileMenu:false,
    }
  },
  methods: {
    async logout() {
      try {
        // Obtém o token do localStorage
        const token = localStorage.getItem('token');

        // Verifica se o token está presente
        if (!token) {
          console.error('Token não encontrado.');
          return;
        }

        console.log(token)

        // Configura os cabeçalhos com o token
        const headers = { Authorization: `Token ${token}` };

        // Realiza a solicitação HTTP para o URL de logout no seu backend
        await axios.post('http://127.0.0.1:8000/logout/', null, { headers });

        // Chama a lógica de logout no Vuex store
        //this.$store.dispatch('logout');

        // Redireciona o usuário para a página de login ou outra página desejada
        this.$router.push('/');
      } catch (error) {
        console.error('Erro durante o logout:', error);
      }
    },
  },
}
</script>
