from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

# ######### jwt
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"  # jwt加密算法
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # 访问令牌过期分钟

oauth2_schema = OAuth2PasswordBearer(tokenUrl="/user/token")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
