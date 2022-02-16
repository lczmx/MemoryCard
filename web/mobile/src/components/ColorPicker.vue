<template>
  <!-- 颜色选择器组件 -->
  <div class="color_wrap">
    <div
      class="color_item"
      v-for="color in colorData"
      :key="color"
      :style="{ 'background-color': color }"
      @click="handlerClick($event)"
      :color="color"
    ></div>
  </div>
</template>

<script lang="ts">
import { defineComponent, toRef } from "vue";

export default defineComponent({
  name: "ColorPicker",
  props: {
    colorArray: {
      type: Array,
    },
  },
  emits: ["picked"],

  setup(props, context) {
    const colorData = toRef(props, "colorArray");

    const handlerClick = (event: MouseEvent) => {
      const ele = event.target as HTMLElement;
      let color = ele.getAttribute("color") as string;
      context.emit("picked", color);
    };
    return {
      // 返回的数据
      handlerClick,
      colorData,
    };
  },
});
</script>

<style lang="scss" scoped>
.color_wrap {
  display: grid;
  justify-content: space-between;
  grid-template-columns: repeat(auto-fill, 40px);
  grid-gap: 10px;

  .color_item {
    width: 40px;
    height: 40px;
    margin-top: 5px;
    border-radius: 5px;
  }
}
</style>