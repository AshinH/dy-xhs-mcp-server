# 项目目录结构说明

## 📁 目录组织

项目文件已按类型归类到以下目录：

### 📄 `docs/` - 文档目录
存放所有项目文档（Markdown文件）：
- `ARCHITECTURE.md` - 架构说明文档
- `DEPLOY.md` - 部署文档
- `DEPLOY_COMPARISON.md` - 部署方式对比
- `DEPLOY_STEPS.md` - 部署步骤
- `FEATURES_SUMMARY.md` - 功能总结
- `QUICK_DEPLOY.md` - 快速部署指南
- `README_DEPLOY.md` - 部署README
- `TROUBLESHOOTING.md` - 故障排查
- `UPLOAD_INSTRUCTIONS.md` - 上传说明
- `UPLOAD_PERMISSION_FIX.md` - 上传权限修复
- `UPLOAD_TO_PYPI.md` - PyPI上传指南
- `VERIFY_UPLOAD.md` - 验证上传
- `WATERMARK_REMOVAL.md` - 水印移除说明
- `XIAOHONGSHU_FEATURES.md` - 小红书功能说明

### ⚙️ `configs/` - 配置目录
存放所有配置文件（JSON文件）：
- `ALIYUN_DEPLOY_CONFIG.json` - 阿里云部署配置
- `ALTERNATIVE_CONFIGS.json` - 替代配置
- `NEW_DEPLOY_CONFIG.json` - 新部署配置
- `deploy_aliyun_mcp.json` - 阿里云MCP部署配置
- `deploy_aliyun_mcp_v1.3.0.json` - v1.3.0版本部署配置

**注意：** `config.json` 保留在项目根目录，因为它是运行时必需的配置文件。

### 🔧 `scripts/` - 脚本目录
存放所有可执行脚本（Python和Shell脚本）：

**Python脚本：**
- `analyze_xhs_text.py` - 小红书文本分析
- `demo_ai_watermark_removal.py` - AI水印移除演示
- `download_vibe_coding_video.py` - Vibe Coding视频下载
- `download_video.py` - 视频下载工具
- `download_xhs_video.py` - 小红书视频下载
- `download_xhs_videos.py` - 批量下载小红书视频
- `quick_check_upload.py` - 快速检查上传
- `upload_to_pypi.py` - PyPI上传脚本
- `test_*.py` - 各种测试脚本

**Shell脚本：**
- `build_and_deploy.sh` - 构建和部署脚本
- `check_pypi_upload.sh` - 检查PyPI上传
- `quick_upload.sh` - 快速上传脚本
- `start_server.sh` - 启动服务器脚本
- `upload_with_auth.sh` - 带认证的上传脚本

### 📦 `douyin_mcp_server/` - 源代码目录
项目的主要源代码目录，采用分层架构：
- `config/` - 配置层
- `utils/` - 工具层
- `services/` - 服务层
- `tools/` - MCP工具层
- `resources/` - MCP资源层
- `server.py` - 主入口文件

## 📝 根目录文件

以下文件保留在根目录：
- `README.md` - 项目主文档
- `LICENSE` - 许可证文件
- `pyproject.toml` - Python项目配置
- `config.json` - 运行时配置文件（必需）
- `.gitignore` - Git忽略文件配置

## 🚀 使用说明

### 运行脚本
```bash
# 运行Python脚本
python scripts/start_server.sh

# 运行Shell脚本
bash scripts/build_and_deploy.sh
```

### 查看文档
```bash
# 查看架构文档
cat docs/ARCHITECTURE.md

# 查看部署文档
cat docs/DEPLOY.md
```

### 使用配置
```bash
# 配置文件在configs目录
# 运行时配置文件config.json在根目录
```
