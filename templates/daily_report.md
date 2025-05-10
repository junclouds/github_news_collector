# GitHub {{ language }} 热门项目速报 ({{ date }})

🎉 今日共收集到 {{ total }} 个热门项目。

{% for repo in repos %}
## [{{ repo.full_name }}]({{ repo.html_url }})

{{ repo.description or "暂无描述" }}

- ⭐ Stars: {{ repo.stargazers_count }}
- 📦 Language: {{ repo.language }}
- 🔄 Updated: {{ repo.updated_at.split('T')[0] }}

{% if repo.topics %}
**标签**: {% for topic in repo.topics %}#{{ topic }} {% endfor %}
{% endif %}

---
{% endfor %}

> 数据来源: GitHub API
> 生成时间: {{ date }} 