<template>
  <!-- 为分类编辑（修改／新增）提供通用组件 -->
  <div class="editor_wrap">
    <van-form ref="addCategoryForm">
      <van-cell-group inset>
        <van-field
          v-model="name"
          name="类别名"
          label="类别名"
          placeholder="新建类别"
          :rules="[{ required: true, message: '请填写类别名' }]"
        />
        <van-field
          v-model="color"
          is-link
          readonly
          name="color"
          label="颜色"
          placeholder="点击选择颜色"
          @click="showColorPopup = true"
          :rules="[{ required: true, message: '请先选择颜色' }]"
        >
          <template #input>
            <div
              class="show_color"
              :style="{ 'background-color': color }"
            ></div>
          </template>
        </van-field>
        <van-popup v-model:show="showColorPopup" position="bottom">
          <color-picker
            :colorArray="colorArray"
            @picked="handlerColorPicked"
            class="color-picker"
          >
          </color-picker>
        </van-popup>
        <van-field
          v-model="icon"
          is-link
          readonly
          name="icon"
          label="图标"
          placeholder="点击选择图标"
          @click="showIconPopup = true"
          :rules="[{ required: true, message: '请先选择图标' }]"
        >
          <template #input>
            <i
              :class="`iconfont ${icon}`"
              :style="{
                'background-color': '#fff',
                color: '#000',
                'font-size': '24px',
              }"
            ></i>
          </template>
        </van-field>
        <van-popup v-model:show="showIconPopup" position="bottom">
          <icon-picker :iconArray="iconArray" @picked="handlerIconPicked">
          </icon-picker>
        </van-popup>
        <!-- 选择复习曲线 -->
        <van-field
          v-model="planText"
          is-link
          readonly
          name="planText"
          label="复习曲线"
          placeholder="点击选择复习曲线"
          @click="showPlanPicker = true"
          :rules="[{ required: true, message: '请先选择复习曲线' }]"
        />
        <van-popup v-model:show="showPlanPicker" position="bottom">
          <van-picker
            :columns="planColumns"
            @confirm="onConfirmPlan"
            @cancel="showPlanPicker = false"
            :loading="loadingPlanData"
            :default-index="defaultPlanIndex"
          />
        </van-popup>
      </van-cell-group>
    </van-form>
  </div>
</template>

<script lang="ts">
import { defineComponent, reactive, ref, watch, onMounted } from "vue";
import { useStore } from "vuex";
import { useRouter } from "vue-router";
import type { FormInstance } from "vant";
import { Method } from "axios";

import ColorPicker from "@/components/ColorPicker.vue";
import IconPicker from "@/components/IconPicker.vue";
import { IPlan, ICategory, IPostCategory } from "@/types";
import { getDataOfPage, postCreateData } from "@/utils/request";
import { Toast } from "vant";
import userIcons from "@/assets/data/icons";
import useColors from "@/assets/data/colors";
export default defineComponent({
  name: "AddCategory",
  components: { ColorPicker, IconPicker },
  props: {
    propTitle: {
      type: String,
    },
    propName: {
      type: String,
      default: "",
    },
    propIcon: {
      type: String,
      default: "",
    },
    propColor: {
      type: String,
      default: "",
    },
    propPlan: {
      type: Number,
    },
    propPlanText: {
      type: String,
      default: "",
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
    // ------------- 分类名

    const name = ref(props.propName);

    // ----------- 颜色
    const color = ref(props.propColor);
    const showColorPopup = ref(false);

    const handlerColorPicked = (pickedColor: string) => {
      showColorPopup.value = false;
      color.value = pickedColor;
    };
    const colors = useColors();
    const colorArray = reactive(colors);

    // --------------- 图标
    const icon = ref(props.propIcon);
    const showIconPopup = ref(false);

    const icons = userIcons(); // 用于被选择的图标
    const iconArray = reactive(icons);
    const handlerIconPicked = (pickedIcon: string) => {
      showIconPopup.value = false;
      icon.value = pickedIcon;
    };

    // ------------ 复习计划
    const defaultPlanIndex = ref(0); // 默认选中的索引
    const loadingPlanData = ref(true);

    const plan = ref<number | undefined>(props.propPlan); // 选中的ID
    const planText = ref(props.propPlanText); // 用于input展示

    const planData: Record<string, number> = {}; // 全部

    let planColumns = ref<string[]>([]); // 给选择的
    const showPlanPicker = ref(false);

    // ----- 请求复习曲线
    let status = {
      method: "GET" as Method,
      limit: 50,
      offset: 0,
      hasMore: true,
    };
    const config = {
      url: `${store.state.serverHost}/plans/`,
    };

    const getPlanData = () => {
      loadingPlanData.value = true;
      getDataOfPage<IPlan>(status, config, false).then((response) => {
        // 加上之前的
        response.forEach((item, index) => {
          // 选项
          planColumns.value.push(item.title);
          planData[item.title] = item.id;
          // 修改默认选中值
          if (
            defaultPlanIndex.value === 0 &&
            item.title === planText.value &&
            item.id === plan.value
          ) {
            defaultPlanIndex.value = index;
          }
        });
        loadingPlanData.value = false;

        if (typeof plan.value === "undefined" && !planText.value) {
          // 初始化plan和planText
          // 修改页面时 跳过
          if (planColumns.value.length > 0) {
            // 默认为第一个
            [planText.value] = planColumns.value;
            onConfirmPlan(planText.value);
          }
        }
      });
    };
    // 正式获取数据
    onMounted(() => {
      getPlanData();
    });
    // TODO 触底事件, 下一页

    const onConfirmPlan = (value: string) => {
      // 选中选项后调用
      planText.value = value;
      if (planData) {
        plan.value = planData[value];
      }
      showPlanPicker.value = false;
    };
    // ------------ validate
    const router = useRouter();
    const addCategoryForm = ref<FormInstance>(); // form标签
    // 监听是否可以提交了
    watch(
      // 监听响应式数据
      () => store.state.submitData,
      (value) => {
        if (value) {
          // 重新改为false
          store.commit("changeSubmitData", false);

          // 检验表单数据
          // 返回Promise对象
          addCategoryForm.value
            ?.validate()
            .then(() => {
              const data = {
                name: name.value,
                icon: icon.value,
                color: color.value,
                plan: plan.value as number,
              };
              const postConfig = {
                method: "post" as Method,
                url: props.postUrl,
                data,
              };

              postCreateData<ICategory, IPostCategory>(postConfig, false).then(
                () => {
                  // 成功创建了
                  Toast.success(props.successText);
                  setTimeout(() => {
                    Toast.clear();
                    router.go(-1);
                  }, 1000);
                }
              );
            })
            .catch((error) => {
              console.log(error);
            });
        }
      }
    );

    // -------- 监听本页面是否已经被修改
    // plan有默认值 不需要选择
    watch([name, color, icon], () => {
      // 监视多个数据

      store.commit("changeChangeState", true);
    });
    return {
      // 返回的数据
      name,
      color,
      icon,
      showColorPopup,
      showIconPopup,
      handlerColorPicked,
      colorArray,
      iconArray,
      handlerIconPicked,
      planText,
      planColumns,
      loadingPlanData,
      showPlanPicker,
      onConfirmPlan,
      addCategoryForm,
      defaultPlanIndex,
    };
  },
});
</script>

<style lang="scss" scoped>
.editor_wrap {
  height: calc(100vh - 46px);
  padding-top: 46px;
  .show_color {
    width: 24px;
    height: 24px;
    border-radius: 5px;
  }
  .color-picker {
    margin: 10px;
  }
}
</style>
