import dayjs from "dayjs";
dayjs.locale("zh-cn");
import relativeTime from "dayjs/plugin/relativeTime";
dayjs.extend(relativeTime);

import "dayjs/locale/zh-cn"; // 导入本地化语言

import { ICardPlan, ICard } from "@/types";
export function useCurrentCardPlan(card: ICard): ICardPlan {
  // 获得当前卡片的复习详情
  const planStepSec: number[] = [];
  card.category.plan.content.split("-").forEach((value) => {
    planStepSec.push(Number(value));
  });
  let nowReviewSecond = 0;
  const reviewAt = dayjs(card.reviewAt).format("YYYY/MM/D H:m:s");
  if (card.reviewTimes < planStepSec.length) {
    // 上次到本次的时间 second
    nowReviewSecond = planStepSec[card.reviewTimes];
  }

  const reviewAtNext = dayjs(card.reviewAt)
    .add(nowReviewSecond, "second")
    .format("YYYY/MM/D H:m:s");
  // 计算
  return {
    reviewAt, // 之前的复习时间
    reviewAtNext, // 本次复习时间
    reviewTimes: card.reviewTimes, // 目前复习次数
    allReviewTimes: planStepSec.length, // 全部复习次数
  };
}
