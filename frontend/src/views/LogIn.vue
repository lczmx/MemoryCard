<template>
  <login-singup :containerCls="containerCls"></login-singup>
</template>

<script setup lang="ts">
import { ref } from "vue";
import LoginSingup from "../components/LoginSingup.vue";

const containerCls = ref("");
</script>
