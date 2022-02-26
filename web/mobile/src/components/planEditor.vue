<template>
  <!-- 为分类编辑（修改／新增）提供通用组件 -->
  <div class="editor-wrap">
    <van-form ref="addPlanForm">
      <van-cell-group inset>
        <van-field
          v-model="title"
          name="名称"
          label="名称"
          placeholder="新建曲线"
          :rules="[{ required: true, message: '请填写复习曲线名称' }]"
        />
        <van-field
          v-model="planText"
          readonly
          name="planText"
          label="复习时间"
          placeholder=""
        >
          <template #button>
            <van-icon
              @click="handlerClickAddPlanBtn"
              class="iconfont"
              class-prefix="icon"
              name="roundaddfill"
              size="24"
              color="#1989fa"
              round
            />
          </template>
        </van-field>
      </van-cell-group>
    </van-form>
  </div>
  <div class="show-plans-wrap">
    <van-steps
      direction="vertical"
      :active="plans.length - 1"
      inactive-color="#41b883"
      active-color="#41b883"
    >
      <van-step
        v-for="(item, index) in plans"
        :key="index"
        @click="handlerClickShowStepOption(index)"
      >
        <div class="show-plan-wrap">
          <p class="show-plan-title" v-text="convert_plan_to_title(index)"></p>
          <p
            class="show-plan-time"
            v-text="convert_plan_to_time(item, index)"
          ></p>
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
  </div>
  <!-- 修改时间弹出层 -->
  <van-popup
    v-model:show="showPlansPopup"
    position="bottom"
    closeable
    close-icon="success"
    @click-close-icon="handlerClickCloseIcon"
  >
    <div class="plans-cell-wrap">
      <van-cell-group inset class="cell-item">
        <van-cell center title-class="content-item" title="日">
          <template #value>
            <van-stepper
              v-model="currentPlan.day"
              min="0"
              theme="round"
              button-size="22"
            />
          </template>
        </van-cell>
        <van-cell center title-class="content-item" title="时">
          <template #value>
            <van-stepper
              v-model="currentPlan.hour"
              min="0"
              theme="round"
              button-size="22"
            />
          </template>
        </van-cell>
        <van-cell center title-class="content-item" title="分">
          <template #value>
            <van-stepper
              v-model="currentPlan.minute"
              min="0"
              theme="round"
              button-size="22"
            />
          </template>
        </van-cell>
        <van-cell center title-class="content-item" title="秒">
          <template #value>
            <van-stepper
              v-model="currentPlan.second"
              min="0"
              theme="round"
              button-size="22"
            />
          </template>
        </van-cell>
      </van-cell-group>
    </div>
  </van-popup>
  <!-- step选项 -->
  <van-action-sheet
    v-model:show="showStepOptionActionSheet"
    :actions="showStepOption"
    cancel-text="取消"
    close-on-click-action
    @cancel="() => (showStepOptionActionSheet = false)"
    @select="onSelectStepOption"
  />
</template>

<script lang="ts">
import { defineComponent, ref, reactive, watch } from "vue";
import { useStore } from "vuex";
import { useRouter } from "vue-router";
import { Toast } from "vant";
import type { ActionSheetAction, FormInstance } from "vant";

import {
  use_fmt_to_sec,
  convert_sec_to_string,
  convert_sec_to_other,
} from "@/hook";

export default defineComponent({
  name: "PlanEditor",

  props: {
    propTitle: {
      type: String,
    },
    successText: {
      type: String,
      required: true,
    },
    postUrl: {
      type: String,
      required: true,
    },
  },
  setup(props) {
    const store = useStore();
    // 修改标题
    store.commit("changePageTitle", props.propTitle);
    const title = ref("");
    const value = ref(0);
    const plans = ref<number[]>([]); // 曲线秒数
    const planText = ref("");

    // -------- 显示 popup
    const showPlansPopup = ref(false);
    const handlerClickAddPlanBtn = () => {
      // 重置数据
      currentPlan.day = 0;
      currentPlan.hour = 0;
      currentPlan.minute = 0;
      currentPlan.second = 0;
      // 显示
      showPlansPopup.value = true;
    };
    // 步进器
    const currentPlan = reactive({
      day: 0,
      hour: 0,
      minute: 0,
      second: 0,
    });
    // -------- 点击关闭, 保存数据
    const handlerClickCloseIcon = () => {
      const sec = use_fmt_to_sec(
        currentPlan.day,
        currentPlan.hour,
        currentPlan.minute,
        currentPlan.second
      );
      // 设置 or 修改
      if (typeof currentStepIndex !== "number") {
        if (sec > 0) {
          plans.value.push(sec);
        }
      } else {
        if (sec > 0) plans.value[currentStepIndex] = sec;
        // 重置index
        currentStepIndex = null;
      }

      showPlansPopup.value = false;
    };

    // ---- 格式化plans的数据
    const convert_plan_to_title = (index: number) => {
      return `第${index + 1}次复习`;
    };
    const convert_plan_to_time = (sec: number, index: number) => {
      return index === 0
        ? `创建卡片${convert_sec_to_string(sec)}后`
        : `距上一次复习${convert_sec_to_string(sec)}后`;
    };
    // ----------- 点击step
    const showStepOptionActionSheet = ref(false);
    let currentStepIndex: number | null = null;
    const showStepOption = ref([
      { name: "修改" },
      { name: "删除", color: "red" },
    ]);
    const handlerClickShowStepOption = (index: number) => {
      currentStepIndex = index;
      showStepOptionActionSheet.value = true;
    };
    // 选中选项
    const onSelectStepOption = (action: ActionSheetAction, index: number) => {
      if (typeof currentStepIndex !== "number") return;
      if (plans.value && plans.value.length <= currentStepIndex) return;
      switch (index) {
        case 0: {
          // 修改
          const sec = plans.value[currentStepIndex];
          const { days, hours, minutes, seconds } = convert_sec_to_other(sec);

          currentPlan.day = days;
          currentPlan.hour = hours;
          currentPlan.minute = minutes;
          currentPlan.second = seconds;
          // 隐藏options
          showPlansPopup.value = true;
          showStepOptionActionSheet.value = false;

          break;
        }
        case 1:
          // 删除
          plans.value.splice(currentStepIndex, 1);
          // 隐藏options
          showStepOptionActionSheet.value = false;
          // 重置
          currentStepIndex = null;
          break;
      }
    };
    // ------------ validate
    const router = useRouter();
    const addPlanForm = ref<FormInstance>(); // form标签
    // 监听是否可以提交了
    watch(
      // 监听响应式数据
      () => store.state.submitData,
      (value) => {
        if (value) {
          // 重新改为false
          store.commit("changeSubmitData", false);
          // 修改PlanText, 让其有值
          if (plans.value.length > 0) {
            planText.value = " ".repeat(plans.value.length);
          } else {
            Toast.fail("请先添加复习时间");
          }

          // 检验表单数据
          // 返回Promise对象
          addPlanForm.value
            ?.validate()
            .then(() => {
              /*
              if (!category.value) {
                return;
              }
              const data = {
                title: title.value,
                category: category.value.id,
                summary: summary.value,
                description: description.value,
              };
              const postConfig = {
                method: "post" as Method,
                url: props.postUrl,
                data,
              };
              postCreateData<ICard, IPostCard>(postConfig, false).then(() => {
                // 成功创建了
                Toast.success(props.successText);
                setTimeout(() => {
                  Toast.clear();
                  router.go(-1);
                }, 1000);
                
              });
              */
            })
            .catch((error) => {
              console.log(error);
            });
        }
      }
    );
    // 监听本页面是否已经被修改
    watch(
      [title, plans.value],
      () => {
        // 监视多个数据
        store.commit("changeChangeState", true);
      },
      {
        deep: true, // 是否是深度监视, 默认是false
      }
    );
    return {
      // 返回的数据
      title,
      value,
      plans,
      planText,
      showPlansPopup,
      handlerClickAddPlanBtn,
      currentPlan,
      handlerClickCloseIcon,
      convert_plan_to_title,
      convert_plan_to_time,
      handlerClickShowStepOption, //显示plan的动作面板
      showStepOptionActionSheet,
      showStepOption,
      onSelectStepOption, // 验证
      addPlanForm,
    };
  },
});
</script>

<style lang="scss">
.editor-wrap {
  height: 88px;
  padding-top: 46px;
}

.show-plans-wrap {
  height: calc(100vh - 46px - 88px - 40px - 5px);
  overflow: scroll;
  padding-top: 20px;
  margin: 5px 16px 20px 16px;
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

.plans-cell-wrap {
  padding: 40px 0 20px 0;
}
</style>
