# ⚙️ 运维与部署手册 (Deployment Guide)

本文档定义了本系统的标准化部署流程和自动化协议。

---

## 🏗️ 核心底层协议

本系统依赖于 **《AI 严格部署协议》 (AI_STRICT_PROTOCOL.md)**，这是 AI 代理进行操作的唯一准则。

### 自动化部署工作流 (Package-to-Live)

1. **识别阶段**：部署代理读取 `backend.zip` 中的 `deploy_manifest.txt`。
2. **端口分配**：
   - 代理查阅 `./Port-Registry/Global_Port_Registry.md`。
   - 找到下一个 `Free` 端口。
   - 在 Docker Compose 中自动注入端口映射。
3. **环境同步**：读取 `.env` 配置文件并合并至 `server/.env`。
4. **启动执行**：执行 `docker compose up -d --build` 进行滚动更新。
5. **记录更新**：将分配结果写回注册表并 Push 至远端。

---

## 🛠️ 环境依赖

- **操作系统**: macOS (推荐) / Linux
- **核心工具**: Docker Desktop, Git, Python 3.10+
- **网络需求**: 需要能够访问 GitHub 及 AI API (如 DeepSeek)。

## 📁 目录权限规范

- `projects/`: 部署代理必须拥有读写权限。
- `Port-Registry/`: 该目录为一个独立的 Git 仓库存放（或已整合为主仓库子目录），代理需具备 Push 权限。

## 🔧 手动干预指令

如果自动化失效，运维人员可以通过以下指令尝试恢复：

```bash
# 强制重建所有核心系统件
cd server && docker compose up -d --force-recreate

# 清理未使用的镜像
docker image prune -f
```

---

## 🛡️ 安全审计

- 管理面板 `Infra-Dash` 默认映射 `docker.sock`，由于其具备控制容器的权限，请仅在局域网内访问。
- `projects/` 下的各个业务项目数据库默认映射至宿主机 `data/` 目录，需定期备份数据库文件。
