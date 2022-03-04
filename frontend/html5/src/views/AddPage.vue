<!--  统一的添加页面  -->

<template>
  <van-nav-bar
    :title="state.addPageTitle"
    left-text="返回"
    right-text="完成"
    left-arrow
    :fixed="true"
    @click-left="backTopPage"
    @click-right="toSubmitData"
  />
  <router-view></router-view>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import { useStore } from "vuex";
import { Dialog } from "vant";

export default defineComponent({
  name: "AddPage",
  setup() {
    const store = useStore();
    const state = store.state;

    // 初始化submitData为false
    store.commit("changeSubmitData", false);
    // 初始化changeState为false
    store.commit("changeChangeState", false);
    //   返回上一页
    const backTopPage = () => {
      //  本页面数据是否被修改
      if (store.state.changeState) {
        Dialog.confirm({
          title: "注意",
          message: "你尚未保存, 本页面修改的数据将不会被记录",
        })
          .then(() => {
            // 确定返回
            store.commit("changeChangeState", false);
            history.back();
          })
          .catch(() => {
            // on cancel
          });
      } else {
        // 直接返回
        history.back();
      }
    };
    // 提交数据
    const toSubmitData = () => {
      // 修改vuex的数据, 让其提交

      store.commit("changeSubmitData", true);
    };
    return {
      // 返回的数据
      backTopPage,
      state,
      toSubmitData,
    };
  },
});
</script>
