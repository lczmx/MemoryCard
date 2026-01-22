import { AxiosRequestConfig } from "axios";
import { IGetClientStatus } from "@/types";

declare function request<T, D>(
  config: AxiosRequestConfig<D>,
  loading: boolean
): Promise<T>;
declare function getDataOfPage<R>(
  clientStatus: IGetClientStatus,
  config: AxiosRequestConfig,
  loading: boolean
): Promise<R[]>;

declare function postCreateData<R, D>(
  // post 创建数据
  config: AxiosRequestConfig<D>,
  loading: boolean
): Promise<R>;
declare function getDataOfOne<R>(
  config: AxiosRequestConfig,
  loading: boolean
): Promise<R>;
