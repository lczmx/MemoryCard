<!--  统一的添加页面  -->

<template>
  <van-nav-bar
    title="关于本项目"
    left-text="返回"
    left-arrow
    :fixed="true"
    @click-left="backTopPage"
  />
  <router-view></router-view>
</template>

<script lang="ts">
import { defineComponent } from "vue";

export default defineComponent({
  name: "About",
  setup() {
    //   返回上一页
    const backTopPage = () => {
      history.back();
    };
    return {
      // 返回的数据
      backTopPage,
    };
  },
});
</script>
