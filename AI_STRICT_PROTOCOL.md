# 🛡️ AI 开发与交付协议 (Strict Protocol v2.0)

## 0. 角色定义 (Role Definition)
- **【开发端】Mac mini (Local Dev)**: 负责代码实现、本地 `localhost` 测试、生成交付包。
- **【部署端】Mac Air (Remote Server)**: 负责在宿主机 `192.168.1.137` 上通过 Docker 隔离运行。

---

## 1. 核心任务流程 (The Workflow)

### 阶段 A：网络与端口预设
1.  **查表**：查阅云端 **[Global Port Registry](https://github.com/luke0708/--------/blob/main/Port-Registry/Global_Port_Registry.md)**，在 **50000+** 区挑选 `⚪️ Free` 且不含数字 "4" 的端口。
2.  **跨端配置**：前端代码必须支持 `BASE_URL` 配置。
    - 默认：`http://localhost:50XXX` (用于 Mac mini 本地验证)。
    - 远程：`http://192.168.1.137:50XXX` (用于前端连接 Mac Air 后端)。

### 阶段 B：构建双轨启动环境
必须在项目中提供两个启动脚本或命令说明：
1.  **`npm run dev:local`**: 连接本地后端 (localhost)。
2.  **`npm run dev:remote`**: 连接远端 Mac Air (192.168.1.137)。

### 阶段 C：构建交付包 (Build Pack)
**严禁包含 `node_modules`, `.git`, `venv`！**
1.  **生成身份清单**：在根目录创建 `deploy_manifest.txt`：
    ```text
    Project: [项目名]
    Port: [50XXX]
    Runtime: Python 3.11 / Node [Version]
    Remote_IP: 192.168.1.137
    ```
2.  **执行打包**：
    ```bash
    zip -r [项目名]-deliverable.zip . -x "**/node_modules/*" -x "**/.git/*" -x "**/venv/*" -x "**/.env"
    ```

---

## 2. 交付物标准 (Deliverables)

一个合格的交付包必须包含且仅包含：
- `backend/`: 完整的后端代码目录（含 Dockerfile）。
- `frontend/`: 前端源码（**不含 node_modules**）。
- `deploy_manifest.txt`: 部署清单。
- `docker-compose.yml`: (可选) 用于本地一键验证。

---

## 3. 部署端 AI 指令 (给我的提醒)
1. 收到包后，首要任务是检测 **清单 (Manifest)**。
2. 自动更新云端端口表并 Push。
3. 把项目代码解压至 Mac Air 的指定 `projects/` 目录。
