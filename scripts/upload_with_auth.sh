#!/bin/bash

# 交互式上传到PyPI脚本

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

# 检查是否已有凭证
if [ -f ~/.pypirc ]; then
    echo "✅ 找到 ~/.pypirc 配置文件"
    read -p "是否使用现有配置？(y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        USE_EXISTING=false
    else
        USE_EXISTING=true
    fi
else
    USE_EXISTING=false
fi

# 如果没有凭证，提示输入
if [ "$USE_EXISTING" = false ]; then
    echo ""
    echo "📝 需要PyPI凭证才能上传"
    echo ""
    echo "💡 获取凭证步骤："
    echo "   1. 访问 https://pypi.org/manage/account/token/"
    echo "   2. 创建新的API Token"
    echo "   3. 复制token（格式：pypi-xxxxx）"
    echo ""
    
    read -p "请输入PyPI Token: " PYPI_TOKEN
    
    if [ -z "$PYPI_TOKEN" ]; then
        echo "❌ Token不能为空"
        exit 1
    fi
    
    # 设置环境变量
    export TWINE_USERNAME=__token__
    export TWINE_PASSWORD="$PYPI_TOKEN"
    
    echo ""
    echo "✅ 凭证已设置（仅本次会话有效）"
fi

echo ""
echo "📤 开始上传到PyPI..."
echo ""

# 上传到PyPI
python3.11 -m twine upload dist/*

echo ""
echo "✅ 上传完成！"
echo ""
echo "📋 下一步："
echo "1. 等待几分钟让PyPI更新（通常1-2分钟）"
echo "2. 验证上传："
echo "   curl https://pypi.org/pypi/douyin-mcp-server/json | grep '\"version\"'"
echo "3. 在阿里云MCP管理界面重新部署"
echo "4. 使用配置: {\"args\": [\"douyin-mcp-server\"]} 或 {\"args\": [\"douyin-mcp-server@1.3.0\"]}"
echo ""
echo "🎉 部署后应该能看到小红书方法了！"