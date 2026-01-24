<template>
  <!-- 颜色选择器组件 -->
  <van-nav-bar
    title="选择颜色"
    left-text="选择"
    left-arrow
    @click-left="onClickLeft"
    :placeholder="true"
    :fixed="true"
  />

  <div class="color_wrap">
    <div
      class="color_item"
      v-for="color in colorData"
      :key="color"
      @click="handlerClick($event)"
      :color="color"
      :style="{
        border: `${nowSelectedColor === color ? '1px solid #41b883' : '1px solid #fff'}`,
      }"
    >
      <div
        class="item"
        :color="color"
        :style="{ 'background-color': color }"
      ></div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { toRef, ref, type PropType } from "vue";

// 定义 props
const props = defineProps({
  colorArray: {
    type: Array as PropType<string[]>,
    default: () => []
  },
  selectColor: {
    type: String,
    default: ""
  }
});

// 定义 emits
const emit = defineEmits<{
  (e: "picked", color: string): void;
}>();

// 响应式数据
const colorData = toRef(props, "colorArray");
const nowSelectedColor = ref(props.selectColor);

// 事件处理
const handlerClick = (event: MouseEvent) => {
  const ele = event.target as HTMLElement;
  const color = ele.getAttribute("color") as string;
  nowSelectedColor.value = color;
};

const onClickLeft = () => {
  emit("picked", nowSelectedColor.value);
};
</script>

<style lang="scss" scoped>
.color_wrap {
  min-height: calc(100vh - 46px);
  margin: 0 16px;
  display: grid;
  justify-content: space-between;
  grid-template-columns: repeat(auto-fill, 40px);
  grid-gap: 10px;

  .color_item {
    width: 40px;
    height: 40px;
    display: flex;
    justify-content: center;
    align-items: center;
    .item {
      width: 30px;
      height: 30px;
      margin: 5px;
      border-radius: 5px;
    }

    border-radius: 5px;
  }
}
</style>
