<!--  统一的添加页面  -->

<template>
  <div class="help-wrap">
    <div class="help-item" v-for="(item, index) in docsData" :key="index">
      <van-cell-group inset>
        <van-cell :title="item.title" is-link @click="showDoc(index)" />
      </van-cell-group>
    </div>
  </div>
  <!-- 文档内弹出层 -->
  <van-popup
    v-model:show="showDocPopup"
    close-icon="close"
    :style="{ height: '75vh', width: '75vw' }"
    round
  >
    <div class="doc-content-wrap">
      <div
        class="doc-content-item"
        v-for="(content, index) in docContentArr"
        :key="index"
      >
        {{ content }}
      </div>
    </div>
  </van-popup>
</template>

<script lang="ts">
import { defineComponent, onMounted, ref } from "vue";
import { useStore } from "vuex";
import { getDataOfOne } from "@/utils/request";
import { IDocs } from "@/types";
export default defineComponent({
  name: "Help",
  setup() {
    const store = useStore();
    store.commit("changeSettingsPageTitle", "帮助中心");
    // -------- 获取文档数据
    const docsData = ref<IDocs[]>();
    const getDocsData = () => {
      getDataOfOne<IDocs[]>(
        { url: `${store.state.serverHost}/help/docs` },
        true
      ).then((response) => {
        docsData.value = response;
      });
    };
    onMounted(() => {
      getDocsData();
    });
    // ------- 显示文档
    const showDocPopup = ref(false);
    const docContentArr = ref<string[]>([]); // 显示的文档内容
    const showDoc = (index: number) => {
      showDocPopup.value = true;
      if (!docsData.value || !docsData.value[index]) return;

      docContentArr.value = docsData.value[index].content.split(/\r?\\n/g);
    };
    return {
      // 返回的数据
      docsData,
      showDoc,
      showDocPopup,
      docContentArr,
    };
  },
});
</script>

<style lang="scss" scoped>
.help-wrap {
  min-height: calc(100vh - 66px);
  background-color: #f3f4f5;
  padding-top: 10px;
  padding-bottom: 10px;
  .help-item {
    margin-bottom: 10px;
  }
}
.doc-content-wrap {
  margin: 15px 0;
  padding: 0 10px;
  height: calc(75vh - 30px);
  overflow: scroll;
  .doc-content-item {
    margin-bottom: 10px;
    text-indent: 1em;
  }
}
</style>
