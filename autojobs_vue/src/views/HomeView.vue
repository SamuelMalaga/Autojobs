<template>
  <div class="container">
    <p class="title has-text-centered">AutoJobs</p>
    <section class="section is-small">
      <div class="container is-small">
        <h1 class="title">Log In</h1>
        <div class="notification ">
          <div class="field">
          <p class="control has-icons-left has-icons-right">
            <input class="input" type="email" placeholder="Email">
            <span class="icon is-small is-left">
              <i class="fas fa-envelope"></i>
            </span>
            <span class="icon is-small is-right">
              <i class="fas fa-check"></i>
            </span>
          </p>
        </div>
        <div class="field">
          <p class="control has-icons-left">
            <input class="input" type="password" placeholder="Password">
            <span class="icon is-small is-left">
              <i class="fas fa-lock"></i>
            </span>
          </p>
        </div>
        </div>
        <button class="button">Log-in</button>
      </div>
    </section>
  </div>
</template>

<script>

export default {
  name: 'HomeView',
  components: {

  },

}
</script>
