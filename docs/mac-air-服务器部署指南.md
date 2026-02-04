# 🖥️ Mac Air 服务器部署指南

> **适用于**: Mac Air M4 (当前) / Ubuntu VPS (未来)
> **角色**: Docker 运行服务器

---

## 快速开始

### 1. 克隆代码

在服务器上克隆所有需要的仓库：

```bash
cd ~/Projects
git clone [your-infra-repo] Infrastructure
git clone [your-demo-repo] Demo-Backend
# ... 其他业务项目
```

### 2. 配置环境变量

```bash
cd Infrastructure
cp .env.example .env
nano .env  # 填入实际的密码和 API Key
```

### 3. 设置脚本权限

```bash
chmod +x update.sh
```

### 4. 启动服务

```bash
./update.sh
```

---

## 日常运维

### 更新所有服务

当 Mac mini 推送新代码后，在服务器运行：

```bash
cd ~/Projects/Infrastructure
./update.sh
```

### 常用 Docker 命令

```bash
# 查看运行状态
docker compose ps

# 查看实时日志
docker compose logs -f [服务名]

# 重启单个服务
docker compose restart [服务名]

# 停止所有服务
docker compose down

# 清理未使用的镜像（释放磁盘空间）
docker system prune -af
```

---

## 故障排查

### 服务启动失败

```bash
# 查看详细日志
docker compose logs [服务名] --tail 100

# 检查 .env 配置
cat .env
```

### 端口冲突

```bash
# 查看端口占用
lsof -i :8001
```

---

## 迁移到 Ubuntu VPS

1. 安装 Docker 和 Docker Compose
2. 克隆代码仓库
3. 配置 `.env` 文件
4. 运行 `./update.sh`

> 💡 `update.sh` 脚本在 Linux 下无需修改即可使用
