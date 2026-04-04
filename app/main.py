import sys
import os

# 添加当前文件所在目录到 sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI
from fastapi.exception_handlers import request_validation_exception_handler
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from tortoise.contrib.fastapi import register_tortoise
from scripts import start_init
from contextlib import asynccontextmanager

from api import bind_router
from logger import CustomizeLogger
from settings import TORTOISE_ORM

# 许可信息数据
license_info = {
    "name": "GPLv3.0",
    "url": "https://www.gnu.org/licenses/gpl-3.0.html",
}
# 联系信息 数据
contact = {
    # 联系的名字
    "name": "lczmx",
    # 联系url
    "url": "https://github.com/lczmx/MemoryCard",
    # 联系的邮箱
    "email": "lczmx@foxmail.com",
}

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    生命周期
    :param app:
    :return:
    """
    # 应用程序启动之前执行
    await start_init()
    yield
    # 应用程序启动之后执行

def create_app() -> FastAPI:
    fast_api_app = FastAPI(title="记忆卡片", description="记忆卡片后端服务", version="0.2.1",
                           license_info=license_info, contact=contact, lifespan=lifespan)
    fast_api_app.logger = CustomizeLogger.make_logger()
    return fast_api_app


app = create_app()

app.add_middleware(
    CORSMiddleware,
    # 允许跨域请求的源列表
    allow_origins=["*"],
    # 指示跨域请求支持 cookies。默认是 False
    # 为True时, allow_origins 不能设定为 ['*']，必须指定源。
    allow_credentials=True,
    # 允许跨域请求的 HTTP 方法列表
    allow_methods=["*"],
    # 允许跨域请求的 HTTP 请求头列表
    allow_headers=["*"],
)


#  格式化异常处理
@app.exception_handler(RequestValidationError)
async def http_exception_handler(request, exc: RequestValidationError):
    content = {
        "status": 0,
        "msg": "验证失败",
        "data": {}
    }
    try:
        for error in exc.args[0][0].exc.args[0]:
            key = error._loc
            value = error.exc.args[0]
            content['data'][key] = value

        return JSONResponse(content, status_code=200)
    except Exception:
        return await request_validation_exception_handler(request, exc)

# 绑定路由
bind_router(app)

# 初始化数据库
register_tortoise(
    app, config=TORTOISE_ORM,
    generate_schemas=True,  # 自动生成表结构
    add_exception_handlers=True  # 启用ORM异常处理
)


if __name__ == '__main__':
    import uvicorn
    uvicorn.run("main:app", port=8366, host="0.0.0.0", reload=True)
