# 🚀 打包部署步骤指南

## ✅ 已完成的工作

1. ✅ **版本更新**: 1.2.0 → 1.3.0（新增小红书功能）
2. ✅ **依赖更新**: 添加了 beautifulsoup4
3. ✅ **代码构建**: 成功构建分发包
4. ✅ **部署配置**: 已准备就绪

## 📦 构建结果

构建产物已生成在 `dist/` 目录：
- `douyin_mcp_server-1.3.0-py3-none-any.whl` - Wheel包
- `douyin_mcp_server-1.3.0.tar.gz` - 源码包

## 🚀 部署步骤

### 步骤1：上传到PyPI（推荐）

```bash
# 上传到PyPI测试环境（先测试）
python3.11 -m twine upload --repository testpypi dist/*

# 测试安装
pip install --index-url https://test.pypi.org/simple/ douyin-mcp-server==1.3.0

# 确认无误后上传到正式环境
python3.11 -m twine upload dist/*
```

### 步骤2：在阿里云MCP管理界面部署

根据您提供的截图，在编辑界面中：

#### 2.1 基本信息
- **服务名称**: 视频去水印（或改为：视频文案提取）
- **描述**: 主要是抖音视频（或改为：支持抖音和小红书视频、图片、文案提取）

#### 2.2 安装方式
- ✅ 选择 **uvx**

#### 2.3 部署方式
- **基础模式**（推荐）：按次计费，0.000156元/秒
- **极速模式**：按小时计费，0.13元/小时（可选）

#### 2.4 MCP服务配置

**如果已上传到PyPI，使用：**
```json
{
  "mcpServers": {
    "douyin-mcp": {
      "command": "uvx",
      "args": [
        "douyin-mcp-server@1.3.0"
      ],
      "env": {
        "DASHSCOPE_API_KEY": "sk-your-api-key-here"
      }
    }
  }
}
```

**如果还未上传，使用最新版本：**
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

### 步骤3：提交部署

点击"提交部署"按钮，等待部署完成。

## 📋 新版本功能

### v1.3.0 新增功能

1. ✅ **小红书支持**
   - 视频笔记提取
   - 图文笔记提取
   - 文案自动提取
   - 图片无水印提取

2. ✅ **无水印处理**
   - 自动去除图片水印参数
   - 视频链接无水印

3. ✅ **增强解析**
   - 改进文案提取逻辑
   - 支持短链接自动解析
   - 增强视频URL提取

## 🔍 验证部署

部署成功后，可以测试：

1. **抖音功能**：
   - `get_douyin_download_link`
   - `extract_douyin_text`
   - `parse_douyin_video_info`

2. **小红书功能**：
   - `get_xiaohongshu_content`
   - `extract_xiaohongshu_text`
   - `extract_xiaohongshu_video_text`
   - `get_xiaohongshu_images`

## ⚠️ 注意事项

1. **版本号**: 如果使用 `@1.3.0`，需要先上传到PyPI
2. **API密钥**: 确保环境变量中的API密钥正确
3. **依赖**: 新版本需要 beautifulsoup4，会自动安装

## 📞 需要帮助？

- 查看详细文档：`README.md`
- 查看部署指南：`DEPLOY.md`
- 查看小红书功能：`XIAOHONGSHU_FEATURES.md`