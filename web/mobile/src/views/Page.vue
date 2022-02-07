<template>
  <!-- 一般的界面 -->
  <!-- 默认 review-->
  <router-view></router-view>

  <van-tabbar v-model="active" router>
    <van-tabbar-item replace to="/" name="review" icon="underway-o">复习</van-tabbar-item>
    <van-tabbar-item replace to="/cards" name="memory" icon="more-o">卡片</van-tabbar-item>
    <van-tabbar-item replace to="/tags" name="tags" icon="label-o">标签</van-tabbar-item>
    <van-tabbar-item replace to="/settings" name="settings" icon="setting-o">设置</van-tabbar-item>


  </van-tabbar>

  

</template>

<script lang="ts">
import { defineComponent, ref } from "vue";

export default defineComponent({
  name: "Page",
  setup() {
    const active = ref("review");

    return {
      active,
    };
  },
});
</script>