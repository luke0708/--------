# 🚀 部署端操作规范 (Deployment Protocol)

> **给部署端 AI (Mac Air/VPS) 的指令**

## 1. 接收任务
当你收到用户提供的 `[项目名]-deliverable.zip` 时：
1. **Unzip**: 先将其解压到临时目录。
2. **Read Manifest**: 查找并读取 `deploy_manifest.txt` 获取端口和项目信息。

## 2. 登记流程 (必须执行)
根据从清单中读取的信息：
1. **Pull**: 进入 `Port-Registry/` 目录，执行 `git pull`。
2. **Update**: 打开 `Global_Port_Registry.md`，将该端口的状态从 `⚪️ Free` 改为 `✅ Active`，填入 `Service ID`。
3. **Commit & Push**: 
   ```bash
   git add Global_Port_Registry.md
   git commit -m "Activate port XXXX for [项目名]"
   git push
   ```

## 3. 部署执行
1. 解压包到 `projects/[项目名]`。
2. 更新 `server/docker-compose.yml`。
3. 运行 `server/update.sh` 或通过 **Infra-Dash** 重建该服务。

## 4. 反馈
告知用户：“端口 `XXXX` 已在云端注册表激活，服务部署完成。”
