import { createStore } from 'vuex'

export default createStore({
  state: {
    FullUserInfo: null,
    userId :null,
    isLoggedIn: false,
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
  },
  getters: {
    getFullUserInfo: (state) => state.FullUserInfo,
    getUserId: (state) => state.userId,
    isLoggedIn: (state)=> state.isLoggedIn
  },
});
