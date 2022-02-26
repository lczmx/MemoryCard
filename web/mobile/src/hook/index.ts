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

// 转换时间, 并返回对应格式
export function convert_sec_to_string(sec: number): string {
  let duration = "";
  const days = Math.floor(sec / 86400);
  const hours = Math.floor((sec % 86400) / 3600);
  const minutes = Math.floor(((sec % 86400) % 3600) / 60);
  const seconds = Math.floor(((sec % 86400) % 3600) % 60);

  if (days > 0) duration += `${days}天`;
  if (hours > 0) duration += `${hours}小时`;
  if (minutes > 0) duration += `${minutes}分`;
  if (seconds > 0) duration += `${seconds}秒`;

  return duration;
}
// 将时间装换成秒数
export function use_fmt_to_sec(
  days: number,
  hours: number,
  minutes: number,
  seconds: number
): number {
  let sec = 0;
  if (days > 0) sec += days * 86400;
  if (hours > 0) sec += hours * 3600;
  if (minutes > 0) sec += minutes * 60;
  if (seconds > 0) sec += seconds;
  return sec;
}

// 将秒数转化为对应的时间单位
export function convert_sec_to_other(sec: number) {
  const days = Math.floor(sec / 86400);
  const hours = Math.floor((sec % 86400) / 3600);
  const minutes = Math.floor(((sec % 86400) % 3600) / 60);
  const seconds = Math.floor(((sec % 86400) % 3600) % 60);

  return { days, hours, minutes, seconds };
}
