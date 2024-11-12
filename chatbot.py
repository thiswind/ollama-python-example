from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import ollama

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

    # 使用 Ollama 进行聊天
    response = ollama.chat(model='llama3.2', messages=[{"role": "user", "content": user_message}])
    bot_reply = response['message']['content']
    
    return jsonify({"reply": bot_reply})

# 登出功能
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=5000)
