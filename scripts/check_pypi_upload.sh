#!/bin/bash

# 检查PyPI上传状态的脚本

PACKAGE_NAME="douyin-mcp-server"
TEST_PYPI_URL="https://test.pypi.org/project/${PACKAGE_NAME}/"
PYPI_URL="https://pypi.org/project/${PACKAGE_NAME}/"

echo "🔍 检查PyPI上传状态"
echo "=" | head -c 50 && echo ""

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo ""
echo "1️⃣ 检查测试环境 (TestPyPI)"
echo "----------------------------------------"

# 检查测试环境
if curl -s "${TEST_PYPI_URL}" > /dev/null 2>&1; then
    echo -e "${GREEN}✅ 测试环境可访问${NC}"
    echo "   访问地址: ${TEST_PYPI_URL}"
    
    # 尝试获取JSON信息
    TEST_JSON=$(curl -s "https://test.pypi.org/pypi/${PACKAGE_NAME}/json" 2>/dev/null)
    if [ ! -z "$TEST_JSON" ]; then
        VERSION=$(echo "$TEST_JSON" | grep -o '"version":"[^"]*"' | head -1 | cut -d'"' -f4)
        if [ ! -z "$VERSION" ]; then
            echo -e "${GREEN}✅ 找到版本: ${VERSION}${NC}"
        else
            echo -e "${YELLOW}⚠️  无法获取版本信息${NC}"
        fi
    else
        echo -e "${YELLOW}⚠️  无法获取包信息${NC}"
    fi
else
    echo -e "${RED}❌ 测试环境不可访问或包不存在${NC}"
    echo "   可能原因："
    echo "   - 包还未上传"
    echo "   - 网络问题"
    echo "   - 包名错误"
fi

echo ""
echo "2️⃣ 检查正式环境 (PyPI)"
echo "----------------------------------------"

# 检查正式环境
if curl -s "${PYPI_URL}" > /dev/null 2>&1; then
    echo -e "${GREEN}✅ 正式环境可访问${NC}"
    echo "   访问地址: ${PYPI_URL}"
    
    # 尝试获取JSON信息
    PYPI_JSON=$(curl -s "https://pypi.org/pypi/${PACKAGE_NAME}/json" 2>/dev/null)
    if [ ! -z "$PYPI_JSON" ]; then
        VERSION=$(echo "$PYPI_JSON" | grep -o '"version":"[^"]*"' | head -1 | cut -d'"' -f4)
        if [ ! -z "$VERSION" ]; then
            echo -e "${GREEN}✅ 找到版本: ${VERSION}${NC}"
            
            # 获取所有版本
            echo ""
            echo "📦 可用版本列表:"
            echo "$PYPI_JSON" | grep -o '"version":"[^"]*"' | cut -d'"' -f4 | sort -V
        else
            echo -e "${YELLOW}⚠️  无法获取版本信息${NC}"
        fi
    else
        echo -e "${YELLOW}⚠️  无法获取包信息${NC}"
    fi
else
    echo -e "${RED}❌ 正式环境不可访问或包不存在${NC}"
fi

echo ""
echo "3️⃣ 测试安装（测试环境）"
echo "----------------------------------------"
echo "尝试从TestPyPI安装..."
echo ""
echo "命令: pip install --index-url https://test.pypi.org/simple/ ${PACKAGE_NAME}"
echo ""
read -p "是否现在测试安装？(y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ ${PACKAGE_NAME}
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ 安装成功！${NC}"
    else
        echo -e "${RED}❌ 安装失败${NC}"
    fi
fi

echo ""
echo "4️⃣ 使用uvx测试（如果已发布到正式环境）"
echo "----------------------------------------"
echo "命令: uvx ${PACKAGE_NAME}"
echo ""
read -p "是否现在测试uvx？(y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    uvx ${PACKAGE_NAME} --help 2>&1 | head -10
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ uvx测试成功！${NC}"
    else
        echo -e "${YELLOW}⚠️  uvx测试失败（可能需要先发布到正式环境）${NC}"
    fi
fi

echo ""
echo "📋 快速检查命令"
echo "----------------------------------------"
echo "1. 浏览器访问测试环境:"
echo "   ${TEST_PYPI_URL}"
echo ""
echo "2. 浏览器访问正式环境:"
echo "   ${PYPI_URL}"
echo ""
echo "3. 命令行检查:"
echo "   curl https://test.pypi.org/pypi/${PACKAGE_NAME}/json"
echo "   curl https://pypi.org/pypi/${PACKAGE_NAME}/json"
echo ""
echo "4. 测试安装:"
echo "   pip install --index-url https://test.pypi.org/simple/ ${PACKAGE_NAME}"
echo ""