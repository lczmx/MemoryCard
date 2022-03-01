import { Method } from "axios";

export interface IResponse<T> {
  status: number;
  msg: string;
  data?: T;
}
// -------------------- 分类相关
export interface IPostCategory {
  // 新增分类接口
  name: string;
  icon: string;
  color: string;
  plan: number;
}

export interface ICategory {
  // 返回的分类
  id: number;
  name: string;
  icon: string;
  color: string;
  cardCount?: number;
  isStar?: boolean;
  plan: IPlan;
}

export interface IStar {
  isStar: boolean;
}

// ---------------- 记录请求
export interface IGetClientStatus {
  method: Method;
  limit?: number;
  offset?: number;
  order?: string;
  hasMore?: boolean;
}

// ---------------- 记录复习请求
export interface IGetReviewClientStatus {
  method: Method;
  limit?: number;
  offset?: number;
  category?: number;
  hasMore?: boolean;
}
// ---------------- 复习曲线相关
export interface IPlan {
  id: number;
  title: string;
  content: string;
  editable: Boolean;
}
export interface IPostPlan {
  title: string;
  content: string;
}

// 卡片复习计划数据
export interface ICardPlan {
  reviewAt: string; // 上一次的复习时间
  reviewAtNext: string; // 本次的复习时间
  reviewTimes: number; // 已经复习的次数
  allReviewTimes: number; // 全部复习的次数
}
// ---------------- 卡片相关

export interface ICard {
  id: number;
  isStar: boolean;
  title: string;
  reviewAt: Date;
  reviewTimes: number;
  category: ICategory;
  summary?: string;
  description?: string;
}
export interface IPostCard {
  title: string;
  category: number;
  summary: string;
  description: string;
}

export interface ICardDragObject {
  // 拖动卡片时的事件的回调数据
  distance: number;
  left: number;
  top: number;
}

export interface IReviewCard {
  // 用于存放复习卡片
  prevCard: ICard | null; // 上一个卡片
  currentCard: ICard; // 当前卡片
  nextCard: ICard | null; // 下一个卡片
}

export interface IGetReviewByDateClientStatus {
  // 根据日期查询
  method: Method;
  limit?: number;
  offset?: number;
  order?: string;
  hasMore?: boolean;
  date: string;
}

export interface IBatchPostCardData {
  // 批量处理卡片
  cards: number[];
}
export interface IBatchPostCategoryData {
  // 批量处理类别
  category: number[];
}

export interface IResetCardReview {
  // 重置复习
  id: number;
  reviewAt: Date;
  reviewTimes: number;
}

// --- 复习曲线展示

export interface IPlanStep {
  title: string; // 第几次复习
  time: string; // 相对于现在的复习的时间
}

// ---------- 登录/注册
export interface IUserSignUpPostData {
  username: string;
  email: string;
  password1: string;
  password2: string;
}
export interface IUserSignUpPostMsg {
  // 错误信息返回
  username?: string;
  email?: string;
  password1?: string;
  password2?: string;
}

export interface IUserLoginPostData {
  // 登录的数据
  username: string;
  password: string;
}

export interface IUerToken {
  accessToken: string;
  tokenType: string;
}

// 当前用户的信息
export interface IUserData {
  email: string;
  username: string;
  phoneNumber?: number;
}

export interface IAnalyseData {
  // 分析的chart数据

  count: number;
  date: string;
}

export interface IAnalysePostData {
  startDate: string;
  endDate: string;
}

export interface IAnalyseSummaryData {
  // 数据统计概览数据
  review: IAnalyseSummaryItem;
  create: IAnalyseSummaryItem;
  categoryCount: number;
}

export interface IAnalyseSummaryItem {
  today: number;
  incr: number;
}
