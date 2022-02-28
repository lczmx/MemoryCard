<template>
  <!-- 登录注册页面通用处理 -->
  <div :class="`container ${containerCls}`" ref="containerRef">
    <div class="forms-container">
      <div class="signin-signup">
        <form action="#" class="sign-in-form">
          <h2 class="title">登录</h2>
          <div class="field-item">
            <div class="input-field">
              <i class="iconfont icon-denglu-copy"></i>
              <input
                type="text"
                v-model="loginAccount"
                placeholder="账号"
                @blur="onBlurLoginAccount"
                @input="onChangeLoginAccount"
              />
            </div>
            <p class="error-msg" v-show="loginAccountErrorMsg">
              {{ loginAccountErrorMsg }}
            </p>
          </div>
          <div class="field-item">
            <div class="input-field">
              <i class="iconfont icon-lock"></i>
              <input
                type="password"
                v-model="loginPassword"
                placeholder="密码"
                @blur="onBlurLoginPassword"
                @input="onChangeLoginPassword"
              />
            </div>
            <p class="error-msg" v-show="loginPasswordErrorMsg">
              {{ loginPasswordErrorMsg }}
            </p>
          </div>

          <input
            type="button"
            value="提交"
            class="btn solid"
            @click="handlerClickLoginSubmitBtn"
          />
        </form>
        <!-- 注册 -->
        <form action="#" class="sign-up-form">
          <h2 class="title">注册</h2>
          <div class="field-item">
            <div class="input-field">
              <i class="iconfont icon-denglu-copy"></i>
              <input
                type="text"
                v-model="singUpUsername"
                placeholder="用户名"
                @blur="onBlurSingUpUsername"
                @input="onChangeSingUpUsername"
              />
            </div>
            <p class="error-msg" v-show="singUpUsernameErrorMsg">
              {{ singUpUsernameErrorMsg }}
            </p>
          </div>
          <div class="field-item">
            <div class="input-field">
              <i class="iconfont icon-ccenvelope"></i>
              <input
                type="email"
                v-model="singUpEmail"
                placeholder="邮箱"
                @blur="onBlurSingUpEmail"
                @input="onChangeSingUpEmail"
              />
            </div>
            <p class="error-msg" v-show="singUpEmailErrorMsg">
              {{ singUpEmailErrorMsg }}
            </p>
          </div>
          <div class="field-item">
            <div class="input-field">
              <i class="iconfont icon-lock"></i>
              <input
                type="password"
                v-model="singUpPassword1"
                placeholder="密码"
                @blur="onBlurSingUpPassword1"
                @input="onChangeSingUpPassword1"
              />
            </div>
            <p class="error-msg" v-show="singUpPassword1ErrorMsg">
              {{ singUpPassword1ErrorMsg }}
            </p>
          </div>
          <div class="field-item">
            <div class="input-field">
              <i class="iconfont icon-lock"></i>
              <input
                type="password"
                v-model="singUpPassword2"
                placeholder="重复密码"
                @blur="onBlurSingUpPassword2"
                @input="onChangeSingUpPassword2"
              />
            </div>
            <p class="error-msg" v-show="singUpPassword2ErrorMsg">
              {{ singUpPassword2ErrorMsg }}
            </p>
          </div>
          <input
            type="button"
            class="btn"
            value="提交"
            @click="handlerClickSignUpSubmitBtn"
          />
        </form>
      </div>
    </div>

    <div class="panels-container">
      <div class="panel left-panel">
        <div class="content">
          <h3>没有账号?</h3>
          <p>
            知识是一种外在的积累，而智慧是一种内在的成长。知识来自于记忆，智慧来自于领悟。
          </p>
          <button
            class="btn transparent"
            id="sign-up-btn"
            @click="handlerClickSignupBtn"
          >
            注册
          </button>
        </div>
        <img :src="require('@/assets/images/log.svg')" class="image" alt="" />
      </div>
      <div class="panel right-panel">
        <div class="content">
          <h3>已有账号?</h3>
          <p>
            人的大脑和肢体一样，多用则灵，不用则废。在掌握了所读东西的记忆特征后，就惟有勤奋二字了。
          </p>
          <button
            class="btn transparent"
            id="sign-in-btn"
            @click="handlerClickLoginBtn"
          >
            登录
          </button>
        </div>
        <img
          :src="require('@/assets/images/register.svg')"
          class="image"
          alt=""
        />
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from "vue";
import { useStore } from "vuex";
import { useRouter } from "vue-router";
import { Toast } from "vant";
import {
  IUserSignUpPostData,
  IUserLoginPostData,
  IUserSignUpPostMsg,
  IUerToken,
} from "@/types";
import { postCreateData } from "@/utils/request";
import qs from "qs";
export default defineComponent({
  name: "LoginSingup",
  props: {
    containerCls: {
      // sign-up-mode 或 ""
      type: String,
      default: "",
    },
  },
  setup() {
    const containerRef = ref<HTMLElement>();
    // ----------------------- 点击切换
    const handlerClickSignupBtn = () => {
      if (!containerRef.value) return;
      containerRef.value.classList.add("sign-up-mode");
      // 清空提示
      loginAccount.value = "";
      loginPassword.value = "";
      loginAccountErrorMsg.value = "";
      loginPasswordErrorMsg.value = "";
      // 清空sign up数据
      singUpUsername.value = "";
      singUpEmail.value = "";
      singUpPassword1.value = "";
      singUpPassword2.value = "";
      singUpUsernameErrorMsg.value = "";
      singUpEmailErrorMsg.value = "";
      singUpPassword1ErrorMsg.value = "";
      singUpPassword2ErrorMsg.value = "";
    };
    const handlerClickLoginBtn = () => {
      if (!containerRef.value) return;
      containerRef.value.classList.remove("sign-up-mode");
      // 清空提示
      loginAccount.value = "";
      loginPassword.value = "";
      loginAccountErrorMsg.value = "";
      loginPasswordErrorMsg.value = "";
      // 清空sign up数据
      singUpUsername.value = "";
      singUpEmail.value = "";
      singUpPassword1.value = "";
      singUpPassword2.value = "";
      singUpUsernameErrorMsg.value = "";
      singUpEmailErrorMsg.value = "";
      singUpPassword1ErrorMsg.value = "";
      singUpPassword2ErrorMsg.value = "";
    };
    // --------------------- 注册数据
    const singUpUsername = ref("");
    const singUpEmail = ref("");
    const singUpPassword1 = ref("");
    const singUpPassword2 = ref("");
    const singUpUsernameErrorMsg = ref(""); // 错误提示ref
    const singUpEmailErrorMsg = ref(""); // 错误提示ref
    const singUpPassword1ErrorMsg = ref(""); // 错误提示ref
    const singUpPassword2ErrorMsg = ref(""); // 错误提示ref

    // ------- 检测数据
    // --- 失去焦点事件
    // 用户名
    const isEmptySingUpUsername = () => {
      if (!singUpUsername.value) {
        singUpUsernameErrorMsg.value = "用户名不能为空";
      } else {
        singUpUsernameErrorMsg.value = "";
      }
    };
    const onBlurSingUpUsername = () => isEmptySingUpUsername();
    const onChangeSingUpUsername = () => isEmptySingUpUsername();
    // 邮箱
    const isEmptySingUpEmail = () => {
      if (!singUpEmail.value) {
        singUpEmailErrorMsg.value = "邮箱不能为空";
      } else {
        singUpEmailErrorMsg.value = "";
      }
    };
    const onBlurSingUpEmail = () => isEmptySingUpEmail();
    const onChangeSingUpEmail = () => {
      isEmptySingUpEmail();
      // 邮箱格式
      let pattern = /^([a-zA-Z0-9_-])+@([a-zA-Z0-9_-])+(.[a-zA-Z0-9_-])+/;
      if (!pattern.test(singUpEmail.value)) {
        singUpEmailErrorMsg.value = "邮箱格式错误";
      } else {
        singUpEmailErrorMsg.value = "";
      }
    };
    // 密码
    const isEmptySingUpPassword1 = () => {
      if (!singUpPassword1.value)
        singUpPassword1ErrorMsg.value = "密码不能为空";
    };
    const isEmptySingUpPassword2 = () => {
      if (!singUpPassword2.value)
        singUpPassword2ErrorMsg.value = "密码不能为空";
    };

    const onBlurSingUpPassword1 = () => isEmptySingUpPassword1();
    const onChangeSingUpPassword1 = () => {
      isEmptySingUpPassword1();
      if (
        singUpPassword2.value &&
        singUpPassword1.value !== singUpPassword2.value
      ) {
        singUpPassword1ErrorMsg.value = "两次输入的密码不一致";
        singUpPassword2ErrorMsg.value = "两次输入的密码不一致";
      } else if (
        singUpPassword2.value &&
        singUpPassword1.value === singUpPassword2.value
      ) {
        singUpPassword1ErrorMsg.value = "";
        singUpPassword2ErrorMsg.value = "";
      }
    };
    const onBlurSingUpPassword2 = () => isEmptySingUpPassword2();
    const onChangeSingUpPassword2 = () => {
      isEmptySingUpPassword2();
      if (
        singUpPassword1.value &&
        singUpPassword1.value !== singUpPassword2.value
      ) {
        singUpPassword1ErrorMsg.value = "两次输入的密码不一致";
        singUpPassword2ErrorMsg.value = "两次输入的密码不一致";
      } else if (
        singUpPassword1.value &&
        singUpPassword1.value === singUpPassword2.value
      ) {
        singUpPassword1ErrorMsg.value = "";
        singUpPassword2ErrorMsg.value = "";
      }
    };

    // 提交数据
    const store = useStore();
    const handlerClickSignUpSubmitBtn = () => {
      // 先检验数据
      new Promise((resolve, reject) => {
        isEmptySingUpUsername();
        onChangeSingUpEmail();
        onChangeSingUpPassword1();
        onChangeSingUpPassword2();
        if (
          singUpUsernameErrorMsg.value ||
          singUpEmailErrorMsg.value ||
          singUpPassword1ErrorMsg.value ||
          singUpPassword2ErrorMsg.value
        ) {
          return;
        }
        // 验证通过
        resolve("success");
      }).then(() => {
        const data = {
          username: singUpUsername.value,
          email: singUpEmail.value,
          password1: singUpPassword1.value,
          password2: singUpPassword2.value,
        };
        postCreateData<IUserSignUpPostMsg, IUserSignUpPostData>(
          {
            url: `${store.state.serverHost}/user/signup`,
            method: "post",
            data,
          },
          true
        )
          .then((response) => {
            // 创建成功
            Toast.success("注册成功");
            // 跳到对应页面
            handlerClickLoginBtn();
            // 设置login账号数据
            loginAccount.value = response.username ? response.username : "";
          })
          .catch((error) => {
            const msg = error.data as IUserSignUpPostMsg;
            if (msg.username) singUpUsernameErrorMsg.value = msg.username;
            if (msg.email) singUpEmailErrorMsg.value = msg.email;
            if (msg.password2 || msg.password1) {
              const passwordError = msg.password2
                ? msg.password2
                : msg.password1;
              singUpPassword1ErrorMsg.value = passwordError as string;
              singUpPassword2ErrorMsg.value = passwordError as string;
            }
          });
      });
    };
    // ------------------ 登录
    const loginAccount = ref("");
    const loginPassword = ref("");
    const loginAccountErrorMsg = ref(""); // 错误提示ref
    const loginPasswordErrorMsg = ref(""); // 错误提示ref
    // 检验
    const isEmptyLoginAccount = () => {
      if (!loginAccount.value) {
        loginAccountErrorMsg.value = "账号不能为空";
      } else {
        loginAccountErrorMsg.value = "";
      }
    };
    const isEmptyLoginPassword = () => {
      if (!loginPassword.value) {
        loginPasswordErrorMsg.value = "密码不能为空";
      } else {
        loginPasswordErrorMsg.value = "";
      }
    };

    const onBlurLoginAccount = () => isEmptyLoginAccount();
    const onChangeLoginAccount = () => isEmptyLoginAccount();
    const onBlurLoginPassword = () => isEmptyLoginPassword();
    const onChangeLoginPassword = () => isEmptyLoginPassword();
    // ------- 提交登录数据
    const router = useRouter();
    const handlerClickLoginSubmitBtn = () => {
      // 先检验数据
      new Promise((resolve, reject) => {
        isEmptyLoginAccount();
        isEmptyLoginAccount();

        if (loginAccountErrorMsg.value || loginPasswordErrorMsg.value) {
          return;
        }
        // 验证通过
        resolve("success");
      }).then(() => {
        const data: IUserLoginPostData = {
          username: loginAccount.value,
          password: loginPassword.value,
        };
        postCreateData<IUerToken, string>(
          {
            url: `${store.state.serverHost}/user/token`,
            method: "post",
            data: qs.stringify(data),
            headers: { "content-type": "application/x-www-form-urlencoded" }, //表单数据
          },
          true
        )
          .then(({ accessToken, tokenType }) => {
            // 创建成功

            // 保存到store
            store.commit("setToken", { accessToken, tokenType });
            Toast.success("登录成功");
            // 跳转上一个页面
            router.go(-1);
          })
          .catch((error) => {
            const msg = error.msg as string;
            loginAccountErrorMsg.value = msg;
            loginPasswordErrorMsg.value = msg;
          });
      });
    };
    return {
      // 返回的数据
      containerRef,
      handlerClickSignupBtn,
      handlerClickLoginBtn,
      singUpUsername, // 注册开始
      singUpEmail,
      singUpPassword1,
      singUpPassword2,
      singUpUsernameErrorMsg,
      singUpEmailErrorMsg,
      singUpPassword1ErrorMsg,
      singUpPassword2ErrorMsg,
      onBlurSingUpUsername,
      onChangeSingUpUsername,
      onBlurSingUpEmail,
      onChangeSingUpEmail,
      onBlurSingUpPassword1,
      onChangeSingUpPassword1,
      onBlurSingUpPassword2,
      onChangeSingUpPassword2,
      handlerClickSignUpSubmitBtn, // 提交
      loginAccount, // 登录
      loginPassword,
      loginAccountErrorMsg,
      loginPasswordErrorMsg,
      onBlurLoginAccount, // 检测数据
      onChangeLoginAccount,
      onBlurLoginPassword,
      onChangeLoginPassword,
      handlerClickLoginSubmitBtn, /// 提交
    };
  },
});
</script>

<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body,
input {
  font-family: "Poppins", sans-serif;
}

.container {
  position: relative;
  width: 100vw;
  height: 100vh;
  background-color: #fff;
  min-height: 100vh;
  overflow: hidden;
  margin: 0;
}
.field-item {
  max-width: 380px;
  width: 100%;
  position: relative;
}
.error-msg {
  position: absolute;
  bottom: -9px;
  padding-right: 30px;
  width: 100%;
  color: #ee0a24;
  font-size: 12px;
  height: 20px;
  display: flex;
  align-items: center;
  justify-content: flex-end;
}
.forms-container {
  position: absolute;
  width: 100%;
  height: 100%;
  top: 0;
  left: 0;
}

.signin-signup {
  position: absolute;
  top: 50%;
  transform: translate(-50%, -50%);
  left: 75%;
  width: 50%;
  transition: 1s 0.7s ease-in-out;
  display: grid;
  grid-template-columns: 1fr;
  z-index: 5;
}

form {
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
  padding: 0rem 5rem;
  transition: all 0.2s 0.7s;
  overflow: hidden;
  grid-column: 1 / 2;
  grid-row: 1 / 2;
}

form.sign-up-form {
  opacity: 0;
  z-index: 1;
}

form.sign-in-form {
  z-index: 2;
}

.title {
  font-size: 2rem;
  color: #444;
  margin-bottom: 10px;
}

.input-field {
  max-width: 380px;
  width: 100%;
  background-color: #f0f0f0;
  margin: 10px 0;
  height: 55px;
  border-radius: 55px;
  display: grid;
  grid-template-columns: 15% 85%;
  padding: 0 0.4rem;
  position: relative;
}

.input-field i {
  text-align: center;
  line-height: 55px;
  color: #acacac;
  transition: 0.5s;
  font-size: 1.1rem;
}

.input-field input {
  background: none;
  outline: none;
  border: none;
  line-height: 1;
  font-weight: 600;
  font-size: 1.1rem;
  color: #333;
}

.input-field input::placeholder {
  color: #aaa;
  font-weight: 500;
}

.social-text {
  padding: 0.7rem 0;
  font-size: 1rem;
}

.social-media {
  display: flex;
  justify-content: center;
}

.social-icon {
  height: 46px;
  width: 46px;
  display: flex;
  justify-content: center;
  align-items: center;
  margin: 0 0.45rem;
  color: #333;
  border-radius: 50%;
  border: 1px solid #333;
  text-decoration: none;
  font-size: 1.1rem;
  transition: 0.3s;
}

.social-icon:hover {
  color: #4481eb;
  border-color: #4481eb;
}

.btn {
  width: 150px;
  background-color: #5995fd;
  border: none;
  outline: none;
  height: 49px;
  border-radius: 49px;
  color: #fff;
  font-weight: 600;
  margin: 10px 0;
  cursor: pointer;
  transition: 0.5s;
}

.btn:hover {
  background-color: #4d84e2;
}
.panels-container {
  position: absolute;
  height: 100%;
  width: 100%;
  top: 0;
  left: 0;
  display: grid;
  grid-template-columns: repeat(2, 1fr);
}

.container:before {
  content: "";
  position: absolute;
  height: 2000px;
  width: 2000px;
  top: -10%;
  right: 48%;
  transform: translateY(-50%);
  background-image: linear-gradient(-45deg, #4481eb 0%, #04befe 100%);
  transition: 1.8s ease-in-out;
  border-radius: 50%;
  z-index: 6;
}

.image {
  width: 100%;
  transition: transform 1.1s ease-in-out;
  transition-delay: 0.4s;
}

.panel {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  justify-content: space-around;
  text-align: center;
  z-index: 6;
}

.left-panel {
  pointer-events: all;
  padding: 3rem 17% 2rem 12%;
}

.right-panel {
  pointer-events: none;
  padding: 3rem 12% 2rem 17%;
}

.panel .content {
  color: #fff;
  transition: transform 0.9s ease-in-out;
  transition-delay: 0.6s;
}

.panel h3 {
  font-weight: 600;
  line-height: 1;
  font-size: 1.5rem;
}

.panel p {
  font-size: 0.95rem;
  padding: 0.7rem 0;
}

.btn.transparent {
  margin: 0;
  background: none;
  border: 2px solid #fff;
  width: 130px;
  height: 41px;
  font-weight: 600;
  font-size: 0.8rem;
}

.right-panel .image,
.right-panel .content {
  transform: translateX(800px);
}

/* ANIMATION */

.container.sign-up-mode:before {
  transform: translate(100%, -50%);
  right: 52%;
}

.container.sign-up-mode .left-panel .image,
.container.sign-up-mode .left-panel .content {
  transform: translateX(-800px);
}

.container.sign-up-mode .signin-signup {
  left: 25%;
}

.container.sign-up-mode form.sign-up-form {
  opacity: 1;
  z-index: 2;
}

.container.sign-up-mode form.sign-in-form {
  opacity: 0;
  z-index: 1;
}

.container.sign-up-mode .right-panel .image,
.container.sign-up-mode .right-panel .content {
  transform: translateX(0%);
}

.container.sign-up-mode .left-panel {
  pointer-events: none;
}

.container.sign-up-mode .right-panel {
  pointer-events: all;
}

@media (max-width: 870px) {
  .container {
    min-height: 800px;
    height: 100vh;
  }
  .signin-signup {
    width: 100%;
    top: 95%;
    transform: translate(-50%, -100%);
    transition: 1s 0.8s ease-in-out;
  }

  .signin-signup,
  .container.sign-up-mode .signin-signup {
    left: 50%;
  }

  .panels-container {
    grid-template-columns: 1fr;
    grid-template-rows: 1fr 2fr 1fr;
  }

  .panel {
    flex-direction: row;
    justify-content: space-around;
    align-items: center;
    padding: 2.5rem 8%;
    grid-column: 1 / 2;
  }

  .right-panel {
    grid-row: 3 / 4;
  }

  .left-panel {
    grid-row: 1 / 2;
  }

  .image {
    width: 200px;
    transition: transform 0.9s ease-in-out;
    transition-delay: 0.6s;
  }

  .panel .content {
    padding-right: 15%;
    transition: transform 0.9s ease-in-out;
    transition-delay: 0.8s;
  }

  .panel h3 {
    font-size: 1.2rem;
  }

  .panel p {
    font-size: 0.7rem;
    padding: 0.5rem 0;
  }

  .btn.transparent {
    width: 110px;
    height: 35px;
    font-size: 0.7rem;
  }

  .container:before {
    width: 1500px;
    height: 1500px;
    transform: translateX(-50%);
    left: 30%;
    bottom: 68%;
    right: initial;
    top: initial;
    transition: 2s ease-in-out;
  }

  .container.sign-up-mode:before {
    transform: translate(-50%, 100%);
    bottom: 32%;
    right: initial;
  }

  .container.sign-up-mode .left-panel .image,
  .container.sign-up-mode .left-panel .content {
    transform: translateY(-300px);
  }

  .container.sign-up-mode .right-panel .image,
  .container.sign-up-mode .right-panel .content {
    transform: translateY(0px);
  }

  .right-panel .image,
  .right-panel .content {
    transform: translateY(300px);
  }

  .container.sign-up-mode .signin-signup {
    top: 5%;
    transform: translate(-50%, 0);
  }
}

@media (max-width: 570px) {
  form {
    padding: 0 1.5rem;
  }

  .image {
    display: none;
  }
  .panel .content {
    padding: 0.5rem 1rem;
  }
  .container {
    padding: 1.5rem;
  }

  .container:before {
    bottom: 72%;
    left: 50%;
  }

  .container.sign-up-mode:before {
    bottom: 28%;
    left: 50%;
  }
}
</style>
