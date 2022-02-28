<template>
  <div class="analyse-wrap">
    <!-- 复习相关 -->
    <p class="analyse-date-text">截止北京时间 2022年2月27日23:48:01</p>
    <!-- 卡片相关 -->
    <div class="analyse-item">
      <van-grid clickable :column-num="2">
        <van-grid-item>
          <!-- 今日复习 相对于昨日 -->
          <div class="review-today-wrap">
            <div class="review-diff-wrap">
              <div>较昨日</div>
              <div class="review-diff-text">
                {{
                  analyse_data.review.incr > 0
                    ? "+" + analyse_data.review.incr
                    : analyse_data.review.incr
                }}
              </div>
            </div>
          </div>
          <div class="review-today-text">{{ analyse_data.review.today }}</div>
          <div class="review-title">今日复习次数</div>
        </van-grid-item>
        <van-grid-item
          icon="chart-trending-o"
          :to="{ name: 'analyseReview' }"
          :badge-props="{ dot: true, color: '#1989fa', offset: [10, 1] }"
        >
          <template #text>
            <div class="all-data-title">累计复习次数</div>
          </template>
        </van-grid-item>
        <!-- 创建卡片 -->
        <van-grid-item>
          <!-- 今日复习 相对于昨日 -->
          <div class="review-today-wrap">
            <div class="review-diff-wrap">
              <div>较昨日</div>
              <div class="review-diff-text">
                {{
                  analyse_data.create.incr > 0
                    ? "+" + analyse_data.create.incr
                    : analyse_data.create.incr
                }}
              </div>
            </div>
          </div>
          <div class="review-today-text">{{ analyse_data.create.incr }}</div>
          <div class="review-title">今日创建卡片</div>
        </van-grid-item>
        <van-grid-item
          icon="bar-chart-o"
          :to="{ name: 'analyseCreate' }"
          :badge-props="{ dot: true, color: '#1989fa', offset: [10, 1] }"
        >
          <template #text>
            <div class="all-data-title">累计创建卡片</div>
          </template>
        </van-grid-item>
      </van-grid>
    </div>
    <!-- 类别数量 -->
    <div class="analyse-item">
      <van-grid :column-num="1">
        <van-grid-item>
          <div class="item-category-wrap">
            <div>类别数量</div>
            <div class="category-count">{{ analyse_data.categoryCount }}</div>
          </div>
        </van-grid-item>
      </van-grid>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from "vue";
import { useStore } from "vuex";
import { IAnalyseSummaryData } from "@/types";
import { getDataOfOne } from "@/utils/request";
export default defineComponent({
  name: "Analyse",
  setup() {
    // ----- 设置标题
    const store = useStore();
    store.commit("changeSettingsPageTitle", "数据统计");
    // ------ 获取数据
    const analyse_data = ref<IAnalyseSummaryData>({
      review: { today: 0, incr: 0 },
      create: { today: 0, incr: 0 },
      categoryCount: 0,
    });
    const config = {
      url: `${store.state.serverHost}/analyse/`,
    };
    const getAnalyseData = () => {
      getDataOfOne<IAnalyseSummaryData>(config, true).then((response) => {
        analyse_data.value = response;
      });
    };

    onMounted(() => {
      getAnalyseData();
    });
    return {
      // 返回的数据
      analyse_data,
    };
  },
});
</script>

<style lang="scss" scoped>
.analyse-wrap {
  min-height: calc(100vh - 66px);
  margin: 0 10px;
  .analyse-date-text {
    color: #969790;
    font-size: 12px;
    margin-top: 10;
    margin-bottom: 10;
  }
  .analyse-item {
    margin-bottom: 30px;
    // 今日复习
    .review-today-wrap {
      font-size: 13px;
      .review-diff-wrap {
        display: flex;
        justify-content: center;
        align-items: center;
        .review-diff-text {
          color: #178b50;
          display: flex;
          justify-content: center;
          align-items: center;
        }
      }
    }
    .review-today-text {
      margin-top: 5px;
      font-size: 18px;
      color: #4e5a65;
      font-weight: bold;
    }
    .review-title {
      margin-top: 5px;
      font-size: 14px;
      color: #7c7c7c;
    }
    // 累计复习
    .all-data-title {
      margin-top: 15px;
      font-size: 14px;
      color: #7c7c7c;
    }
    .item-category-wrap {
      display: flex;
      justify-content: space-around;
      align-items: center;
      width: 70%;
      font-size: 15px;
      color: #7c7c7c;
      .category-count {
        color: #178b50;
        display: flex;
        justify-content: space-around;
        align-items: center;
        font-weight: bold;
        font-size: 17px;
      }
    }
  }
}
</style>
