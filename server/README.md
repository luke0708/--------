# 🏗️ Infrastructure 总控工程

统一管理所有微服务的 Docker 编排中心。

## 快速开始

### 1. 配置环境变量

```bash
cp .env.example .env
# 编辑 .env 填入实际的密码和 API Key
```

### 2. 设置脚本权限（仅首次）

```bash
chmod +x update.sh
```

### 3. 启动所有服务

```bash
./update.sh
```

## 常用命令

```bash
# 查看运行状态
docker compose ps

# 查看日志
docker compose logs -f [服务名]

# 停止所有服务
docker compose down

# 重启单个服务
docker compose restart [服务名]
```

## 添加新服务

1. 在 `docker-compose.yml` 中添加服务配置
2. 在 `update.sh` 的 `PROJECTS` 数组中添加项目名称
3. 运行 `./update.sh`

## 目录结构

```text
~/Projects/
├── Infrastructure/          ← 你在这里
│   ├── docker-compose.yml
│   ├── .env
│   └── update.sh
├── Demo-Backend/
├── Your-Backend/
└── ...
```

## 端口分配

| 服务 | 端口 |
|-----|------|
| demo-backend | 8001 |
| (预留) | 8002-8099 |
