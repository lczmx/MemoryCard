<template>
  <!-- 显示复习进度 -->
  <div class="process-wrap">
    <van-progress
      pivot-text=""
      color="#f2826a"
      :percentage="percentage"
      stroke-width="5"
    />
  </div>
</template>

<script lang="ts">
import { defineComponent, PropType, ref } from "vue";
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
    const active = ref(1);
    const currentCardPlan = useCurrentCardPlan(props.card);

    const pivotText = `${currentCardPlan.reviewTimes} / ${currentCardPlan.allReviewTimes}`;
    const percentage = Math.round(
      (currentCardPlan.reviewTimes / currentCardPlan.allReviewTimes) * 100
    );

    return {
      active,
      pivotText,
      percentage,
    };
  },
});
</script>

<style lang="scss" scoped>
.process-wrap {
  height: 5px;
}
</style>
