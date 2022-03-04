from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from api import bind_router
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exception_handlers import request_validation_exception_handler
from service import orm_database, create_all
from scripts import start_init

app = FastAPI()

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

app.state.database = orm_database


@app.on_event("startup")
async def startup() -> None:
    database_ = app.state.database
    if not database_.is_connected:
        await database_.connect()
        # 连接数据库后才初始化
    # await start_init()  # 执行离线脚本
    # await create_all()  # 创建表关系


@app.on_event("shutdown")
async def shutdown() -> None:
    database_ = app.state.database
    if database_.is_connected:
        await database_.disconnect()
