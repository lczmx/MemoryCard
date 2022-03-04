<template>
  <!-- 图标选择器组件 -->
  <van-nav-bar
    title="选择图标"
    left-text="选择"
    left-arrow
    @click-left="onClickLeft"
    :placeholder="true"
    :fixed="true"
  />

  <!-- 使用iconfont的图标 -->
  <div class="icon_wrap">
    <!-- <i class="iconfont icon-check-box"></i> -->

    <i
      :class="`icon_item iconfont ${icon}`"
      v-for="icon in iconData"
      :key="icon"
      :icon="icon"
      @click="handlerClick($event)"
      :style="{ color: `${icon === nowSelectedIcon ? '#41b883' : '#000'}` }"
    ></i>
  </div>
</template>

<script lang="ts">
import { defineComponent, toRef, ref } from "vue";

export default defineComponent({
  name: "IconPicker",
  props: {
    iconArray: {
      type: Array,
    },
    // 默认选中项
    selectIcon: {
      type: String,
      default: "",
    },
  },
  emits: ["picked"],

  setup(props, context) {
    const iconData = toRef(props, "iconArray");
    const nowSelectedIcon = ref(props.selectIcon);
    const handlerClick = (event: MouseEvent) => {
      const ele = event.target as HTMLElement;
      let icon = ele.getAttribute("icon") as string;
      nowSelectedIcon.value = icon;
    };
    const onClickLeft = () => {
      context.emit("picked", nowSelectedIcon.value);
    };
    return {
      // 返回的数据
      handlerClick,
      onClickLeft,
      iconData,
      nowSelectedIcon,
    };
  },
});
</script>

<style lang="scss" scoped>
.icon_wrap {
  min-height: calc(100vh - 46px);
  margin: 0 16px;
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
