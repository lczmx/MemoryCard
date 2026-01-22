<template>
  <plan-editor 
  :propTitle="title" 
  :postUrl="url"
  :successText="successText"
  > </plan-editor>
</template>

<script lang="ts">
import { defineComponent, ref } from "vue";

import PlanEditor from "@/components/planEditor.vue";
import { useStore } from "vuex";
export default defineComponent({
  name: "AddPlan",
  components: { PlanEditor },
  setup() {
    const store = useStore();
    const title = ref("新增复习曲线"); // 导航栏标题
    const successText = ref("已创建复习曲线");
    const url = ref(`${store.state.serverHost}/plans/`);

    return {
      // 返回的数据
      title,
      successText,
      url,
    };
  },
});
</script>
