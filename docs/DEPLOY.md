# 阿里云MCP服务部署指南

## 📦 部署前准备

### 1. 确保项目已发布到PyPI

项目需要先发布到PyPI，然后才能通过`uvx`安装。

#### 发布步骤：

```bash
# 1. 安装构建工具
pip install build twine

# 2. 构建分发包
python -m build

# 3. 检查构建结果
ls -la dist/

# 4. 上传到PyPI（测试环境）
python -m twine upload --repository testpypi dist/*

# 5. 上传到PyPI（正式环境）
python -m twine upload dist/*
```

### 2. 本地测试打包

```bash
# 使用uvx本地测试
uvx douyin-mcp-server

# 或者指定版本
uvx douyin-mcp-server@1.2.0
```

## 🚀 阿里云MCP部署配置

### 方式1：使用uvx部署（推荐）

在阿里云MCP管理界面中，使用以下配置：

```json
{
  "mcpServers": {
    "douyin-mcp": {
      "command": "uvx",
      "args": [
        "douyin-mcp-server"
      ],
      "env": {
        "DASHSCOPE_API_KEY": "your-dashscope-api-key-here"
      }
    }
  }
}
```

**配置说明：**
- **安装方式**: 选择 `uvx`
- **部署方式**: 基础模式（按次计费）或极速模式（按小时计费）
- **部署地域**: 选择离您最近的地域
- **MCP服务配置**: 粘贴上面的JSON配置，替换`your-dashscope-api-key-here`为您的真实API密钥

### 方式2：使用npx部署（如果发布到npm）

如果项目也发布到npm，可以使用npx：

```json
{
  "mcpServers": {
    "douyin-mcp": {
      "command": "npx",
      "args": [
        "douyin-mcp-server"
      ],
      "env": {
        "DASHSCOPE_API_KEY": "your-dashscope-api-key-here"
      }
    }
  }
}
```

### 方式3：使用HTTP部署（自定义服务器）

如果您的项目部署为HTTP服务：

```json
{
  "mcpServers": {
    "douyin-mcp": {
      "url": "https://your-server.com/mcp",
      "headers": {
        "Authorization": "Bearer your-token"
      }
    }
  }
}
```

## ⚙️ 环境变量配置

### 必需的环境变量

- `DASHSCOPE_API_KEY`: 阿里云百炼API密钥（必需）

### 可选的环境变量

- `DOUYIN_MODEL`: 语音识别模型，默认为 `paraformer-v2`
- `DOUYIN_TEMP_DIR`: 临时文件目录，默认为 `temp`

## 📋 部署检查清单

- [ ] 项目已发布到PyPI
- [ ] 在本地使用uvx测试成功
- [ ] 准备好阿里云百炼API密钥
- [ ] 选择合适的地域部署
- [ ] 配置正确的环境变量
- [ ] 测试部署后的服务

## 🔍 故障排查

### 问题1：uvx找不到包

**解决方案：**
- 确保包已正确发布到PyPI
- 检查包名是否正确：`douyin-mcp-server`
- 尝试指定版本号：`douyin-mcp-server@1.2.0`

### 问题2：API密钥错误

**解决方案：**
- 检查环境变量`DASHSCOPE_API_KEY`是否正确设置
- 确认API密钥有效且有足够的额度
- 查看阿里云函数计算的日志

### 问题3：服务启动失败

**解决方案：**
- 检查Python版本（需要3.10+）
- 查看函数计算的执行日志
- 确认所有依赖都已正确安装

## 💰 费用说明

### 基础模式（按次计费）
- 首次请求：5~10秒连接时间
- 计费：0.000156元/秒
- 连接断开后自动释放，不计费

### 极速模式（按小时计费）
- 冷启动：≤5毫秒
- 计费：0.13元/小时
- 需要手动关闭服务

## 📞 支持

如有问题，请查看：
- 项目GitHub: https://github.com/yzfly/douyin-mcp-server
- 阿里云函数计算文档
- MCP协议文档