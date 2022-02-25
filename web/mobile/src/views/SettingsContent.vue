<template>
  <van-nav-bar
    :title="store.state.settingsItemPageTitle"
    left-text="返回"
    left-arrow
    @click-left="clickHistoryBack"
    :placeholder="true"
    :fixed="true"
  />
  <router-view></router-view>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import { useStore } from "vuex";
import { useRouter } from "vue-router";

export default defineComponent({
  name: "SettingsContent",

  setup() {
    // ---------- 点击返回
    const router = useRouter();
    const clickHistoryBack = () => {
      router.push({ name: "settings" });
    };
    const store = useStore();

    return {
      clickHistoryBack,
      store,
    };
  },
});
</script>
