<template>
  <!-- 先loading -->
  <div class="loading_wrap" v-if="loading">
    <van-loading color="#1989fa" />
  </div>
  <card-editor
    v-else
    :propTitle="title"
    :propCardTitle="cardTitle"
    :propCategory="category"
    :propCategoryText="categoryText"
    :propSummary="summary"
    :propSummaryText="summaryText"
    :propDescription="description"
    :propDescriptionText="descriptionText"
    :postUrl="url"
    :successText="successText"
  >
  </card-editor>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from "vue";
import { useStore } from "vuex";
import { useRouter } from "vue-router";

import { ICard, ICategory } from "@/types";
import { getDataOfOne } from "@/utils/request";

import CardEditor from "@/components/cardEditor.vue";
export default defineComponent({
  name: "EditorCard",
  components: { CardEditor },
  setup() {
    const router = useRouter();
    const store = useStore();

    const { cid } = router.currentRoute.value.params;
    const loading = ref(true);
    const successText = ref("已修改卡片");

    // -------- 初始化数据
    const title = ref("编辑卡片"); // 导航栏标题
    const cardTitle = ref(""); // 卡片名

    const url = ref(`${store.state.serverHost}/cards/${cid}`);
    const category = ref<ICategory>();
    const categoryText = ref("");
    const summary = ref("");
    const summaryText = ref("");
    const description = ref("");
    const descriptionText = ref("");

    const config = {
      url: url.value,
    };

    const getCardData = () => {
      getDataOfOne<ICard>(config, false).then((response) => {
        cardTitle.value = response.title;
        category.value = response.category;
        categoryText.value = response.category.name;
        // 不能用<string>, eslint报错
        if (response.summary && response.description) {
          summary.value = response.summary;
          summaryText.value = summary.value.replace(/<\/?.+?>/g, "");
          description.value = response.description;
          descriptionText.value = description.value.replace(/<\/?.+?>/g, "");
        }

        loading.value = false;
      });
    };
    onMounted(() => {
      getCardData();
    });

    return {
      loading,
      title,
      cardTitle,
      category,
      categoryText,
      summary,
      summaryText,
      description,
      descriptionText,
      url,
      successText,
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
