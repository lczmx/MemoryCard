<template>
  <!-- 先loading -->
  <div class="loading_wrap" v-if="loading">
    <van-loading color="#1989fa" />
  </div>

  <category-editor
    v-else
    propTitle="修改类别"
    successText="已修改类别"
    :postUrl="url"
    :propName="name"
    :propIcon="icon"
    :propColor="color"
    :propPlan="plan"
    :propPlanText="planText"
  ></category-editor>
</template>
<script lang="ts">
import { defineComponent, ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import { useStore } from "vuex";

import { getDataOfOne } from "@/utils/request";
import { ICategory } from "@/types";

import CategoryEditor from "@/components/categoryEditor.vue";
export default defineComponent({
  name: "EditorCategory",
  components: { CategoryEditor },
  setup() {
    const store = useStore();
    // 修改标题
    store.commit("changePageTitle", "");

    const router = useRouter();
    const { cid } = router.currentRoute.value.params;
    // ---------- 一些初始化数据
    const loading = ref(true);
    const name = ref<string>();
    const icon = ref<string>();
    const color = ref<string>();
    const plan = ref<number>();
    const planText = ref<string>();
    const url = ref(`${store.state.serverHost}/category/${cid}`);
    // ------------- 获取当前类别的数据
    const config = {
      url: url.value,
    };

    const getCategoryData = () => {
      getDataOfOne<ICategory>(config, false).then((response) => {
        name.value = response.name;
        icon.value = response.icon;
        color.value = response.color;
        plan.value = response.plan.id;
        planText.value = response.plan.title;
        loading.value = false;
      });
    };
    onMounted(() => {
      getCategoryData();
    });
    return {
      loading,
      url,
      name,
      icon,
      color,
      plan,
      planText,
    };
  },
});
</script>

<style lang="scss" scoped>
.loading_wrap {
  margin-top: 46px;
  height: calc(100vh - 46px);
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>
