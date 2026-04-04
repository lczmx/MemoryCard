<template>
  <category-editor
    propTitle="添加类别"
    successText="已创建类别"
    :postUrl="url"
  ></category-editor>
</template>

<script setup lang="ts">
import { ref } from "vue";
import { useStore } from "vuex";

import CategoryEditor from "../components/categoryEditor.vue";

const store = useStore();
const url = ref(`${store.state.serverHost}/category`);
</script>
