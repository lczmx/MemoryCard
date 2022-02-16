<template>
  <!-- 图标选择器组件 -->
  <!-- 使用iconfont的图标 -->
  <div class="icon_wrap">
    <!-- <i class="iconfont icon-check-box"></i> -->

    <i
      :class="`icon_item iconfont ${icon}`"
      v-for="icon in iconData"
      :key="icon"
      :icon="icon"
      @click="handlerClick($event)"

    ></i>
  </div>
</template>

<script lang="ts">
import { defineComponent, toRef } from "vue";

export default defineComponent({
  name: "IconPicker",
  props: {
    iconArray: {
      type: Array,
    },
  },
  emits: ["picked"],

  setup(props, context) {
    const iconData = toRef(props, "iconArray");

    const handlerClick = (event: MouseEvent) => {
      const ele = event.target as HTMLElement;
      let icon = ele.getAttribute("icon") as string;
      context.emit("picked", icon);
    };
    return {
      // 返回的数据
      handlerClick,
      iconData,
    };
  },
});
</script>

<style lang="scss" scoped>
.icon_wrap {
  display: grid;
  justify-content: space-between;
  grid-template-columns: repeat(auto-fill, 40px);
  grid-gap: 10px;

  .icon_item {
    width: 40px;
    height: 40px;
    background-color: #fff;
    color: #000;
    margin-top: 5px;
    border-radius: 5px;
    font-size: 32px;
  }
}
</style>