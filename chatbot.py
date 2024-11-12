from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import ollama
import requests
from readability import Document  # 导入 Readability 模块
from lxml import html  # 确保正确导入 lxml.html 为 html



app = Flask(__name__)
app.secret_key = 'your_secret_key'  # 用于会话管理的密钥

# 硬编码的用户名和密码
USERNAME = 'admin'
PASSWORD = 'password123'

# 登录页面
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == USERNAME and password == PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('chat'))
        else:
            error = "Invalid credentials. Please try again."
            return render_template('login.html', error=error)
    return render_template('login.html')

# 聊天页面
@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('chat.html')

# 处理聊天的API
@app.route('/chat_api', methods=['POST'])
def chat_api():
    if not session.get('logged_in'):
        return jsonify({"error": "Unauthorized"}), 401
    
    user_message = request.json.get('message', '')
    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    response = ollama.chat(model='llama3.2', messages=[{"role": "user", "content": user_message}])
    bot_reply = response['message']['content']
    
    return jsonify({"reply": bot_reply})

# 爬取页面
@app.route('/scratch', methods=['GET', 'POST'])
def scratch():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        url = request.form.get('url')
        try:
            # 获取网页内容
            response = requests.get(url)
            response.raise_for_status()
            response.encoding = response.apparent_encoding
            html_content = response.text

            # 使用 Readability 提取主要内容的 HTML
            doc = Document(html_content)
            main_content_html = doc.summary()  # 获取主要内容的 HTML

            # 使用 lxml 提取纯文本
            main_content_element = html.fromstring(main_content_html)
            main_content_text = main_content_element.text_content().strip()  # 提取纯文本并去除首尾空白

            # 使用 Ollama 模型生成总结
            summary_prompt = (
                f"请对以下新闻内容进行总结，包含：1) 提纲要点 2) 中心思想：\n{main_content_text}"
            )
            summary_response = ollama.chat(model='llama3.2', messages=[{"role": "user", "content": summary_prompt}])
            summary = summary_response[0]['content'] if isinstance(summary_response, list) else summary_response['message']['content']

            return render_template('scratch.html', url=url, main_content=main_content_text, summary=summary)
        
        except requests.RequestException:
            error = "无法访问该 URL，请检查链接是否正确。"
            return render_template('scratch.html', error=error)

    return render_template('scratch.html')



# 登出功能
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=5000)
