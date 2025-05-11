# GitHub News Collector

GitHub News Collector 是一个自动收集 GitHub 热门项目并生成日报的工具。它可以帮助你追踪特定编程语言的最新热门项目。现在新增了 Chrome 扩展支持，可以实时接收项目更新通知。

## 功能特点

- 支持多种编程语言的项目收集
- 自定义项目筛选条件（最小星标数、时间范围等）
- 生成美观的 Markdown 格式报告
- 支持邮件和 Telegram 通知（可选）
- 完整的日志记录
- 灵活的配置系统
- 🆕 Chrome 扩展实时通知功能
  - 定时检查项目更新（可配置为每周五早上10点）
  - 桌面通知提醒
  - 一键查看详细信息
  - 美观的 Web 界面展示

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
├── chrome_extension/   # Chrome 扩展目录
│   ├── manifest.json   # 扩展配置文件
│   ├── background.js   # 后台脚本
│   ├── popup.html     # 弹出页面
│   ├── popup.js       # 弹出页面脚本
│   └── icon.png       # 扩展图标
├── api_server.py      # API 服务器
├── .env               # 环境变量文件
├── setup.py           # 包安装配置
└── README.md          # 项目文档
```

## 安装

### 1. API 服务器

1. 克隆仓库：
```bash
git clone https://github.com/junclouds/github_news_collector.git
cd github_news_collector
```

2. 安装依赖：
```bash
pip install -r requirements.txt
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

### 2. Chrome 扩展

1. 打开 Chrome 浏览器，进入扩展管理页面 (`chrome://extensions/`)
2. 开启"开发者模式"（右上角开关）
3. 点击"加载已解压的扩展程序"
4. 选择项目中的 `chrome_extension` 目录

## 配置

### API 服务器配置

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

### Chrome 扩展配置

在 `chrome_extension/background.js` 中可以配置：
- 更新检查时间（默认每周五早上10点）
- 通知显示样式
- API 服务器地址

## 使用方法

### API 服务器

1. 启动服务器：
```bash
python api_server.py
```

2. 访问接口：
- 获取最新更新：`GET http://127.0.0.1:5000/latest-update`
- 查看特定文件：`GET http://127.0.0.1:5000/view-markdown?filename=YYYY-MM-DD_python.md`
- 列出所有文件：`GET http://127.0.0.1:5000/list-markdown-files`

### Chrome 扩展

1. 安装扩展后，会在浏览器右上角显示图标
2. 点击图标可以手动检查更新
3. 扩展会自动在设定的时间检查更新
4. 收到通知后，可以：
   - 点击通知直接查看详情
   - 点击"查看详情"按钮在新标签页中打开

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
