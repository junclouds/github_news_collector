"""
GitHub API请求模块
处理与GitHub API的所有交互，包括速率限制处理和自动重试
"""

import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional

import aiohttp
import backoff
from loguru import logger

from ..utils.config import config

class GitHubAPI:
    def __init__(self):
        """初始化GitHub API客户端"""
        self.base_url = config.get('github.base_url')
        self.token = config.get('github.api_token')
        self.headers = {
            'Authorization': f'token {self.token}',
            'Accept': 'application/vnd.github.v3+json',
        }
        
    @backoff.on_exception(
        backoff.expo,
        (aiohttp.ClientError, aiohttp.ClientResponseError),
        max_tries=config.get('github.rate_limit.max_retries', 3)
    )
    async def _make_request(self, endpoint: str, params: Optional[Dict] = None) -> Dict:
        """
        发送API请求并处理响应
        
        Args:
            endpoint: API端点
            params: 查询参数
            
        Returns:
            Dict: API响应数据
        """
        async with aiohttp.ClientSession() as session:
            url = f"{self.base_url}/{endpoint.lstrip('/')}"
            async with session.get(url, headers=self.headers, params=params) as response:
                if response.status == 403:  # 速率限制
                    reset_time = int(response.headers.get('X-RateLimit-Reset', 0))
                    wait_time = max(reset_time - time.time(), 0)
                    logger.warning(f"达到API速率限制，等待 {wait_time} 秒")
                    time.sleep(wait_time)
                    return await self._make_request(endpoint, params)
                    
                response.raise_for_status()
                return await response.json()
                
    async def search_trending_repos(
        self,
        language: str,
        days: int = 1,
        min_stars: int = 100,
        per_page: int = 10
    ) -> List[Dict]:
        """
        搜索热门仓库
        
        Args:
            language: 编程语言
            days: 时间范围（天）
            min_stars: 最小星标数
            per_page: 每页结果数
            
        Returns:
            List[Dict]: 仓库信息列表
        """
        date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
        query = f"language:{language} created:>={date} stars:>=1"
        
        params = {
            'q': query,
            'sort': 'stars',
            'order': 'desc',
            'per_page': per_page,
        }
        
        try:
            result = await self._make_request('search/repositories', params)
            return result.get('items', [])
        except Exception as e:
            logger.error(f"搜索仓库失败: {str(e)}")
            return []
            
    async def get_repo_details(self, owner: str, repo: str) -> Dict:
        """
        获取仓库详细信息
        
        Args:
            owner: 仓库所有者
            repo: 仓库名称
            
        Returns:
            Dict: 仓库详细信息
        """
        try:
            return await self._make_request(f'repos/{owner}/{repo}')
        except Exception as e:
            logger.error(f"获取仓库详情失败: {str(e)}")
            return {} 