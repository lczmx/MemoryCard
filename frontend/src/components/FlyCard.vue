<template>
  <div
    class="card-review-container"
    :style="{ width: cardWidth + 'px', height: cardHeight + 'px' }"
  >
    <div
      class="card"
      style="z-index: 13"
      :style="{
        width: cardWidth + 'px',
        height: cardHeight + 'px',
        left: left + 'px',
        top: top + 'px',
        'border-radius': borderRadius + 'px',
        backgroundColor: cardBgColor,
      }"
      :class="{
        animation: isAnimating,
        shadowEffect: hasShadow,
        boderEffect: hasBorder,
      }"
      @touchstart="touchStart"
      @touchmove="touchMove"
      @touchcancel="touchCancel"
      @touchend="touchCancel"
    >
      <slot name="firstCard"></slot>
    </div>
    <div
      class="card"
      style="z-index: 12"
      :style="{
        width: cardWidth - 4 + 'px',
        height: cardHeight - 9 + 'px',
        left: left2 + 'px',
        top: top2 + 'px',
        'border-radius': borderRadius + 'px',
        backgroundColor: cardBgColor,
      }"
      :class="{
        animation: isAnimating,
        shadowEffect: hasShadow,
        boderEffect: hasBorder,
      }"
    >
      <slot name="secondCard"></slot>
    </div>
    <div
      class="card"
      style="z-index: 11"
      :style="{
        width: cardWidth - 8 + 'px',
        height: cardHeight - 18 + 'px',
        left: left3 + 'px',
        top: top3 + 'px',
        'border-radius': borderRadius + 'px',
        backgroundColor: cardBgColor,
      }"
      :class="{
        animation: isAnimating,
        shadowEffect: hasShadow,
        boderEffect: hasBorder,
      }"
    >
      <slot name="thirdCard"></slot>
    </div>
    <div
      class="card"
      style="z-index: 10"
      :style="{
        width: cardWidth - 12 + 'px',
        height: cardHeight - 27 + 'px',
        left: left4 + 'px',
        top: top4 + 'px',
        'border-radius': borderRadius + 'px',
        backgroundColor: cardBgColor,
        opacity: opacity4,
      }"
      :class="{
        animation: isAnimating,
        shadowEffect: hasShadow,
        boderEffect: hasBorder,
      }"
    ></div>
  </div>
</template>

<script setup lang="ts">
import useTouch from "../hook/touch";

// 定义 props
const props = defineProps<{
  // 正常卡片宽度
  cardWidth?: number;
  // 正常卡片高度
  cardHeight?: number;
  // 卡片层叠的横向边距
  leftPad?: number;
  // 卡片层叠的纵向边距
  topPad?: number;
  // 卡片背景色
  cardBgColor?: string;
  // 卡片拖拽方向
  dragDirection?: string; //all,vertical,horizontal
  // 卡片的圆角弧度
  borderRadius?: number;
  // 卡片触发飞卡效果的距离
  throwTriggerDistance?: number;
  // 飞卡的移动距离
  throwDistance?: number;
  // 是否开启卡片描边效果
  hasBorder?: boolean;
  // 是否开启阴影效果
  hasShadow?: boolean;
}>();

// 定义 emits
const emit = defineEmits<{
  (e: "onDragStart"): void;
  (e: "onDragMove", obj: any): void;
  (e: "onDragStop", obj: any): void;
  (e: "onThrowFail"): void;
  (e: "onThrowStart"): void;
  (e: "onThrowDone"): void;
}>();

// 使用 touch hook
const touchState = useTouch(props, {
  onDragStart: () => emit("onDragStart"),
  onDragMove: (obj) => emit("onDragMove", obj),
  onDragStop: (obj) => emit("onDragStop", obj),
  onThrowFail: () => emit("onThrowFail"),
  onThrowStart: () => emit("onThrowStart"),
  onThrowDone: () => emit("onThrowDone"),
});

// 暴露 touchState 中的所有属性
defineExpose(touchState);
</script>

<style lang="scss" scoped>
.card-review-container {
  position: relative;
  .card {
    position: absolute;
    overflow: hidden;
  }
  .card.boderEffect {
    border: 1px solid #ccc;
  }
  .card.shadowEffect {
    box-shadow: 0px 4px 20px rgba(0, 0, 0, 0.3);
  }
  .card.animation {
    transition: opacity 0.4s ease-out, left 0.4s ease-out, top 0.4s ease-out,
      width 0.4s ease-out, height 0.4s ease-out;
  }
}
</style>
