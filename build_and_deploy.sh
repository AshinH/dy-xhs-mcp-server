#!/bin/bash

# 抖音MCP服务器打包和部署脚本

set -e

echo "🚀 抖音MCP服务器打包部署脚本"
echo "=" | head -c 50 && echo ""

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 检查Python版本
echo "📋 检查Python版本..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "当前Python版本: $python_version"

# 检查必要的工具
echo ""
echo "🔍 检查构建工具..."
if ! command -v python3 -m build &> /dev/null; then
    echo -e "${YELLOW}⚠️  build工具未安装，正在安装...${NC}"
    pip3 install build twine
fi

# 清理旧的构建文件
echo ""
echo "🧹 清理旧的构建文件..."
rm -rf dist/ build/ *.egg-info

# 构建项目
echo ""
echo "📦 开始构建项目..."
python3 -m build

# 检查构建结果
if [ -d "dist" ]; then
    echo -e "${GREEN}✅ 构建成功!${NC}"
    echo ""
    echo "📦 构建产物:"
    ls -lh dist/
    echo ""
    
    # 显示下一步操作
    echo "📋 下一步操作:"
    echo "1. 测试安装:"
    echo "   pip install dist/douyin_mcp_server-*.whl"
    echo ""
    echo "2. 上传到PyPI测试环境:"
    echo "   python3 -m twine upload --repository testpypi dist/*"
    echo ""
    echo "3. 上传到PyPI正式环境:"
    echo "   python3 -m twine upload dist/*"
    echo ""
    echo "4. 使用uvx测试:"
    echo "   uvx douyin-mcp-server"
    echo ""
    echo "5. 在阿里云MCP管理界面部署，使用以下配置:"
    echo "   $(cat deploy_aliyun_mcp.json)"
    
else
    echo -e "${RED}❌ 构建失败!${NC}"
    exit 1
fi