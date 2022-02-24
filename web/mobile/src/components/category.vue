<template>
  <van-nav-bar
    :fixed="true"
    :title="selectMode ? '' : '类别'"
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
  <!-- 标签 -->
  <van-list
    v-model:loading="loading"
    :finished="!status.hasMore"
    @load="getCategoryData"
    loading-text="加载中..."
  >
    <template #loading>
      <div class="loading-text-wrap">
        <van-loading color="#1989fa" />
      </div>
    </template>
    <van-empty
      description="请先添加类别"
      :style="{ backgroundColor: '#f4f3f5' }"
      v-if="!loading && data.length <= 0"
      class="category_body_empty"
    />
    <!-- 标签主体 -->
    <div
      v-else
      class="category_body van-clearfix"
      v-touch:swipe.bottom="handlerShowAddCategoryBtn"
      v-touch:swipe.top="handlerHideAddCategoryBtn"
    >
      <van-checkbox-group v-model="checkedCategory" ref="checkboxGroupRef">
        <van-cell-group
          inset
          v-for="(item, index) in data"
          :key="item.id"
          class="cell_item"
          :style="{ 'background-color': item.color }"
          @click="toggleCategoryCheckboxStatus(index)"
        >
          <van-cell
            center
            title-class="content_item"
            label-class="content_date"
          >
            <template #icon>
              <!-- 使用iconfont -->
              <i
                :class="`left-icon iconfont ${item.icon}`"
                :style="{ fontSize: '24px', color: '#fff' }"
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
              <!-- 是否为复选框? -->
              <van-checkbox
                v-if="selectMode"
                :name="item.id"
                :ref="(el) => (checkboxRefs[index] = el)"
                @click.stop
              >
                <!-- 自定义图标 -->
                <template #icon="props">
                  <van-icon
                    name="success"
                    :color="props.checked ? '#1989fa' : '#bfbfbf'"
                    :style="{ backgroundColor: '#fff', fontWeight: 'bold' }"
                  />
                </template>
              </van-checkbox>
              <div
                v-else
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
      </van-checkbox-group>
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
import { PopoverAction, ActionSheetAction, Toast, Dialog } from "vant";
import type { CheckboxInstance, CheckboxGroupInstance } from "vant";
import { useStore } from "vuex";
import { useRouter } from "vue-router";
import { useToggle } from "@vant/use";
import { getDataOfPage, postCreateData, deleteData } from "@/utils/request";
import { ICategory, IStar, IBatchPostData } from "@/types";
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
    // ------ 弹框选项选中回调
    const onSelect = (action: PopoverAction, index: number) => {
      switch (index) {
        case 1:
          onlyShowStarCard(action);
          break;
        case 2:
          handlerClickSelectBtn();
          break;
      }
    };
    // ------------- 只看星标
    let dataBak: ICategory[]; // 用于备份
    const onlyShowStarCard = (action: PopoverAction) => {
      if (action.text === "只看星标") {
        if (typeof data.value !== "undefined") {
          dataBak = data.value as ICategory[];
        }

        data.value = data.value.filter((value) => value.isStar);
        actions[1].text = "显示全部";
      } else {
        if (typeof dataBak !== "undefined") {
          data.value = dataBak;
        }

        actions[1].text = "只看星标";
      }
    };

    // --------- 选择模式 开始
    const selectMode = ref(false); // 是否为选择模式
    let hasMoreBak: boolean; // 备份是否还有下一页, 原数据将会被修改
    const handlerClickSelectBtn = () => {
      selectMode.value = true;
      // 不需要额外设置宽度, 有星标的位置

      // 禁止, 触底获取数据
      // 免得, 新获取的数据与原来的数据样式不一样
      // finished也要修改, 防止多一次触底
      hasMoreBak = status.hasMore;
      status.hasMore = false;
    };
    // 复选框
    const checkedCategory = ref<number[]>([]);
    const checkboxRefs = ref<CheckboxInstance[]>([]);
    const checkboxGroupRef = ref<CheckboxGroupInstance>();
    // 点击类别切换
    const toggleCategoryCheckboxStatus = (index: number) => {
      // 不在选择模式, 不能选中
      if (!selectMode.value) return;
      if (checkboxRefs.value) {
        checkboxRefs.value[index].toggle();
      }
    };
    // 取消
    const handlerClickCancel = () => {
      selectMode.value = false;
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
      if (!checkedCategory.value || checkedCategory.value.length <= 0) {
        // 提示先选择
        Toast("请先选择卡片");
        return;
      }

      const config = {
        method: "post" as Method,
        url: `${store.state.serverHost}/category/batch-star`,
        data: {
          cards: checkedCategory.value,
        },
      };

      postCreateData<null, IBatchPostData>(config, false).then(() => {
        // 提示
        Toast.success("已批量星标");
        // 切换选中的星标状态
        const shouldStarCount = checkedCategory.value.length; // 应该星标的数量
        let currentStarCount = 0;

        for (let item of data.value) {
          if (checkedCategory.value.includes(item.id)) {
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
      if (!checkedCategory.value || checkedCategory.value.length <= 0) {
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
            url: `${store.state.serverHost}/category/batch-delete`,
            data: {
              cards: checkedCategory.value,
            },
          };

          deleteData<IBatchPostData>(config, false).then(() => {
            // 提示
            Toast.success("已批量删除");
            // 删除选中
            const shouldDeleteCount = checkedCategory.value.length;
            let currentDeleteCount = 0;
            // 需要倒序遍历, 否则后面元素将往前移动

            for (let index = data.value.length - 1; index >= 0; index--) {
              const item = data.value[index];
              if (checkedCategory.value.includes(item.id)) {
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

    // --------- 选择模式 结束

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
    // 执行长按选项
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
    const router = useRouter();
    const editCategory = (id: number) => {
      router.push({ name: "editorCategory", params: { cid: id } });
    };
    const deleteCategory = (id: number) => {
      // 删除标签
      const config = {
        method: "delete" as Method,
        url: `${store.state.serverHost}/category/${id}`,
      };
      deleteData(config, false).then(() => {
        // 提示
        Toast.success("已删除");
        // 移除
        for (let index in data.value) {
          // index 为string
          const numIndex = Number(index);
          if (data.value[numIndex].id === id) {
            data.value.splice(numIndex, 1);
            break;
          }
        }
      });
    };

    /* ----- 长按结束 --------- */
    /* ----- 添加分类开始 --------- */

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
      handlerShowAddCategoryBtn,
      handlerHideAddCategoryBtn,
      handlerToggleStarStatus,
      showAddCategoryBtnState,
      loading,
      status,
      getCategoryData,
      checkedCategory,
      checkboxRefs,
      checkboxGroupRef,
      selectMode,
      toggleCategoryCheckboxStatus,
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
.category_body_empty {
  background-color: #f4f3f5;
  min-height: calc(100vh - 56px);
  padding-top: 56px;
  padding-bottom: 50px;
}

.category_body {
  background-color: #f4f3f5;
  min-height: calc(100vh - 106px);
  padding-top: 56px;
  padding-bottom: 50px;
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
        width: calc(100% - 65px);
        padding-right: 10px;

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
