"""
Flask API 服务
提供简单的 API 接口获取最新的 GitHub 热门项目信息
"""

import os
import subprocess
from datetime import datetime
from flask import Flask, Response, request, render_template, abort, jsonify
import logging
import markdown
import re

app = Flask(__name__)

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_latest_file_path():
    """
    调用main.py生成最新的文件并返回文件路径
    """
    try:
        # 获取当前脚本所在目录
        current_dir = os.path.dirname(os.path.abspath(__file__))
        main_script_path = os.path.join(current_dir, 'src', 'main.py')
        
        logger.info(f"尝试执行脚本: {main_script_path}")
        
        # 调用main.py生成新的数据文件，使用-m选项来执行模块
        subprocess.run([
            'python',
            '-m',
            'src.main'
        ], check=True, cwd=current_dir)
        
        # 获取今天的日期
        today = datetime.now()
        file_path = os.path.join(current_dir, "data/daily", f"{today.strftime('%Y-%m-%d')}_python.md")
        
        logger.info(f"生成的文件路径: {file_path}")
        return file_path, f"{today.strftime('%Y-%m-%d')}_python.md"
    except subprocess.CalledProcessError as e:
        logger.error(f"生成数据文件时出错: {e}")
        # 如果生成失败，返回最新的已存在的文件
        data_dir = os.path.join(current_dir, "data/daily")
        if os.path.exists(data_dir):
            files = sorted([f for f in os.listdir(data_dir) if f.endswith('_python.md')], reverse=True)
            if files:
                return os.path.join(data_dir, files[0]), files[0]
        return None, None

@app.route('/latest-update', methods=['GET', 'OPTIONS'])
def latest_update():
    """
    返回最新的项目更新
    """
    # 处理 OPTIONS 请求（预检请求）
    if request.method == 'OPTIONS':
        return build_cors_preflight_response()
    
    # 处理 GET 请求
    try:
        # 强制生成新的报告
        file_path, filename = get_latest_file_path()
        
        if not file_path or not os.path.exists(file_path):
            logger.error("无法生成或找到报告文件")
            return build_cors_actual_response(jsonify({
                "error": "无法生成报告文件",
                "status": 500
            }))
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 返回文件内容和查看链接
        response_data = {
            "content": content,
            "view_url": f"http://127.0.0.1:5000/view-markdown?filename={filename}",
            "generated_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
            
        return build_cors_actual_response(jsonify(response_data))
    except Exception as e:
        logger.error(f"生成报告时发生错误: {str(e)}")
        return build_cors_actual_response(jsonify({
            "error": f"生成报告时发生错误: {str(e)}",
            "status": 500
        }))

@app.route('/view-markdown', methods=['GET'])
def view_markdown():
    """
    获取指定Markdown文件并渲染为HTML
    参数: filename - Markdown文件名
    """
    filename = request.args.get('filename')
    if not filename:
        return Response("缺少文件名参数", status=400)
    
    # 安全检查：确保文件名只包含安全字符，并防止目录遍历
    if not re.match(r'^[a-zA-Z0-9_\-\.]+$', filename) or '..' in filename:
        return Response("无效的文件名", status=400)
    
    # 获取当前脚本所在目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(current_dir, "data/daily")
    file_path = os.path.join(data_dir, filename)
    
    if not os.path.exists(file_path):
        return Response(f"文件 {filename} 不存在", status=404)
    
    # 读取Markdown内容
    with open(file_path, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    # 提取标题
    title = "GitHub 项目更新"
    title_match = re.search(r'^# (.+)$', md_content, re.MULTILINE)
    if title_match:
        title = title_match.group(1)
    
    # 渲染Markdown为HTML
    html_content = markdown.markdown(
        md_content,
        extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc',
            'markdown.extensions.tables'
        ]
    )
    
    # 渲染HTML模板
    return render_template(
        'markdown_viewer.html',
        title=title,
        content=html_content,
        timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    )

@app.route('/list-markdown-files', methods=['GET'])
def list_markdown_files():
    """
    列出所有可用的Markdown文件
    """
    # 获取当前脚本所在目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(current_dir, "data/daily")
    
    if not os.path.exists(data_dir):
        return Response(
            '{"files": [], "message": "无可用文件"}',
            mimetype='application/json'
        )
    
    markdown_files = [
        f for f in os.listdir(data_dir) 
        if f.endswith('.md') and os.path.isfile(os.path.join(data_dir, f))
    ]
    
    # 按日期排序（最新的在前）
    markdown_files.sort(reverse=True)
    
    return Response(
        '{"files": ' + str(markdown_files).replace("'", '"') + '}',
        mimetype='application/json'
    )

def build_cors_preflight_response():
    response = Response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "*")
    response.headers.add("Access-Control-Allow-Methods", "*")
    return response

def build_cors_actual_response(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True) 