# 🚀 AntiGravity-Infrastructure 自动化部署总控系统

> **AI 驱动的个人服务器运维革命。从开发到上线，只需一个 ZIP 包。**

本项目是一个高度自动化的分布式部署控制系统，专为“Mac mini 开发 + MacBook Air 部署”的协作模式打造。它通过 AI 代理协议，实现了从代码打包、端口分配、容器编排到自动化部署的全闭环流程。

---

## 🌟 核心理念

- **大脑与身体分离**：Mac mini 负责“脑力开发”，Mac Air 负责“肉体运行”。
- **AI 严格协议**：部署过程不依赖人工指令，而是遵循 `AI_STRICT_PROTOCOL.md` 进行自动化交付。
- **一键生产力**：开发者只需生成包，系统自动处理所有的宿主机关联、环境配置和端口冲突。

## 🛠️ 项目结构

- 📂 `server/`：基础设施编排。包含：
  - **Infra-Dash**：可视化管理面板 (Port 39999)
  - **Dozzle**：实时容器日志监控 (Port 39998)
- 📂 `projects/`：业务项目存放区（如 News-Tracker, Demo-Backend）。
- 📂 `Port-Registry/`：全局端口登记处，维护唯一的端口分配真相。
- 📂 `docs/`：所有的操作手册与开发规范。
- 📄 `agent.md`：赋予 AI 代理操作本仓库的神性代码。

## 🚦 快速开始

### 1. 部署环境安装
```bash
./vps-one-click.sh
```

### 2. 启动总控制中心
```bash
cd server && docker compose up -d
```

### 3. 加入新项目
参考 `DEPLOYMENT.md` 了解如何使用 AI 自动识别并发布新的业务项目。

---

## 🔗 相关链接
- [用户使用手册](./USER_MANUAL.md)
- [自动化部署指南](./DEPLOYMENT.md)
- [开发者交接文档](./DEV_HANDOVER.md)
- [未来规划](./ROADMAP.md)
