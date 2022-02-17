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
  <van-list
    v-model:loading="loading"
    :finished="!status.hasMore"
    @load="getCategoryData"
    loading-text="加载中..."
  >
    <template #finished>
      <div class="finished-text-wrap">
        <p>没有更多数据了</p>
      </div>
    </template>
    <template #loading>
      <div class="loading-text-wrap">
        <van-loading  color="#1989fa" />
      </div>
    </template>
    <div
      class="category_body van-clearfix"
      ref="container"
      v-touch:swipe.bottom="handlerShowAddCategoryBtn"
      v-touch:swipe.top="handlerHideAddCategoryBtn"
    >
      <van-cell-group
        inset
        v-for="(item, index) in data"
        :key="item.id"
        class="cell_item"
        :style="{ 'background-color': item.color }"
      >
        <van-cell center title-class="content_item" label-class="content_date">
          <template #icon>
            <!-- 使用iconfont -->
            <i
              :class="`left-icon iconfont ${item.icon}`"
              :style="{ 'font-size': 24, color: '#fff' }"
            >
            </i>
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
            <div
              class="right-icon-wrap"
              @click="handlerToggleStarStatus($event, index, item.id)"
            >
              <van-icon
                v-show="item.isStar"
                class="iconfont star_true"
                class-prefix="icon"
                name="favorfill"
                size="24"
              />
              <van-icon
                v-show="!item.isStar"
                class="iconfont star_false"
                class-prefix="icon"
                name="favor"
                size="24"
              />
            </div>
          </template>
        </van-cell>
      </van-cell-group>
    </div>
  </van-list>
  <!-- 添加分类的btn -->
  <!-- 上滑进入 -->
  <transition name="van-slide-up">
    <div class="addCategoryBtnWrap" v-show="showAddCategoryBtnState">
      <van-button
        icon="plus"
        type="primary"
        round
        to="/add/category"
        color="#35495e"
      ></van-button>
    </div>
  </transition>

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
import { useStore } from "vuex";
import { useToggle } from "@vant/use";
import { getDataOfPage, postCreateData } from "@/utils/request";
import { ICategory, IStar } from "@/types";
import { Method } from "axios";

export default defineComponent({
  name: "Category",

  setup() {
    const data = ref<ICategory[]>([]);
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
    /* ----- 获取分类数据 --------- */
    const loading = ref(false);
    const finished = ref(false);
    const store = useStore();
    let status = {
      method: "GET" as Method,
      limit: 10,
      offset: 0,
      hasMore: true,
    };
    const config = {
      url: `${store.state.serverHost}/category/`,
    };

    const getCategoryData = () => {
      getDataOfPage<ICategory>(status, config, false).then((response) => {
        data.value = [...data.value, ...response];

        loading.value = false;
        if (!status.hasMore) {
          finished.value = true;
        }
      });
    };

    // ---------- 点击星标后
    const handlerToggleStarStatus = (
      event: MouseEvent,
      index: number,
      cid: number
    ) => {
      const ele = event.target as HTMLElement;

      let starStatus = ele.classList.contains("star_true") ? true : false;

      const postConfig = {
        method: "post" as Method,
        url: `${store.state.serverHost}/category/${cid}/star`,
        data: {
          isStar: starStatus,
        },
      };

      postCreateData<IStar, IStar>(postConfig, false).then((response) => {
        data.value[index].isStar = response.isStar;
      });
    };

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
      handlerToggleStarStatus,
      showAddCategoryBtnState,
      loading,
      status,
      getCategoryData,
    };
  },
});
</script>

<style lang="scss">
.finished-text-wrap {
  padding-bottom: 50px;
  background-color: #f4f3f5;
  p {
    margin: 0;
  }
}
.loading-text-wrap {
  // 加载中...
  background-color: #f4f3f5;
  color: #fff;
}
.category_body {
  background-color: #f4f3f5;
  min-height: calc(100vh - 156px);
  padding-top: 56px;
  .cell_item {
    margin-bottom: 10px;
    .right-icon-wrap {
      .star_true {
        color: #eefd6a;
      }
      .star_false {
        color: #fff;
      }
    }
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
}
.addCategoryBtnWrap {
  position: fixed;
  bottom: 80px;
  right: 30px;
}
</style>
