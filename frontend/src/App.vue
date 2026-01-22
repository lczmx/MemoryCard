<template>
  <router-view />
</template>

<script lang="ts">
import { defineComponent } from "vue";
import { useStore } from "vuex";
export default defineComponent({
  name: "App",
  setup() {
    // 动态设置后端host
    /*
    2.window.location.protocol（协议）
            结果：http
    4.window.location.hostname（域名）

    */
    const protocol = window.location.protocol;
    const hostname = window.location.hostname;

    const store = useStore();
    store.commit(
      "setServiceHost",
      `${protocol}//${hostname}`
    );
    console.log("App ")
    return {
      // 返回的数据
    };
  },
});
</script>
