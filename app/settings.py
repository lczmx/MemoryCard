import os
from pydantic_settings import BaseSettings
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

# 获取项目根目录
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE_PATH = os.path.join(BASE_DIR, "logs")
LOG_FILE_FORMATE = "MemoryCard_{time}.log"


class Settings(BaseSettings):
    """配置模型类"""
    # 数据库配置
    db_type: str = "pgsql"  # 支持的数据库类型: pgsql, mysql, sqlite
    
    # PostgreSQL配置
    db_host: str = "localhost"
    db_port: int = 5432
    db_name: str = "memorycard"
    db_user: str = "admin"
    db_password: str = "password"
    
    # SQLite配置
    db_file: str = "memorycard.db"
    
    # JWT配置
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 360
    
    # 日志配置
    log_level: str = "info"
    log_rotation: str = "1 MB"
    log_retention: str = "1 months"
    
    @property
    def async_sqlalchemy_database_url(self) -> str:
        """根据数据库类型动态构建数据库URL"""
        if self.db_type == "pgsql":
            return f"postgresql+asyncpg://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"
        elif self.db_type == "mysql":
            return f"mysql+aiomysql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"
        elif self.db_type == "sqlite":
            return f"sqlite+aiosqlite:///{os.path.join(BASE_DIR, self.db_file)}"
        else:
            raise ValueError(f"不支持的数据库类型: {self.db_type}")
    
    class Config:
        env_file = ".env"
        case_sensitive = False
        env_nested_delimiter = "_"


# 创建配置实例
settings = Settings()

# JWT相关配置
oauth2_schema = OAuth2PasswordBearer(tokenUrl="/user/token")
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

# 日志配置
LOGGING_CONFIG = {
    "logger": {
        "path": LOG_FILE_PATH,
        "filename": LOG_FILE_FORMATE,
        "level": settings.log_level,
        "rotation": settings.log_rotation,
        "retention": settings.log_retention,
        "format": "<level>{level: <8}</level> <green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> request id: {extra[request_id]} - <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>"
    }
}

# 一些初始数据
OPERATION_DATA = {
    "delete_card": 1,
    "create_card": 2,
    "review_card": 3,
    "delete_category": 4,
    "create_category": 5,
    "delete_plan": 6,
    "create_plan": 7,
}
