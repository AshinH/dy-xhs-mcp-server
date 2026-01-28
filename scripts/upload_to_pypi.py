#!/usr/bin/env python3
"""
上传douyin-mcp-server到PyPI的脚本
"""

import os
import sys
import subprocess
from pathlib import Path

def check_build_files():
    """检查构建产物"""
    dist_dir = Path("dist")
    if not dist_dir.exists():
        print("❌ dist目录不存在，需要先构建")
        return False
    
    files = list(dist_dir.glob("douyin_mcp_server-1.3.0*"))
    if not files:
        print("❌ 未找到1.3.0版本的构建产物")
        return False
    
    print("✅ 找到构建产物:")
    for f in files:
        print(f"   {f.name} ({f.stat().st_size / 1024:.1f} KB)")
    return True

def get_pypi_token():
    """获取PyPI Token"""
    # 先检查环境变量
    if os.getenv("TWINE_PASSWORD") and os.getenv("TWINE_PASSWORD").startswith("pypi-"):
        print("✅ 找到环境变量中的Token")
        return os.getenv("TWINE_PASSWORD")
    
    # 检查配置文件
    pypirc = Path.home() / ".pypirc"
    if pypirc.exists():
        print("✅ 找到 ~/.pypirc 配置文件")
        # 简单解析（实际应该用configparser）
        content = pypirc.read_text()
        if "password" in content:
            print("   将使用配置文件中的凭证")
            return None  # 使用配置文件
    
    # 提示输入
    print()
    print("📝 需要PyPI Token才能上传")
    print()
    print("💡 获取Token步骤：")
    print("   1. 访问 https://pypi.org/manage/account/token/")
    print("   2. 创建新的API Token（如果还没有）")
    print("   3. 复制token（格式：pypi-xxxxx）")
    print()
    
    token = input("请输入PyPI Token: ").strip()
    
    if not token:
        print("❌ Token不能为空")
        return None
    
    if not token.startswith("pypi-"):
        print("⚠️  警告: Token通常以 'pypi-' 开头")
        confirm = input("是否继续？(y/n): ").strip().lower()
        if confirm != 'y':
            return None
    
    return token

def upload_to_pypi(token=None):
    """上传到PyPI"""
    # 设置环境变量
    if token:
        os.environ["TWINE_USERNAME"] = "__token__"
        os.environ["TWINE_PASSWORD"] = token
    
    print()
    print("📤 开始上传到PyPI...")
    print()
    
    try:
        # 运行twine upload
        result = subprocess.run(
            [sys.executable, "-m", "twine", "upload", "dist/*"],
            check=True,
            capture_output=True,
            text=True
        )
        
        print(result.stdout)
        print()
        print("✅ 上传成功！")
        return True
        
    except subprocess.CalledProcessError as e:
        print("❌ 上传失败:")
        print(e.stdout)
        print(e.stderr)
        return False

def main():
    print("🚀 上传douyin-mcp-server 1.3.0到PyPI")
    print("=" * 60)
    print()
    
    # 检查构建产物
    if not check_build_files():
        print()
        print("💡 运行以下命令构建:")
        print("   python3.11 -m build")
        return 1
    
    print()
    
    # 获取Token
    token = get_pypi_token()
    if token is None and not os.getenv("TWINE_PASSWORD"):
        print("❌ 无法获取凭证，取消上传")
        return 1
    
    # 确认上传
    print()
    confirm = input("确认上传到PyPI？(y/n): ").strip().lower()
    if confirm != 'y':
        print("已取消")
        return 0
    
    # 上传
    if upload_to_pypi(token):
        print()
        print("📋 下一步：")
        print("1. 等待1-2分钟让PyPI更新")
        print("2. 验证上传:")
        print("   curl https://pypi.org/pypi/douyin-mcp-server/json | grep version")
        print("3. 在阿里云MCP管理界面重新部署")
        print("4. 使用配置: {\"args\": [\"douyin-mcp-server\"]}")
        print()
        print("🎉 部署后应该能看到小红书方法了！")
        return 0
    else:
        return 1

if __name__ == "__main__":
    sys.exit(main())