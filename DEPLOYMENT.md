# ⚙️ DEPLOYMENT.md (运维手册)

本手册面向运维人员，描述项目底层架构与生产环境运维操作。

## 1. 架构说明
项目采用 **总控-子项目** 模式：
- **Infrastructure**: 定义核心网络、共享卷、监控工具和所有项目的 Docker 编排。
- **Projects**: 存放具体的业务代码，每个项目有独立的 `Dockerfile`。

## 2. 生产环境要求 (VPS)
- **系统**: Ubuntu 20.04+ (LTS)
- **建议内存**: 1GB (必须配置 2GB+ Swap)
- **基础软件**: Docker 20.10+, Docker Compose Plugin

## 3. 全新服务器部署
```bash
# 执行一键安装脚本
sudo bash vps-one-click.sh
```

## 4. 日常维护命令
进入 `server/` 目录执行：
- **平滑更新所有项目**: `./update.sh`
- **查看服务状态**: `docker compose ps`
- **彻底停止并删除容器**: `docker compose down`
- **清理磁盘 (删除无用镜像)**: `docker system prune -af`

## 5. 安全建议
- **端口暴露**: 建议在生产环境前端架设 **Nginx Proxy Manager** 或反向代理，仅开放 80/443 端口。
- **密钥管理**: `.env` 文件被列入 `.gitignore`，严禁上传到公开仓库。

## 6. 端口注册表
所有新增服务必须在 `Port-Registry/Global_Port_Registry.md` 中进行登记，避免端口冲突。
- **39998**: Dozzle
- **39999**: Infra-Dash
- **50003**: News-Tracker
