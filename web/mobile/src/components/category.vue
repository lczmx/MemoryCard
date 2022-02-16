
<template>
  <van-nav-bar :fixed="true" title="类别" @click-right="more">
    <template #right>
      <!-- 弹出层 -->
      <van-popover
        v-model:show="showPopover"
        :actions="actions"
        :show-arrow="false"
        :offset="[-40, 0]"
        class="popover"
        @select="onSelect"
      >
        <template #reference>
          <van-icon name="ellipsis" size="20" />
        </template>
      </van-popover>
    </template>
  </van-nav-bar>

  <!-- 标签 -->
  <div
    class="category_body"
    ref="container"
    v-touch:swipe.bottom="handlerShowAddCategoryBtn"
    v-touch:swipe.top="handlerHideAddCategoryBtn"
  >
    <!-- 加载框 -->
    <van-loading color="#1989fa" v-if="!data" />

    <van-cell-group
      v-else
      inset
      v-for="item in data.data"
      :key="item.id"
      class="cell_item"
      :style="{ 'background-color': item.color }"
    >
      <van-cell center title-class="content_item" label-class="content_date">
        <template #icon>
          <van-icon
            :name="item.icon"
            class="left-icon"
            size="24"
            color="#fff"
          />
        </template>
        <template #title>
          <div
            class="van-ellipsis item-title"
            :tid="item.id"
            v-touch:hold="touchHoldHandler"
          >
            {{ item.name }}
          </div>
        </template>
        <template #right-icon>
          <!-- 右边图标 (星标) -->

          <van-icon
            v-if="item.isStar"
            class="iconfont"
            class-prefix="icon"
            name="favorfill"
            size="24"
            color="#eefd6a"
          />
          <van-icon
            v-else
            class="iconfont"
            class-prefix="icon"
            name="favor"
            size="24"
            color="#fff"
          />
        </template>
      </van-cell>
    </van-cell-group>
    <!-- 添加分类的btn -->
    <!-- 上滑进入 -->
    <transition name="van-slide-up">
      <div class="addCategoryBtnWrap" v-show="showAddCategoryBtnState">

        <van-button icon="plus" type="primary" round  to="/add/category"></van-button>

      </div>
    </transition>
  </div>
  <!-- 动作面板 -->
  <van-action-sheet
    v-model:show="showCategoryActionSheet"
    :actions="categoryActions"
    cancel-text="取消"
    close-on-click-action
    @select="onSelectCategoryActionSheet"
    @cancel="onCancelCategoryActionSheet"
  />
</template>

<script lang="ts">
import { defineComponent, ref } from "vue";
import { PopoverAction, ActionSheetAction } from "vant";
import { useToggle } from "@vant/use";

import axios from "axios";

export default defineComponent({
  name: "Category",

  setup() {
    const data = ref("");
    /* ----- 更多开始 --------- */
    const showPopover = ref(false);
    const more = () => {
      showPopover.value = true;
      console.log("点击了更多");
    };

    // 弹框选项
    const actions = [
      { text: "排序", icon: " iconfont icon-sorting" },
      { text: "只看星标", icon: " iconfont icon-favor" },
      { text: "选择标签", icon: " iconfont icon-select" },
    ];
    // 弹框选项选中回调
    const onSelect = (action: PopoverAction, index: number) => {
      console.log(action, index);
    };
    /* ----- 更多结束 --------- */
    /* ----- 长按开始 --------- */
    const showCategoryActionSheet = ref(false);
    let tid: number | null = null;
    const categoryActions = [
      { name: "编辑" },
      { name: "删除", color: "red", subname: "删除后无法撤销" },
    ];
    const touchHoldHandler = (event: MouseEvent) => {
      // 使用类型转换
      const targetElement = event.target as HTMLElement;
      tid = Number(targetElement.getAttribute("tid"));

      showCategoryActionSheet.value = true;
      // 处理长按, 弹出提示
    };
    const onCancelCategoryActionSheet = () => {
      // 取消后, tid设置null
      tid = null;
    };
    const onSelectCategoryActionSheet = (
      action: ActionSheetAction,
      index: number
    ) => {
      if (typeof tid == "number") {
        switch (index) {
          case 0:
            editCategory(tid);
            break;
          case 1:
            deleteCategory(tid);
            break;
        }
      }
    };
    const editCategory = (id: number) => {
      // TODO
      console.log("editCategory", id);
    };
    const deleteCategory = (id: number) => {
      // TODO
      console.log("deleteCategory", id);
    };

    /* ----- 长按结束 --------- */
    /* ----- 添加分类开始 --------- */
    const container = ref(null);

    const [showAddCategoryBtnState, toggleAddCategoryBtn] = useToggle(true);
    const handlerShowAddCategoryBtn = () => {
      // 显示
      if (showAddCategoryBtnState.value == false) {
        toggleAddCategoryBtn();
      }
    };
    const handlerHideAddCategoryBtn = () => {
      // 隐藏
      if (showAddCategoryBtnState.value == true) {
        toggleAddCategoryBtn();
      }
    };
    /* ----- 添加分类结束 --------- */

    axios({
      method: "get",
      url: "http://localhost:8080/data/category/category.json",
    }).then((response) => {
      data.value = response.data;
    });

    console.log(data);
    return {
      more,
      showPopover,
      data,
      onSelect,
      actions,
      touchHoldHandler,
      showCategoryActionSheet,
      categoryActions,
      onSelectCategoryActionSheet,
      onCancelCategoryActionSheet,
      container,
      handlerShowAddCategoryBtn,
      handlerHideAddCategoryBtn,
      showAddCategoryBtnState,
    };
  },
});
</script>


<style lang="scss">
.category_body {
  background-color: #f4f3f5;
  min-height: calc(100vh - 106px);
  margin-bottom: 50px;
  padding-top: 56px;
  padding-bottom: 10px;
  position: relative;
  .cell_item {
    margin-bottom: 10px;
    // 自动生成van-cell
    .van-cell {
      // 修改默认的白色背景
      background-color: unset;
      .content_item {
        justify-content: flex-start;
        display: flex;
        flex-direction: column;
        margin-left: 15px;
        .item-category {
          display: flex;
          font-size: 8px;
        }
        .item-title {
          font-size: 16px;
          font-weight: 600;
          display: flex;
          color: #fff;
        }
        .content_date {
          color: #8f8e90;
          display: flex;
        }
      }
    }

    .swipe_right_wrap {
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;

      // height: 66px;
      margin-right: 5px;
      .swipe_right_btn {
        margin-bottom: 5px;
      }
    }
  }
  .addCategoryBtnWrap {
    position: fixed;
    bottom: 80px;
    right: 30px;
  }
}
</style>
