<template>
  <section class="section is-small">
    <div class="container is-small">
      <h1 class="title">Log In</h1>
      <div class="notification ">
        <div class="field">
          <p class="control">
            <h2 class="subtitle"><label for="username">Username/Email</label></h2>
            <input class="input" type="text" v-model="username" placeholder="Email/Username" required>
          </p>
        </div>
        <div class="field">
          <p class="control">
            <h2 class="subtitle"><label for="password">Password</label></h2>
            <input class="input" type="password" v-model="password" placeholder="Password" required>
          </p>
        </div>
      </div>
      <button class="button" @click="login">Log-in</button>
    </div>
  </section>
</template>

<script>
import axios from 'axios';
import { parseJwt } from '@/utils';


export default {
  data() {
    return {
      username: '',
      password: '',
    };
  },
  methods: {
    async login() {
      try {
        const response = await axios.post('http://127.0.0.1:8000/login/', {
          username: this.username,
          password: this.password,
        });

        // Armazene o token retornado (se aplicável) e realize ações necessárias após o login
        const token = response.data.token;
        const userId = response.data.user.id;
        this.$store.dispatch('updateUserId', userId);

        // Armazene o token no localStorage ou em outro local seguro
        localStorage.setItem('token', token);
        // Retrieves additional user data
        const AdditionalUserInfoResponse = await axios.get(`http://127.0.0.1:8000/users/${userId}/myProfile`, {
          headers: {
            Authorization: `Token ${token}`,
          },
        });

        this.$store.dispatch('login');

        const AdditionalUserInfo = AdditionalUserInfoResponse.data;
        const FullUserInfo ={
          firstName:response.data.user.first_name,
          lastName:response.data.user.last_name,
          email:response.data.user.email,
          city:AdditionalUserInfo.city,
          country:AdditionalUserInfo.country,
          bio:AdditionalUserInfo.bio,
          userId : userId
        }
        this.$store.dispatch('updateFullUserInfo', FullUserInfo);
        this.$router.push({ name: 'myProfile'});

        // Redirecione para outra página ou faça outras ações após o login bem-sucedido
      } catch (error) {
        // Trate erros de login, exiba mensagens de erro, etc.
        console.error('Erro durante o login:', error);
      }
    },
  },
};
</script>
