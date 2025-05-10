"""
示例脚本：收集昨天的GitHub热门项目
"""

import asyncio
import os
import sys
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from src.main import NewsCollector
from src.utils.config import config

async def collect_yesterday():
    """收集昨天的热门项目"""
    # 修改配置以收集昨天的数据
    config.config['fetch']['time_range'] = '1d'
    
    # 确保必要的目录存在
    os.makedirs(project_root / 'data' / 'daily', exist_ok=True)
    os.makedirs(project_root / 'data' / 'logs', exist_ok=True)
    
    # 运行收集器
    collector = NewsCollector()
    await collector.run()
    
if __name__ == "__main__":
    asyncio.run(collect_yesterday()) 