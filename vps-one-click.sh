#!/bin/bash

# ======================================================
# Infrastructure VPS 一键部署脚本 (One-Click Setup)
# 适用于: Ubuntu 20.04+ (x86_64 / ARM)
# 功能: 安装 Docker, 设置 Swap, 配置项目环境, 启动服务
# ======================================================

# 报错即停止
set -e

echo "🚀 [Start] 开始初始化 VPS 环境..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# 1. 检查权限
if [ "$EUID" -ne 0 ]; then
  echo "❌ 请使用 root 权限运行此脚本 (sudo bash vps-one-click.sh)"
  exit 1
fi

# 2. 设置 Swap 虚拟内存 (解决 1G 内存构建失败问题)
if [ ! -f /swapfile ]; then
    echo "💾 正在配置 2GB Swap 虚拟内存..."
    fallocate -l 2G /swapfile
    chmod 600 /swapfile
    mkswap /swapfile
    swapon /swapfile
    echo '/swapfile none swap sw 0 0' >> /etc/fstab
    echo "✅ Swap 2GB 配置完成"
else
    echo "ℹ️  Swap 已存在，跳过配置"
fi

# 3. 更新系统并安装基础依赖
echo "📦 正在更新系统组件..."
apt-get update && apt-get install -y curl git jq

# 4. 安装 Docker & Docker Compose
if ! command -v docker &> /dev/null; then
    echo "🐳 正在安装 Docker..."
    curl -fsSL https://get.docker.com | bash -s docker
    systemctl enable --now docker
    echo "✅ Docker 安装完成"
else
    echo "ℹ️  Docker 已安装"
fi

if ! docker compose version &> /dev/null; then
    echo "📦 正在安装 Docker Compose 插件..."
    apt-get install -y docker-compose-plugin
    echo "✅ Docker Compose 安装完成"
else
    echo "ℹ️  Docker Compose 已安装"
fi

# 5. 初始化环境配置
if [ -d "server" ]; then
    echo "📁 进入 server 目录..."
    cd server
    
    if [ ! -f .env ]; then
        echo "📝 正在根据模板生成 .env 文件..."
        cp .env.example .env
        echo "⚠️  [Action Required] 请编辑 server/.env 文件填入实际的 API Key。"
    else
        echo "ℹ️  .env 文件已存在"
    fi
    
    chmod +x update.sh
    
    # 6. 启动服务
    echo "🏗️  正在构建并启动 Docker 容器 (这可能需要几分钟)..."
    docker compose up -d --build --remove-orphans
    
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "🎉 [Success] 部署初始化完成！"
    echo "------------------------------------------------"
    PUBLIC_IP=$(curl -s ifconfig.me || echo "VPS_IP")
    echo "Infra-Dash 管理面板: http://${PUBLIC_IP}:39999"
    echo "Dozzle 日志面板:     http://${PUBLIC_IP}:39998"
    echo "------------------------------------------------"
    echo "提示: 如果无法访问，请确保 VPS 防火墙开放了 39998, 39999, 50003 端口。"
    
else
  echo "❌ 错误: 未能在当前目录下找到 server 目录。请确保在项目根目录下运行此脚本。"
  exit 1
fi
