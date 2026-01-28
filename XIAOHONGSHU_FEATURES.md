# 📱 小红书功能使用指南

## 🎯 功能概览

本项目现已支持小红书内容提取功能，包括：

- ✅ 视频笔记内容提取
- ✅ 图文笔记内容提取
- ✅ 文案自动提取
- ✅ 图片链接获取
- ✅ 视频语音识别（需要API密钥）

## 🛠️ 可用工具

### 1. `get_xiaohongshu_content` - 获取完整内容

获取小红书笔记的完整信息，包括视频、图片、文案等。

**示例：**
```python
from douyin_mcp_server.server import get_xiaohongshu_content

result = get_xiaohongshu_content("https://www.xiaohongshu.com/explore/xxxxx")
print(result)
```

**返回格式：**
```json
{
  "status": "success",
  "note_id": "xxxxx",
  "title": "笔记标题",
  "description": "笔记描述内容",
  "type": "video",  // 或 "image"
  "video_url": "视频链接（如果是视频笔记）",
  "images": ["图片链接1", "图片链接2"],
  "author": {
    "name": "作者名称",
    "id": "作者ID"
  },
  "tags": ["标签1", "标签2"],
  "metrics": {
    "likes": 1000,
    "comments": 100,
    "collected": 500
  }
}
```

### 2. `extract_xiaohongshu_text` - 提取文案

快速提取笔记的文案内容（标题、描述、标签）。

**示例：**
```python
from douyin_mcp_server.server import extract_xiaohongshu_text

text = extract_xiaohongshu_text("https://www.xiaohongshu.com/explore/xxxxx")
print(text)
```

**特点：**
- ✅ 无需API密钥
- ✅ 快速提取
- ✅ 包含标题、描述、标签

### 3. `extract_xiaohongshu_video_text` - 提取视频语音

从视频笔记中提取语音内容（需要API密钥）。

**示例：**
```python
from douyin_mcp_server.server import extract_xiaohongshu_video_text

text = await extract_xiaohongshu_video_text("https://www.xiaohongshu.com/explore/xxxxx")
print(text)
```

**特点：**
- ⚠️ 需要API密钥
- ✅ 支持语音识别
- ✅ 自动组合文案和语音内容

### 4. `get_xiaohongshu_images` - 获取图片

获取笔记中的所有图片链接。

**示例：**
```python
from douyin_mcp_server.server import get_xiaohongshu_images

result = get_xiaohongshu_images("https://www.xiaohongshu.com/explore/xxxxx")
print(result)
```

## 📋 使用场景

### 场景1：提取图文笔记文案
```python
# 快速提取文案，无需API密钥
text = extract_xiaohongshu_text("小红书链接")
```

### 场景2：获取视频笔记完整内容
```python
# 获取视频链接、文案、图片等
content = get_xiaohongshu_content("小红书链接")
video_url = json.loads(content)["video_url"]
```

### 场景3：提取视频语音内容
```python
# 需要API密钥，提取视频中的语音
text = await extract_xiaohongshu_video_text("小红书链接")
```

### 场景4：批量下载图片
```python
# 获取所有图片链接
result = get_xiaohongshu_images("小红书链接")
images = json.loads(result)["images"]
for img_url in images:
    # 下载图片
    pass
```

## ⚙️ 配置说明

### 基础配置（无需API密钥）

大部分功能无需API密钥即可使用：
- ✅ 获取笔记内容
- ✅ 提取文案
- ✅ 获取图片链接

### 高级配置（需要API密钥）

以下功能需要配置API密钥：
- ⚠️ 视频语音识别

在 `config.json` 中配置：
```json
{
  "api_key": "sk-your-api-key-here",
  "model": "paraformer-v2"
}
```

## 🔍 链接格式支持

支持以下小红书链接格式：

- `https://www.xiaohongshu.com/explore/{note_id}`
- `https://www.xiaohongshu.com/note/{note_id}`
- 分享链接（会自动解析）

## ⚠️ 注意事项

1. **合规使用**：请遵守小红书平台的使用条款
2. **API限制**：语音识别功能有API调用限制
3. **内容类型**：自动识别视频笔记和图文笔记
4. **网络要求**：需要稳定的网络连接

## 🆘 常见问题

### Q: 为什么有些笔记无法解析？
A: 可能是链接格式不正确，或笔记已被删除/设为私密。

### Q: 图片链接无法访问？
A: 小红书图片链接可能有访问限制，建议尽快下载。

### Q: 语音识别失败？
A: 检查API密钥是否正确配置，以及视频是否包含有效音频。

## 📚 相关文档

- [抖音功能文档](./README.md)
- [部署指南](./DEPLOY.md)
- [配置说明](./README.md#配置要求)