<template>
  <!-- 用于popup -->
  <!-- 有指定的高度 -->
  <van-nav-bar
    :title="title"
    left-text="完成"
    :fixed="true"
    left-arrow
    @click-left="clickSuccessBtn"
  />
  <div class="container">
    <slot name="content"> </slot>
  </div>
</template>

<script lang="ts">
import { defineComponent, nextTick } from "vue";
import { watch } from "vue";
import { useWindowSize } from "@vant/use";

export default defineComponent({
  name: "PopupEditor",
  props: {
    title: {
      type: String,
      default: "title",
    },
  },
  emits: ["onSuccess"],
  setup(props, { emit }) {
    const clickSuccessBtn = () => {
      // 触发onSuccess事件
      emit("onSuccess");
    };

    const { width: windowWidth, height: windowHeight } = useWindowSize();

    watch([windowWidth, windowHeight], ([_, h]) => {
      console.log("reset");

      setProseMirrorHeight(h);
    });
    // 计算toolbar高度
    // 得出编辑框的高度
    const setProseMirrorHeight = (wHeight: number) => {
      let toolBarNodes = document.querySelectorAll(".toolbar");
      let toolBarNodeHeight: number;
      toolBarNodes.forEach((toolBarNode) => {
        // 计算元素高度
        const { height } = toolBarNode.getBoundingClientRect();
        if (height) {
          // 不能为0
          toolBarNodeHeight = height;
          return;
        }
      });

      let proseMirrorNodes = document.querySelectorAll(".ProseMirror");

      proseMirrorNodes.forEach((proseMirrorNode) => {
        // 设置top
        const nowHeight = toolBarNodeHeight + 46;
        const ele = proseMirrorNode as HTMLElement;
        ele.style.top = String(nowHeight) + "px";
      });
    };
    nextTick(() => {
      // 可以使用回调函数的写法
      // 这个函数中DOM必定渲染完成
      setProseMirrorHeight(windowHeight.value);
    });

    return {
      // 返回的数据

      clickSuccessBtn,
    };
  },
});
</script>
<style lang="scss">
.container {
  margin: 0 5px;
  height: calc(100vh - 46px);
  #text-editor {
    margin-top: 46px;
    border: unset;
    .ProseMirror {
      padding: 10px;
      margin: 5px;
      overflow: scroll;
      position: fixed;
      bottom: 0;
      width: calc(100% - 35px);
      ul > li {
        list-style: square;
        margin: 20px;
        padding: unset;
      }
      ol > li {
        list-style: demical;
        margin: 20px;
        padding: unset;
      }
    }
  }
}
</style>
