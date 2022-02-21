<template>
  <card-editor 
  :propTitle="title" 
  :postUrl="url"
  :successText="successText"
  > </card-editor>
</template>

<script lang="ts">
import { defineComponent, ref } from "vue";

import CardEditor from "@/components/cardEditor.vue";
import { useStore } from "vuex";
export default defineComponent({
  name: "AddCard",
  components: { CardEditor },
  setup() {
    const store = useStore();
    const title = ref("新增卡片"); // 导航栏标题
    const successText = ref("已创建卡片");
    const url = ref(`${store.state.serverHost}/cards/`);

    return {
      // 返回的数据
      title,
      successText,
      url,
    };
  },
});
</script>
