<template>
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
          :rules="[{ required: true, message: '请先选择图标' }]"
        />
        <van-popup v-model:show="showPlanPicker" position="bottom">
          <van-picker
            :columns="planColumns"
            @confirm="onConfirmPlan"
            @cancel="showPlanPicker = false"
            :loading="loadingPlanData"
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
import { IPlan, ICategory, IResponse, IPostCategory } from "@/types";
import { getDataOfPage, postCreateData } from "@/utils/request";
import { Toast } from "vant";
import userIcons from "@/assets/data/icons";
import useColors from "@/assets/data/colors";
export default defineComponent({
  name: "AddCategory",
  components: { ColorPicker, IconPicker },
  setup() {
    const name = ref("");
    const color = ref("");
    const icon = ref("");
    const showColorPopup = ref(false);
    const showIconPopup = ref(false);
    const store = useStore();
    // 监听本页面是否已经被修改
    watch([name, color, icon], () => {
      // 监视多个数据

      store.commit("changeChangeState", true);
    });

    // ----------- 颜色
    const handlerColorPicked = (pickedColor: string) => {
      showColorPopup.value = false;
      color.value = pickedColor;
    };
    const colors = useColors();
    const colorArray = reactive(colors);
    // ------------- 图标
    const icons = userIcons();
    const iconArray = reactive(icons);
    const handlerIconPicked = (pickedIcon: string) => {
      showIconPopup.value = false;
      icon.value = pickedIcon;
    };

    // ------------ 复习计划
    const loadingPlanData = ref(true);

    const plan = ref<number | null>(null); // 选中的ID
    const planText = ref(""); // 用于input展示

    const planData: Record<string, number> = {}; // 全部

    let planColumns = ref<string[]>([]); // 给选择的
    const showPlanPicker = ref(false);

    // 请求复习曲线
    let status = {
      method: "GET" as Method,
      limit: 10,
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
        response.forEach((item) => {
          // 选项
          planColumns.value.push(item.title);
          planData[item.title] = item.id;
        });
        loadingPlanData.value = false;
        if (plan.value === null) {
          // 初始化plan和planText
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
                url: `${store.state.serverHost}/category/`,
                data,
              };

              postCreateData<ICategory, IPostCategory>(postConfig, false).then(
                () => {
                  // 成功创建了
                  Toast.success("已创建");
                  setTimeout(() => {
                    Toast.clear();
                    router.push({ name: "category" });
                  }, 1000);
                }
              );

              console.log(data);
            })
            .catch((error) => {
              console.log(error);
            });
        }
      }
    );

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
