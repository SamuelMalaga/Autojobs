import { createStore } from 'vuex'

export default createStore({
  state: {
    FullUserInfo: null,
    userId :null,
    isLoggedIn: false,
    baseURL:'http://127.0.0.1:8000/'
  },
  mutations: {
    setFullUserInfo(state, FullUserInfo) {
      state.FullUserInfo = FullUserInfo;
    },
    setUserId(state, userId) {
      state.userId = userId;
    },
    setLoggedIn(state, value) {
      state.isLoggedIn = value;
    },
    updatePartialUserInfo(state, { bio, country, city }) {
      // Atualizar apenas as informações específicas do usuário
      state.FullUserInfo.bio = bio;
      state.FullUserInfo.country = country;
      state.FullUserInfo.city = city;
    },
  },
  actions: {
    updateFullUserInfo({ commit }, FullUserInfo) {
      commit('setFullUserInfo', FullUserInfo);
    },
    updateUserId({ commit }, userId) {
      //console.log('Atualizando userId:', userId);
      commit('setUserId', userId);
    },
    login({ commit }) {
      // Lógica de login
      commit('setLoggedIn', true);
    },
    logout({ commit }) {
      // Lógica de logout
      commit('setLoggedIn', false);
    },
    updatePartialUserInfo({ commit }, { bio, country, city }) {
      // Chamar a mutation para atualizar as informações do usuário
      commit('updatePartialUserInfo', { bio, country, city });
    },
  },
  getters: {
    getFullUserInfo: (state) => state.FullUserInfo,
    getUserId: (state) => state.userId,
    isLoggedIn: (state)=> state.isLoggedIn,
    getBaseURL: (state)=> state.baseURL
  },
});
