<template>
  <van-nav-bar title="卡片" @click-left="reload" @click-right="more">
    <template #left>
      <van-icon name="replay" size="20" />
    </template>
    <template #right>
      <van-icon name="ellipsis" size="20" />
    </template>
  </van-nav-bar>
</template>

<script lang="ts">
import { defineComponent } from "vue";

export default defineComponent({
  name: "Cards",
  setup() {
    const reload = () => {
      console.log("log");
    };
    const more = () => {
      console.log("more");
    };
    return {
      // 返回的数据
      reload,
      more,
    };
  },
});
</script>