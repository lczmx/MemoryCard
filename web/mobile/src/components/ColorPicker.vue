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

<script lang="ts">
import { defineComponent, toRef, ref } from "vue";

export default defineComponent({
  name: "ColorPicker",
  props: {
    colorArray: {
      type: Array,
    },
    // 默认选中项
    selectColor: {
      type: String,
      default: "",
    },
  },
  emits: ["picked"],

  setup(props, context) {
    const colorData = toRef(props, "colorArray");
    const nowSelectedColor = ref(props.selectColor);
    const handlerClick = (event: MouseEvent) => {
      const ele = event.target as HTMLElement;
      let color = ele.getAttribute("color") as string;
      nowSelectedColor.value = color;
    };
    const onClickLeft = () => {
      context.emit("picked", nowSelectedColor.value);
    };
    return {
      // 返回的数据
      handlerClick,
      onClickLeft,
      colorData,
      nowSelectedColor,
    };
  },
});
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
