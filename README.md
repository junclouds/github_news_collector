# GitHub News Collector

GitHub News Collector 是一个自动收集 GitHub 热门项目并生成日报的工具。它可以帮助你追踪特定编程语言的最新热门项目。

## 功能特点

- 支持多种编程语言的项目收集
- 自定义项目筛选条件（最小星标数、时间范围等）
- 生成美观的 Markdown 格式报告
- 支持邮件和 Telegram 通知（可选）
- 完整的日志记录
- 灵活的配置系统

## 项目结构

```
github_news_collector/
├── config/             # 配置文件目录
│   └── config.yaml     # 主配置文件
├── src/                # 源代码目录
│   ├── fetcher/        # 数据获取模块
│   │   └── github_api.py   # GitHub API 封装
│   ├── formatter/      # 格式化模块
│   │   └── markdown.py     # Markdown 格式化器
│   ├── utils/          # 工具模块
│   │   └── config.py       # 配置加载器
│   └── main.py         # 主程序入口
├── data/               # 数据目录
│   ├── daily/          # 日报存储目录
│   └── logs/           # 日志文件目录
├── templates/          # 模板目录
├── .env                # 环境变量文件
├── .vscode/            # VSCode 配置
│   └── launch.json     # 调试配置
├── setup.py           # 包安装配置
└── README.md          # 项目文档
```

## 安装

1. 克隆仓库：
```bash
git clone https://github.com/junclouds/github_news_collector.git
cd github_news_collector
```

2. 安装依赖：
```bash
pip install -e .
```

3. 创建配置文件：
```bash
mkdir -p config data/logs data/daily templates
```

4. 配置 GitHub Token：

创建 `.env` 文件并添加你的 GitHub Token：
```bash
echo "GITHUB_TOKEN=your_github_token_here" > .env
```

你可以从 https://github.com/settings/tokens 获取一个新的 token。

## 配置

主要配置文件位于 `config/config.yaml`，包含以下配置项：

```yaml
# GitHub API配置
github:
  api_token: ${GITHUB_TOKEN}  # 从环境变量读取
  base_url: "https://api.github.com"
  rate_limit:
    max_retries: 3
    retry_interval: 60  # 秒
    
# 数据获取设置
fetch:
  languages:
    - python
  min_stars: 100
  time_range: "1d"  # 1d, 7d, 30d
  max_repos_per_language: 10
  
# 输出设置
output:
  format: "markdown"  # markdown, html, json
  template_dir: "templates"
  output_dir: "data/daily"
  
# 日志设置
logging:
  level: "INFO"
  file: "data/logs/collector.log"
  rotation: "1 day"
  retention: "30 days"
```

## 使用方法

运行收集器：
```bash
python -m src.main
```

程序会自动：
1. 收集配置的编程语言的热门仓库
2. 生成日报文件到 `data/daily` 目录
3. 如果配置了通知功能，发送通知

## 通知配置（可选）

### 邮件通知

在 `.env` 文件中添加：
```bash
EMAIL_SENDER=your_email@example.com
EMAIL_RECIPIENT=recipient@example.com
```

### Telegram 通知

在 `.env` 文件中添加：
```bash
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id
```

## 日志

- 日志文件位于：`data/logs/collector.log`
- 默认保留 30 天的日志记录
- 每天自动轮换日志文件

## 贡献

欢迎提交 Issue 和 Pull Request！

## 许可证

MIT License
