<template>
  <div class="editor_wrap">
    <van-form ref="addCardForm">
      <van-cell-group inset>
        <van-field
          v-model="title"
          name="卡片名称"
          label="卡片名称"
          placeholder="新建卡片"
          :rules="[{ required: true, message: '请填写卡片名' }]"
        />
        <!-- 选择类别 -->
        <van-field
          v-model="categoryText"
          is-link
          readonly
          name="categoryText"
          label="类别"
          placeholder="点击选择类别"
          @click="showCategoryPicker = true"
          :rules="[{ required: true, message: '请先选择类别' }]"
        >
          <template #input>
            <div class="show-category-wrap" ref="categoryContentEle">
              <div class="category-placeholder" v-if="!categoryText">
                <input
                  type="text"
                  class="van-field__control"
                  readonly=""
                  placeholder="点击选择选择类别"
                  aria-labelledby="van-field-22-label"
                />
              </div>
              <div v-else class="category-content">
                <!-- 只有一行 -->
                <div class="category-name">
                  <p>{{ category.name }}</p>
                </div>
                <div class="category-icon">
                  <!-- 使用iconfont -->
                  <i
                    :class="`category-icon iconfont ${category.icon}`"
                    :style="{ color: category.color }"
                  >
                  </i>
                </div>
              </div>
            </div>
          </template>
        </van-field>

        <van-popup v-model:show="showCategoryPicker" position="bottom">
          <van-picker
            :columns="categoryColumns"
            @confirm="onConfirmCategory"
            @cancel="showCategoryPicker = false"
            :loading="loadingCategoryData"
          />
        </van-popup>
        <!-- 编辑概要 -->
        <van-field
          v-model="summary"
          is-link
          readonly
          name="summary "
          label="概要"
          placeholder="点击编辑概要信息"
          @click="showSummaryPicker = true"
          :rules="[{ required: true, message: '请先填写概要信息' }]"
        >
          <template #input>
            <div class="show-editor-wrap" ref="summaryEle">
              <div class="editor-placeholder" v-if="!summary">
                <input
                  type="text"
                  class="van-field__control"
                  readonly=""
                  placeholder="点击编辑概要信息"
                  aria-labelledby="van-field-22-label"
                />
              </div>
              <div v-else class="editor-content">
                <p>
                  {{ summaryText }}
                </p>
              </div>
            </div>
          </template>
        </van-field>

        <van-popup v-model:show="showSummaryPicker" position="bottom">
          <popup-editor
            :title="summaryEditorTitle"
            @onSuccess="showSummaryPicker = false"
          >
            <template #content> <TiptapEditor v-model="summary" /></template>
          </popup-editor>
        </van-popup>
        <!-- 编辑详细描述 -->
        <van-field
          v-model="description"
          is-link
          readonly
          name="description "
          label="详细备注"
          placeholder="点击编辑详细备注"
          @click="showDescriptionPicker = true"
          :rules="[{ required: true, message: '请先填写详细信息' }]"
        >
          <template #input>
            <div class="show-editor-wrap" ref="descriptionEle">
              <div class="editor-placeholder" v-if="!description">
                <input
                  type="text"
                  class="van-field__control"
                  readonly=""
                  placeholder="点击编辑详细备注"
                  aria-labelledby="van-field-22-label"
                />
              </div>
              <div v-else class="editor-content">
                <p>
                  {{ descriptionText }}
                </p>
              </div>
            </div>
          </template>
        </van-field>
        <van-popup v-model:show="showDescriptionPicker" position="bottom">
          <popup-editor
            :title="descriptionEditorTitle"
            @onSuccess="showDescriptionPicker = false"
          >
            <template #content>
              <TiptapEditor v-model="description"
            /></template>
          </popup-editor>
        </van-popup>
      </van-cell-group>
    </van-form>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, watch, onMounted, nextTick } from "vue";
import { useStore } from "vuex";
import { useRouter } from "vue-router";
import { useRect } from "@vant/use";
import type { FormInstance } from "vant";
import { Toast } from "vant";
import { Method } from "axios";

import { ICard, IPostCard, ICategory } from "@/types";
import { getDataOfPage, postCreateData } from "@/utils/request";
import TiptapEditor from "@/components/TiptapEditor.vue";
import PopupEditor from "@/components/PopupEditor.vue";
export default defineComponent({
  name: "AddCard",
  components: { TiptapEditor, PopupEditor },
  setup() {
    const store = useStore();
    // 修改标题
    store.commit("changePageTitle", "新增卡片");
    // ------------ 名称
    const title = ref("");
    // --------------------- 类别
    // TODO: 下一页

    /* ----- 获取分类数据 --------- */
    const loadingCategoryData = ref(true);

    const category = ref<ICategory>(); // 选中的类别
    const categoryText = ref(""); // 用于v-model绑定

    const categoryData: Record<string, ICategory> = {}; // 全部 name:id

    let categoryColumns = ref<string[]>([]); // 给选择的
    const showCategoryPicker = ref(false);
    let getCategoryStatus = {
      method: "GET" as Method,
      limit: 50,
      offset: 0,
      hasMore: true,
    };
    const getCategoryConfig = {
      url: `${store.state.serverHost}/category/`,
    };

    const getCategoryData = () => {
      loadingCategoryData.value = true;

      getDataOfPage<ICategory>(
        getCategoryStatus,
        getCategoryConfig,
        false
      ).then((response) => {
        response.forEach((item) => {
          // 选项
          categoryColumns.value.push(item.name);
          categoryData[item.name] = item;
        });
        loadingCategoryData.value = false;
      });
    };

    const onConfirmCategory = (value: string) => {
      if (categoryData) {
        category.value = categoryData[value];
        categoryText.value = category.value.name;
      }
      showCategoryPicker.value = false;
    };

    // ---------------------- 概要信息
    const showSummaryPicker = ref(false);
    const summary = ref("");
    const summaryText = ref(""); // 用于展示

    watch(summary, () => {
      summaryText.value = summary.value.replace(/<\/?.+?>/g, "");
    });

    // 编辑内容

    const summaryEditorTitle = ref("编辑概要");
    // ---------------------- 详细信息
    const showDescriptionPicker = ref(false);
    const description = ref("");
    const descriptionText = ref(""); // 用于展示

    const descriptionEditorTitle = ref("编辑详细备注");

    watch(description, () => {
      descriptionText.value = description.value.replace(/<\/?.+?>/g, "");
    });
    // ------------ validate
    const router = useRouter();
    const addCardForm = ref<FormInstance>(); // form标签
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
          addCardForm.value
            ?.validate()
            .then(() => {
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
                url: `${store.state.serverHost}/cards/`,
                data,
              };
              postCreateData<ICard, IPostCard>(postConfig, false).then(() => {
                // 成功创建了
                Toast.success("已创建卡片");
                setTimeout(() => {
                  Toast.clear();
                  router.push({ name: "cards" });
                }, 1000);
              });
            })
            .catch((error) => {
              console.log(error);
            });
        }
      }
    );
    //  设置展示的width
    const categoryContentEle = ref<HTMLElement>();
    const summaryEle = ref<HTMLElement>();
    const descriptionEle = ref<HTMLElement>();
    nextTick(() => {
      const categoryRect = useRect(categoryContentEle);
      console.log(categoryRect);

      if (categoryContentEle.value) {
        categoryContentEle.value.style.width =
          String(categoryRect.width) + "px";
      }
      if (summaryEle.value) {
        summaryEle.value.style.width = String(categoryRect.width) + "px";
      }
      if (descriptionEle.value) {
        descriptionEle.value.style.width = String(categoryRect.width) + "px";
      }
    });

    // 正式获取数据
    onMounted(() => {
      getCategoryData(); // 分类数据
    });
    // 监听本页面是否已经被修改
    // TODO: 加上其他的
    watch([title, categoryText, summaryText], () => {
      // 监视多个数据

      store.commit("changeChangeState", true);
    });
    return {
      // 返回的数据
      title,
      addCardForm,
      category,
      categoryText,
      showCategoryPicker,
      categoryColumns,
      onConfirmCategory,
      loadingCategoryData,
      categoryContentEle,
      showSummaryPicker,
      summary,
      summaryText,
      summaryEle,
      summaryEditorTitle,
      showDescriptionPicker,
      description,
      descriptionText,
      descriptionEle,
      descriptionEditorTitle,
    };
  },
});
</script>

<style lang="scss" scoped>
.editor_wrap {
  height: calc(100vh - 46px);

  padding-top: 46px;
  display: flex;
  form {
    width: 100%;
  }
  .show-category-wrap {
    .category-placeholder {
      color: #c8c9cc;
    }
    .category-content {
      display: flex;

      .category-name {
        width: calc(100% - 46px);
        p {
          text-overflow: ellipsis;
          overflow: hidden;
          height: 24px;
          margin: 0;
        }
      }
      .category-icon {
        flex: 1;
        font-size: 24px;
        justify-content: center;
        align-items: center;
      }
    }
  }
  .show-editor-wrap {
    .editor-placeholder {
      color: #c8c9cc;
    }

    .editor-content {
      p {
        text-overflow: ellipsis;
        overflow: hidden;
        height: 24px;
        margin: 0;
      }
    }
  }
}
</style>
