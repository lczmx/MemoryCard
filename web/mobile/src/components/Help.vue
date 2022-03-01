<!--  统一的添加页面  -->

<template>帮助</template>

<script lang="ts">
import { defineComponent } from "vue";
import { useStore } from "vuex";

export default defineComponent({
  name: "Help",
  setup() {
    const store = useStore();
    store.commit("changeSettingsPageTitle", "关于");

    return {
      // 返回的数据
    };
  },
});
</script>
