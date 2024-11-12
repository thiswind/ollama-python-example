

# Ollama Python Example - Scratch 功能升级指南

本次更新在 Ollama Python Example 项目中新增了一个功能页面 `Scratch`，该功能可以自动从输入的网页中提取主要内容并生成总结。这是一个方便的网页内容提取和快速阅读工具，用户可通过输入 URL 获取网页的核心信息和总结。

本指南将指导您在现有项目的基础上，添加和配置新的 `Scratch` 功能。

---

## 1. 安装新依赖

请确保您已在项目根目录下的虚拟环境中，并使用以下命令安装 `Scratch` 功能所需的额外依赖：

```bash
pip install -r requirements.txt
```

确认 `requirements.txt` 包含以下内容：

```plaintext
ollama
flask
requests
readability-lxml
lxml
```

---

## 2. 覆盖源文件

请依次找到以下源文件，并按照下面的步骤覆盖原文件内容，以完成新功能的添加。

### 2.1 覆盖 `chatbot.py`

1. 打开项目中的 `chatbot.py` 文件。
2. 将以下代码粘贴到 `chatbot.py` 中，完全覆盖原有内容：

   ```python
   from flask import Flask, render_template, request, redirect, url_for, session, jsonify
   import ollama
   import requests
   from readability import Document
   from lxml import html

   app = Flask(__name__)
   app.secret_key = 'your_secret_key'

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
   ```

---

## 3. 创建新模板文件

在 `templates` 文件夹下，创建一个名为 `scratch.html` 的新文件。然后将以下代码粘贴到该文件中，确保它与项目的其他模板文件位于同一目录下：

```html
{% extends "base.html" %}

{% block content %}
<div class="container">
    <h2>Scratch 页面</h2>
    <form method="post" action="{{ url_for('scratch') }}">
        <div class="form-group">
            <label for="url">输入 URL：</label>
            <input type="text" name="url" class="form-control" id="url" placeholder="输入要爬取的网页 URL" required>
        </div>
        <button type="submit" class="btn btn-primary">提交</button>
    </form>
    {% if main_content and summary %}
    <hr>
    <h3>主要内容</h3>
    <p>{{ main_content }}</p>
    <hr>
    <h3>总结</h3>
    <p>{{ summary }}</p>
    {% endif %}
</div>
{% endblock %}
```

---

## 4. 启动并测试 `Scratch` 功能

完成上述步骤后，在项目根目录中启动应用，确保一切配置正常：

```bash
python chatbot.py
```

打开浏览器，访问 `http://127.0.0.1:5000/scratch`。在页面中输入任意有效的网页 URL，测试 `Scratch` 功能是否正常运行。此功能会提取网页的主要内容并生成总结。
