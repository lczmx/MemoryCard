<template>
  <van-list
    v-model:loading="loadingPlanData"
    :finished="!status.hasMore"
    @load="getPlanData"
  >
  <template #loading></template>
    <van-empty
      description="复习曲线为空"
      :style="{ backgroundColor: '#f4f3f5' }"
      v-if="!loadingPlanData && planData.length <= 0"
      class="empty-plan"
    />
    <!-- 全部卡片 主体 -->
    <div
      v-else
      class="plan-body van-clearfix"
      v-touch:swipe.bottom="handlerShowAddPlanBtn"
      v-touch:swipe.top="handlerHideAddPlanBtn"
    >
      <van-cell-group
        inset
        v-for="(item, index) in planData"
        :key="item.id"
        class="cell-item"
        @click="handlerClickShowPlan(index)"
      >
        <van-swipe-cell>
          <van-cell
            center
            title-class="content-item"
            :label="getPlanAllTime(item.content)"
          >
            <template #icon>
              <!-- 使用iconfont -->
              <van-icon
                class="iconfont"
                class-prefix="icon"
                name="fsux_tubiao_fenbuquxiantu"
                size="16"
                color="#07c160"
              />
            </template>
            <template #title>
              <div class="van-ellipsis item-title">
                {{ item.title }}
              </div>
            </template>
          </van-cell>
          <template #right>
            <!-- 右边滑动区域 -->
            <div class="swipe-right-wrap" v-if="item.editable">
              <van-button
                class="swipe-right-btn"
                icon="edit"
                type="primary"
                round
                :block="true"
                :to="{ name: 'editorPlan', params: { pid: item.id } }"
              />
              <van-button
                class="swipe-right-btn"
                icon="delete-o"
                type="danger"
                round
                :block="true"
                @click="handlerDeleteBtn(item.id)"
              />
            </div>
            <div v-else class="cant-not-editable">默认复习曲线不可编辑</div>
          </template>
        </van-swipe-cell>
      </van-cell-group>
    </div>
  </van-list>
  <!-- 添加卡片的btn -->
  <!-- 上滑进入 -->
  <transition name="van-slide-up">
    <div class="add-card-btn-wrap" v-show="showAddPlanBtnState">
      <van-button
        icon="plus"
        type="primary"
        round
        :to="{ name: 'addPlan' }"
        color="#07c160"
      ></van-button>
    </div>
  </transition>
  <!-- 复习曲线展示 -->
  <van-popup v-model:show="showPlan" position="top" :style="{ height: '50vh' }">
    <van-steps
      direction="vertical"
      :active="planSteps.length - 1"
      inactive-color="#41b883"
      active-color="#41b883"
    >
      <van-step v-for="(item, index) in planSteps" :key="index">
        <div class="show-plan-wrap">
          <p class="show-plan-title">{{ item.title }}</p>
          <p class="show-plan-time">{{ item.time }}</p>
        </div>
        <template #inactive-icon>
          <svg
            t="1645805766529"
            class="icon"
            viewBox="0 0 1024 1024"
            version="1.1"
            xmlns="http://www.w3.org/2000/svg"
            p-id="28895"
            width="20"
            height="20"
          >
            <path
              d="M573.056 752l308.8-404.608A76.8 76.8 0 0 0 820.736 224H203.232a76.8 76.8 0 0 0-61.056 123.392l308.8 404.608a76.8 76.8 0 0 0 122.08 0z"
              p-id="28896"
              fill="#41b883"
            ></path>
          </svg>
        </template>
        <template #active-icon>
          <svg
            t="1645805766529"
            class="icon"
            viewBox="0 0 1024 1024"
            version="1.1"
            xmlns="http://www.w3.org/2000/svg"
            p-id="28895"
            width="20"
            height="20"
          >
            <path
              d="M573.056 752l308.8-404.608A76.8 76.8 0 0 0 820.736 224H203.232a76.8 76.8 0 0 0-61.056 123.392l308.8 404.608a76.8 76.8 0 0 0 122.08 0z"
              p-id="28896"
              fill="#41b883"
            ></path>
          </svg>
        </template>
      </van-step>
    </van-steps>
  </van-popup>
  <div class="loading-wrap" v-show="loadingPlanData">
    <van-loading color="#1989fa" />
  </div>
</template>
<script lang="ts">
import { defineComponent, ref } from "vue";
import { useStore } from "vuex";
import { getDataOfPage, deleteData } from "@/utils/request";
import { IPlan, IPlanStep } from "@/types";
import { convert_sec_to_string } from "@/hook";
import { Method } from "axios";
import { Toast } from "vant";
export default defineComponent({
  name: "Plan",

  setup() {
    // ----- 设置标题
    const store = useStore();
    store.commit("changeSettingsPageTitle", "复习曲线");
    // --------- 获取数据
    const loadingPlanData = ref(true);
    let status = {
      method: "GET" as Method,
      limit: 50,
      offset: 0,
      hasMore: true,
    };

    const config = {
      url: `${store.state.serverHost}/plans/`,
    };
    const planData = ref<IPlan[]>([]);

    const getPlanData = () => {
      loadingPlanData.value = true;
      getDataOfPage<IPlan>(status, config, false).then((response) => {
        // 加上之前的
        planData.value = [...planData.value, ...response];
        loadingPlanData.value = false;
      });
    };
    // --------------- 添加按钮
    const showAddPlanBtnState = ref(true);
    const handlerShowAddPlanBtn = () => {
      showAddPlanBtnState.value = true;
    };
    const handlerHideAddPlanBtn = () => {
      showAddPlanBtnState.value = false;
    };
    const handlerDeleteBtn = (pid: number) => {
      // 删除卡片
      const config = {
        method: "delete" as Method,
        url: `${store.state.serverHost}/plans/${pid}`,
      };
      deleteData(config, false)
        .then(() => {
          // 提示
          Toast.success("已删除");
          // 移除
          for (let index in planData.value) {
            // index 为string
            const numIndex = Number(index);
            if (planData.value[numIndex].id === pid) {
              planData.value.splice(numIndex, 1);
              break;
            }
          }
        })
        .catch(() => {
          Toast.fail("删除失败");
        });
    };
    // ----------- 显示曲线
    const allPlanSteps = ref<IPlanStep[][]>([]);
    const planSteps = ref<IPlanStep[]>([]);
    const showPlan = ref(false);
    const handlerClickShowPlan = (index: number) => {
      //点击显示曲线
      showPlan.value = true;
      planSteps.value = allPlanSteps.value[index];
    };
    // 获取整个曲线所需时间
    const getPlanAllTime = (planContent: string): string => {
      let temp: IPlanStep[] = [];

      let allSec = 0;
      let reviewCount = 0;
      planContent.split("-").forEach((sec, index) => {
        allSec += Number(sec);

        const time =
          index === 0
            ? `创建卡片${convert_sec_to_string(Number(sec))}后`
            : `距上一次复习${convert_sec_to_string(Number(sec))}后`;
        const title = `第${index + 1}次复习`;
        temp.push({ title, time });
        reviewCount += 1;
      });
      allPlanSteps.value.push(temp);
      const duration = convert_sec_to_string(allSec);

      return `复习:${reviewCount}次 共需: ${duration}`;
    };

    return {
      loadingPlanData, // 获取复习曲线开始
      status,
      getPlanData,
      planData,
      showAddPlanBtnState,
      handlerShowAddPlanBtn, // 按钮控制
      handlerHideAddPlanBtn,
      handlerDeleteBtn,
      handlerClickShowPlan, //点击显示曲线
      showPlan,
      planSteps,
      getPlanAllTime,
    };
  },
});
</script>
<style lang="scss">
// 加载中
.loading-wrap {
  position: absolute;
  bottom: 0;
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100vw;
}
.empty-plan {
  background-color: #f4f3f5;
  min-height: calc(100vh - 56px);
}
.plan-body {
  background-color: #f4f3f5;
  min-height: calc(100vh - 56px);
  padding-top: 10px;
  .cell-item {
    margin-bottom: 10px;
    .content-item {
      // 32px: cell的margin, 64px: content的margin
      width: calc(100vw - 64px - 32px);
      justify-content: flex-start;
      display: flex;
      flex-direction: column;
      margin-left: 15px;
    }
    .swipe-right-wrap {
      display: flex;
      justify-content: center;
      align-items: center;

      height: 66px;
      margin-right: 5px;
      .swipe-right-btn {
        height: 34px;
        width: 34px;
        margin-right: 5px;
      }
    }
    .cant-not-editable {
      height: 66px;
      margin-right: 5px;
      display: flex;
      justify-content: center;
      align-items: center;
      color: #969799;
      font-size: 12px;
    }
  }
}
.add-card-btn-wrap {
  position: fixed;
  bottom: 80px;
  right: 30px;
  button {
    width: 44px;
    height: 44px;
    border-radius: 22px;
  }
}
// 展示复习曲线样式
.van-step {
  padding: 5px 0;
  .show-plan-wrap {
    margin-top: 5px;
    margin-left: 5px;
    .show-plan-title {
      color: #000;
      margin: 0;
      padding: 0;
      font-size: 14px;
    }

    .show-plan-time {
      margin: 5px 0 0 0;
      padding: 0;
      color: #969799;
      font-size: 12px;
    }
  }
}
</style>
