import os
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from loguru import logger

from exceptions import MissingRequireConfig

# #### 日志路径
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

LOG_FILE_PATH = os.path.join(BASE_DIR, "logs")
LOG_FILE_FORMATE = "MemoryCard_{time}.log"

# 日志配置
LOGGING_CONFIG = {
    "logger": {
        "path": LOG_FILE_PATH,
        "filename": LOG_FILE_FORMATE,
        "level": "info",
        "rotation": "1 MB",
        "retention": "1 months",
        "format": "<level>{level: <8}</level> <green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> request id: {extra[request_id]} - <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>"

    }
}

# ####### 数据库链接
ASYNC_SQLALCHEMY_DATABASE_URL = ''

# ######### jwt
SECRET_KEY = ""
ALGORITHM = "HS256"  # jwt加密算法
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 6  # 访问令牌过期分钟, 默认6小时
oauth2_schema = OAuth2PasswordBearer(tokenUrl="/user/token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ###### 检验配置
if os.path.isfile("local_settings.py"):
    from local_settings import *
else:
    f = open("local_settings.py", mode="w", encoding="utf-8")
    f.close()

if not SECRET_KEY:
    f = open("local_settings.py", mode="a", encoding="utf-8")
    # 动态 生成 SECRET_KEY
    import secrets

    SECRET_KEY = secrets.token_hex(32)
    f.write(f"\nSECRET_KEY = '{SECRET_KEY}'\n")
    f.close()
    logger.add(os.path.join(LOG_FILE_PATH, "init_settings.log"), rotation="1 MB",
               format=LOGGING_CONFIG["logger"]["format"])  # 滚动大日志文件
    logger.warning("初始化SECRET_KEY")

if not ASYNC_SQLALCHEMY_DATABASE_URL:
    raise MissingRequireConfig("ASYNC_SQLALCHEMY_DATABASE_URL")

# ######### 一些初始数据

OPERATION_DATA = {
    "delete_card": 1,
    "create_card": 2,
    "review_card": 3,
    "delete_category": 4,
    "create_category": 5,
    "delete_plan": 6,
    "create_plan": 7,
}
