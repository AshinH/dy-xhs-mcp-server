# 🚀 快速部署到阿里云MCP服务

## 📋 部署配置（直接复制使用）

在阿里云MCP管理界面的"MCP服务配置"中，粘贴以下JSON：

```json
{
  "mcpServers": {
    "douyin-mcp": {
      "command": "uvx",
      "args": [
        "douyin-mcp-server"
      ],
      "env": {
        "DASHSCOPE_API_KEY": "sk-your-api-key-here"
      }
    }
  }
}
```

## ⚙️ 部署步骤

### 1. 选择安装方式
- ✅ 选择 **uvx** （Python包管理器）

### 2. 选择部署方式
- **基础模式**（推荐）：按次计费，适合低频使用
- **极速模式**：按小时计费，适合高频使用

### 3. 选择部署地域
- 选择离您最近的地域（如：华东1-杭州）

### 4. 配置MCP服务
- 复制上面的JSON配置
- 替换 `DASHSCOPE_API_KEY` 为您的真实API密钥（如果需要）

### 5. 提交部署
- 点击"提交部署"按钮
- 等待部署完成（首次部署需要5-10秒）

## 🔑 重要说明

### API密钥配置
- 如果您的API密钥已经在配置中，可以直接使用
- 如果需要更换，修改JSON中的 `DASHSCOPE_API_KEY` 值

### 包发布状态
⚠️ **注意**：项目需要先发布到PyPI才能通过uvx安装

如果项目还未发布，有两种选择：

#### 选项A：发布到PyPI（推荐）
```bash
# 1. 构建包
python3 -m build

# 2. 上传到PyPI
python3 -m twine upload dist/*
```

#### 选项B：使用本地包（开发测试）
如果只是测试，可以修改配置使用本地路径（需要先打包）

## 📦 本地打包测试

在部署前，建议先在本地测试：

```bash
# 1. 构建包
./build_and_deploy.sh

# 2. 测试安装
pip install dist/douyin_mcp_server-*.whl

# 3. 测试运行
python3 -m douyin_mcp_server.server
```

## ✅ 部署后验证

部署成功后，您可以通过以下方式验证：

1. **查看函数计算日志**：检查是否有错误
2. **测试MCP工具**：尝试调用 `get_douyin_download_link` 工具
3. **检查环境变量**：确认API密钥正确加载

## 🆘 常见问题

### Q: uvx找不到包怎么办？
A: 确保包已发布到PyPI，或使用完整版本号：`douyin-mcp-server@1.2.0`

### Q: 如何更新部署？
A: 在MCP管理界面重新提交配置即可，会自动更新

### Q: 费用如何计算？
A: 
- 基础模式：按实际调用时长，0.000156元/秒
- 极速模式：按部署时长，0.13元/小时

## 📞 需要帮助？

- 查看详细文档：`DEPLOY.md`
- 项目GitHub：https://github.com/yzfly/douyin-mcp-server