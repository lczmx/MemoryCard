import { createStore } from "vuex";

export default createStore({
  state: {
    // sever hostname
    serverHost: "http://192.168.0.110:8000",
    // 用于记录当前页面是否被修改
    changeState: false,
    // 是否被提交
    submitData: false,
    // 添加/修改页面的标题
    pageTitle: "title",
    // 设置内部页面的标题
    settingsItemPageTitle: "title",
  },
  mutations: {
    // 切换
    changeChangeState(state, status) {
      state.changeState = status;
    },
    changeSubmitData(state, status) {
      state.submitData = status;
    },
    changePageTitle(state, title) {
      state.pageTitle = title;
    },
    changeSettingsPageTitle(state, title) {
      state.settingsItemPageTitle = title;
    },
  },
  actions: {},
  modules: {},
});
