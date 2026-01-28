#!/bin/bash

# 抖音MCP服务器启动脚本

echo "🚀 启动抖音MCP服务器..."

# 检查配置文件是否存在
if [ ! -f "config.json" ]; then
    echo "❌ 错误: 未找到 config.json 配置文件"
    echo "💡 请创建 config.json 文件并配置API密钥"
    exit 1
fi

# 设置Python路径
export PYTHONPATH="/Users/holidayhe/IdeaProjects/douyin-mcp-server:$PYTHONPATH"

# 启动服务器
cd /Users/holidayhe/IdeaProjects/douyin-mcp-server
python3.11 -m douyin_mcp_server.server

echo "服务器已停止"