# 🏗️ Infrastructure: 自动化部署总控工程

> **自动化、容器化、极简主义的生产部署方案。**

本仓库是所有后台服务的“指挥中心”，通过 Git + Docker 实现从开发环境到生产服务器的无缝同步与自动化部署。

## 🌟 核心能力
- **一键部署**: 专为 1G 内存 VPS 优化的部署脚本，自动配置 Swap 与环境。
- **全量更新**: `update.sh` 同步所有子项目代码并平滑重启。
- **可视化管理**: 内嵌 `Infra-Dash` 面板与 `Dozzle` 日志监控系统。
- **端口管理**: 统一的全局端口注册表（Port-Registry），避免冲突。

## 📂 项目结构
```text
~/Projects/
├── Infrastructure/          ← (本仓库) 总控中心
│   ├── server/              # 核心配置 (docker-compose, update.sh)
│   ├── vps-one-click.sh     # VPS 初始化脚本
│   └── docs/                # 详细文档
└── projects/                # 各业务子项目 (由脚本管理)
    ├── news-tracker/
    └── ...
```

## 🚀 快速开始
1. **获取代码**: `git clone [repo_url] Infrastructure && cd Infrastructure`
2. **VPS 安装**: `sudo bash vps-one-click.sh`
3. **配置密钥**: 编辑 `server/.env`

---
*更多细节请参考下面的各分册文档：*

- [📖 使用手册 (USER_MANUAL)](USER_MANUAL.md) - *如何使用管理面板和日志工具*
- [⚙️ 部署手册 (DEPLOYMENT)](DEPLOYMENT.md) - *详细的服务器环境配置与架构说明*
- [💻 开发者交接 (DEV_HANDOVER)](DEV_HANDOVER.md) - *如何添加新项目、开发规范与架构说明*
- [🛣️ 未来规划 (ROADMAP)](ROADMAP.md) - *项目后续功能迭代计划*
