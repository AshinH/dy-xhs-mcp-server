#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
import re
import json

print('🔍 深度分析小红书文案内容')
print('=' * 60)

test_link = 'http://xhslink.com/o/5Xbdx1j7ab0'

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) EdgiOS/121.0.2277.107 Version/17.0 Mobile/15E148 Safari/604.1'
}

try:
    # 访问链接
    response = requests.get(test_link, headers=HEADERS, allow_redirects=True, timeout=15)
    final_url = response.url
    html_content = response.text
    
    print(f'📎 最终URL: {final_url}')
    print()
    
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # 查找所有script标签，搜索文案内容
    script_tags = soup.find_all('script')
    print(f'📜 分析 {len(script_tags)} 个script标签...')
    print()
    
    found_desc = False
    all_descs = []
    all_titles = []
    
    for i, script in enumerate(script_tags):
        script_text = script.string
        if script_text and ('desc' in script_text.lower() or 'content' in script_text.lower() or 'text' in script_text.lower()):
            # 尝试提取desc字段 - 多种格式
            # 格式1: "desc": "内容"
            desc_matches1 = re.findall(r'"desc"\s*:\s*"([^"]+)"', script_text)
            # 格式2: desc: "内容"
            desc_matches2 = re.findall(r'desc\s*:\s*"([^"]+)"', script_text)
            # 格式3: 处理转义字符
            desc_matches3 = re.findall(r'"desc"\s*:\s*"((?:[^"\\\\]|\\\\.)+)"', script_text)
            
            all_matches = desc_matches1 + desc_matches2 + desc_matches3
            if all_matches:
                print(f'📝 Script {i+1} 中找到desc字段:')
                for desc in all_matches[:5]:  # 显示前5个
                    # 处理转义字符
                    desc = desc.replace('\\n', '\n').replace('\\t', '\t').replace('\\"', '"').replace('\\\\', '\\')
                    if len(desc) > 20:  # 只显示有意义的描述
                        print(f'   {desc[:300]}...' if len(desc) > 300 else f'   {desc}')
                        all_descs.append(desc)
                        found_desc = True
                print()
            
            # 尝试提取title字段
            title_matches = re.findall(r'"title"\s*:\s*"([^"]+)"', script_text)
            if title_matches:
                for title in title_matches[:3]:
                    title = title.replace('\\n', '\n').replace('\\t', '\t').replace('\\"', '"')
                    if len(title) > 5 and title not in all_titles:
                        all_titles.append(title)
    
    # 显示找到的内容
    if all_descs:
        print('📄 找到的文案内容:')
        print('=' * 60)
        # 选择最长的描述（通常是最完整的）
        longest_desc = max(all_descs, key=len)
        print(longest_desc)
        print('=' * 60)
        print()
    
    if all_titles:
        print('📝 找到的标题:')
        for title in all_titles:
            print(f'   - {title}')
        print()
    
    if not found_desc:
        print('⚠️  未在script标签中找到明显的文案内容')
        print('💡 可能原因:')
        print('   1. 文案通过JavaScript动态加载')
        print('   2. 文案在加密的JSON中')
        print('   3. 文案在图片中，需要使用OCR')
    
    # 检查meta标签
    print()
    print('📋 Meta标签信息:')
    og_desc = soup.find('meta', property='og:description')
    if og_desc:
        desc = og_desc.get('content', '')
        if desc and len(desc) > 10:
            print(f'   og:description: {desc[:200]}...')
        else:
            print(f'   og:description: {desc}')
    else:
        print('   og:description: 未找到')
    
    # 尝试从JSON中提取
    print()
    print('🔍 尝试从JSON数据中提取:')
    for script in script_tags:
        script_text = script.string
        if script_text and ('note' in script_text.lower() or 'item' in script_text.lower()):
            try:
                # 查找可能的JSON对象
                json_matches = re.findall(r'\{[^{}]*"desc"[^{}]*\}', script_text)
                for match in json_matches[:3]:
                    try:
                        data = json.loads(match)
                        if 'desc' in data:
                            desc = data['desc']
                            if len(desc) > 20:
                                print(f'   找到描述: {desc[:200]}...')
                    except:
                        pass
            except:
                pass
    
except Exception as e:
    print(f'❌ 分析失败: {e}')
    import traceback
    traceback.print_exc()