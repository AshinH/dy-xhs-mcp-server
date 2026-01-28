# 项目架构说明

## 分层架构

本项目采用简单的分层架构，将代码按功能模块化组织：

```
douyin_mcp_server/
├── __init__.py          # 包初始化
├── __main__.py          # 入口点
├── server.py            # MCP服务器主入口，组装所有模块
│
├── config/              # 配置层
│   ├── __init__.py
│   └── settings.py      # 配置管理（加载配置文件、环境变量等）
│
├── utils/               # 工具层
│   ├── __init__.py
│   ├── http_client.py   # HTTP客户端工具
│   └── watermark.py     # 水印处理工具
│
├── services/            # 服务层（业务逻辑）
│   ├── __init__.py
│   ├── douyin_service.py      # 抖音服务
│   └── xiaohongshu_service.py # 小红书服务
│
├── tools/               # 工具层（MCP工具函数）
│   ├── __init__.py
│   ├── douyin_tools.py        # 抖音相关MCP工具
│   └── xiaohongshu_tools.py   # 小红书相关MCP工具
│
└── resources/           # 资源层（MCP资源处理）
    ├── __init__.py
    ├── douyin_resources.py      # 抖音相关MCP资源
    └── xiaohongshu_resources.py # 小红书相关MCP资源
```

## 各层职责

### 1. config 层 - 配置管理
- **职责**: 统一管理配置信息
- **功能**:
  - 加载配置文件（config.json）
  - 读取环境变量
  - 提供默认配置

### 2. utils 层 - 工具函数
- **职责**: 提供通用的工具函数
- **功能**:
  - HTTP请求封装（http_client.py）
  - 水印处理工具（watermark.py）

### 3. services 层 - 业务逻辑
- **职责**: 实现核心业务逻辑
- **功能**:
  - 抖音视频处理（douyin_service.py）
  - 小红书内容处理（xiaohongshu_service.py）

### 4. tools 层 - MCP工具函数
- **职责**: 封装MCP工具接口
- **功能**:
  - 调用services层的业务逻辑
  - 格式化返回结果
  - 处理MCP上下文

### 5. resources 层 - MCP资源处理
- **职责**: 处理MCP资源请求
- **功能**:
  - 提供资源访问接口
  - 调用services层获取数据

### 6. server.py - 主入口
- **职责**: 组装所有模块，启动MCP服务器
- **功能**:
  - 创建FastMCP实例
  - 注册所有工具和资源
  - 启动服务器

## 数据流向

```
MCP客户端请求
    ↓
server.py (注册的工具/资源)
    ↓
tools/ 或 resources/ (格式化请求)
    ↓
services/ (业务逻辑处理)
    ↓
utils/ (工具函数支持)
    ↓
config/ (配置信息)
    ↓
返回结果给MCP客户端
```

## 优势

1. **职责清晰**: 每层都有明确的职责，易于理解和维护
2. **易于扩展**: 新增功能只需在对应层添加代码
3. **代码复用**: 工具函数可在多个服务中复用
4. **测试友好**: 各层可独立测试
5. **维护简单**: 修改某个功能只需关注对应层的代码

## 扩展指南

### 添加新的平台支持（如B站）

1. 在 `services/` 创建 `bilibili_service.py`
2. 在 `tools/` 创建 `bilibili_tools.py`
3. 在 `resources/` 创建 `bilibili_resources.py`（如需要）
4. 在 `server.py` 中注册新的工具和资源

### 添加新的工具函数

1. 在对应的 `tools/` 文件中添加函数
2. 在 `server.py` 中使用 `@mcp.tool()` 装饰器注册

### 添加新的工具类

1. 在 `utils/` 中创建新的工具文件
2. 在需要的地方导入使用
