# 配置文件目录

## ⚠️ 重要提示

此目录下的所有 `.json` 文件**不会被提交到Git仓库**（已在 `.gitignore` 中配置）。

## 📝 使用方法

### 1. 创建本地配置文件

从示例文件创建您的本地配置：

```bash
# 复制示例文件
cp NEW_DEPLOY_CONFIG.json.example NEW_DEPLOY_CONFIG.json

# 编辑文件，替换占位符为您的真实API密钥
# "sk-your-api-key-here" -> "sk-您的真实密钥"
```

### 2. 配置文件说明

- `NEW_DEPLOY_CONFIG.json.example` - 新部署配置示例
- `ALIYUN_DEPLOY_CONFIG.json.example` - 阿里云部署配置示例
- `deploy_aliyun_mcp.json.example` - 阿里云MCP部署配置示例
- `ALTERNATIVE_CONFIGS.json` - 替代配置（已清理密钥）

### 3. 环境变量方式（推荐）

您也可以使用环境变量来设置API密钥，无需创建配置文件：

```bash
export DASHSCOPE_API_KEY="your-real-api-key-here"
```

## 🔐 安全建议

1. **永远不要提交包含真实密钥的文件**
2. **定期轮换API密钥**
3. **如果密钥泄露，立即撤销并重新生成**
4. **使用环境变量管理密钥（更安全）**

## 📚 相关文档

- [安全说明](../../docs/SECURITY.md)
- [部署文档](../../docs/DEPLOY.md)
