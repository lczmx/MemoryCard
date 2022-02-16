from fastapi import FastAPI
from router import review_router, cards_router, category_router, \
    analyse_router, plans_router
from fastapi.middleware.cors import CORSMiddleware
import srcipts  # 执行自定义脚本

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    # 允许跨域请求的源列表
    allow_origins=[
        "http://localhost",
        "http://localhost:8080"
    ],
    # 指示跨域请求支持 cookies。默认是 False
    # 为True时, allow_origins 不能设定为 ['*']，必须指定源。
    allow_credentials=True,
    # 允许跨域请求的 HTTP 方法列表
    allow_methods=["*"],
    # 允许跨域请求的 HTTP 请求头列表
    allow_headers=["*"],
)

app.include_router(review_router)
app.include_router(cards_router)
app.include_router(category_router)
app.include_router(analyse_router)
app.include_router(plans_router)
