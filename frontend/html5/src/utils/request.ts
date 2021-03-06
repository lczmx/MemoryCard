import axios from "axios";
import { AxiosRequestConfig } from "axios";

import store from "@/store";
import router from "@/router";
import {
  IGetClientStatus,
  IGetReviewClientStatus,
  IResponse,
  IGetReviewByDateClientStatus,
} from "@/types";
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
  // 设置jwt
  if (!config.headers) config.headers = {};
  const token = store.state.token.accessToken;
  const jwt_auth = `${store.state.token.tokenType} ${token}`;
  if (token) {
    config.headers = { ...config.headers, ...{ Authorization: jwt_auth } };
  }

  // 请求数据
  return axios
    .request<T>(config)
    .then((res) => {
      // 请求成功返回
      Toast.clear(); // 取消 加载中
      if (!res.data) {
        throw new Error("请求错误");
      }
      // 提示msg的信息
      // res.data 是 axios 包装的 AxiosResponse<T> ，再 .data
      // 才是你自己定义的 ResponseData<T>；另外尽可能用 Promise.resolve 包裹起来，
      // 以防 polyfill 时出现兼容问题。
      return Promise.resolve(res.data);
    })
    .catch((e) => {
      // 请求错误
      // 取消 加载中
      // 异常捕捉后被你吞了，相当于返回了 Promise<void>；所以需要继续向上抛出。
      const status = e.toJSON().status;
      switch (status) {
        case 401:
          // 跳转到登录页面
          setTimeout(() => {
            router.push({ name: "LogIn" });
          }, 1500);
          Toast.fail({
            message: "请先登录",
            duration: 1000,
          });

          break;
        case 403:
          // 无权访问, 返回上一页
          setTimeout(() => {
            router.go(-1);
          }, 1500);
          Toast.fail({
            message: "拒绝访问",
            duration: 1000,
          });
          break;
        case 404:
          Toast.fail({
            message: "未找到资源",
            duration: 1000,
          });
          break;
        case 422:
          Toast.fail({
            message: "数据验证失败",
            duration: 1000,
          });
          break;
        default:
          console.log(status);
          Toast.fail({
            message: "未知错误",
            duration: 1000,
          });
      }
      console.log(status);

      return Promise.reject(e);
    });
}

/* get多条数据 */
/*
// 一般例子
const store = useStore();
let status = {
  method: "GET" as Method,
  limit: 10,
  offset: 0,
  hasMore: true,
};
const config = {
  url: `${store.state.serverHost}/category/`,
};

const getCategoryData = () => {
  getDataOfPage<ICategory>(status, config).then((response) => {
    data.value = response;
  });
};

*/

export async function getDataOfPage<R>(
  // 处理有分页的数据
  clientStatus: IGetClientStatus,
  config: AxiosRequestConfig,
  loading = true
): Promise<R[]> {
  const fake_res = [] as R[];
  // 判断有无下一页
  // 只有在显示loading的情况下提示
  if (
    !clientStatus.hasMore &&
    typeof clientStatus.hasMore !== "undefined" &&
    loading
  ) {
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
      order: clientStatus.order,
    },
  };

  return request<IResponse<R[]>, undefined>(RequestConfig, loading).then(
    (response) => {
      if (!response.data) {
        // undefined
        return Promise.resolve(fake_res);
      }

      if (response.status === 1) {
        // status为1时, 为正常情况
        if (response.data.length <= 0) {
          // 没数据了
          clientStatus.hasMore = false;
          if (loading) {
            Toast({
              message: "已经到底了",
              position: "bottom",
            });
          }
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
        return Promise.reject(response.msg);
      }
    }
  );
}

export async function getReviewDataOfPage<R>(
  // 处理有分页的数据
  clientStatus: IGetReviewClientStatus,
  config: AxiosRequestConfig,
  loading = true
): Promise<R[]> {
  const fake_res = [] as R[];
  // 判断有无下一页
  // 只有在显示loading的情况下提示
  if (
    !clientStatus.hasMore &&
    typeof clientStatus.hasMore !== "undefined" &&
    loading
  ) {
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
      category: clientStatus.category,
    },
  };

  return request<IResponse<R[]>, undefined>(RequestConfig, loading).then(
    (response) => {
      if (!response.data) {
        // undefined
        return Promise.resolve(fake_res);
      }

      if (response.status === 1) {
        // status为1时, 为正常情况
        if (response.data.length <= 0) {
          // 没数据了
          clientStatus.hasMore = false;
          if (loading) {
            Toast({
              message: "已经到底了",
              position: "bottom",
            });
          }
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
        return Promise.reject(response.msg);
      }
    }
  );
}
/* post数据 */
/* 
// 一般例子
const data = {
  name: name.value,
  icon: icon.value,
  color: color.value,
  plan: plan.value as number,
};
const postConfig = {
  method: "post" as Method,
  url: `${store.state.serverHost}/category/`,
  data,
};

postCreateData<ICategory, IPostCategory>(postConfig, false).then(
  (response) => {
    // 成功创建了
    Toast.success("已创建");
    setTimeout(() => {
      Toast.clear();
      router.push({ name: "category" });
    }, 1000);
  }
);


*/
export async function postCreateData<R, D>(
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
      return Promise.reject(response);
    }
  });
}

/* get单条数据 */
export async function getDataOfOne<R>(
  config: AxiosRequestConfig,
  loading = true
): Promise<R> {
  const fake_res = {} as R;

  return request<IResponse<R>, undefined>(config, loading).then((response) => {
    if (!response.data) {
      // undefined
      return Promise.resolve(fake_res);
    }

    if (response.status === 1) {
      // status为1时, 为正常情况
      return Promise.resolve(response.data);
    } else {
      Toast.fail(response.msg);
      return Promise.reject(response.msg);
    }
  });
}

/* 删除数据 */
/* 
可以有请求提
但没有响应体
*/
export async function deleteData<D>(
  config: AxiosRequestConfig<D>,
  loading = false
): Promise<string> {
  return request<IResponse<null>, D>(config, loading).then((response) => {
    if (response.status === 1) {
      // status为1时, 为正常情况
      return Promise.resolve(response.msg);
    } else {
      Toast.fail(response.msg);
      return Promise.reject(response.msg);
    }
  });
}

export async function getReviewCardByDateData<R>(
  // 处理有分页的数据
  clientStatus: IGetReviewByDateClientStatus,
  config: AxiosRequestConfig,
  loading = true
): Promise<R[]> {
  const fake_res = [] as R[];
  // 判断有无下一页
  // 只有在显示loading的情况下提示
  if (
    !clientStatus.hasMore &&
    typeof clientStatus.hasMore !== "undefined" &&
    loading
  ) {
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
      date: clientStatus.date,
    },
  };

  return request<IResponse<R[]>, undefined>(RequestConfig, loading).then(
    (response) => {
      if (!response.data) {
        // undefined
        return Promise.resolve(fake_res);
      }

      if (response.status === 1) {
        // status为1时, 为正常情况
        if (response.data.length <= 0) {
          // 没数据了
          clientStatus.hasMore = false;
          if (loading) {
            Toast({
              message: "已经到底了",
              position: "bottom",
            });
          }
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
        return Promise.reject(response.msg);
      }
    }
  );
}
