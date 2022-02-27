from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic.error_wrappers import ErrorWrapper
from router import review_router, cards_router, category_router, \
    analyse_router, plans_router, user_router
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exception_handlers import request_validation_exception_handler
import srcipts  # 执行自定义脚本

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


app.include_router(review_router)
app.include_router(cards_router)
app.include_router(category_router)
app.include_router(analyse_router)
app.include_router(plans_router)
app.include_router(user_router)
