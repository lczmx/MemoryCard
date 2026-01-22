<template>
  <!-- 先loading -->
  <div class="loading_wrap" v-if="loading">
    <van-loading color="#1989fa" />
  </div>
  <plan-editor
    v-else
    :propTitle="title"
    :postUrl="url"
    :successText="successText"
    :planTitle="planTitle"
    :planPlans="planPlans"
  >
  </plan-editor>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from "vue";
import { useStore } from "vuex";
import { useRouter } from "vue-router";
import { Toast } from "vant";

import { IPlan } from "@/types";
import { getDataOfOne } from "@/utils/request";

import PlanEditor from "@/components/planEditor.vue";
export default defineComponent({
  name: "EditorPlan",
  components: { PlanEditor },
  setup() {
    const router = useRouter();
    const store = useStore();

    const { pid } = router.currentRoute.value.params;
    const loading = ref(true);
    const successText = ref("已修改复习曲线");

    // -------- 初始化数据
    const title = ref("编辑复习曲线"); // 导航栏标题
    const planTitle = ref(""); // 曲线名
    const planPlans = ref<number[]>([]); // 曲线名

    const url = ref(`${store.state.serverHost}/plans/${pid}`);

    const config = {
      url: url.value,
    };

    const getPlanData = () => {
      getDataOfOne<IPlan>(config, false)
        .then((response) => {
          planTitle.value = response.title;
          if (!planPlans.value) return;
          response.content.split("-").forEach((sec) => {
            planPlans.value.push(Number(sec));
          });

          loading.value = false;
        })
        .catch(() => {
          Toast.fail("编辑复习曲线失败");
          router.go(-1); // 返回上一页
        });
    };
    onMounted(() => {
      getPlanData();
    });

    return {
      loading,
      title,
      planTitle,
      planPlans,
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
