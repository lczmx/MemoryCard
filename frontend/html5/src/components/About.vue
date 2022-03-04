<!--  统一的添加页面  -->

<template>
  <div class="about-wrap">关于</div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import { useStore } from "vuex";

export default defineComponent({
  name: "About",
  setup() {
    const store = useStore();
    store.commit("changeSettingsPageTitle", "关于");

    return {
      // 返回的数据
    };
  },
});
</script>

<style lang="scss" scoped>
.about-wrap {
  min-height: calc(100vh - 56px);
  background-color: #f3f4f5;
  padding: 10px 16px 0;
}
</style>
