<template>
  <div class="card-review-wrap">
    <!-- 拖拽提示 -->
    <div class="show_drag_text">提示</div>
    <fly-card
      @onDragMove="onCardDragMove"
      @onThrowDone="onCardThrowDone"
      @onThrowFail="onCardThrowFail"
      :cardWidth="cardWidth"
      :cardHeight="cardHeight"
      :throwTriggerDistance="100"
      :hasShadow="true"
    >
      <template #firstCard>
        <van-loading color="#1989fa" v-show="loading" />
        <div class="card-review-container" v-show="!loading">
          <div class="card-info van-ellipsis">
            <!-- 图标和标题 -->
            <div class="card-category-icon">
              <!-- 使用iconfont -->
              <i
                :class="`category-icon iconfont ${currentCardCategory.icon}`"
                :style="{ color: currentCardCategory.color }"
              >
              </i>
            </div>
            <div class="card-title" ref="titleEle">
              {{ reviewCard.currentCard.title }}
            </div>
          </div>
          <!-- 概要信息 -->
          <div
            class="card-summary"
            v-html="reviewCard.currentCard.summary"
            ref="summaryEle"
          ></div>
          <!-- 详细信息 -->
          <div class="card-description-wrap">
            <!-- 显示信息按钮 -->
            <div class="show-desc-btn">
              <van-switch v-model="showDescBtn" />
            </div>
            <!-- <div
              
              v-html="reviewCard.currentCard.description"
            ></div> -->

            <van-skeleton
              class="card-desc-content"
              title
              :row="3"
              :loading="!showDescBtn"
            >
              <div>实际内容</div>
            </van-skeleton>
          </div>
        </div>
      </template>
    </fly-card>
    <!-- 卡片工具栏 -->
    <div class="card-tool-bar">tool bar</div>
  </div>
</template>

<script lang="ts">
import { defineComponent, watch, ref, reactive, onMounted } from "vue";
import { useRouter } from "vue-router";
import { useStore } from "vuex";

import { useWindowSize } from "@vant/use";
import FlyCard from "@/components/FlyCard.vue";
import { ICardDragObject, ICard, IReviewCard, ICategory } from "@/types";
import { getDataOfOne, getDataOfPage } from "@/utils/request";
import { Method } from "axios";

export default defineComponent({
  name: "CardReview",
  components: {
    FlyCard,
  },
  setup() {
    // ---------- 动态调整卡片宽和高

    const { width, height } = useWindowSize();

    const cardWidth = ref(Math.round(width.value * 0.8));
    const cardHeight = ref(Math.round(height.value * 0.8));
    watch([width, height], () => {
      if (width.value && height.value) {
        cardWidth.value = Math.round(width.value * 0.8);
        cardHeight.value = Math.round(height.value * 0.8);
        resetSDStyle(cardWidth.value, cardHeight.value);
      }
    });

    const titleEle = ref<HTMLElement>();
    const summaryEle = ref<HTMLElement>();
    // const descriptionEle = ref<HTMLElement>();

    const resetSDStyle = (w: number, h: number) => {
      // summary和description样式
      if (titleEle.value) {
        titleEle.value.style.width = w - 30 + "px";
      }
      if (summaryEle.value) {
        summaryEle.value.style.width = Math.round(h * 0.5) + "px";
      }
    };
    // ---------- 处理的函数
    const dragLeft = () => {
      console.log("dragLeft", reviewCard);
      console.log(currentCardIndex);
    };
    const dragRight = () => {
      console.log("dragRight");
    };
    const dragTop = () => {
      console.log("dragTop");
    };
    const dragBottom = () => {
      console.log("dragBottom");
    };
    let direction = "";
    const onCardDragMove = (obj: ICardDragObject) => {
      // 1. 判断方向
      if (Math.abs(obj.left) > Math.abs(obj.top)) {
        // 左右滑动
        direction = obj.left < 0 ? "left" : "right";
      } else {
        // 上下滑动
        direction = obj.top < 0 ? "top" : "bottom";
      }
    };

    const onCardThrowDone = () => {
      // 执行处理函数
      switch (direction) {
        case "left":
          dragLeft();
          break;

        case "right":
          dragRight();
          break;

        case "top":
          dragTop();
          break;

        case "bottom":
          dragBottom();
          break;
      }
    };
    const onCardThrowFail = () => {
      // 清空方向
      direction = "";
    };
    // ---- 获取当前卡片的数据
    const reviewCard = reactive<IReviewCard>({
      prevCard: null,
      currentCard: {} as ICard,
      nextCard: null,
    }); // 卡片数据, 有三个卡片
    const currentCardCategory = reactive<ICategory>({} as ICategory); // 类别
    let currentCardIndex: number;
    let needReview = ref<number[]>([]); // 需要复习的卡片ID
    const loading = ref(true);

    const store = useStore();
    const router = useRouter();

    const getCardData = (cid: number) => {
      loading.value = true;
      const config = {
        url: `${store.state.serverHost}/review/${cid}`,
      };
      getDataOfOne<ICard>(config, false).then((response) => {
        // 修改当前卡片
        reviewCard.currentCard = response;
        // {...currentCardCategory} = response.category;
        // {currentCardCategory} = response.category
        Object.assign(currentCardCategory, response.category);
        loading.value = false;
      });
    };
    // --------- 需要复习的ID
    let status = {
      method: "GET" as Method,
      limit: 10,
      offset: 0,
      hasMore: true,
    };
    const config = {
      url: `${store.state.serverHost}/review/need`,
    };

    const getNeedReviewCardID = async () => {
      // 获取需要复习的卡片ID数组

      getDataOfPage<number>(status, config, false)
        .then((response) => {
          // 获取当前id的索引
          response.forEach((cardID, index) => {
            if (reviewCard.currentCard.id === cardID) {
              currentCardIndex = index;
            }
          });

          // 加入卡片ID数组
          needReview.value = [...needReview.value, ...response];
        })
        .catch(() => {
          // 异常
          status.hasMore = false;
        });
    };

    watch([needReview], () => {
      // 同步获取
      if (status.hasMore) {
        getNeedReviewCardID();
      } else {
        // 已经全部获取完了
        getPrevAndNextCard(); // 上下两张卡
        resetSDStyle(cardWidth.value, cardHeight.value);
      }
    });

    // ----------- 获取其余两张卡片
    const getPrevAndNextCard = () => {
      if (currentCardIndex > 0) {
        // 有上一张
        const prevCardID = needReview.value[currentCardIndex - 1];

        const config = {
          url: `${store.state.serverHost}/review/${prevCardID}`,
        };

        getDataOfOne<ICard>(config, false).then((response) => {
          // 修改上一个卡片
          reviewCard.prevCard = response;
        });
      } else {
        // 没有上一卡片了
        reviewCard.prevCard = null;
      }

      if (currentCardIndex < needReview.value.length - 1) {
        // 有下一卡片
        const nextCardID = needReview.value[currentCardIndex + 1];
        const config = {
          url: `${store.state.serverHost}/review/${nextCardID}`,
        };

        getDataOfOne<ICard>(config, false).then((response) => {
          reviewCard.nextCard = response;
        });
      } else {
        // 没有下一卡片
        reviewCard.nextCard = null;
      }
    };

    onMounted(() => {
      const cid = Number(router.currentRoute.value.params.cid);
      getCardData(cid); // 获取本页面的卡片数据
      getNeedReviewCardID(); // 获取所有ID, 内部获取上下卡片
    });

    // ----------- 显示/隐藏 详细信息
    const showDescBtn = ref(false);
    return {
      cardWidth,
      cardHeight,
      titleEle,
      summaryEle,
      onCardDragMove,
      onCardThrowDone,
      onCardThrowFail,
      reviewCard,
      currentCardCategory,
      loading,
      showDescBtn,
    };
  },
});
</script>

<style lang="scss" scoped>
.card-review-wrap {
  .show_drag_text {
    background-color: #f4f3f5;
  }
  .card-review-container {
    padding: 10px;
    .card-info {
      display: flex;
      width: 100%;
      height: 24px;
      justify-content: center;
      align-items: center;
      .card-category-icon {
        margin-right: 20px;
        i {
          font-size: 24px;
        }
      }

      .card-title {
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
      }
    }
    .card-summary {
      padding: 10px 0;
      height: 300px;
    }

    .card-description-wrap {
      .card-desc-content {
        margin-top: 10px;
        padding: 0;
      }
    }
  }

  .card-tool-bar {
  }
}

.card-review-wrap {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  widows: 100vw;
}
</style>
