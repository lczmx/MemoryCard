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
  isStar?: boolean;
  plan: IPlan;
}

// ---------------- 记录请求
export interface IGetClientStatus {
  method: Method;
  limit?: number;
  offset?: number;
  hasMore?: boolean;
}
// ---------------- 复习曲线相关
export interface IPlan {
  id: number;
  title: string;
  content: string;
}
// ---------------- 卡片相关
export interface ICard {
  id: number;
  title: string;
  reviewDate: string;
  category: ICategory;
}
