<template>
  <van-nav-bar title="设置" :fixed="true"> </van-nav-bar>
  <div class="settings_body" v-if="user.username">
    <div class="user-info-wrap">
      <!-- 是否已经登录 -->
      <div class="user-info">
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

    <van-cell-group inset>
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
      <van-cell value="" is-link :to="{ name: 'Help' }">
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
      <van-cell value="" is-link :to="{ name: 'About' }">
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
    <van-cell-group inset>
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
  <div class="loading-setting" v-show="!user.username">
    <van-loading color="#1989fa" />
  </div>
</template>
<script lang="ts">
import { defineComponent, ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import { useStore } from "vuex";
import { IUserData } from "@/types";
import { getDataOfOne } from "@/utils/request";
export default defineComponent({
  name: "Settings",
  setup() {
    /* 用户相关 */
    // -----------------获取用户数据 开始
    const store = useStore();
    const user = ref<IUserData>({ email: "", username: "" } as IUserData);
    const getUserData = () => {
      const url = `${store.state.serverHost}/user/`;
      getDataOfOne<IUserData>({ url }, true).then((response) => {
        user.value = response;
      });
    };
    // -----------------获取用户数据 结束
    // ------------- 跳转到About页面
    const router = useRouter();

    onMounted(() => {
      getUserData();
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
      handlerClickLogout,
    };
  },
});
</script>

<style lang="scss">
.loading-setting {
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 999;
  position: fixed;
  bottom: 0;
  top: 46px;
  right: 0;
  left: 0;
  background: #f4f3f5;
}

.settings_body {
  background-color: #f4f3f5;
  padding-top: 10px;
  min-height: calc(100vh - 107px);
  margin-bottom: 50px;
  margin-top: 47px;
  .user-info-wrap {
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
