import { createStore } from "vuex";
import persistedState from "vuex-persistedstate"; // 持久化

export default createStore({
  state: {
    // sever hostname
    serverHost: "",
    serverPort: "8366",
    // 用于记录当前页面是否被修改
    changeState: false,
    // 是否被提交
    submitData: false,
    // 添加/修改页面的标题
    pageTitle: "title",
    // 设置内部页面的标题
    settingsItemPageTitle: "title",
    // token
    token: { accessToken: "", tokenType: "" },
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
    setToken(state, { accessToken, tokenType }) {
      state.token.accessToken = accessToken;
      state.token.tokenType = tokenType;
    },
    setServiceHost(state, host) {
      // 动态设置serverHost
      state.serverHost = `${host}:${state.serverPort}`;
    },
  },
  actions: {},
  modules: {},
  plugins: [persistedState()], // 添加插件, 持久化
});
