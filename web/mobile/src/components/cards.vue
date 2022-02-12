<template>
  <van-nav-bar title="卡片" @click-left="reload" @click-right="more">
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

  <!-- 复习页面的主题 -->
  <div class="cards_body">
    <!-- 加载框 -->
    <van-loading color="#1989fa" v-if="!data" />

    <van-cell-group
      v-else
      inset
      v-for="item in data.data"
      :key="item.id"
      class="cell_item"
    >
      <van-swipe-cell>
        <van-cell center title-class="content_item" label-class="content_date">
          <template #icon>
            <van-icon
              :name="item.icon"
              class="left-icon"
              size="24"
              :color="item.color"
            />
          </template>
          <template #title>
            <span class="item-title">{{ item.title }}</span>
          </template>
          <template #label>
            <span class="item-tag">
              <van-tag :color="item.color" text-color="#fff">{{
                item.tag_name
              }}</van-tag>

              {{ item.next_review_at }}
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
</template>

<script lang="ts">
import { defineComponent, ref } from "vue";
import { PopoverAction } from "vant";
import axios from "axios";

export default defineComponent({
  name: "Cards",

  setup() {
    const data = ref("");
    const showPopover = ref(false);
    const showCal = ref(false); // 显示日历
    // 弹框选项
    const actions = [
      { text: "排序", icon: " iconfont icon-c" },
      { text: "只看星标", icon: " iconfont icon-tag" },
      { text: "选择卡片", icon: " iconfont icon-check-box" },
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

    const handlerConfirmCal = (value: Date) => {
      console.log("handlerConfirmCal", value);
      showCal.value = false;
    };

    axios({
      method: "get",
      // TODO: 修改url
      url: "http://localhost:8080/data/review/cards.json",
    }).then((response) => {
      data.value = response.data;
    });

    console.log(data);
    return {
      reload,
      more,
      data,
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
  min-height: calc(100vh - 96px);
  margin-bottom: 50px;

  .cell_item {
    margin-bottom: 10px;
    .content_item {
      justify-content: flex-start;
      display: flex;
      flex-direction: column;
      margin-left: 15px;
      .item-tag {
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