# 💻 Mac mini 开发规范

> **适用于**: Mac mini M4 开发机
> **角色**: 代码编写、构建镜像、推送 GitHub

---

## 新项目创建流程

### 1. 准备项目结构

```text
~/Projects/
├── My-New-Backend/
│   ├── main.py           # 业务代码
│   ├── requirements.txt  # 依赖
│   ├── Dockerfile        # 必须
│   └── .dockerignore     # 必须
```

### 2. 代码规范

#### ✅ 必须遵守

- **环境变量**: 敏感信息通过 `os.getenv()` 读取
- **端口**: 容器内统一 `8000`
- **日志**: 输出到 stdout/stderr，不写本地文件
- **无状态**: 不依赖本地文件存储

#### ❌ 严禁

- 硬编码密码、API Key
- 在代码中指定宿主机端口

---

## Dockerfile 模板

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# 先安装依赖（利用缓存）
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["gunicorn", "main:app", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "-b", "0.0.0.0:8000"]
```

---

## .dockerignore 模板

```text
.git
__pycache__
venv
.env
*.pyc
.DS_Store
```

---

## 注册到 Infrastructure

完成项目后，需要在 `Infrastructure/docker-compose.yml` 添加服务配置：

```yaml
  my-new-service:
    build: ../My-New-Backend
    container_name: my-new-service
    restart: always
    ports:
      - "8002:8000"  # 分配空闲端口
    env_file:
      - .env
```

---

## 推送部署

```bash
# 1. 提交代码
git add .
git commit -m "feat: new feature"
git push origin main

# 2. 通知服务器更新
# 在 Mac Air 上运行: ./update.sh
```
