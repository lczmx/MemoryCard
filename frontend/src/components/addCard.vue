<template>
  <card-editor 
  :propTitle="title" 
  :postUrl="url"
  :successText="successText"
  > </card-editor>
</template>

<script setup lang="ts">
import { ref } from "vue";

import CardEditor from "../components/cardEditor.vue";
import { useStore } from "vuex";

const store = useStore();
const title = ref("新增卡片"); // 导航栏标题
const successText = ref("已创建卡片");
const url = ref(`${store.state.serverHost}/cards`);
</script>
