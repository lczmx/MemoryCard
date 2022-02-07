<template>
  <van-nav-bar title="类别" @click-right="more">
    <template #right>
      <van-icon name="ellipsis" size="20" />
    </template>
  </van-nav-bar>
</template>

<script lang="ts">
import { defineComponent } from "vue";

export default defineComponent({
  name: "Tags",
  setup() {
    const more = () => {
      console.log("more");
    };
    return {
      // 返回的数据
      more,
    };
  },
});
</script>