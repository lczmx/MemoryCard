<!--  统一的添加页面  -->

<template>
  <div class="help-wrap">
    <div class="help-item">
      <van-cell-group inset>
        <van-cell title="如何创建卡片" is-link />
      </van-cell-group>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import { useStore } from "vuex";

export default defineComponent({
  name: "Help",
  setup() {
    const store = useStore();
    store.commit("changeSettingsPageTitle", "帮助中心");

    return {
      // 返回的数据
    };
  },
});
</script>

<style lang="scss" scoped>
.help-wrap {
  min-height: calc(100vh - 56px);
  background-color: #f3f4f5;
  padding-top: 10px;
  .help-item {
    margin-bottom: 10px;
  }
}
</style>
