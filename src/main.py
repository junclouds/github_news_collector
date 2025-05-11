"""
主程序入口
协调数据获取、格式化和输出的整个流程
"""

import asyncio
import os
from datetime import datetime
from pathlib import Path

from loguru import logger

from src.fetcher.github_api import GitHubAPI
from src.formatter.markdown import MarkdownFormatter
from src.utils.config import config

class NewsCollector:
    def __init__(self):
        """初始化新闻收集器"""
        self.github_api = GitHubAPI()
        self.formatter = MarkdownFormatter()
        self.setup_logging()
        
    def setup_logging(self):
        """配置日志"""
        log_file = config.get('logging.file', 'data/logs/collector.log')
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        
        logger.add(
            log_file,
            rotation=config.get('logging.rotation', '1 day'),
            retention=config.get('logging.retention', '30 days'),
            level=config.get('logging.level', 'INFO')
        )
        
    async def collect_language_repos(self, language: str) -> str:
        """
        收集特定语言的仓库信息并生成报告
        
        Args:
            language: 编程语言
            
        Returns:
            str: 生成的报告内容
        """
        logger.info(f"开始收集 {language} 语言的热门仓库")
        
        repos = await self.github_api.search_trending_repos(
            language=language,
            days=config.get('fetch.time_range', 1),
            min_stars=config.get('fetch.min_stars', 100),
            per_page=config.get('fetch.max_repos_per_language', 10)
        )
        
        if not repos:
            logger.warning(f"未找到 {language} 语言的热门仓库")
            return ""
            
        return self.formatter.format_repos(repos, language)
        
    async def run(self):
        """运行收集器"""
        languages = config.get('fetch.languages', ['python'])
        output_dir = config.get('output.output_dir', 'data/daily')
        date_str = datetime.now().strftime('%Y-%m-%d')
        
        os.makedirs(output_dir, exist_ok=True)
        
        for language in languages:
            content = await self.collect_language_repos(language)
            if content:
                output_file = Path(output_dir) / f"{date_str}_{language}.md"
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                logger.info(f"已生成 {language} 语言的报告: {output_file}")
                
async def main():
    """主函数"""
    collector = NewsCollector()
    await collector.run()
    
if __name__ == "__main__":
    asyncio.run(main()) 