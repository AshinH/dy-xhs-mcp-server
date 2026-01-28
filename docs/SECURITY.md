# 安全说明

## 🔐 API密钥管理

为了保护您的API密钥安全，项目已配置为不将包含真实密钥的文件提交到Git仓库。

### 本地密钥管理

1. **配置文件位置**
   - 运行时配置：`config.json`（项目根目录）
   - 部署配置：`configs/*.json`（本地管理，不提交到Git）

2. **创建本地配置文件**
   ```bash
   # 复制示例文件
   cp configs/NEW_DEPLOY_CONFIG.json.example configs/NEW_DEPLOY_CONFIG.json
   
   # 编辑并填入您的真实API密钥
   # 注意：这些文件已被.gitignore忽略，不会提交到Git
   ```

3. **环境变量方式（推荐）**
   ```bash
   # 在系统环境变量中设置
   export DASHSCOPE_API_KEY="your-real-api-key-here"
   ```

### 已清理的敏感信息

项目历史记录中的真实API密钥已被清理，所有配置文件中的密钥已替换为占位符：
- `sk-your-api-key-here` - 请替换为您的真实密钥

### 注意事项

⚠️ **重要提醒：**
- 永远不要将包含真实API密钥的文件提交到Git仓库
- 定期轮换API密钥
- 如果密钥意外泄露，请立即在服务提供商处撤销并重新生成
