# ⚠️ 上传权限问题解决方案

## 问题

上传失败，错误信息：
```
The user 'ashinhe' isn't allowed to upload to project 'douyin-mcp-server'
```

## 原因

PyPI上的 `douyin-mcp-server` 项目属于其他用户（可能是 `yzfly`），当前账号 `ashinhe` 没有维护者权限。

## 解决方案

### 方案1：联系项目所有者添加维护者（推荐）

1. 联系项目所有者（可能是 yzfly，邮箱：yz.liu.me@gmail.com）
2. 请求添加为项目维护者（Maintainer）
3. 添加后即可上传新版本

### 方案2：使用不同的项目名称

如果无法获得权限，可以：

1. **修改项目名称**（在 `pyproject.toml` 中）：
   ```toml
   name = "douyin-xhs-mcp-server"  # 或其他名称
   ```

2. **重新构建**：
   ```bash
   python3.11 -m build
   ```

3. **上传新项目**：
   ```bash
   export TWINE_USERNAME=__token__
   export TWINE_PASSWORD="你的token"
   python3.11 -m twine upload dist/*
   ```

4. **更新部署配置**：
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

### 方案3：检查是否有其他上传方式

检查项目是否有其他维护者账号或CI/CD配置。

## 当前状态

- ✅ 代码已准备好（1.3.0版本，包含小红书功能）
- ✅ 构建产物已生成
- ❌ 需要上传权限才能发布到PyPI

## 建议

1. **优先尝试方案1**：联系原项目所有者添加维护者权限
2. **如果无法联系**：使用方案2，创建新项目名称
3. **临时方案**：可以先将包上传到GitHub Releases，然后使用HTTP方式部署