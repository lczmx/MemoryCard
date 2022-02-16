<template>
  <van-nav-bar
    title="卡片"
    :fixed="true"
    @click-left="reload"
    @click-right="more"
  >
    <template #left>
      <van-icon name="replay" size="20" />
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

  <!-- 全部卡片 主体 -->
  <div class="cards_body">
    <div class="data_wrap" v-if="data.length > 0">
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
              <van-icon
                :name="item.category.icon"
                class="left-icon"
                size="24"
                :color="item.category.color"
              />
            </template>
            <template #title>
              <div class="van-ellipsis item-title">{{ item.title }}</div>
            </template>
            <template #label>
              <span class="item-category">
                <van-tag :color="item.category.color" text-color="#fff">{{
                  item.category.name
                }}</van-tag>

                {{ item.reviewDate }}
              </span>
            </template>
          </van-cell>
          <template #right>
            <!-- 右边滑动区域 -->
            <div class="swipe_right_wrap">
              <van-button
                class="swipe_right_btn"
                icon="success"
                size="small"
                type="success"
                @click="handlerSuccessBtn(item.id)"
              />
              <van-button
                class="swipe_right_btn"
                icon="edit"
                size="small"
                type="primary"
                @click="handlerEditBtn(item.id)"
                :cid="item.id"
              />
            </div>
          </template>
        </van-swipe-cell>
      </van-cell-group>
    </div>
    <!-- 没有数据 -->
    <van-empty v-if="!loading && data.length <= 0" description="暂无数据" />
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from "vue";
import { PopoverAction, Toast } from "vant";
import { ICard } from "@/types";
import { getDataOfPage } from "@/utils/request";
import { Method } from "axios";
export default defineComponent({
  name: "Cards",

  setup() {
    const data = ref<ICard[]>([]);
    const showPopover = ref(false);
    // 弹框选项
    const actions = [
      { text: "排序", icon: " iconfont icon-sorting" },
      { text: "只看星标", icon: " iconfont icon-star" },
      { text: "选择卡片", icon: " iconfont icon-select" },
    ];
    // 弹框选项选中回调
    const onSelect = (action: PopoverAction, index: number) => {
      console.log(action, index);
    };

    const handlerSuccessBtn = (cid: number) => {
      console.log(`handlerSuccessBtn: ${cid}`);
    };
    const handlerEditBtn = (cid: number) => {
      console.log(`handlerEditBtn: ${cid}`);
    };

    const reload = () => {
      console.log("log");
    };
    const more = () => {
      console.log("more");
    };
    // ------------------- 获取数据
    const loading = ref(true); // 表示正在加载中
    let status = {
      method: "GET" as Method,
      limit: 10,
      offset: 0,
      hasMore: true,
    };
    const config = {
      // TODO: URL和触底事件
      url: "http://localhost:8080/data/review/cards.json",
    };
    const getData = () => {
      getDataOfPage<ICard>(status, config).then((response) => {
        // 加上之间的
        data.value = [...data.value, ...response];
        loading.value = false;
      });
    };

    onMounted(() => {
      getData();
      console.log(data);
    });

    return {
      reload,
      more,
      data,
      loading,
      handlerSuccessBtn,
      handlerEditBtn,
      showPopover,
      onSelect,
      actions,
    };
  },
});
</script>

<style lang="scss">
.cards_body {
  background-color: #f4f3f5;
  min-height: calc(100vh - 106px);
  margin-bottom: 50px;
  padding-top: 56px;
  padding-bottom: 10px;
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
      flex-direction: column;
      justify-content: center;
      align-items: center;

      // height: 90px;
      margin-right: 5px;
      .swipe_right_btn {
        margin-bottom: 5px;
      }
    }
  }
}
</style>
