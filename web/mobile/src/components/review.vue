<template>
  <van-nav-bar title="复习" @click-left="calendar" @click-right="more">
    <template #left>
      <van-icon name="calendar-o" size="20" />
    </template>
    <template #right>
      <van-icon name="ellipsis" size="20" />
    </template>
  </van-nav-bar>
</template>

<script lang="ts">
import { defineComponent } from "vue";

export default defineComponent({
  name: "Review",
  setup() {
    const calendar = () => {
      console.log("点击了日历");
    };
    const more = () => {
      console.log("点击了更多");
    };
    return {
      calendar,
      more,
    };
  },
});
</script>