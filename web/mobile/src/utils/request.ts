import axios from "axios";
import { AxiosRequestConfig } from "axios";
import { IGetClientStatus, IResponse } from "@/types";
import { Toast } from "vant";

export async function request<T, D>(
  config: AxiosRequestConfig<D>,
  loading = true
): Promise<T> {
  // 加载中
  if (loading) {
    Toast.loading({
      message: "加载中...",
      forbidClick: true,
      loadingType: "spinner",
      duration: 0, // 一直存在loading, 除非手动取消
    });
  }

  // 请求数据
  return axios
    .request<T>(config)
    .then((res) => {
      // 请求成功返回
      Toast.clear(); // 取消 加载中
      if (!res.data) {
        // TODO: 异常处理
        throw new Error("请求错误");
      }
      // 提示msg的信息
      // res.data 是 axios 包装的 AxiosResponse<T> ，再 .data
      // 才是你自己定义的 ResponseData<T>；另外尽可能用 Promise.resolve 包裹起来，
      // 以防 polyfill 时出现兼容问题。
      return Promise.resolve(res.data);
    })
    .catch((e) => {
      console.error(e);
      // 请求错误
      // 取消 加载中
      // 异常捕捉后被你吞了，相当于返回了 Promise<void>；所以需要继续向上抛出。
      // TODO: 异常处理
      return Promise.reject(e);
    });
}

export function getDataOfPage<R>(
  // 处理有分页的数据
  clientStatus: IGetClientStatus,
  config: AxiosRequestConfig,
  loading = true
): Promise<R[]> {
  const fake_res = [] as R[];
  // 判断有无下一页
  if (!clientStatus.hasMore && typeof clientStatus.hasMore !== "undefined") {
    Toast({
      message: "已经到底了",
      position: "bottom",
    });

    return Promise.resolve(fake_res);
  }
  const RequestConfig = {
    ...config,
    method: clientStatus.method,
    params: {
      limit: clientStatus.limit,
      offset: clientStatus.offset,
    },
  };

  return request<IResponse<R[]>, undefined>(RequestConfig, loading).then((response) => {
    if (!response.data) {
      // undefined
      return Promise.resolve(fake_res);
    }

    if (response.status === 1) {
      // status为1时, 为正常情况
      if (response.data.length <= 0) {
        // 没数据了
        clientStatus.hasMore = false;
        Toast({
          message: "已经到底了",
          position: "bottom",
        });
      }
      // 修改offset, 不能为undefined
      if (
        typeof clientStatus.offset !== "undefined" &&
        typeof clientStatus.limit !== "undefined"
      ) {
        clientStatus.offset += clientStatus.limit;
      }
      return Promise.resolve(response.data);
    } else {
      Toast.fail(response.msg);
      return Promise.resolve(fake_res);
    }
  });
}

export function postCreateData<R, D>(
  // post 创建数据
  config: AxiosRequestConfig<D>,
  loading = false
): Promise<R> {
  const fake_res = {} as R;
  return request<IResponse<R>, D>(config, loading).then((response) => {
    if (!response.data) {
      // undefined
      return Promise.resolve(fake_res);
    }

    if (response.status === 1) {
      // status为1时, 为正常情况
      return Promise.resolve(response.data);
    } else {
      Toast.fail(response.msg);
      return Promise.resolve(fake_res);
    }
  });
}
