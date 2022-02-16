import { AxiosRequestConfig } from "axios";
declare function request<T, D>(config: AxiosRequestConfig<D>): Promise<T>;
