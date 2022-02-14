<template>
  <!-- 一般的界面 -->
  <!-- 默认 review-->
  <router-view></router-view>

  <van-tabbar v-model="active" router :fixed="true">
    <van-tabbar-item replace to="/" name="review" icon="underway-o"
      >复习</van-tabbar-item
    >
    <van-tabbar-item replace to="/cards" name="cards" icon="more-o"
      >卡片</van-tabbar-item
    >
    <van-tabbar-item replace to="/tags" name="tags" icon="label-o"
      >标签</van-tabbar-item
    >
    <van-tabbar-item replace to="/settings" name="settings" icon="setting-o"
      >设置</van-tabbar-item
    >
  </van-tabbar>
</template>

<script lang="ts">
import { defineComponent, ref } from "vue";
import { useRouter } from "vue-router";
export default defineComponent({
  name: "Page",
  setup() {
    // 根据路由的name, 动态修改active
    const router = useRouter();
    const currentRoute = router.currentRoute.value.name;
    const active = ref(currentRoute);

    return {
      active,
    };
  },
});
</script>