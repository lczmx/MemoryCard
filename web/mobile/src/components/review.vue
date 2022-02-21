<template>
  <van-nav-bar
    title="复习"
    :fixed="true"
    @click-left="calendar"
    @click-right="more"
  >
    <template #left>
      <van-icon name="calendar-o" size="20" />
    </template>
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
    v-model:show="showCal"
    @confirm="handlerConfirmCal"
  />

  <van-list
    v-model:loading="loading"
    :finished="!status.hasMore"
    @load="getReviewData"
    loading-text="加载中..."
  >
    <template #finished>
      <div class="finished-text-wrap">
        <p>没有更多数据了</p>
      </div>
    </template>
    <template #loading>
      <div class="loading-text-wrap">
        <van-loading color="#1989fa" />
      </div>
    </template>
    <!-- 复习页面的主体 -->
    <div class="review_body van-clearfix">
      <van-cell-group
        inset
        v-for="item in data"
        :key="item.id"
        class="cell_item"
      >
        <van-swipe-cell>
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
    </div>
  </van-list>
</template>

<script lang="ts">
import { defineComponent, ref, watch } from "vue";
import { PopoverAction } from "vant";
import { useWindowSize } from "@vant/use";
import { useStore } from "vuex";
import { useRouter } from "vue-router";
import { Method } from "axios";
import { ICard } from "@/types";
import { getDataOfPage } from "@/utils/request";

export default defineComponent({
  name: "Review",

  setup() {
    const showPopover = ref(false);
    const showCal = ref(false); // 显示日历
    // 弹框选项
    const actions = [
      { text: "今日卡片", icon: " iconfont icon-c" },
      { text: "筛选类别", icon: " iconfont icon-tag" },
      { text: "选择卡片", icon: " iconfont icon-select" },
    ];
    // 弹框选项选中回调
    const onSelect = (action: PopoverAction, index: number) => {
      console.log(action, index);
    };

    const handlerSuccessBtn = (cid: number) => {
      console.log(`handlerSuccessBtn: ${cid}`);
    };
    const router = useRouter();
    const handlerEditBtn = (cid: number) => {
      router.push({ name: "editorCard", params: { cid } });
    };

    const calendar = () => {
      // 点击日历的事件
      showCal.value = true;
      console.log("点击了日历");
    };
    const more = () => {
      showPopover.value = true;
      console.log("点击了更多");
    };
    const handlerConfirmCal = (value: Date) => {
      console.log("handlerConfirmCal", value);
      showCal.value = false;
    };
    // ----------------------- 获取复习卡片
    const loading = ref(false);
    const data = ref<ICard[]>([]);
    const store = useStore();
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
      getDataOfPage<ICard>(status, config, false).then((response) => {
        data.value = [...data.value, ...response];
        loading.value = false;
      });
    };
    // ----------------------- 限制category和title的width
    const resetFiledWidth = () => {
      const field = document.querySelector(".van-swipe-cell") as HTMLElement;
      if (!field) return;
      const { width: fieldWidth } = field.getBoundingClientRect();
      const titleNodes = document.querySelectorAll(".item-title");
      const categoryNodes = document.querySelectorAll(".item-category");
      // 30 - 24 - 15
      // 代表 图标的两边margin - 图标大小 - 右边的空白
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
    watch([width, height], resetFiledWidth);
    // 有新数据时
    watch([data], resetFiledWidth);
    return {
      calendar,
      more,
      loading,
      status,
      getReviewData,
      data,
      handlerSuccessBtn,
      handlerEditBtn,
      showPopover,
      showCal,
      onSelect,
      actions,
      handlerConfirmCal,
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

.review_body {
  background-color: #f4f3f5;
  min-height: calc(100vh - 156px);
  padding-top: 56px;
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
