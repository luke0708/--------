#!/bin/bash

# ===========================================
# Infrastructure 自动化更新脚本
# 用于 MacBook Air / VPS 运行端
# ===========================================

# ================== 配置区 ==================
# 列出所有需要更新的项目文件夹名称
PROJECTS=(
    "Demo-Backend"
    # 添加新项目时在此追加，例如：
    # "User-Backend"
    # "Order-Backend"
)

# Git 分支名称
BRANCH="main"
# ============================================

set -e  # 遇到错误立即退出

echo "🚀 [Start] 开始全量更新流程..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# 1. 遍历所有项目拉取最新代码
for proj in "${PROJECTS[@]}"; do
    target_dir="../projects/$proj"
    
    if [ -d "$target_dir" ]; then
        echo ""
        echo "⬇️  正在更新项目: $proj"
        cd "$target_dir" || exit
        
        # 强制丢弃本地修改，与远程仓库保持完全一致
        git fetch --all
        git reset --hard origin/$BRANCH
        git pull origin $BRANCH
        
        echo "✅ $proj 已同步至最新版本"
        
        # 回到总控目录
        cd - > /dev/null
    else
        echo ""
        echo "⚠️  警告: 找不到目录 $target_dir，跳过该项目"
    fi
done

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📦 所有代码已同步完成"
echo ""

# 2. Docker 容器重构与重启
echo "🐳 正在重建并重启 Docker 服务..."
echo ""

# --build: 强制重新构建镜像
# -d: 后台运行
# --remove-orphans: 清理已删除的旧服务
docker compose up -d --build --remove-orphans

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🎉 [Success] 所有后台服务已更新并正在运行！"
echo ""
docker compose ps
