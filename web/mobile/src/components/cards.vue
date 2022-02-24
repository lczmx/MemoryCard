<template>
  <van-nav-bar
    :title="selectMode ? '' : '卡片'"
    :fixed="true"
    @click-left="() => (selectMode ? (selectMode = true) : reload())"
    @click-right="() => (selectMode ? (selectMode = true) : more())"
  >
    <!-- 根据selectMode和判断不同的执行方式 -->
    <template #left>
      <div class="select-mode-left-tool-wrap" v-if="selectMode">
        <div class="tool-item" @click.stop="handlerClickCancel">取消</div>
        <div class="tool-item" @click.stop="handlerClickSelectInverse">
          反选
        </div>
        <div class="tool-item" @click.stop="handlerClickSelectAll">全选</div>
      </div>
      <van-icon
        v-else
        size="20"
        v-show="!loading"
        class="iconfont"
        class-prefix="icon"
        name="reload"
        color="#1989fa"
      />

      <van-loading color="#1989fa" size="20" v-show="loading" />
    </template>
    <template #right>
      <div class="select-mode-right-tool-wrap" v-if="selectMode">
        <div class="tool-item tool-star" @click.stop="handlerClickBatchStar">
          批量星标
        </div>
        <div
          class="tool-item tool-delete"
          @click.stop="handlerClickBatchDelete"
        >
          批量删除
        </div>
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
  <van-list
    v-model:loading="loading"
    :finished="!status.hasMore"
    @load="getCardData"
    loading-text="加载中..."
  >
    <template #loading>
      <div class="loading-text-wrap">
        <van-loading color="#1989fa" />
      </div>
    </template>
    <van-empty
      description="请先添加卡片"
      :style="{ backgroundColor: '#f4f3f5' }"
      v-if="!loading && data.length <= 0"
      class="cards_body_empty"
    />
    <!-- 全部卡片 主体 -->
    <div
      v-else
      class="cards_body van-clearfix"
      v-touch:swipe.bottom="handlerShowAddCardBtn"
      v-touch:swipe.top="handlerHideAddCardBtn"
    >
      <div class="data_wrap">
        <van-checkbox-group v-model="checkedCard" ref="checkboxGroupRef">
          <van-cell-group
            inset
            v-for="(item, index) in data"
            :key="item.id"
            class="cell_item"
            @click="toggleCardCheckboxStatus(index)"
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
            <!-- 复习计划 -->
            <show-plan :card="item"></show-plan>
          </van-cell-group>
        </van-checkbox-group>
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
import { PopoverAction, Toast, Dialog } from "vant";
import type { CheckboxInstance, CheckboxGroupInstance } from "vant";
import { useToggle, useWindowSize } from "@vant/use";
import { ICard, IStar, IBatchPostData } from "@/types";
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
      switch (
        index // TODO: 排序按钮
      ) {
        case 1:
          onlyShowStarCard(action);
          break;
        case 2:
          handlerClickSelectBtn();
          break;
      }
      console.log(action, index);
    };
    // ------------- 只看星标
    let dataBak: ICard[]; // 用于备份
    const onlyShowStarCard = (action: PopoverAction) => {
      if (action.text === "只看星标") {
        // 1. 查看是否有下一页, 继续获取
        // 2. 备份
        // 3 . 修改选项内容

        actions[1].text = "显示全部";

        if (status.hasMore) {
          // 假如还有的话, 需要继续获取星标, 因为 星标数据不是全部的
          // 内部函数将备份dataBak
          dataBak = [];
          reload();
        } else {
          dataBak = data.value as ICard[];
          data.value = data.value.filter((value) => value.isStar);
        }
      } else {
        // 显示全部

        // 1. 恢复备份
        // 2. 清空备份
        // 3. 修改选项内容
        data.value = dataBak as ICard[];
        dataBak = [];

        actions[1].text = "只看星标";
      }
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
    };
    // 复选框
    const checkedCard = ref<number[]>([]);
    const checkboxRefs = ref<CheckboxInstance[]>([]);
    const checkboxGroupRef = ref<CheckboxGroupInstance>();
    // 点击卡片切换
    const toggleCardCheckboxStatus = (index: number) => {
      // 不在选择模式, 不能选中
      if (!selectMode.value) return;
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
    // 批量星标
    const handlerClickBatchStar = () => {
      if (!checkedCard.value || checkedCard.value.length <= 0) {
        // 提示先选择
        Toast("请先选择卡片");
        return;
      }

      const config = {
        method: "post" as Method,
        url: `${store.state.serverHost}/cards/batch-star`,
        data: {
          cards: checkedCard.value,
        },
      };

      postCreateData<null, IBatchPostData>(config, false).then(() => {
        // 提示
        Toast.success("已批量星标");
        // 切换选中的星标状态
        const shouldStarCount = checkedCard.value.length; // 应该星标的数量
        let currentStarCount = 0;

        for (let item of data.value) {
          if (checkedCard.value.includes(item.id)) {
            // 符合要求, 星标
            item.isStar = true;
            currentStarCount += 1;
            if (currentStarCount === shouldStarCount) break;
          }
        }

        // 关闭选择模式
        handlerClickCancel();
      });
    };
    // 批量删除
    const handlerClickBatchDelete = () => {
      if (!checkedCard.value || checkedCard.value.length <= 0) {
        // 提示先选择
        Toast("请先选择卡片");
        return;
      }

      Dialog.confirm({
        title: "警告",
        message: "删除后无法恢复, 你确定要继续吗?",
      })
        .then(() => {
          const config = {
            method: "delete" as Method,
            url: `${store.state.serverHost}/cards/batch-delete`,
            data: {
              cards: checkedCard.value,
            },
          };

          deleteData<IBatchPostData>(config, false).then(() => {
            // 提示
            Toast.success("已批量删除");
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
        })
        .catch(() => {
          Toast("已经取消");
        });
    };

    // --------- 选择卡片 结束
    // ----- 编辑按钮
    const router = useRouter();
    const handlerEditBtn = (cid: number) => {
      router.push({ name: "editorCard", params: { cid } });
    };

    const reload = () => {
      // 重新加载 卡片数据
      loading.value = true;
      data.value = [];
      dataBak = [];
      status.hasMore = true;
      status.limit = 10;
      status.offset = 0;
      getCardData();
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
        // 判断是否为只看星标

        if (actions[1].text === "显示全部") {
          // 只看星标状态
          // 1. 备份全部
          dataBak = [...dataBak, ...response];
          // 2. 过滤星标
          data.value = [
            ...data.value,
            ...response.filter((value) => value.isStar),
          ];
        } else {
          // 要显示全部 (默认)
          data.value = [...data.value, ...response];
        }

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
      resetFiledWidth();
    });
    // 有新数据时
    watch([data], () => {
      // 选择模式下, 不应该重新设置宽度
      if (selectMode.value) return;
      resetFiledWidth();
    });

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
      checkedCard,
      checkboxRefs,
      checkboxGroupRef,
      selectMode,
      toggleCardCheckboxStatus,
      handlerClickCancel,
      handlerClickSelectInverse,
      handlerClickSelectAll,
      handlerClickBatchStar,
      handlerClickBatchDelete,
    };
  },
});
</script>

<style lang="scss">
// 选择模式样式
.select-mode-left-tool-wrap {
  display: flex;
  justify-content: flex-start;
  align-items: center;
  .tool-item {
    margin-right: 10px;
    color: #35495e;
  }
}
.select-mode-right-tool-wrap {
  display: flex;
  justify-content: flex-start;
  align-items: center;
  .tool-item {
    margin-right: 20px;
  }
  .tool-star {
    color: #53bb86;
  }
  .tool-delete {
    color: #ee0a24;
  }
}

.loading-text-wrap {
  // 加载中...
  background-color: #f4f3f5;
  color: #fff;
}

.cards_body_empty {
  background-color: #f4f3f5;
  min-height: calc(100vh - 56px);
  padding-top: 56px;
  padding-bottom: 50px;
}
.cards_body {
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
.addCardBtnWrap {
  position: fixed;
  bottom: 80px;
  right: 30px;
}
</style>
