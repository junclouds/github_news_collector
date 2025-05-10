# GitHub News Collector

一个用于自动收集GitHub热门项目并生成每日快讯的工具。

## 功能特点

- 支持多种编程语言的热门项目收集
- 自动处理GitHub API速率限制
- 可配置的项目筛选条件（星标数、时间范围等）
- Markdown格式输出，支持自定义模板
- 完善的日志记录
- 模块化设计，易于扩展

## 项目结构

```
github_news_collector/
├── config/             # 配置文件目录
│   └── config.yaml     # 主配置文件
├── src/                # 源代码目录
│   ├── fetcher/        # 数据获取模块
│   ├── formatter/      # 格式化模块
│   ├── utils/          # 工具模块
│   ├── handlers/       # 错误处理模块
│   └── main.py         # 主程序入口
├── data/               # 数据目录
│   ├── daily/          # 每日快讯存储
│   └── logs/           # 日志文件
├── templates/          # 模板目录
├── examples/           # 示例代码
├── notebooks/          # Jupyter notebooks
├── requirements.txt    # 项目依赖
└── README.md           # 项目文档
```

## 安装步骤

1. 克隆项目：

```bash
git clone https://github.com/junclouds/github_news_collector.git
cd github_news_collector
```

2. 创建虚拟环境（推荐）：

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows
```

3. 安装依赖：

```bash
pip install -r requirements.txt
```

4. 配置GitHub Token：

在项目根目录创建 `.env` 文件：

```env
GITHUB_TOKEN=your_github_token_here
```

## 使用说明

1. 修改配置文件 `config/config.yaml`：
   - 设置要收集的编程语言
   - 调整筛选条件
   - 配置输出格式和路径

2. 运行收集器：

```bash
# 收集今天的数据
python src/main.py

# 或使用示例脚本收集昨天的数据
python examples/collect_yesterday.py
```

3. 查看输出：
   - 快讯文件保存在 `data/daily/` 目录
   - 日志文件保存在 `data/logs/` 目录

## 自定义模板

你可以通过修改 `templates/daily_report.md` 文件来自定义快讯的格式。模板使用Jinja2语法，支持以下变量：

- `repos`: 仓库列表
- `language`: 编程语言
- `date`: 日期
- `total`: 仓库总数

## 扩展功能

项目设计支持通过插件方式扩展功能：

1. 在 `config.yaml` 中启用所需插件
2. 实现对应的处理器类
3. 在主程序中注册插件

## 常见问题

1. API速率限制：
   - 使用个人访问令牌可提高限制
   - 程序会自动处理限制并等待

2. 数据获取失败：
   - 检查网络连接
   - 确认GitHub Token是否有效
   - 查看日志文件了解详细错误信息

## 贡献指南

欢迎提交Issue和Pull Request！在提交代码前，请确保：

- 遵循项目的代码风格（PEP8）
- 添加必要的测试用例
- 更新相关文档

## 许可证

MIT License
