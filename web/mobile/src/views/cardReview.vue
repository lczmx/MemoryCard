<template>
  <div class="card-review-wrap">
    <!-- 拖拽提示 -->
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
        <van-loading
          color="#1989fa"
          v-show="loading"
          :style="{
            top: `${Math.round(cardHeight / 2) - 10}px`,
            left: `${Math.round(cardWidth / 2) - 10}px`,
          }"
        />
        <div
          class="card-review-container"
          v-show="!loading"
          id="description_teleport"
        >
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
            class="card-summary-wrap"
            @touchstart.stop="null"
            @touchmove.stop="null"
            @touchcancel.stop="null"
            @touchend.stop="null"
            ref="summaryEle"
          >
            <van-cell title="卡片概要信息">
              <template #label>
                <div
                  class="card-summary"
                  :style="{
                    width: cardWidth - 52 + 'px',
                    height: cardHeight - 144 - 24 - 60 - 16 - 20 + 'px',
                  }"
                  v-html="reviewCard.currentCard.summary"
                ></div>
              </template>
            </van-cell>
          </div>

          <!-- 详细信息 -->
          <div class="card-desc-skeleton-wrap">
            <!-- 显示信息按钮 -->
            <div class="show-desc-btn">
              <van-cell center title="显示卡片详细信息">
                <template #right-icon>
                  <van-switch v-model="showDescBtn" />
                </template>
              </van-cell>
            </div>

            <van-skeleton title :row="3" :loading="!showDescBtn">
            </van-skeleton>
          </div>
          <!-- 显示进度 -->

          <div
            class="progress-wrap"
            v-show="!isNaN(currentCardIndex) && needReview.length > 0"
          >
            <div class="progress-now">{{ currentCardIndex + 1 }}</div>
            <div class="progress-char">/</div>
            <div class="progress-all">{{ needReview.length }}</div>
            <!-- 占位符 -->
            <div :style="{ width: '50px' }"></div>
          </div>
        </div>
      </template>
      <!-- 底部展示的卡片 -->
      <template #secondCard>
        <div v-if="bottomShowReviewCard" class="card-review-container">
          <div class="card-info van-ellipsis">
            <!-- 图标和标题 -->
            <div class="card-category-icon">
              <!-- 使用iconfont -->
              <i
                :class="`category-icon iconfont ${bottomShowReviewCard.category.icon}`"
                :style="{ color: bottomShowReviewCard.category.color }"
              >
              </i>
            </div>
            <div
              class="card-title"
              :style="{
                width: cardWidth - 30 + 'px',
              }"
            >
              {{ bottomShowReviewCard.title }}
            </div>
          </div>
          <!-- 概要信息 -->
          <div
            class="card-summary-wrap"
            :style="{
              width: cardWidth - 30 + 'px',
              height: cardHeight - 144 - 24 - 60 + 'px',
            }"
          >
            <van-cell title="卡片概要信息">
              <template #label>
                <div
                  class="card-summary"
                  :style="{
                    width: cardWidth - 52 + 'px',
                    height: cardHeight - 144 - 24 - 60 - 16 - 20 + 'px',
                  }"
                  v-html="bottomShowReviewCard.summary"
                ></div>
              </template>
            </van-cell>
          </div>

          <!-- 详细信息 -->
          <div class="card-desc-skeleton-wrap">
            <!-- 显示信息按钮 -->
            <div class="show-desc-btn">
              <van-cell center title="显示卡片详细信息">
                <template #right-icon>
                  <van-switch v-model="showDescBtn" />
                </template>
              </van-cell>
            </div>
            <van-skeleton title :row="3" :loading="true"> </van-skeleton>
          </div>
        </div>
      </template>
    </fly-card>

    <!-- 卡片工具栏 -->
    <div class="card-tool-bar">
      <div class="card-tool-item">
        <van-icon
          class="iconfont"
          class-prefix="icon"
          name="bianji"
          size="24"
          @click="handlerClickEditor"
        />
      </div>
      <div class="card-tool-item">
        <van-icon
          v-show="reviewCard.currentCard.isStar"
          class="iconfont"
          class-prefix="icon"
          name="favorfill"
          color="#f08300"
          size="24"
          @click="handlerClickStar"
        />
        <van-icon
          v-show="!reviewCard.currentCard.isStar"
          class="iconfont"
          class-prefix="icon"
          name="favor"
          size="24"
          @click="handlerClickStar"
        />
      </div>
      <div class="card-tool-item">
        <van-icon
          class="iconfont"
          class-prefix="icon"
          name="fanhui"
          size="24"
          @click="handlerClickBack"
        />
      </div>
    </div>
  </div>
  <van-popup
    @touchstart.stop="null"
    @touchmove.stop="null"
    @touchcancel.stop="null"
    @touchend.stop="null"
    v-model:show="showDescBtn"
    round
    duration=".5"
    :overlay-style="{ backgroundColor: '#fff', opacity: 0 }"
    :style="{ width: cardWidth + 'px', height: cardHeight + 'px' }"
    teleport="#description_teleport"
    class="popup-desc-wrap"
  >
    <div
      class="card-review-desc-wrap"
      v-html="reviewCard.currentCard.description"
    ></div>
  </van-popup>
</template>

<script lang="ts">
import { defineComponent, watch, ref, reactive, onMounted } from "vue";
import { useRouter } from "vue-router";
import { useStore } from "vuex";
import { Notify, Dialog } from "vant";
import { useEventListener } from "@vant/use";

import { useWindowSize } from "@vant/use";
import FlyCard from "@/components/FlyCard.vue";
import { ICardDragObject, ICard, IReviewCard, ICategory, IStar } from "@/types";
import { getDataOfOne, getDataOfPage, postCreateData } from "@/utils/request";
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

    const resetSDStyle = (w: number, h: number) => {
      // summary和description样式
      if (titleEle.value) {
        titleEle.value.style.width = w - 30 + "px";
      }
      if (summaryEle.value) {
        summaryEle.value.style.width = w - 30 + "px";
        // 卡片高度 - desc骨架高度 - title高度 - 所有margin/
        summaryEle.value.style.height = h - 144 - 24 - 60 + "px";
      }
    };
    // ---------- 处理的函数
    const dragLeft = async () => {
      // 下张

      if (reviewCard.nextCard) {
        loading.value = true;
        /*
          p  c  n
             p  c  n (获取)

        */
        if (typeof currentCardIndex.value !== "undefined") {
          currentCardIndex.value += 1;
        }

        reviewCard.prevCard = reviewCard.currentCard;
        reviewCard.currentCard = reviewCard.nextCard;
        await getNextCard();
        Object.assign(currentCardCategory, reviewCard.currentCard.category);
        loading.value = false;
      } else {
        Notify({ type: "warning", message: "已经是最后一张了" });
      }
    };
    const dragRight = async () => {
      // 上张
      if (reviewCard.prevCard) {
        loading.value = true;
        /*
                   p  c  n
         (获取) p  c  n

        */
        if (typeof currentCardIndex.value !== "undefined") {
          currentCardIndex.value -= 1;
        }

        reviewCard.nextCard = reviewCard.currentCard;
        reviewCard.currentCard = reviewCard.prevCard;
        await getPrevCard();
        Object.assign(currentCardCategory, reviewCard.currentCard.category);
        loading.value = false;
      } else {
        Notify({ type: "warning", message: "已经是第一张了" });
      }
    };
    const dragTop = () => {
      // 完成复习

      // 发送请求 -> 移除当前卡片
      const cid = reviewCard.currentCard.id;

      const postConfig = {
        method: "post" as Method,
        url: `${store.state.serverHost}/review/${cid}`,
      };

      postCreateData<null, null>(postConfig, false).then(() => {
        // 调用移除
        dragBottom();
      });
    };
    const dragBottom = async () => {
      // 移除
      if (typeof currentCardIndex.value !== "undefined") {
        needReview.value.splice(currentCardIndex.value, 1);
      }

      // 判断那边有值

      if (reviewCard.nextCard) {
        loading.value = true;
        /*
        1 2 3 4 5
        1 3 4 5

        不需要修改index
        */
        reviewCard.currentCard = reviewCard.nextCard;
        await getPrevAndNextCard();
        Object.assign(currentCardCategory, reviewCard.currentCard.category);
        loading.value = false;
      } else if (reviewCard.prevCard) {
        loading.value = true;
        /*
        1 2 3 4
        1 2 3
        */
        if (typeof currentCardIndex.value !== "undefined") {
          currentCardIndex.value -= 1;
        }

        reviewCard.currentCard = reviewCard.prevCard;
        await getPrevAndNextCard();
        Object.assign(currentCardCategory, reviewCard.currentCard.category);
        loading.value = false;
      } else {
        // 复习完毕
        reviewDone();
      }
    };
    const reviewDone = () => {
      Dialog.alert({
        message: "已复习完毕",
      }).then(() => {
        // on close
        handlerClickBack();
      });
    };

    let direction = "";
    const onCardDragMove = (obj: ICardDragObject) => {
      // 1. 判断方向
      if (Math.abs(obj.left) > Math.abs(obj.top)) {
        // 左右滑动
        direction = obj.left < 0 ? "left" : "right";
        // 拖动提示
        if (direction == "left") {
          Notify({ type: "primary", message: "下一张卡片" });

          // 拖动卡片时, 底部的卡片

          if (reviewCard.nextCard) {
            bottomShowReviewCard.value = reviewCard.nextCard as ICard;
          } else {
            bottomShowReviewCard.value = reviewCard.currentCard as ICard;
          }
        } else {
          Notify({ type: "primary", message: "上一张卡片" });
          // 拖动卡片时, 底部的卡片
          if (reviewCard.prevCard) {
            bottomShowReviewCard.value = reviewCard.prevCard as ICard;
          } else {
            bottomShowReviewCard.value = reviewCard.currentCard as ICard;
          }
        }
      } else {
        // 上下滑动
        direction = obj.top < 0 ? "top" : "bottom";
        if (direction == "top") {
          Notify({ type: "success", message: "完成复习" });
        } else {
          Notify({ type: "danger", message: "忽略本卡片" });
        }
      }
    };

    const onCardThrowDone = () => {
      // 清空 bottomShowReviewCard.value
      bottomShowReviewCard.value = null;
      // 关闭提示
      Notify.clear();

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
      // 清空 bottomShowReviewCard.value
      bottomShowReviewCard.value = null;
      // 关闭提示
      Notify.clear();
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
    let currentCardIndex = ref<number>();
    let needReview = ref<number[]>([]); // 需要复习的卡片ID
    const bottomShowReviewCard = ref<ICard | null>(); // 用于滑动时 在当前卡片底部显示
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
              currentCardIndex.value = index;
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
      if (status.hasMore) {
        getNeedReviewCardID();
      } else if (
        typeof currentCardIndex.value !== "undefined" &&
        0 <= currentCardIndex.value &&
        currentCardIndex.value < needReview.value.length
      ) {
        // 已经全部获取完了
        getPrevAndNextCard(); // 上下两张卡
        resetSDStyle(cardWidth.value, cardHeight.value);
      }
    });

    // ----------- 获取其余两张卡片
    const getPrevAndNextCard = async () => {
      getPrevCard();
      getNextCard();
    };
    const getPrevCard = async () => {
      if (typeof currentCardIndex.value === "undefined") return;
      // 获取上一张卡片
      if (currentCardIndex.value > 0) {
        // 有上一张
        const prevCardID = needReview.value[currentCardIndex.value - 1];

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
    };
    const getNextCard = async () => {
      if (typeof currentCardIndex.value === "undefined") return;
      // 获取下一张卡片
      if (currentCardIndex.value < needReview.value.length - 1) {
        // 有下一卡片
        const nextCardID = needReview.value[currentCardIndex.value + 1];
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
      const cid = Number(router.currentRoute.value.query.cid);
      console.log(router.currentRoute.value.query.cid);

      if (!isNaN(cid)) {
        getCardData(cid); // 获取本页面的卡片数据
        getNeedReviewCardID(); // 获取所有ID, 内部获取上下卡片
      } else {
        Dialog.alert({
          message: "需要卡牌的ID",
        }).then(() => {
          // on close
          handlerClickBack();
        });
      }
    });
    // -------------- 处理toolbar按钮
    const handlerClickBack = () => {
      router.go(-1);
    };
    const handlerClickEditor = () => {
      router.push({
        name: "editorCard",
        params: { cid: reviewCard.currentCard.id },
      });
    };

    const handlerClickStar = () => {
      const starStatus = reviewCard.currentCard.isStar;
      const cid = reviewCard.currentCard.id;

      const postConfig = {
        method: "post" as Method,
        url: `${store.state.serverHost}/cards/${cid}/star`,
        data: {
          isStar: starStatus,
        },
      };

      postCreateData<IStar, IStar>(postConfig, false).then((response) => {
        reviewCard.currentCard.isStar = response.isStar;
      });
    };

    // ----------- 显示/隐藏 详细信息
    const showDescBtn = ref(false);

    // ------------ 禁止移动端滑动返回, 防止影响拖拽卡片

    useEventListener(
      "touchmove",
      (e) => {
        e.preventDefault();
        e.stopPropagation();
      },
      { target: document.body }
    );
    return {
      cardWidth,
      cardHeight,
      titleEle,
      summaryEle,
      onCardDragMove,
      onCardThrowDone,
      onCardThrowFail,
      reviewCard,
      needReview,
      currentCardIndex,
      bottomShowReviewCard,
      currentCardCategory,
      loading,
      showDescBtn,
      handlerClickBack,
      handlerClickEditor,
      handlerClickStar,
    };
  },
});
</script>

<style lang="scss">
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
      padding: 0 16px;
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
    .card-summary-wrap {
      .card-summary {
        padding-bottom: 10px;
        word-wrap: break-word;
        overflow: scroll;
      }
    }
    .progress-wrap {
      position: absolute;
      bottom: 0;
      display: flex;
      width: 100%;
      justify-content: flex-end;
      .progress-now {
        font-size: 16px;
      }

      .progress-char {
        font-size: 30px;
      }

      .progress-all {
        font-size: 24px;
      }
    }
  }

  .card-tool-bar {
    position: fixed;
    bottom: 0;
    display: flex;
    height: 10%; // 卡片是80%
    min-height: 24px;
    width: 80%;
    justify-content: center;
    align-items: center;
    .card-tool-item {
      width: 33.33%;
      display: flex;
      justify-content: center;
      align-items: center;
    }
  }
}

.card-review-wrap {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  widows: 100vw;
}
.popup-desc-wrap {
  position: absolute;
  .card-review-desc-wrap {
    // 展示详细页面
    padding: 10px;
    overflow: scroll;
    height: calc(100% - 20px);
  }
  .card-review-desc-wrap > * {
    // 修改子标签默认样式
    padding: 0;
    margin: 0;
  }
}
</style>
