from setuptools import setup, find_packages

setup(
    name="github_news_collector",
    version="0.1.0",
    description="一个自动收集 GitHub 热门项目并生成日报的工具",
    author="junclouds",
    author_email="your.email@example.com",
    url="https://github.com/junclouds/github_news_collector",
    packages=find_packages(),
    install_requires=[
        "loguru",      # 用于日志记录
        "pyyaml",      # 用于解析 YAML 配置文件
        "python-dotenv", # 用于加载 .env 环境变量
        "aiohttp",     # 用于异步 HTTP 请求
        "jinja2",      # 用于模板渲染
    ],
    python_requires=">=3.7",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
) 