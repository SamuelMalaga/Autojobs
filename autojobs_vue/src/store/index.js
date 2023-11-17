import { createStore } from 'vuex'
//DEFAULT CREATESTORE
// export default createStore({
//   state: {
//   },
//   getters: {
//   },
//   mutations: {
//   },
//   actions: {
//   },
//   modules: {
//   }
// })
export default createStore({
  state: {
    FullUserInfo: null,
  },
  mutations: {
    setFullUserInfo(state, FullUserInfo) {
      state.FullUserInfo = FullUserInfo;
    },
  },
  actions: {
    updateFullUserInfo({ commit }, FullUserInfo) {
      commit('setFullUserInfo', FullUserInfo);
    },
  },
  getters: {
    getFullUserInfo: (state) => state.FullUserInfo,
  },
});
