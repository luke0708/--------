# 📦 后端代码打包指令

> **给 Mac mini AI 的指令**：请阅读此文档，帮我把后端代码打包成符合规范的 `backend.zip`

---

## 任务目标

把当前项目的**后端部分**打包成一个可直接部署到 Docker 的压缩包。

---

## 你需要做的事

### 1. 确认后端目录

找到项目中的后端代码目录（通常是 `backend/`、`server/`、`api/` 或项目根目录）

### 2. 确保包含以下文件

| 文件 | 必须 | 说明 |
|-----|------|------|
| `main.py` 或入口文件 | ✅ | 应用入口 |
| `requirements.txt` | ✅ | Python 依赖清单 |
| `Dockerfile` | ✅ | 如果没有，请按下方模板创建 |
| `.dockerignore` | ✅ | 如果没有，请按下方模板创建 |

### 3. 创建 Dockerfile（如果不存在）

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 安装 Python 依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制代码
COPY . .

# 暴露端口
EXPOSE 8000

# 启动命令（根据框架调整）
# FastAPI:
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
# 或 Flask:
# CMD ["gunicorn", "app:app", "-b", "0.0.0.0:8000"]
```

### 4. 创建 .dockerignore（如果不存在）

```text
.git
__pycache__
*.pyc
venv
.venv
.env
.DS_Store
*.log
```

### 5. 检查环境变量配置

确保代码中的敏感配置使用环境变量：

```python
import os

# ✅ 正确
DB_HOST = os.getenv("DB_HOST", "localhost")
API_KEY = os.getenv("API_KEY")

# ❌ 错误（不要硬编码）
# DB_PASSWORD = "123456"
```

### 6. 打包

```bash
cd [后端目录的父目录]
zip -r backend.zip [后端文件夹名] -x "*.git*" -x "*venv*" -x "*__pycache__*" -x "*.env"
```

**示例**：
```bash
# 如果结构是 ~/Projects/MyApp/backend/
cd ~/Projects/MyApp
zip -r backend.zip backend -x "*.git*" -x "*venv*" -x "*__pycache__*" -x "*.env"
```

---

## 打包完成后

1. 把 `backend.zip` 上传到 **Google Drive**
2. 通知我：**"后端已打包上传"**

---

## 前端配置（打包后需要做）

后端部署完成后，需要修改前端的 API 地址为：

```
http://192.168.1.137:8002
```

通常在以下位置修改：
- `.env` 或 `.env.local` 文件中的 `API_URL` 或 `VITE_API_URL`
- `src/config.js` 或 `src/api/index.js`
