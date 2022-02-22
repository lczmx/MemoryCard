<template>
  <van-nav-bar
    title="卡片"
    :fixed="true"
    @click-left="reload"
    @click-right="more"
  >
    <template #left>
      <van-icon name="replay" size="20" v-show="!loading" />

      <van-loading color="#1989fa" size="20" v-show="loading" />
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
  <van-list
    v-model:loading="loading"
    :finished="!status.hasMore"
    @load="getCardData"
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
    <!-- 全部卡片 主体 -->
    <div
      class="cards_body van-clearfix"
      v-touch:swipe.bottom="handlerShowAddCardBtn"
      v-touch:swipe.top="handlerHideAddCardBtn"
    >
      <div class="data_wrap">
        <van-cell-group
          inset
          v-for="(item, index) in data"
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
                <div class="van-ellipsis item-title">
                  {{ item.title }}
                </div>
              </template>
              <template #label>
                <div class="van-ellipsis item-category">
                  <van-tag :color="item.category.color" text-color="#fff">{{
                    item.category.name
                  }}</van-tag>
                </div>
              </template>
            </van-cell>
            <template #right>
              <!-- 右边滑动区域 -->
              <div class="swipe_right_wrap">
                <van-button
                  class="swipe_right_btn"
                  icon="edit"
                  type="primary"
                  round
                  :block="true"
                  @click="handlerEditBtn(item.id)"
                  :cid="item.id"
                />
                <van-button
                  class="swipe_right_btn"
                  icon="delete-o"
                  type="danger"
                  round
                  :block="true"
                  @click="handlerDeleteBtn(item.id)"
                  :cid="item.id"
                />
                <van-button
                  color="#f08300"
                  class="swipe_right_btn"
                  round
                  plain
                  :block="true"
                  @click="handlerToggleStarStatus($event, index, item.id)"
                >
                  <template #icon>
                    <van-icon
                      v-show="item.isStar"
                      class="iconfont star_true"
                      color="#f08300"
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
                  </template>
                </van-button>
              </div>
            </template>
          </van-swipe-cell>
          <show-plan :card="item"></show-plan>
        </van-cell-group>
      </div>
    </div>
  </van-list>
  <!-- 添加卡片的btn -->
  <!-- 上滑进入 -->
  <transition name="van-slide-up">
    <div class="addCardBtnWrap" v-show="showAddCardBtnState">
      <van-button
        icon="plus"
        type="primary"
        round
        to="/add/card"
        color="#41b883"
      ></van-button>
    </div>
  </transition>
</template>

<script lang="ts">
import { defineComponent, ref, watch } from "vue";
import { useStore } from "vuex";
import { PopoverAction, Toast } from "vant";
import { useToggle, useWindowSize } from "@vant/use";
import { ICard, IStar } from "@/types";
import { getDataOfPage, postCreateData, deleteData } from "@/utils/request";
import ShowPlan from "@/components/showPlan.vue";
import { Method } from "axios";
import { useRouter } from "vue-router";
export default defineComponent({
  name: "Cards",
  components: { ShowPlan },
  setup() {
    const data = ref<ICard[]>([]);
    const showPopover = ref(false);
    // 弹框选项
    const actions = [
      { text: "排序", icon: " iconfont icon-sorting" },
      { text: "只看星标", icon: " iconfont icon-star" },
      { text: "选择卡片", icon: " iconfont icon-select" },
    ];
    // ------ 弹框选项选中回调
    const onSelect = (action: PopoverAction, index: number) => {
      switch (index) {
        case 1:
          onlyShowStarCard(action);
          break;
      }
      console.log(action, index);
    };
    // ------------- 只看星标
    let dataBak: ICard[]; // 用于备份
    const onlyShowStarCard = (action: PopoverAction) => {
      if (action.text === "只看星标") {
        if (typeof data.value !== "undefined") {
          dataBak = data.value as ICard[];
        }

        data.value = data.value.filter((value) => value.isStar);
        actions[1].text = "显示全部";
      } else {
        if (typeof dataBak !== "undefined") {
          data.value = dataBak;
        }

        actions[1].text = "只看星标";
      }

      console.log("onlyShowStarCard");
    };

    const handlerDeleteBtn = (cid: number) => {
      // 删除卡片
      const config = {
        method: "delete" as Method,
        url: `${store.state.serverHost}/cards/${cid}`,
      };
      deleteData(config, false).then(() => {
        // 提示
        Toast.success("已删除");
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
    // ----- 编辑按钮
    const router = useRouter();
    const handlerEditBtn = (cid: number) => {
      router.push({ name: "editorCard", params: { cid } });
    };

    const reload = () => {
      // 重新加载 卡片数据
      loading.value = true;
      data.value = [];
      status.hasMore = true;
      status.limit = 10;
      status.offset = 0;
      getCardData();
      console.log(loading.value);
    };

    const more = () => {
      console.log("more");
    };
    // ----------------------- 添加按钮显示与隐藏
    const [showAddCardBtnState, toggleAddCardBtn] = useToggle(true);

    const handlerShowAddCardBtn = () => {
      toggleAddCardBtn(true);
    };
    const handlerHideAddCardBtn = () => {
      toggleAddCardBtn(false);
    };

    // ------------------- 获取数据
    const loading = ref(false);
    const store = useStore();
    let status = {
      method: "GET" as Method,
      limit: 10,
      offset: 0,
      hasMore: true,
    };
    const config = {
      url: `${store.state.serverHost}/cards/`,
    };

    const getCardData = () => {
      getDataOfPage<ICard>(status, config, false).then((response) => {
        data.value = [...data.value, ...response];

        loading.value = false;
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
        url: `${store.state.serverHost}/cards/${cid}/star`,
        data: {
          isStar: starStatus,
        },
      };

      postCreateData<IStar, IStar>(postConfig, false).then((response) => {
        data.value[index].isStar = response.isStar;
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
      reload,
      more,
      data,
      loading,
      status,
      getCardData,
      handlerDeleteBtn,
      handlerEditBtn,
      handlerToggleStarStatus,
      showPopover,
      onSelect,
      actions,
      handlerShowAddCardBtn,
      handlerHideAddCardBtn,
      showAddCardBtnState,
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
.cards_body {
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
.addCardBtnWrap {
  position: fixed;
  bottom: 80px;
  right: 30px;
}
</style>
