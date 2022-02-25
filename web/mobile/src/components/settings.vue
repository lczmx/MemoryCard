<template>
  <van-nav-bar title="设置" :fixed="true"> </van-nav-bar>
  <div class="settings_body">
    <div class="user-info-wrap">
      <!-- 是否已经登录 -->
      <div class="uer-login" v-if="!user.username">
        <!-- TODO: 替换 router-link -->
        <van-notice-bar color="#28414a" background="#ecf9ff" left-icon="info-o">
          当前处于游客模式, 你可以<a href="#" class="">登录</a>或<a href="#"
            >注册</a
          >
        </van-notice-bar>
      </div>
      <div class="user-info" else>
        用户信息展示: {{ user.username }}-{{ user.email }}
      </div>
    </div>
    <!-- 第一部分开始 -->
    <!-- 数据分析, 需要登录 -->

    <van-cell-group inset v-if="user.username">
      <van-cell value="" is-link>
        <template #icon>
          <van-icon
            class="iconfont item-icon"
            class-prefix="icon"
            name="settings"
            size="16"
          />
        </template>
        <!-- 使用 title 插槽来自定义标题 -->
        <template #title>
          <span class="custom-title">用户设置</span>
        </template>
      </van-cell>
      <van-cell value="" is-link :to="{ name: 'Plan' }">
        <template #icon>
          <van-icon
            class="iconfont item-icon"
            class-prefix="icon"
            name="fsux_tubiao_fenbuquxiantu"
            size="16"
          />
        </template>
        <!-- 使用 title 插槽来自定义标题 -->
        <template #title>
          <span class="custom-title">复习曲线</span>
        </template>
      </van-cell>
      <van-cell value="" is-link>
        <template #icon>
          <van-icon
            class="iconfont item-icon"
            class-prefix="icon"
            name="tongji"
            size="16"
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
            size="16"
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
            size="16"
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
      <van-cell value="" is-link>
        <template #icon>
          <van-icon
            class="iconfont item-icon"
            class-prefix="icon"
            name="logout"
            size="16"
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
import { defineComponent, ref } from "vue";
import { useRouter } from "vue-router";

export default defineComponent({
  name: "Settings",
  setup() {
    /* 用户相关 */
    // -----------------获取用户数据 开始
    const fake_user = {
      username: "lczmx",
      email: "xxx@example.com",
    };
    const user = ref({});
    user.value = fake_user;

    // -----------------获取用户数据 结束
    // ------------- 跳转到About页面
    const router = useRouter();

    const handlerClickAbout = () => {
      router.push({ name: "About" });
    };
    return {
      // 返回的数据
      user,
      handlerClickAbout,
    };
  },
});
</script>

<style lang="scss">
.settings_body {
  background-color: #f4f3f5;
  padding-top: 10px;
  min-height: calc(100vh - 106px);
  margin-bottom: 50px;
  margin-top: 47px;
  .user-info-wrap {
    .uer-login {
    }
    .user-info {
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
