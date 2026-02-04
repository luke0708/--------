# Infrastructure 总控工程指南

## 1. 目录结构规划
请确保你的文件目录结构严格如下所示（利用相对路径管理兄弟项目）：

```text
~/Projects/ (你的根目录)
├── Infrastructure/          <-- 【本项目】总控中心
│   ├── docker-compose.yml   <-- 核心编排文件
│   ├── .env                 <-- 全局环境变量（密码/Key）
│   └── update.sh            <-- 自动化更新脚本（见文档3）
│
├── User-Backend/            <-- [项目1] 用户系统
├── Order-Backend/           <-- [项目2] 订单系统
├── Payment-Backend/         <-- [项目3] 支付系统
└── ...

```

## 2. 核心文件：docker-compose.yml

在 `Infrastructure` 目录下创建此文件。

```yaml
version: '3.8'

services:
  # --- 服务 1: 用户系统 ---
  user-service:
    # 指向与 Infrastructure 同级的 User-Backend 文件夹
    build: ../User-Backend
    container_name: user_service
    restart: always
    ports:
      - "8001:8000"  # 外部访问 http://localhost:8001
    env_file:
      - .env         # 读取同级目录下的 .env 文件

  # --- 服务 2: 订单系统 ---
  order-service:
    build: ../Order-Backend
    container_name: order_service
    restart: always
    ports:
      - "8002:8000"  # 外部访问 http://localhost:8002
    env_file:
      - .env
    depends_on:
      - user-service # 确保用户服务先启动

  # --- 服务 3: 支付系统 ---
  payment-service:
    build: ../Payment-Backend
    container_name: payment_service
    restart: always
    ports:
      - "8003:8000"
    env_file:
      - .env

  # ...在此处继续添加其他服务...

```

## 3. 全局配置：.env

在 `Infrastructure` 目录下创建此文件，存放所有项目共用的密码。

```properties
# 数据库配置
DB_HOST=host.docker.internal
DB_USER=root
DB_PASSWORD=your_secure_password

# API 密钥
OPENAI_API_KEY=sk-xxxxxxxxxxxx
SECRET_KEY=complex_random_string

```
