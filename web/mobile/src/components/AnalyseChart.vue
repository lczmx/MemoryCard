<template>
  <div class="chart-wrap">
    <!-- 快捷时间选择 -->
    <div class="date-tool-bar">
      <div class="tool-item">
        <van-button
          :type="activeDateIndex === 0 ? 'primary' : 'default'"
          @click="handlerClickDateBtn(0)"
          >近一周</van-button
        >
      </div>
      <div class="tool-item">
        <van-button
          :type="activeDateIndex === 1 ? 'primary' : 'default'"
          @click="handlerClickDateBtn(1)"
          >近一月</van-button
        >
      </div>
      <div class="tool-item">
        <van-button
          :type="activeDateIndex === 2 ? 'primary' : 'default'"
          @click="handlerClickDateBtn(2)"
          >近半年</van-button
        >
      </div>
      <div class="tool-item">
        <van-button
          :type="activeDateIndex === 3 ? 'primary' : 'default'"
          @click="handlerClickDateBtn(3)"
          >近一年</van-button
        >
      </div>
    </div>
    <div id="container"></div>

    <!-- 自定义时间选择 -->
    <div class="date-wrap" @click="showCalendar = true">
      <div class="date-select">
        <div class="date-icon">
          <van-icon class="iconfont" class-prefix="icon" name="rili" />
        </div>
        选择日期
      </div>
      <div class="show-date">
        <div class="date1 date">{{ showDateStart }}</div>
        <div class="date-char">/</div>
        <div class="date2 date">{{ showDateEnd }}</div>
      </div>
    </div>
  </div>
  <!-- 日期选择器 -->
  <van-calendar
    v-model:show="showCalendar"
    type="range"
    @confirm="onConfirmCalendar"
    :min-date="beforeYear.toDate()"
    :max-date="now.toDate()"
    color="#1989fa"
    :default-date="[dayjs(showDateStart).toDate(), dayjs(showDateEnd).toDate()]"
  />
  <!-- line loading -->
  <div class="loading-chart" v-show="loadingChart">
    <van-loading color="#1989fa" />
  </div>

  <!-- 设置背景颜色 -->
  <div class="chart-wrap-bkg"></div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from "vue";
import dayjs from "dayjs";
dayjs.locale("zh-cn");
import { Line } from "@antv/g2plot";
import { IAnalyseData, IAnalysePostData } from "@/types";
import { postCreateData } from "@/utils/request";
import { Method } from "axios";
import { Toast } from "vant";
import { useStore } from "vuex";
export default defineComponent({
  name: "AnalyseChart",
  props: {
    url: {
      type: String,
      required: true,
    },
    title: {
      type: String,
      required: true,
    },
  },
  setup(props) {
    // ----- 设置标题
    const store = useStore();
    store.commit("changeSettingsPageTitle", props.title);

    const data = ref<IAnalyseData[]>();
    // 获取数据:
    const getAnalyseData = () => {
      if (!showDateStart.value || !showDateEnd.value) {
        Toast.fail("非法时间格式");
        return;
      }
      const config = {
        method: "post" as Method,
        url: props.url,
        data: {
          startDate: showDateStart.value,
          endDate: showDateEnd.value,
        },
      };

      postCreateData<IAnalyseData[], IAnalysePostData>(config, true).then(
        (response) => {
          data.value = response;
          // 渲染
          if (!line) initChart();
          changeData();
        }
      );
    };
    // -- 更新数据
    const changeData = () => {
      if (!data.value) return;
      line.changeData(data.value);
    };
    // ---------- 创建line实例
    let line: Line;
    const loadingChart = ref(true); // 加载line实例中
    const initChart = () => {
      line = new Line("container", {
        data: [], // 后面才指定
        xField: "date",
        yField: "count",
        xAxis: {
          range: [0, 1],
          tickCount: 5,
        },
        smooth: true,
      });
      line.render();
      loadingChart.value = false;
    };
    // 初始化开始-截止时间
    const showDateStart = ref<string>();
    const showDateEnd = ref<string>();

    const now = dayjs(); // 目前
    const beforeYear = now.subtract(1, "year");
    const initDate = (value = 7, unit = "day") => {
      const before = now.subtract(value, unit);
      showDateStart.value = before.format("YYYY-MM-DD");
      showDateEnd.value = now.format("YYYY-MM-DD");
    };
    // -------- 日历选择

    const showCalendar = ref(false);
    const onConfirmCalendar = (values: Date[]) => {
      showCalendar.value = false;
      const [start, end] = values;
      showDateStart.value = dayjs(start).format("YYYY-MM-DD");
      showDateEnd.value = dayjs(end).format("YYYY-MM-DD");
      getAnalyseData();
    };
    // ------- 时间选择 btn组
    const activeDateIndex = ref(0);
    const handlerClickDateBtn = (index: number) => {
      switch (index) {
        case 0:
          initDate(7, "day");
          getAnalyseData();
          break;
        case 1:
          initDate(1, "month");
          getAnalyseData();
          break;
        case 2:
          initDate(6, "month");
          getAnalyseData();
          break;
        case 3:
          initDate(1, "year");
          getAnalyseData();
          break;
      }
      activeDateIndex.value = index;
    };
    onMounted(() => {
      initDate();
      getAnalyseData();
    });
    // ------- 修改日期时 重新获取数据
    return {
      now,
      beforeYear,
      showDateStart,
      showDateEnd,
      showCalendar,
      onConfirmCalendar,
      activeDateIndex,
      handlerClickDateBtn,
      loadingChart,
      dayjs,
    };
  },
});
</script>

<style lang="scss">
.loading-chart {
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 999;
  position: fixed;
  bottom: 0;
  top: 46px;
  right: 0;
  left: 0;
  background: #fff;
}
.chart-wrap-bkg {
  z-index: -999;
  position: fixed;
  bottom: 0;
  top: 46px;
  right: 0;
  left: 0;
  background: #f3f4f5;
}
.chart-wrap {
  padding: 10px;
  background-color: #f3f4f5;
  // 图表容器占位
  .date-tool-bar {
    display: flex;
    align-items: center;
    justify-content: center;
    padding-bottom: 30px;
    .tool-item {
      .van-button__text {
        font-size: 12px;
      }
    }
  }

  #container {
    border-radius: 8px;
    background-color: #fff;
    padding: 10px;
  }

  .date-wrap {
    background-color: #fff;
    border-radius: 8px;
    margin-top: 30px;
    padding: 10px 20px;
    display: flex;
    align-items: center;
    justify-content: center;
    .date-select {
      flex: 1;
      display: flex;
      align-items: center;
      font-size:14px;
      .date-icon {
        margin-right: 5px;
        display: flex;
        align-items: center;
      }
    }
    .show-date {
      flex: 1;
      display: flex;
      align-items: center;
      .date {
        font-size: 12px;
      }
      .date-char {
        font-size: 30px;
      }
    }
  }
}
</style>
