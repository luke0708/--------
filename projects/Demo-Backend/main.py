"""
Demo-Backend - 示例后端服务
演示如何符合 Infrastructure 架构规范
"""

import os
from datetime import datetime
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Demo Backend",
    description="Infrastructure 架构示例项目",
    version="1.0.0"
)

# CORS 配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """根路径 - 服务信息"""
    return {
        "service": "Demo-Backend",
        "status": "running",
        "timestamp": datetime.now().isoformat()
    }


@app.get("/health")
async def health_check():
    """健康检查端点 - 供 Docker 健康检查使用"""
    return {"status": "healthy"}


@app.get("/config")
async def show_config():
    """显示环境变量配置（仅用于演示，生产环境请移除）"""
    return {
        "DB_HOST": os.getenv("DB_HOST", "未配置"),
        "DEBUG": os.getenv("DEBUG", "false"),
        "LOG_LEVEL": os.getenv("LOG_LEVEL", "INFO"),
        # 敏感信息只显示是否配置，不显示实际值
        "SECRET_KEY": "已配置" if os.getenv("SECRET_KEY") else "未配置",
        "DB_PASSWORD": "已配置" if os.getenv("DB_PASSWORD") else "未配置"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
