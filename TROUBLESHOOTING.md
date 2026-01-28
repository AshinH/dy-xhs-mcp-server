# 🔧 部署错误排查指南

## 错误信息
- **错误码**: 100000
- **提示**: 系统异常

## 可能的原因和解决方案

### 1. 包名称问题

**检查**: 确认使用的是新包名 `douyin-xhs-mcp-server`

**正确配置**:
```json
{
  "mcpServers": {
    "douyin-mcp": {
      "command": "uvx",
      "args": ["douyin-xhs-mcp-server"]
    }
  }
}
```

### 2. 包还未完全同步

**问题**: PyPI上传后需要几分钟同步时间

**解决**: 
- 等待2-5分钟
- 验证包是否可用：
  ```bash
  curl https://pypi.org/pypi/douyin-xhs-mcp-server/json
  ```

### 3. 环境变量配置问题

**检查**: 确保环境变量正确设置

**配置**:
```json
{
  "mcpServers": {
    "douyin-mcp": {
      "command": "uvx",
      "args": ["douyin-xhs-mcp-server"],
      "env": {
        "DASHSCOPE_API_KEY": "sk-your-api-key-here"
      }
    }
  }
}
```

### 4. uvx命令不可用

**问题**: 阿里云环境可能不支持uvx

**解决方案A**: 使用旧包名（如果有权限）
```json
{
  "args": ["douyin-mcp-server"]
}
```

**解决方案B**: 使用HTTP方式部署（如果支持）

### 5. 服务启动中

**问题**: 首次部署需要下载和安装，可能需要5-10秒

**解决**: 等待几分钟后刷新页面

### 6. 版本号问题

**尝试**: 指定具体版本
```json
{
  "args": ["douyin-xhs-mcp-server@1.3.0"]
}
```

## 快速检查清单

- [ ] 包名称是否正确：`douyin-xhs-mcp-server`
- [ ] 等待了足够时间让PyPI同步（2-5分钟）
- [ ] 环境变量已正确配置
- [ ] 配置JSON格式正确
- [ ] 尝试重新部署

## 验证步骤

1. **验证包是否可用**:
   ```bash
   curl https://pypi.org/pypi/douyin-xhs-mcp-server/json
   ```

2. **检查配置格式**:
   ```bash
   python3 -m json.tool NEW_DEPLOY_CONFIG.json
   ```

3. **尝试本地测试**:
   ```bash
   uvx douyin-xhs-mcp-server --help
   ```

## 如果仍然失败

1. 检查阿里云MCP服务的日志
2. 尝试使用旧包名（如果有权限）
3. 联系阿里云技术支持
4. 检查是否有其他错误信息