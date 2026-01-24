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

<script setup lang="ts">
import { toRef, ref, type PropType } from "vue";

// 定义props
interface Props {
  iconArray?: string[];
  selectIcon?: string;
}
const props = defineProps({
  iconArray: {
    type: Array as PropType<string[]>,
    default: () => []
  },
  selectIcon: {
    type: String,
    default: "",
  },
})

const emit = defineEmits<{(e: "picked", icon: string)}>();
// 响应式数据

  const iconData = toRef(props, "iconArray");
  const nowSelectedIcon = ref(props.selectIcon);
// 事件处理

const handlerClick = (event: MouseEvent) => {
  const ele = event.target as HTMLElement;
  let icon = ele.getAttribute("icon") as string;
  nowSelectedIcon.value = icon;
};
const onClickLeft = () => {
  emit("picked", nowSelectedIcon.value);
};

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
