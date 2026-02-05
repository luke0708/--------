# 👨‍💻 开发者交接与交底文档 (Dev Handover)

此文档旨在帮助后续开发者（或 AI 开发者）理解项目架构，以便进行功能扩展。

---

## 🧩 核心组件解析

### 1. Infra-Dash (Python/FastAPI)
- **位置**: `server/infra-dash/`
- **逻辑**: 通过 API 实时读取 `/var/run/docker.sock`，实现对宿主机容器状态的获取。
- **扩展建议**: 若要在面板添加控制按钮（如重启、停止），需在 `main.py` 中增加对应的 Docker SDK 调用。

### 2. 部署代理逻辑 (Agent Knowledge)
- **指令文件**: `agent.md`
- **核心逻辑**: 本系统不使用复杂的 Webhook，而是通过 AI 识别文件结构来驱动部署。
- **改动禁忌**: 严禁在未经用户允许的情况下修改 `Port-Registry` 的文件名，这会导致 AI 寻找注册表失败。

---

## 🛠️ 如何开发一个新项目并接入

必须遵循 **`docs/mac-mini-开发规范.md`**：
1. **容器化**: 项目必须包含 `Dockerfile`。
2. **清单化**: 根目录必须提供 `deploy_manifest.txt`，包含：
   - `service_name`: 服务名
   - `internal_port`: 容器内部端口
   - `dependencies`: 环境变量需求（如 API KEY）
3. **隔离性**: 静态资源与逻辑代码分离，node_modules 等严禁入包。

---

## 🧪 测试流程

1. 修改代码后，在本地 `npm run dev` 或 `python main.py` 测试逻辑。
2. 打包生成 `backend.zip`。
3. 在测试目录模拟解压，并校验 `docker-compose.yml` 文件的生成逻辑是否正确。

## 📝 编码风格

- **后端**: Python 遵循 PEP8，使用 SQLModel/FastAPI。
- **前端**: React/Vue 必须使用 Vanilla CSS 进行组件化封装。
- **文档**: 所有新增功能必须同步更新 `ROADMAP.md`。
