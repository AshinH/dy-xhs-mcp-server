# 📤 上传到PyPI操作指南

## ✅ 构建产物已准备就绪

- `douyin_mcp_server-1.3.0-py3-none-any.whl` (20.7 KB)
- `douyin_mcp_server-1.3.0.tar.gz` (112.1 KB)

## 🚀 快速上传方法

### 方法1：使用环境变量（推荐）

```bash
# 1. 设置PyPI Token（替换为你的实际token）
export TWINE_USERNAME=__token__
export TWINE_PASSWORD=pypi-你的token

# 2. 上传
python3.11 -m twine upload dist/*
```

### 方法2：使用配置文件

创建 `~/.pypirc` 文件：

```ini
[pypi]
username = __token__
password = pypi-你的token
```

然后运行：
```bash
python3.11 -m twine upload dist/*
```

### 方法3：交互式脚本

```bash
# 运行交互式脚本，会提示输入token
./upload_with_auth.sh
```

## 📝 获取PyPI Token步骤

1. 访问 https://pypi.org/account/login/ 登录（如果没有账号先注册）
2. 访问 https://pypi.org/manage/account/token/
3. 点击 "Add API token"
4. 输入token名称（如：douyin-mcp-server-upload）
5. 选择Scope：整个账户（Entire account）
6. 点击 "Add token"
7. 复制token（格式：`pypi-xxxxx`，只显示一次，请保存好）

## ✅ 验证上传

上传成功后，等待1-2分钟，然后验证：

```bash
curl https://pypi.org/pypi/douyin-mcp-server/json | grep '"version"'
```

应该看到 `"version": "1.3.0"`

## 🔄 重新部署

上传成功后，在阿里云MCP管理界面：

1. 重新部署服务
2. 使用配置：
```json
{
  "mcpServers": {
    "douyin-mcp": {
      "command": "uvx",
      "args": ["douyin-mcp-server"],
      "env": {
        "DASHSCOPE_API_KEY": "sk-your-api-key-here"
      }
    }
  }
}
```

3. 部署后应该能看到小红书方法了！

## 📋 应该看到的工具列表

### 抖音工具（原有）
- ✅ `get_douyin_download_link`
- ✅ `extract_douyin_text`
- ✅ `parse_douyin_video_info`

### 小红书工具（新增）
- ✅ `get_xiaohongshu_content`
- ✅ `extract_xiaohongshu_text`
- ✅ `extract_xiaohongshu_video_text`
- ✅ `get_xiaohongshu_images`