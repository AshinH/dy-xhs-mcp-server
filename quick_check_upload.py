#!/usr/bin/env python3
"""
快速检查PyPI上传状态的Python脚本
"""

import requests
import json
import sys

PACKAGE_NAME = "douyin-mcp-server"

def check_pypi(package_name, test=False):
    """检查PyPI包是否存在"""
    base_url = "https://test.pypi.org" if test else "https://pypi.org"
    url = f"{base_url}/pypi/{package_name}/json"
    env_name = "测试环境 (TestPyPI)" if test else "正式环境 (PyPI)"
    
    print(f"\n🔍 检查{env_name}...")
    print(f"   访问地址: {url}")
    
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 上传成功！")
            print(f"📦 包名: {data['info']['name']}")
            print(f"📝 描述: {data['info']['summary']}")
            print(f"📌 最新版本: {data['info']['version']}")
            print(f"🔗 访问地址: {base_url}/project/{package_name}/")
            
            # 显示所有版本
            versions = list(data['releases'].keys())
            if len(versions) > 0:
                print(f"\n📋 所有版本 ({len(versions)}个):")
                for version in sorted(versions, reverse=True):
                    print(f"   - {version}")
            
            return True
        elif response.status_code == 404:
            print(f"❌ 包不存在 (404)")
            print(f"   可能原因：")
            print(f"   - 还未上传到{env_name}")
            print(f"   - 包名错误")
            print(f"   - 需要等待几分钟同步")
            return False
        else:
            print(f"❌ 检查失败 (状态码: {response.status_code})")
            return False
    except requests.exceptions.Timeout:
        print(f"❌ 请求超时，请检查网络连接")
        return False
    except Exception as e:
        print(f"❌ 检查失败: {e}")
        return False

def main():
    print("=" * 60)
    print("🔍 PyPI上传状态检查工具")
    print("=" * 60)
    
    # 检查测试环境
    test_success = check_pypi(PACKAGE_NAME, test=True)
    
    print("\n" + "-" * 60)
    
    # 检查正式环境
    pypi_success = check_pypi(PACKAGE_NAME, test=False)
    
    print("\n" + "=" * 60)
    print("📊 检查总结")
    print("=" * 60)
    print(f"测试环境: {'✅ 已上传' if test_success else '❌ 未找到'}")
    print(f"正式环境: {'✅ 已上传' if pypi_success else '❌ 未找到'}")
    
    if pypi_success:
        print("\n💡 提示：")
        print("   - 正式环境已有包，可以直接使用uvx部署")
        print("   - 配置: uvx douyin-mcp-server")
    
    if not test_success and not pypi_success:
        print("\n⚠️  建议：")
        print("   1. 检查上传命令是否正确")
        print("   2. 等待几分钟后重新检查（PyPI需要时间同步）")
        print("   3. 确认包名是否正确")

if __name__ == "__main__":
    main()