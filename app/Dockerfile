# ==================== MemoryCard Dockerfile ====================
# 多阶段构建，优化镜像大小

# -------------------- 阶段1: Builder --------------------
FROM python:3.12-slim AS builder

# 设置环境变量
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# 安装构建依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# 设置工作目录
WORKDIR /app

# 复制依赖文件
COPY pyproject.toml uv.lock ./

# 安装 Python 依赖
RUN pip install --upgrade pip && \
    pip install uv && \
    uv sync --frozen --no-dev

# -------------------- 阶段2: Runtime --------------------
FROM python:3.12-slim AS runtime

# 标签
LABEL maintainer="lczmx <lczmx@foxmail.com>"
LABEL description="MemoryCard - 记忆卡片后端服务"

# 设置环境变量
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    APP_HOME=/app

# 安装运行时依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && useradd --create-home --shell /bin/bash appuser

# 设置工作目录
WORKDIR $APP_HOME

# 从 builder 阶段复制依赖
COPY --from=builder /root/.local/share/uv/python/cpython-3.12.5-linux-x86_64-gnu /root/.local/share/uv/python/cpython-3.12.5-linux-x86_64-gnu
COPY --from=builder /root/.local/share/uv/venvs /root/.local/share/uv/venvs
ENV PATH="/root/.local/share/uv/venvs/memory-card-0.2.1/bin:$PATH"

# 复制应用代码
COPY --chown=appuser:appuser . .

# 创建日志目录
RUN mkdir -p logs && chown appuser:appuser logs

# 切换到非 root 用户
USER appuser

# 暴露端口
EXPOSE 8366

# 健康检查
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8366/docs || exit 1

# 默认启动命令
ENTRYPOINT ["sh", "/app/docker/entrypoint.sh"]
CMD ["python", "main.py"]
