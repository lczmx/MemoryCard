<template>
  <van-nav-bar
    :title="selectMode ? '' : '复习'"
    :fixed="true"
    @click-left="() => (selectMode ? (showCal = false) : (showCal = true))"
    @click-right="
      () => (selectMode ? handlerClickSuccessReview() : (showPopover = true))
    "
  >
    <template #left>
      <div class="select-mode-tool-wrap" v-if="selectMode">
        <div class="tool-item" @click.stop="handlerClickCancel">取消</div>
        <div class="tool-item" @click.stop="handlerClickSelectInverse">
          反选
        </div>
        <div class="tool-item" @click.stop="handlerClickSelectAll">全选</div>
      </div>
      <van-icon
        v-else
        Inverse
        class="iconfont"
        class-prefix="icon"
        name="rili"
        size="16"
      />
    </template>
    <template #right>
      <div v-if="selectMode" class="select-mode-tool-success-review">
        完成复习
      </div>
      <!-- 弹出层 -->
      <van-popover
        v-else
        v-model:show="showPopover"
        :actions="actions"
        :show-arrow="false"
        :offset="[-40, 0]"
        class="popover"
        @select="onSelect"
      >
        <template #reference>
          <van-icon
            v-show="!showPopover"
            size="20"
            class="iconfont"
            class-prefix="icon"
            name="ellipsis-h-solid"
          />
          <van-icon
            v-show="showPopover"
            size="20"
            class="iconfont"
            class-prefix="icon"
            name="ellipsis-v-solid"
          />
        </template>
      </van-popover>
    </template>
  </van-nav-bar>
  <!-- 日历 -->
  <van-calendar
    color="#1989fa"
    :min-date="
      // 前60天
      new Date(
        new Date(new Date().toLocaleDateString()).getTime() -
          6 * 30 * 24 * 3600 * 1000
      )
    "
    :max-date="new Date()"
    v-model:show="showCal"
    @confirm="handlerConfirmCal"
  />

  <van-list
    v-model:loading="loading"
    :finished="finished"
    @load="getReviewData"
    loading-text="加载中..."
  >
    <template #loading>
      <div class="loading-text-wrap">
        <van-loading color="#1989fa" />
      </div>
    </template>
    <van-empty
      description="没有需要复习的卡片"
      :style="{ backgroundColor: '#f4f3f5' }"
      v-if="!loading && data.length <= 0"
      class="review_body_empty"
    />
    <!-- 复习页面的主体 -->
    <div class="review_body van-clearfix" v-else>
      <van-checkbox-group v-model="checkedCard" ref="checkboxGroupRef">
        <van-cell-group
          inset
          v-for="(item, index) in data"
          :key="item.id"
          class="cell_item"
          @click="
            () =>
              selectMode
                ? toggleCardCheckboxStatus(index)
                : handlerClickReviewBody(item.id)
          "
        >
          <!-- 选择模式禁用滑动 -->
          <van-swipe-cell :disabled="selectMode">
            <van-cell
              center
              title-class="content_item"
              label-class="content_date"
            >
              <template #icon>
                <!-- 使用iconfont -->
                <i
                  :class="`left-icon iconfont ${item.category.icon}`"
                  :style="{ 'font-size': '24px', color: item.category.color }"
                  class="left-icon"
                >
                </i>
              </template>
              <template #title>
                <div class="van-ellipsis item-title">{{ item.title }}</div>
              </template>
              <template #label>
                <span class="van-ellipsis item-category">
                  <van-tag :color="item.category.color" text-color="#fff">{{
                    item.category.name
                  }}</van-tag>
                </span>
              </template>
              <!-- 右边复选框 -->
              <template #right-icon>
                <van-checkbox
                  v-show="selectMode"
                  :name="item.id"
                  :ref="(el) => (checkboxRefs[index] = el)"
                  @click.stop
                />
              </template>
            </van-cell>
            <template #right>
              <!-- 右边滑动区域 -->
              <div class="swipe_right_wrap">
                <van-button
                  class="swipe_right_btn"
                  icon="success"
                  type="success"
                  round
                  :block="true"
                  @click="handlerSuccessBtn(item.id)"
                  :cid="item.id"
                />
                <van-button
                  class="swipe_right_btn"
                  icon="edit"
                  type="primary"
                  round
                  :block="true"
                  @click="handlerEditBtn(item.id)"
                  :cid="item.id"
                />
              </div>
            </template>
          </van-swipe-cell>
        </van-cell-group>
      </van-checkbox-group>
    </div>
  </van-list>
</template>

<script lang="ts">
import { defineComponent, ref, watch } from "vue";
import { PopoverAction, Toast } from "vant";
import { useWindowSize } from "@vant/use";
import type { CheckboxInstance, CheckboxGroupInstance } from "vant";
import { useStore } from "vuex";
import { useRouter } from "vue-router";
import { Method } from "axios";
import { ICard, IBatchReviewPostData } from "@/types";
import dayjs from "dayjs";
import {
  getDataOfPage,
  postCreateData,
  getReviewCardByDateData,
} from "@/utils/request";

export default defineComponent({
  name: "Review",

  setup() {
    const store = useStore();
    const showPopover = ref(false);
    const showCal = ref(false); // 显示日历
    // 弹框选项

    const actions = [
      { text: "今日卡片", icon: " iconfont icon-jinri" },
      { text: "筛选类别", icon: " iconfont icon-fenlei" },
      { text: "选择卡片", icon: " iconfont icon-select" },
    ];
    // 弹框选项选中回调
    const onSelect = (action: PopoverAction, index: number) => {
      switch (index) {
        case 0:
          showTodayReviewCard(action);
          break;
        case 1:
          filterCardByCategory();
          break;
        case 2:
          handlerClickSelectBtn();
          break;
      }
    };
    // ------- 今日卡片
    const showTodayReviewCard = (action: PopoverAction) => {
      // 初始化状态
      getReviewDataStatus.hasMore = true;
      getReviewDataStatus.limit = 10;
      getReviewDataStatus.offset = 0;
      data.value = [];
      if (action.text === "今日卡片") {
        action.text = "显示全部";
        action.icon = " iconfont icon-all";
        getReviewDataStatus.date = dayjs().format("YYYY-MM-DD");
        // 只修改日期
        // 在getReviewData中获取数据
        getReviewData();
      } else {
        action.text = "今日卡片";
        action.icon = " iconfont icon-jinri";
        getReviewData();
      }
    };

    let getReviewDataStatus = {
      method: "GET" as Method,
      limit: 10,
      offset: 0,
      hasMore: true,
      date: "",
    };
    const getReviewCardByDateConfig = {
      url: `${store.state.serverHost}/review/date`,
    };

    // ------- 根据日期查询卡片
    const getReviewCardByDate = () => {
      loading.value = true;
      getReviewCardByDateData<ICard>(
        getReviewDataStatus,
        getReviewCardByDateConfig,
        false
      ).then((response) => {
        data.value = [...data.value, ...response];
        loading.value = false;
        if (!getReviewDataStatus.hasMore) {
          finished.value = true;
        }
      });
    };

    // ----------- 筛选类别
    const filterCardByCategory = () => {
      console.log("filterCardByCategory");
    };
    // --------- 选择卡片 开始
    const selectMode = ref(false); // 是否为选择模式
    let hasMoreBak: boolean; // 备份是否还有下一页, 原数据将会被修改
    const handlerClickSelectBtn = () => {
      selectMode.value = true;
      // 默认的宽度会将CheckBox挤到外部
      // 需要重新设置宽度
      // --- copy from resetFiledWidth
      const field = document.querySelector(".van-swipe-cell") as HTMLElement;
      if (!field) return;
      const { width: fieldWidth } = field.getBoundingClientRect();

      const contentItem = document.querySelectorAll(".content_item");
      const titleNodes = document.querySelectorAll(".item-title");
      const categoryNodes = document.querySelectorAll(".item-category");

      contentItem.forEach((titleNode) => {
        const ele = titleNode as HTMLElement;
        ele.style.width = String(fieldWidth - 30 - 24 - 15 - 30) + "px";
      });
      titleNodes.forEach((titleNode) => {
        const ele = titleNode as HTMLElement;
        ele.style.width = String(fieldWidth - 30 - 24 - 15 - 40) + "px";
      });
      categoryNodes.forEach((titleNode) => {
        const ele = titleNode as HTMLElement;
        ele.style.width = String(fieldWidth - 30 - 24 - 15 - 40) + "px";
      });
      // 禁止, 触底获取数据
      // 免得, 新获取的数据与原来的数据样式不一样
      // finished也要修改, 防止多一次触底
      hasMoreBak = status.hasMore;
      status.hasMore = false;
      finished.value = true;
    };
    // 复选框
    const checkedCard = ref<number[]>([]);
    const checkboxRefs = ref<CheckboxInstance[]>([]);
    const checkboxGroupRef = ref<CheckboxGroupInstance>();
    // 点击卡片切换
    const toggleCardCheckboxStatus = (index: number) => {
      if (checkboxRefs.value) {
        checkboxRefs.value[index].toggle();
      }
    };
    // 取消
    const handlerClickCancel = () => {
      selectMode.value = false;
      // 恢复宽度
      resetFiledWidth();
      // 恢复hasMore
      status.hasMore = hasMoreBak;
      finished.value = !status.hasMore;
      // 全部取消选择
      if (checkboxGroupRef.value) {
        checkboxGroupRef.value.toggleAll(false);
      }
    };
    // 反选
    const handlerClickSelectInverse = () => {
      if (checkboxGroupRef.value) {
        checkboxGroupRef.value.toggleAll();
      }
    };
    // 全选
    const handlerClickSelectAll = () => {
      if (checkboxGroupRef.value) {
        checkboxGroupRef.value.toggleAll(true);
      }
    };
    // 批量完成复习
    const handlerClickSuccessReview = () => {
      if (!checkedCard.value || checkedCard.value.length <= 0) {
        // 提示先选择
        Toast("请先选择卡片");
        return;
      }
      const postConfig = {
        method: "post" as Method,
        url: `${store.state.serverHost}/review/batch-review`,
        data: {
          cards: checkedCard.value,
        },
      };

      postCreateData<null, IBatchReviewPostData>(postConfig, false).then(() => {
        // 提示
        Toast.success("选中卡片已复习完成");
        // 删除选中
        const shouldDeleteCount = checkedCard.value.length;
        let currentDeleteCount = 0;
        // 需要倒序遍历, 否则后面元素将往前移动

        for (let index = data.value.length - 1; index >= 0; index--) {
          const item = data.value[index];
          if (checkedCard.value.includes(item.id)) {
            // 符合要求, 删除
            data.value.splice(index, 1);
            currentDeleteCount += 1;

            // 检测是否已经判断完了
            if (currentDeleteCount === shouldDeleteCount) break;
          }
        }
        // 关闭选择模式
        handlerClickCancel();
      });
    };

    // --------- 选择卡片 结束

    // ------- 滑动-完成复习
    const handlerSuccessBtn = (cid: number) => {
      const postConfig = {
        method: "post" as Method,
        url: `${store.state.serverHost}/review/${cid}`,
      };

      postCreateData<null, null>(postConfig, false).then(() => {
        // 提示
        Toast.success("已跳过");
        // 移除
        for (let index in data.value) {
          // index 为string
          const numIndex = Number(index);
          if (data.value[numIndex].id === cid) {
            data.value.splice(numIndex, 1);
            break;
          }
        }
      });
    };
    const router = useRouter();
    const handlerEditBtn = (cid: number) => {
      router.push({ name: "editorCard", params: { cid } });
    };
    // ---- 点击日历回调
    const handlerConfirmCal = (value: Date) => {
      showCal.value = false;
      // 修改配置
      // 初始化状态
      getReviewDataStatus.hasMore = true;
      getReviewDataStatus.limit = 10;
      getReviewDataStatus.offset = 0;
      getReviewDataStatus.date = dayjs(value).format("YYYY-MM-DD");
      data.value = [];
      actions[0].text = "显示全部";
      actions[0].icon = " iconfont icon-all";
      finished.value = false;
      getReviewData();
    };
    // ----------------------- 获取复习卡片
    const loading = ref(false);
    const data = ref<ICard[]>([]);
    const finished = ref(false);
    let status = {
      method: "GET" as Method,
      limit: 10,
      offset: 0,
      hasMore: true,
    };
    const config = {
      url: `${store.state.serverHost}/review/`,
    };

    const getReviewData = () => {
      // 1. 判断是否为根据日期查看
      // 2. 直接获取, 日期在其他函数中获取
      finished.value = false;
      if (actions[0].text === "今日卡片") {
        loading.value = true;
        getDataOfPage<ICard>(status, config, false).then((response) => {
          data.value = [...data.value, ...response];
          loading.value = false;
          // 判断是否完成
          if (!status.hasMore) {
            finished.value = true;
          }
        });
      } else {
        getReviewCardByDate();
      }
    };
    // ----------------------- 限制category和title的width
    const resetFiledWidth = () => {
      const field = document.querySelector(".van-swipe-cell") as HTMLElement;
      if (!field) return;
      const { width: fieldWidth } = field.getBoundingClientRect();

      const contentItem = document.querySelectorAll(".content_item");
      const titleNodes = document.querySelectorAll(".item-title");
      const categoryNodes = document.querySelectorAll(".item-category");
      // 30 - 24 - 15
      // 代表 图标的两边margin - 图标大小 - 右边的空白
      contentItem.forEach((titleNode) => {
        const ele = titleNode as HTMLElement;
        ele.style.width = String(fieldWidth - 30 - 24 - 15) + "px";
      });
      titleNodes.forEach((titleNode) => {
        const ele = titleNode as HTMLElement;
        ele.style.width = String(fieldWidth - 30 - 24 - 15) + "px";
      });
      categoryNodes.forEach((titleNode) => {
        const ele = titleNode as HTMLElement;
        ele.style.width = String(fieldWidth - 30 - 24 - 15) + "px";
      });
    };

    const { width, height } = useWindowSize();
    // 窗口大小改变时
    watch([width, height], () => {
      // 选择模式下, 不应该重新设置宽度
      if (selectMode.value) return;
      resetFiledWidth;
    });
    // 有新数据时
    watch([data], () => {
      // 选择模式下, 不应该重新设置宽度
      if (selectMode.value) return;
      resetFiledWidth;
    });

    // ---------- 点击跳转到复习页面
    const handlerClickReviewBody = (cid: number) => {
      router.push({ name: "CardReview", query: { cid } });
    };

    return {
      loading,
      finished,
      getReviewData,
      data,
      handlerSuccessBtn,
      handlerEditBtn,
      showPopover,
      showCal,
      onSelect,
      actions,
      handlerConfirmCal,
      handlerClickReviewBody,
      checkedCard,
      checkboxRefs,
      checkboxGroupRef,
      selectMode,
      toggleCardCheckboxStatus,
      handlerClickCancel,
      handlerClickSelectInverse,
      handlerClickSelectAll,
      handlerClickSuccessReview,
    };
  },
});
</script>

<style lang="scss">
// 选择模式样式
.select-mode-tool-wrap {
  display: flex;
  justify-content: flex-start;
  align-items: center;
  .tool-item {
    margin-right: 20px;
    color: #35495e;
  }
}
.select-mode-tool-success-review {
  color: #53bb86;
}
.loading-text-wrap {
  // 加载中...
  background-color: #f4f3f5;
  color: #fff;
}
.review_body_empty {
  background-color: #f4f3f5;
  min-height: calc(100vh - 56px);
  padding-top: 56px;
  padding-bottom: 50px;
}
.review_body {
  background-color: #f4f3f5;
  min-height: calc(100vh - 106px);
  padding-top: 56px;
  padding-bottom: 50px;

  .cell_item {
    margin-bottom: 10px;
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
      }
      .content_date {
        color: #8f8e90;
        display: flex;
      }
    }
    .swipe_right_wrap {
      display: flex;
      justify-content: center;
      align-items: center;

      height: 64px;
      margin-right: 5px;
      .swipe_right_btn {
        // margin-bottom: 5px;
        width: 44px;
        margin-right: 5px;
      }
    }
  }
}
</style>
