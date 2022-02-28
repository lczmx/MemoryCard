<template>
  <div class="profile-wrap">
    <div class="profile-item">
      <van-cell-group inset>
        <van-cell center title="用户名">
          <template #value>
            <div class="value-wrap">lczmx</div>
          </template>
          <template #right-icon>
            <div class="icon-wrap" @click="handlerClickEditor(0)">
              <van-icon name="edit" size="16" />
            </div>
          </template>
        </van-cell>
      </van-cell-group>
    </div>
    <div class="profile-item">
      <van-cell-group inset>
        <van-cell center title="邮箱">
          <template #value>
            <div class="value-wrap">lczmx@foxmail.com</div>
          </template>
          <template #right-icon>
            <div class="icon-wrap" @click="handlerClickEditor(1)">
              <van-icon name="edit" size="16" />
            </div>
          </template>
        </van-cell>
      </van-cell-group>
    </div>
  </div>
  <!-- 编辑用户数据 -->
  <van-popup
    v-model:show="showEditor"
    position="top"
    :style="{ height: '20%' }"
  >
    <div class="editor-wrap">
      <van-cell-group inset>
        <van-field
          v-model="editorValue"
          :label="editorTitle"
          :placeholder="editorPlaceholder"
        >
          <template #button>
            <van-button
              size="small"
              type="success"
              icon="success"
              round
              @click="handlerClickEditorSubmit"
            ></van-button> </template
        ></van-field>
      </van-cell-group>
    </div>
  </van-popup>
</template>

<script lang="ts">
import { defineComponent, ref } from "vue";
import { useStore } from "vuex";
import { Toast } from "vant";
import { postCreateData } from "@/utils/request";
export default defineComponent({
  name: "Profile",
  setup() {
    // --------- 设置标题
    const store = useStore();
    store.commit("changeSettingsPageTitle", "用户配置");
    const showEditor = ref(false);
    // 编辑数据
    const handlerClickEditor = (flag: number) => {
      switch (flag) {
        case 0:
          // 编辑用户名
          showEditor.value = true;
          editorValue.value = "lczmx";
          editorOriginValue.value = "lczmx";

          editorTitle.value = "用户名";
          editorPlaceholder.value = "请输入用户名";
          editorPostKey.value = "username";

          break;
        case 1:
          // 编辑邮箱
          showEditor.value = true;
          editorValue.value = "lczmx@foxmail.com";
          editorOriginValue.value = "lczmx@foxmail.com";

          editorTitle.value = "邮箱";
          editorPlaceholder.value = "请输入邮箱";
          editorPostKey.value = "email";
          break;
      }
    };
    // 编辑 popup
    const editorOriginValue = ref(""); // 旧的值
    const editorValue = ref("");

    const editorTitle = ref("");
    const editorPlaceholder = ref("");
    const editorPostKey = ref(""); // 发送post请求时的key
    // ---- 提交editor的数据
    const handlerClickEditorSubmit = () => {
      if (editorValue.value === editorOriginValue.value) {
        // 未修改
        Toast({
          message: "未修改",
          position: "bottom",
        });
        return;
      }
      // 发送数据
      if (!editorPostKey.value || !editorValue.value) return;

      //   创建数据
      let data = {};
      switch (editorPostKey.value) {
        case "username":
          data = { username: editorValue.value };
          break;
        case "email":
          data = { email: editorValue.value };
          break;
      }
      const config = {
        url: `${store.state.serverHost}/analyse/`,
        data,
      };
      postCreateData<null, Record<string, string>>(config, true)
        .then(() => {
          Toast.success("修改成功");
          showEditor.value = false;
          setTimeout(() => {
            location.reload();
          }, 2000);
        })
        .catch(() => {
          Toast.fail("修改失败");
        });
    };
    return {
      // 返回的数据
      showEditor,
      handlerClickEditor,
      editorValue, // 编辑input
      editorTitle,
      editorPlaceholder,
      handlerClickEditorSubmit,
    };
  },
});
</script>
<style lang="scss">
.profile-wrap {
  min-height: calc(100vh - 56px);
  padding: 10px 0;
  background-color: #f4f3f5;
  .profile-item {
    margin-bottom: 10px;
    .value-wrap {
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
    }
    .icon-wrap {
      height: 44px;
      display: flex;
      align-items: center;
      margin-left: 5px;
    }
  }
}
.editor-wrap {
  background-color: #f4f3f5;
  height: calc(100%);
  width: 100vw;
  display: flex;
  align-items: center;
  justify-items: center;
  padding: 0;
  .van-cell-group {
    width: 100%;
  }
}
</style>
