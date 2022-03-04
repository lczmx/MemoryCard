<template>
  <div style="height: 300px">
    <div
      v-if="actionName != ''"
      style="
        color: #fff;
        background: rgba(0, 0, 0, 0.3);
        padding: 10px 20px;
        font-size: 24px;
        position: absolute;
        z-index: 999;
        left: 50%;
        top: 50%;
        transform: translate(-50%, -50%);
      "
    >
      {{ actionName }}
    </div>
    <fly-card
      @onDragMove="onCardDragMove"
      @onDragStop="onCardDragStop"
      @onThrowDone="onCardThrowDone"
      :cardWidth="200"
      :cardHeight="240"
      :throwTriggerDistance="100"
      dragDirection="horizontal"
      :hasShadow="true"
    >
      <template #firstCard style="width: 100%; height: 100%">
        <div v-if="cards[0]" class="tantanCard">
          <img
            :src="cards[0].img"
            style="width: 100%; height: 100%"
            mode="aspectFill"
          />
        </div>
      </template>
      <template #secondCard style="width: 100%; height: 100%">
        <div v-if="cards[1]" class="tantanCard">
          <img
            :src="cards[1].img"
            style="width: 100%; height: 100%"
            mode="aspectFill"
          />
        </div>
      </template>
      <template #thirdCard style="width: 100%; height: 100%">
        <div v-if="cards[2]" class="tantanCard">
          <img
            :src="cards[2].img"
            style="width: 100%; height: 100%"
            mode="aspectFill"
          />
        </div>
      </template>
    </fly-card>
  </div>
</template>

<script>
import FlyCard from "../components/FlyCard.vue";
import img1 from "../assets/1.jpg";
import img2 from "../assets/2.jpg";
import img3 from "../assets/3.jpg";
import img4 from "../assets/4.jpg";
import img5 from "../assets/5.jpg";
export default {
  components: {
    FlyCard,
  },
  data() {
    return {
      actionName: "",
      cards: [
        {
          img: img1,
        },
        {
          img: img2,
        },
        {
          img: img3,
        },
        {
          img: img4,
        },
        {
          img: img5,
        },
      ],
    };
  },
  methods: {
    onCardDragMove(obj) {
      if (obj.left < -10) {
        this.actionName = "不喜欢";
      } else if (obj.left > 10) {
        this.actionName = "喜欢";
      } else {
        this.actionName = "";
      }
    },
    onCardDragStop(obj) {
      this.actionName = "";
    },
    onCardThrowDone(obj) {
      this.cards.splice(0, 1);
    },
  },
};
</script>

<style>
div {
  box-sizing: border-box;
}
.tantanCard {
  width: 100%;
  height: 100%;
}
</style>
