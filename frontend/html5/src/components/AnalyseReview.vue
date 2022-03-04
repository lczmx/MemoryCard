<template>
  <analyse-chart :url="url" :title="title"></analyse-chart>
</template>

<script lang="ts">
import { defineComponent, ref } from "vue";
import AnalyseChart from "@/components/AnalyseChart.vue";
import { useStore } from "vuex";
export default defineComponent({
  name: "AnalyseReview",
  components: { AnalyseChart },
  setup() {
    const store = useStore();
    const url = ref(`${store.state.serverHost}/analyse/review`);
    const title = ref("累计复习卡片趋势");

    return {
      // 返回的数据
      url,
      title,
    };
  },
});
</script>
