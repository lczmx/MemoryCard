<template>
  <van-nav-bar title="设置" :fixed="true"> </van-nav-bar>
  <div class="settings_body">
    <div class="user-info-wrap">
      <!-- 是否已经登录 -->
      <div class="uer-login" v-if="!user.username">
        <van-notice-bar color="#28414a" background="#ecf9ff" left-icon="info-o">
          当前处于游客模式, 你可以
          <router-link :to="{ name: 'LogIn' }">登录</router-link>或
          <router-link :to="{ name: 'SignUp' }">注册</router-link>
        </van-notice-bar>
      </div>
      <div class="user-info" v-else>
        <van-cell-group inset>
          <van-cell class="user-info-cell">
            <template #title>
              <div class="user-info-username">
                {{ user.username }}
              </div>
            </template>
            <template #icon>
              <van-icon
                class="iconfont"
                class-prefix="icon"
                name="taogongzi"
                size="40"
                color="#41b883"
              />
            </template>
          </van-cell>
        </van-cell-group>
      </div>
    </div>
    <!-- 第一部分开始 -->
    <!-- 数据分析, 需要登录 -->

    <van-cell-group inset v-if="user.username">
      <van-cell value="" is-link :to="{ name: 'Profile' }">
        <template #icon>
          <van-icon
            class="iconfont item-icon"
            class-prefix="icon"
            name="settings"
            size="20"
          />
        </template>
        <!-- 使用 title 插槽来自定义标题 -->
        <template #title>
          <span class="custom-title">用户配置</span>
        </template>
      </van-cell>
      <van-cell value="" is-link :to="{ name: 'Plan' }">
        <template #icon>
          <van-icon
            class="iconfont item-icon"
            class-prefix="icon"
            name="fsux_tubiao_fenbuquxiantu"
            size="20"
          />
        </template>
        <!-- 使用 title 插槽来自定义标题 -->
        <template #title>
          <span class="custom-title">复习曲线</span>
        </template>
      </van-cell>
      <van-cell value="" is-link :to="{ name: 'Analyse' }">
        <template #icon>
          <van-icon
            class="iconfont item-icon"
            class-prefix="icon"
            name="tongji"
            size="20"
          />
        </template>
        <!-- 使用 title 插槽来自定义标题 -->
        <template #title>
          <span class="custom-title">数据统计</span>
        </template>
      </van-cell>
    </van-cell-group>
    <!-- 第一部分结束 -->

    <!-- 第二部分开始 -->
    <!-- 关于项目等 -->
    <van-cell-group inset>
      <van-cell value="" is-link>
        <template #icon>
          <van-icon
            class="iconfont item-icon"
            class-prefix="icon"
            name="question"
            size="20"
          />
        </template>
        <!-- 使用 title 插槽来自定义标题 -->
        <template #title>
          <span class="custom-title">帮助中心</span>
        </template>
      </van-cell>
      <van-cell value="" is-link @click="handlerClickAbout">
        <template #icon>
          <van-icon
            class="iconfont item-icon"
            class-prefix="icon"
            name="about"
            size="20"
          />
        </template>
        <!-- 使用 title 插槽来自定义标题 -->
        <template #title>
          <span class="custom-title">关于本项目</span>
        </template>
      </van-cell>
    </van-cell-group>
    <!-- 第二部分结束 -->
    <!-- 第三部分开始 -->
    <!-- 登录等, 用户操作, 需要登录 -->
    <van-cell-group inset v-if="user.username">
      <van-cell is-link @click="handlerClickLogout">
        <template #icon>
          <van-icon
            class="iconfont item-icon"
            class-prefix="icon"
            name="logout"
            size="20"
          />
        </template>
        <!-- 使用 title 插槽来自定义标题 -->
        <template #title>
          <span class="custom-title">退出登录</span>
        </template>
      </van-cell>
    </van-cell-group>
    <!-- 第三部分结束 -->
  </div>
</template>
<script lang="ts">
import { defineComponent, ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import { useStore } from "vuex";
import jwt_decode from "jwt-decode";
import { IUserData, JWTPayLoad } from "@/types";

export default defineComponent({
  name: "Settings",
  setup() {
    /* 用户相关 */
    // -----------------获取用户数据 开始
    const store = useStore();
    const user = ref<IUserData>({ username: "", uid: 0, email: "" });
    const parseUserDataFromJWT = () => {
      // 从jwt中解析用户数据
      const token = store.state.token.accessToken;
      if (!token) return;
      let payload = jwt_decode(token);
      const jwtPayLoad = payload as JWTPayLoad;

      if (!user.value) return;
      user.value.uid = jwtPayLoad.uid;
      user.value.username = jwtPayLoad.sub;
      user.value.email = jwtPayLoad.email;
      user.value.phoneNumber = jwtPayLoad.phoneNumber;
    };

    // -----------------获取用户数据 结束
    // ------------- 跳转到About页面
    const router = useRouter();

    const handlerClickAbout = () => {
      router.push({ name: "About" });
    };

    onMounted(() => {
      parseUserDataFromJWT();
    });
    // ---------- 注销登录
    const handlerClickLogout = () => {
      store.commit("setToken", { accessToken: "", tokenType: "" });
      // 跳转到登录页面
      router.push({ name: "LogIn" });
    };
    return {
      // 返回的数据
      user,
      handlerClickAbout,
      handlerClickLogout,
    };
  },
});
</script>

<style lang="scss">
.settings_body {
  background-color: #f4f3f5;
  padding-top: 10px;
  min-height: calc(100vh - 107px);
  margin-bottom: 50px;
  margin-top: 47px;
  .user-info-wrap {
    .uer-login {
    }
    .user-info {
      .user-info-cell {
        height: 80px;
        display: flex;
        justify-content: center;
        align-items: center;
        .user-info-username {
          text-align: right;
          font-size: 20px;
          width: calc(100vw - 112px);
          overflow: hidden;
          white-space: nowrap;
          text-overflow: ellipsis;
        }
      }
    }
    margin-bottom: 20px;
  }
  .van-cell-group {
    margin-bottom: 20px;
    .item-icon {
      margin-right: 5px;
    }
  }
}
</style>
