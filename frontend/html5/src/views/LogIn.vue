<template>
  <login-singup :containerCls="containerCls"></login-singup>
</template>

<script lang="ts">
import { defineComponent, ref } from "vue";
import LoginSingup from "@/components/LoginSingup.vue";
export default defineComponent({
  name: "Login",
  components: { LoginSingup },
  setup() {
    const containerCls = ref("");
    return {
      // 返回的数据
      containerCls,
    };
  },
});
</script>
