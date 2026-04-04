<template>
  <analyse-chart :url="url" :title="title"></analyse-chart>
</template>

<script setup lang="ts">
import { ref } from "vue";
import AnalyseChart from "../components/AnalyseChart.vue";
import { useStore } from "vuex";

const store = useStore();
const url = ref(`${store.state.serverHost}/analyse/create`);
const title = ref("累计创建卡片趋势");
</script>
