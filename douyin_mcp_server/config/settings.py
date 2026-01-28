"""配置管理"""

import os
import json
from pathlib import Path
from typing import Dict, Any

# 默认 API 配置
DEFAULT_MODEL = "paraformer-v2"

# 配置文件路径
CONFIG_FILE = Path(__file__).parent.parent.parent / "config.json"


def load_config() -> Dict[str, Any]:
    """加载配置文件"""
    try:
        if CONFIG_FILE.exists():
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            # 如果配置文件不存在，尝试从环境变量读取
            api_key = os.getenv('DASHSCOPE_API_KEY')
            if api_key:
                return {
                    "api_key": api_key,
                    "model": DEFAULT_MODEL,
                    "language_hints": ["zh", "en"],
                    "temp_dir": "temp"
                }
            else:
                raise FileNotFoundError("未找到配置文件 config.json，且未设置环境变量 DASHSCOPE_API_KEY")
    except Exception as e:
        raise Exception(f"加载配置文件失败: {e}")


# 加载配置
try:
    CONFIG = load_config()
except Exception as e:
    print(f"配置加载失败: {e}")
    CONFIG = {
        "api_key": os.getenv('DASHSCOPE_API_KEY', ''),
        "model": DEFAULT_MODEL,
        "language_hints": ["zh", "en"],
        "temp_dir": "temp"
    }
