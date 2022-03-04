<template>
  <category-editor
    propTitle="添加类别"
    successText="已创建类别"
    :postUrl="url"
  ></category-editor>
</template>

<script lang="ts">
import { defineComponent, ref } from "vue";
import { useStore } from "vuex";

import CategoryEditor from "@/components/categoryEditor.vue";
export default defineComponent({
  name: "AddCategory",
  components: { CategoryEditor },
  setup() {
    const store = useStore();
    const url = ref(`${store.state.serverHost}/category/`);
    return { url };
  },
});
</script>
