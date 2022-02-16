import { createStore } from 'vuex'

export default createStore({

  state: {
    // sever hostname
    serverHost: 'http://localhost:8000',
    // 用于记录当前页面是否被修改
    changeState: false,
    // 是否被提交
    submitData: false


  },
  mutations: {
    // 切换
    changeChangeState(state, status) {
      state.changeState = status;

    },
    changeSubmitData(state, status) {
      state.submitData = status
    }

  },
  actions: {
  },
  modules: {
  }
})
