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
        const token = response.data.access_token;
        const userId = response.data.user_id;
        this.$store.dispatch('updateUserId', userId);
        //console.log('userId da response', userId)
        //console.log('userIdObtido pelo getter',this.$store.getters.getUserId)
        // Armazene o token no localStorage ou em outro local seguro
        localStorage.setItem('token', token);
        // Retrieves additional user data
        const AdditionalUserInfoResponse = await axios.get(`http://127.0.0.1:8000/users/${userId}/myProfile`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        const AdditionalUserInfo = AdditionalUserInfoResponse.data;
        const FullUserInfo ={
          firstName:response.data.first_name,
          lastName:response.data.last_name,
          email:response.data.email,
          city:AdditionalUserInfo.city,
          country:AdditionalUserInfo.country,
          bio:AdditionalUserInfo.bio,
          userId : userId
        }
        //console.log(FullUserInfo)
        this.$store.dispatch('updateFullUserInfo', FullUserInfo);
        //console.log('useriNFOObtido pelo getter',this.$store.getters.getFullUserInfo)
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
