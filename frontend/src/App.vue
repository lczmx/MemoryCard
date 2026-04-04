<template>
  <router-view />
</template>

<script setup lang="ts">
import { useStore } from "vuex";

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
console.log("App ");
</script>
