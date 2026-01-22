<template>
  <van-nav-bar
    :title="store.state.settingsItemPageTitle"
    left-text="返回"
    left-arrow
    @click-left="clickHistoryBack"
     @click-right="clickGoHome"
    :placeholder="true"
    :fixed="true"
  >
    <template #right>
      <div class="setting-content-right-wrap">
        <van-icon name="wap-home" size="20" />
      </div>
    </template>
  </van-nav-bar>
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
      // router.push({ name: "settings" });
      router.go(-1);
      
    };
    // ------- 返回首页
    const clickGoHome = () => {
      router.push({ name: "settings" });

    }
    const store = useStore();

    return {
      clickHistoryBack,
      store,
      clickGoHome
    };
  },
});
</script>
