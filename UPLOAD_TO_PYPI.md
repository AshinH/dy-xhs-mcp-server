# 📤 上传新版本到PyPI指南

## 🔍 问题分析

部署后没有看到小红书方法的原因是：
- **当前PyPI上的版本**: 可能是1.2.0（没有小红书功能）
- **本地构建的版本**: 1.3.0（包含小红书功能）
- **部署配置**: 使用 `douyin-mcp-server`（无版本号），会从PyPI安装最新版本

## ✅ 解决方案

### 方案1：上传到PyPI（推荐）

#### 步骤1：准备PyPI凭证

1. 访问 https://pypi.org/account/register/ 注册账号（如果还没有）
2. 访问 https://pypi.org/manage/account/token/ 创建API Token
3. 保存token（格式：`pypi-xxxxx`）

#### 步骤2：配置凭证

创建或编辑 `~/.pypirc` 文件：

```ini
[pypi]
username = __token__
password = pypi-你的token
```

或者使用环境变量：
```bash
export TWINE_USERNAME=__token__
export TWINE_PASSWORD=pypi-你的token
```

#### 步骤3：上传到PyPI

```bash
# 先上传到测试环境（可选，用于测试）
python3.11 -m twine upload --repository testpypi dist/*

# 上传到正式环境
python3.11 -m twine upload dist/*
```

#### 步骤4：验证上传

```bash
# 检查PyPI上的版本
curl https://pypi.org/pypi/douyin-mcp-server/json | python3 -m json.tool | grep version
```

#### 步骤5：重新部署

在阿里云MCP管理界面：
1. 使用配置：`"args": ["douyin-mcp-server"]`（会自动安装最新版本1.3.0）
2. 或者指定版本：`"args": ["douyin-mcp-server@1.3.0"]`
3. 重新部署服务

### 方案2：使用本地构建的包（临时方案）

如果暂时不想上传到PyPI，可以：

1. 将构建的包上传到可访问的位置（如GitHub Releases）
2. 修改部署配置使用HTTP方式安装

## 📋 上传命令

```bash
# 1. 确保已构建
python3.11 -m build

# 2. 检查构建产物
ls -lh dist/

# 3. 上传到PyPI测试环境（先测试）
python3.11 -m twine upload --repository testpypi dist/*

# 4. 测试安装
pip install --index-url https://test.pypi.org/simple/ douyin-mcp-server==1.3.0

# 5. 确认无误后上传到正式环境
python3.11 -m twine upload dist/*
```

## 🔍 验证部署

部署成功后，应该能看到以下工具：

### 抖音工具（原有）
- ✅ `get_douyin_download_link`
- ✅ `extract_douyin_text`
- ✅ `parse_douyin_video_info`

### 小红书工具（新增）
- ✅ `get_xiaohongshu_content` - 获取完整内容
- ✅ `extract_xiaohongshu_text` - 提取文案
- ✅ `extract_xiaohongshu_video_text` - 提取视频语音
- ✅ `get_xiaohongshu_images` - 获取图片

## ⚠️ 注意事项

1. **版本号**: 确保 `pyproject.toml` 和 `__init__.py` 中的版本号一致（1.3.0）
2. **依赖**: 新版本需要 `beautifulsoup4`，会自动安装
3. **缓存**: 如果部署后还是旧版本，可能需要清除缓存或等待几分钟

## 🆘 如果上传失败

1. **检查版本号**: 确保版本号比PyPI上的高
2. **检查凭证**: 确保PyPI token正确
3. **检查网络**: 确保能访问pypi.org
4. **查看错误**: 根据错误信息调整

## 📞 需要帮助？

- 查看构建脚本：`build_and_deploy.sh`
- 查看部署指南：`DEPLOY_STEPS.md`