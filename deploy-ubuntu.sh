#!/bin/bash
# OpenClaw Ubuntu 部署脚本
# 适用于阿里云 Ubuntu 服务器

set -e

echo "🚀 OpenClaw 部署脚本 - 开始"
echo "================================"

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 配置变量
OPENCLAW_PORT=18789
NODE_VERSION=22

echo -e "${GREEN}[1/7]${NC} 更新系统包..."
sudo apt-get update
sudo apt-get upgrade -y

echo -e "${GREEN}[2/7]${NC} 安装基础依赖..."
sudo apt-get install -y \
    curl \
    git \
    wget \
    build-essential \
    ufw

echo -e "${GREEN}[3/7]${NC} 安装 Node.js v${NODE_VERSION}..."
# 检查是否已安装
if command -v node &> /dev/null; then
    NODE_VER=$(node -v | cut -d'v' -f2 | cut -d'.' -f1)
    if [ "$NODE_VER" -ge 20 ]; then
        echo "✅ Node.js 已安装 (v$(node -v))"
    else
        echo -e "${YELLOW}⚠️  Node.js 版本过旧，需要升级${NC}"
        curl -fsSL https://deb.nodesource.com/setup_${NODE_VERSION}.x | sudo -E bash -
        sudo apt-get install -y nodejs
    fi
else
    curl -fsSL https://deb.nodesource.com/setup_${NODE_VERSION}.x | sudo -E bash -
    sudo apt-get install -y nodejs
fi

node -v
npm -v

echo -e "${GREEN}[4/7]${NC} 安装 OpenClaw..."
sudo npm install -g openclaw
openclaw --version

echo -e "${GREEN}[5/7]${NC} 创建 OpenClaw 用户..."
# 创建专用用户（可选，更安全）
if ! id "openclaw" &>/dev/null; then
    sudo useradd -r -m -s /bin/bash openclaw
    echo "✅ 已创建 openclaw 用户"
else
    echo "✅ openclaw 用户已存在"
fi

echo -e "${GREEN}[6/7]${NC} 配置防火墙..."
# 配置 UFW 防火墙
sudo ufw allow ssh
sudo ufw allow ${OPENCLAW_PORT}/tcp
sudo ufw --force enable || true
echo "✅ 防火墙已配置 (端口 ${OPENCLAW_PORT})"

echo -e "${GREEN}[7/7]${NC} 安装 OpenClaw systemd 服务..."
# 使用 OpenClaw 自带命令安装服务
sudo openclaw gateway install --user openclaw

# 重新加载 systemd
sudo systemctl daemon-reload
sudo systemctl enable openclaw-gateway

echo ""
echo "================================"
echo -e "${GREEN}✅ 部署完成！${NC}"
echo ""
echo "📋 下一步操作："
echo ""
echo "1️⃣  切换到 openclaw 用户并初始化配置："
echo "   sudo su - openclaw"
echo "   openclaw init"
echo ""
echo "2️⃣  配置阿里云百炼 API（编辑配置文件）："
echo "   nano ~/.openclaw/openclaw.json"
echo ""
echo "3️⃣  启动服务："
echo "   sudo systemctl start openclaw-gateway"
echo ""
echo "4️⃣  查看状态："
echo "   sudo systemctl status openclaw-gateway"
echo "   openclaw gateway status"
echo ""
echo "5️⃣  阿里云安全组：确保开放端口 ${OPENCLAW_PORT}"
echo ""
echo "🔗 访问地址：http://<服务器IP>:${OPENCLAW_PORT}"
echo ""

# 创建配置模板
echo "📝 创建配置模板..."
cat > /tmp/openclaw-config-template.json <<'TEMPLATE'
{
  "models": {
    "providers": {
      "aliyun": {
        "baseUrl": "https://coding.dashscope.aliyuncs.com/v1",
        "apiKey": "YOUR_API_KEY_HERE",
        "api": "openai-completions",
        "models": [
          {
            "id": "qwen3.5-plus",
            "name": "Qwen 3.5 Plus",
            "reasoning": false,
            "input": ["text", "image"],
            "contextWindow": 128000,
            "maxTokens": 8192
          }
        ]
      }
    }
  },
  "agents": {
    "defaults": {
      "model": {
        "primary": "aliyun/qwen3.5-plus"
      }
    }
  },
  "gateway": {
    "port": 18789,
    "bind": "0.0.0.0",
    "auth": {
      "mode": "token",
      "token": "GENERATE_A_STRONG_TOKEN"
    }
  }
}
TEMPLATE

echo "📄 配置模板已保存到：/tmp/openclaw-config-template.json"
echo ""
echo -e "${YELLOW}⚠️  记得替换 API Key 和 Token！${NC}"
echo ""
