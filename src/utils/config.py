"""
配置加载模块
负责读取和解析YAML配置文件，支持环境变量替换
"""

import os
from pathlib import Path
from typing import Any, Dict

import yaml
from dotenv import load_dotenv

class ConfigLoader:
    def __init__(self, config_path: str = None):
        """
        初始化配置加载器
        
        Args:
            config_path: 配置文件路径，默认为 config/config.yaml
        """
        load_dotenv()  # 加载 .env 文件中的环境变量
        self.config_path = config_path or str(Path(__file__).parent.parent.parent / "config" / "config.yaml")
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """
        加载并解析配置文件
        
        Returns:
            Dict[str, Any]: 配置字典
        """
        if not os.path.exists(self.config_path):
            raise FileNotFoundError(f"配置文件不存在: {self.config_path}")
            
        with open(self.config_path, 'r', encoding='utf-8') as f:
            # 读取YAML并替换环境变量
            config = yaml.safe_load(os.path.expandvars(f.read()))
            
        return config
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        获取配置项
        
        Args:
            key: 配置键名，支持点号分隔的嵌套键
            default: 默认值
            
        Returns:
            Any: 配置值
        """
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k, default)
            else:
                return default
                
        return value

config = ConfigLoader()  # 全局配置实例 