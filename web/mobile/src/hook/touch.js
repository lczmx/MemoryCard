import { onMounted, reactive, toRefs } from "vue";

function getDistance(x1, y1, x2, y2) {
  var _x = Math.abs(x1 - x2);
  var _y = Math.abs(y1 - y2);
  return Math.sqrt(_x * _x + _y * _y);
}

function useTouch(
  props,
  {
    onDragStart,
    onDragMove,
    onDragStop,
    onThrowStart,
    onThrowDone,
    onThrowFail,
  }
) {
  const cardOneState = reactive({
    left: 0,
    top: 0,
    startLeft: 0,
    startTop: 0,
    isDrag: false,
    isThrow: false,
    needBack: false,
    isAnimating: false,
  });
  function touchStart(e) {
    if (cardOneState.isAnimating) return;

    cardOneState.isDrag = true;
    cardOneState.needBack = false;
    cardOneState.isThrow = false;
    var curTouch = e.touches[0];
    cardOneState.startLeft = curTouch.clientX - cardOneState.left;
    cardOneState.startTop = curTouch.clientY - cardOneState.top;

    onDragStart();
  }
  function touchMove(e) {
    if (cardOneState.isAnimating) return;

    var curTouch = e.touches[0];
    if (props.dragDirection == "all" || props.dragDirection == "horizontal")
      cardOneState.left = curTouch.clientX - cardOneState.startLeft;
    if (props.dragDirection == "all" || props.dragDirection == "vertical")
      cardOneState.top = curTouch.clientY - cardOneState.startTop;
    const distance = getDistance(0, 0, cardOneState.left, cardOneState.top);

    onDragMove({
      left: cardOneState.left,
      top: cardOneState.top,
      distance: distance,
    });
  }
  function touchCancel(e) {
    let distance = getDistance(0, 0, cardOneState.left, cardOneState.top);

    cardOneState.isDrag = false;
    onDragStop({
      left: cardOneState.left,
      top: cardOneState.top,
      distance: distance,
    });
    if (cardOneState.isAnimating) return;

    distance = getDistance(0, 0, cardOneState.left, cardOneState.top);
    if (distance > props.throwTriggerDistance) {
      makeCardThrow();
    } else {
      makeCardBack();
    }
  }

  const otherCardsState = reactive({
    left2: 0,
    top2: 0,
    width2: 0,
    height2: 0,

    left3: 0,
    top3: 0,
    width3: 0,
    height3: 0,

    left4: 0,
    top4: 0,
    width4: 0,
    height4: 0,
    opacity4: 0,
  });
  function resetAllCardDown() {
    cardOneState.left = 0;
    cardOneState.top = 0;

    otherCardsState.width2 = props.cardWidth - props.leftPad * 2;
    otherCardsState.height2 = props.cardHeight - props.topPad * 2;
    otherCardsState.left2 = props.leftPad;
    otherCardsState.top2 = props.topPad * 3;

    otherCardsState.width3 = props.cardWidth - props.leftPad * 4;
    otherCardsState.height3 = props.cardHeight - props.topPad * 4;
    otherCardsState.left3 = props.leftPad * 2;
    otherCardsState.top3 = props.topPad * 6;

    otherCardsState.width4 = props.cardWidth - props.leftPad * 6;
    otherCardsState.height4 = props.cardHeight - props.topPad * 6;
    otherCardsState.left4 = props.leftPad * 3;
    otherCardsState.top4 = props.topPad * 9;
    otherCardsState.opacity4 = 0;
  }
  function resetAllCard() {
    resetAllCardDown();
  }
  function makeCardThrow() {
    cardOneState.isThrow = true;
    cardOneState.needBack = false;

    var angle = Math.atan2(cardOneState.top - 0, cardOneState.left - 0);
    cardOneState.left = Math.cos(angle) * props.throwDistance;
    cardOneState.top = Math.sin(angle) * props.throwDistance;

    otherCardsState.width2 = props.cardWidth;
    otherCardsState.height2 = props.cardHeight;
    otherCardsState.left2 = 0;
    otherCardsState.top2 = 0;

    otherCardsState.width3 = props.cardWidth - props.leftPad * 2;
    otherCardsState.height3 = props.cardHeight - props.topPad * 2;
    otherCardsState.left3 = props.leftPad;
    otherCardsState.top3 = props.topPad * 3;

    otherCardsState.width4 = props.cardWidth - props.leftPad * 4;
    otherCardsState.height4 = props.cardHeight - props.topPad * 4;
    otherCardsState.left4 = props.leftPad * 2;
    otherCardsState.top4 = props.topPad * 6;
    otherCardsState.opacity4 = 1;

    cardOneState.isAnimating = true;

    onThrowStart();
    setTimeout(function () {
      cardOneState.isThrow = false;
      cardOneState.isAnimating = false;
      onThrowDone();
      resetAllCard();
    }, 400);
  }
  function makeCardBack() {
    cardOneState.isThrow = false;
    cardOneState.needBack = true;

    if (cardOneState.needBack) {
      cardOneState.left = 0;
      cardOneState.top = 0;
    }

    cardOneState.isAnimating = true;
    setTimeout(function () {
      onThrowFail();
      cardOneState.isAnimating = false;
      cardOneState.needBack = true;
    }, 600);
  }
  onMounted(() => {
    resetAllCard();
  });

  return {
    ...toRefs(cardOneState),
    ...toRefs(otherCardsState),
    touchStart,
    touchMove,
    touchCancel,
  };
}

export default useTouch;
