<template>
  <van-nav-bar title="复习" @click-left="calendar" @click-right="more">
    <template #left>
      <van-icon name="calendar-o" size="20" />
    </template>
    <template #right>
      <van-icon name="ellipsis" size="20" />
    </template>
  </van-nav-bar>
  <div class="wrap">{{data}}</div>
</template>

<script lang="ts">
import { defineComponent, ref } from "vue";
import axios from "axios";

export default defineComponent({
  name: "Review",

  setup() {
    const calendar = () => {
      console.log("点击了日历");
    };
    const more = () => {
      console.log("点击了更多");
    };
    const data = ref("");

    axios({
      method: "get",
      url: "http://127.0.0.1:8000/home/",
    }).then((res) => {
      data.value = "dfs";
    });

    console.log(data);
    return {
      calendar,
      more,
      data,
    };
  },
});
</script>