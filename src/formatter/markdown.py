"""
Markdown格式化模块
将GitHub仓库数据转换为Markdown格式的快讯
"""

from datetime import datetime
from typing import Dict, List

from jinja2 import Environment, FileSystemLoader
from loguru import logger

from ..utils.config import config

class MarkdownFormatter:
    def __init__(self):
        """初始化Markdown格式化器"""
        template_dir = config.get('output.template_dir', 'templates')
        self.env = Environment(
            loader=FileSystemLoader(template_dir),
            trim_blocks=True,
            lstrip_blocks=True
        )
        
    def format_repos(self, repos: List[Dict], language: str) -> str:
        """
        格式化仓库列表为Markdown文本
        
        Args:
            repos: 仓库信息列表
            language: 编程语言
            
        Returns:
            str: Markdown格式的文本
        """
        try:
            template = self.env.get_template('daily_report.md')
            return template.render(
                repos=repos,
                language=language,
                date=datetime.now().strftime('%Y-%m-%d'),
                total=len(repos)
            )
        except Exception as e:
            logger.error(f"格式化Markdown失败: {str(e)}")
            # 降级使用基础模板
            return self._format_basic_markdown(repos, language)
            
    def _format_basic_markdown(self, repos: List[Dict], language: str) -> str:
        """
        使用基础模板格式化（作为备选方案）
        
        Args:
            repos: 仓库信息列表
            language: 编程语言
            
        Returns:
            str: Markdown格式的文本
        """
        lines = [
            f"# GitHub {language} 热门项目速报 ({datetime.now().strftime('%Y-%m-%d')})\n",
            f"今日共收集到 {len(repos)} 个热门项目。\n",
            "## 项目列表\n"
        ]
        
        for repo in repos:
            lines.extend([
                f"### [{repo['full_name']}]({repo['html_url']})\n",
                f"⭐ Stars: {repo['stargazers_count']}\n",
                f"{repo.get('description', '暂无描述')}\n",
            ])
            
        return '\n'.join(lines) 