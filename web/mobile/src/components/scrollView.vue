<!-- 触底事件组件 -->
<!-- 事件:scrollToLower -->
<!-- 插槽:content -->

<template>
  <div>
    <slot name="content"> </slot>
    <!-- 标记底部 -->
    <p class="lower" ref="target"></p>
  </div>
</template>

<script lang="ts">
import { useIntersectionObserver } from "@vueuse/core";
import { defineComponent, reactive, ref, watch, onMounted } from "vue";

export default defineComponent({
  name: "ScrollView",
  emits: ["scrollToLower"],
  setup(props, { emit }) {
    const target = ref(null);

    useIntersectionObserver(target, ([{ isIntersecting }], observerElement) => {
      if (isIntersecting) {
        //   触底了, 触发事件
        console.log("scrollToLowerscrollToLowerscrollToLower");
        emit("scrollToLower");
      }
    });
    return { target };
  },
});
</script>
<style lang="scss" scoped>
.lower {
  visibility: hidden;
  width: 1px;
  height: 1px;
}
</style>
