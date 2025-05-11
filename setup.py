from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="github_news_collector",
    version="0.1.0",
    author="junclouds",
    author_email="junclouds@example.com",
    description="GitHub项目更新通知系统，包含Flask API服务器和Chrome扩展",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/junclouds/github_news_collector",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=[
        "flask>=2.0.0",
        "flask-cors>=3.0.0",
        "requests>=2.25.0",
        "markdown>=3.3.0",
        "loguru>=0.5.0",
        "python-dotenv>=0.19.0",
        "pyyaml>=6.0.0",      # 用于解析 YAML 配置文件
        "jinja2>=3.0.0",      # 用于模板渲染
        "aiohttp>=3.8.0",     # 用于异步 HTTP 请求
    ],
    entry_points={
        "console_scripts": [
            "github-news-collector=src.main:main",
            "github-news-server=api_server:app.run",
        ],
    },
    include_package_data=True,
    package_data={
        "": [
            "templates/*.html",
            "chrome_extension/*",
            "config/*.yaml",
        ],
    },
    data_files=[
        ('config', ['config/config.yaml']),
        ('chrome_extension', [
            'chrome_extension/manifest.json',
            'chrome_extension/background.js',
            'chrome_extension/popup.html',
            'chrome_extension/popup.js',
            'chrome_extension/icon.png',
        ]),
    ],
) 