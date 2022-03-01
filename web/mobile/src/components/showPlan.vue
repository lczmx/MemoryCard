<template>
  <!-- 显示复习进度 -->
  <div class="process-wrap">
    <van-progress
      pivot-text=""
      color="#f2826a"
      :percentage="
        Math.round(
          (useCurrentCardPlan(cardRef).reviewTimes /
            useCurrentCardPlan(cardRef).allReviewTimes) *
            100
        )
      "
      stroke-width="5"
    />
  </div>
</template>

<script lang="ts">
import { defineComponent, PropType, ref, toRef } from "vue";
import { ICard } from "@/types";
import { useCurrentCardPlan } from "@/hook";
export default defineComponent({
  name: "ShowPlan",
  props: {
    card: {
      type: Object as PropType<ICard>,
      required: true,
    },
  },
  setup(props) {
    const cardRef = toRef(props, "card");
    return {
      cardRef,
      useCurrentCardPlan,
    };
  },
});
</script>

<style lang="scss" scoped>
.process-wrap {
  height: 5px;
}
</style>
