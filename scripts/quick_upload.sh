#!/bin/bash

# 快速上传到PyPI脚本

set -e

echo "🚀 上传douyin-mcp-server 1.3.0到PyPI"
echo "=" | head -c 50 && echo ""

# 检查构建产物
if [ ! -d "dist" ] || [ -z "$(ls -A dist/*.whl 2>/dev/null)" ]; then
    echo "❌ 未找到构建产物，先构建..."
    python3.11 -m build
fi

echo ""
echo "📦 构建产物:"
ls -lh dist/

echo ""
echo "📤 准备上传到PyPI..."
echo ""
echo "⚠️  请确保已配置PyPI凭证："
echo "   方式1: 创建 ~/.pypirc 文件"
echo "   方式2: 设置环境变量 TWINE_USERNAME 和 TWINE_PASSWORD"
echo ""

read -p "是否继续上传？(y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "已取消"
    exit 1
fi

# 上传到PyPI
echo ""
echo "📤 上传中..."
python3.11 -m twine upload dist/*

echo ""
echo "✅ 上传完成！"
echo ""
echo "📋 下一步："
echo "1. 等待几分钟让PyPI更新"
echo "2. 在阿里云MCP管理界面重新部署"
echo "3. 使用配置: {\"args\": [\"douyin-mcp-server\"]} 或 {\"args\": [\"douyin-mcp-server@1.3.0\"]}"
echo ""
echo "🔍 验证上传："
echo "   curl https://pypi.org/pypi/douyin-mcp-server/json | grep version"