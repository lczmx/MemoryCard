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

<script setup lang="ts">
import { toRef } from "vue";
import { ICard } from "../types";
import { useCurrentCardPlan } from "../hook";

const props = defineProps<{
  card: ICard;
}>();

const cardRef = toRef(props, "card");
</script>

<style lang="scss" scoped>
.process-wrap {
  height: 5px;
}
</style>
