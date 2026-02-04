# 💻 DEV_HANDOVER.md (贡献指南/交接)

本手册面向开发者，说明如何维护代码、增加新功能或添加新项目。

## 1. 开发机环境 (Mac mini)
- 建议使用 Cursor 或 VS Code 进行开发。
- 业务代码放在主目录外的独立仓库或 `projects/` 目录下（开发模式建议放在同级目录）。

## 2. 添加新服务流程
1. **创建项目**: 包含 `Dockerfile` 和 `.dockerignore`。
2. **测试构建**: `docker build -t test-service .`
3. **注册端口**: 修改 `Port-Registry/Global_Port_Registry.md` 分配新端口。
4. **修改总控**:
   - 在 `server/docker-compose.yml` 中添加服务定义。
   - 在 `server/update.sh` 的 `PROJECTS` 数组中添加项目名。
5. **提交代码**: `git push` 到 GitHub。

## 3. 开发规范
- **无状态设计**: 所有持久化数据必须写到 `/app/data` 并在 `docker-compose.yml` 中挂载 Volume。
- **配置分离**: 严禁在代码中硬编码任何敏感信息，必须通过 `os.getenv` 读取环境变量。
- **镜像优化**: 尽量使用 `python:3.x-slim` 或 `alpine` 基础镜像，减少 VPS 存储占用。

## 4. 目录契约
- 代码目录与 `docker-compose.yml` 中的相对路径必须保持一致。
- 环境变量模板统一放在 `server/.env.example`。
