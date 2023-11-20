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
        <div class="navbar-start">
          <a class="navbar-item">
            Job Tracker
          </a>

          <a class="navbar-item">
            My Resumé
          </a>

          <a class="navbar-item">
            Dashboard
          </a>
        </div>

        <div class="navbar-end">
          <div class="navbar-item">
            <div class="buttons">
              <router-link to="/signup" class="button is-primary">
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
export default{
  data(){
    return{
      showMobileMenu:false,
    }
  }
}
</script>
