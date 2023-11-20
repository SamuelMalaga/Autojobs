import { createStore } from 'vuex'

export default createStore({
  state: {
    FullUserInfo: null,
    userId :null,
  },
  mutations: {
    setFullUserInfo(state, FullUserInfo) {
      state.FullUserInfo = FullUserInfo;
    },
    setUserId(state, userId) {
      state.userId = userId;
    },
  },
  actions: {
    updateFullUserInfo({ commit }, FullUserInfo) {
      commit('setFullUserInfo', FullUserInfo);
    },
    updateUserId({ commit }, userId) {
      console.log('Atualizando userId:', userId);
      commit('setUserId', userId);
    },
  },
  getters: {
    getFullUserInfo: (state) => state.FullUserInfo,
    getUserId: (state) => state.userId,
  },
});
