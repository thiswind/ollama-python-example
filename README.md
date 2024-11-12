# 使用 Ollama 和 Flask 的简单 Chatbot 项目

## 项目简介

本项目展示了如何通过 Flask 和 Ollama 创建一个带有登录功能的简单聊天应用程序，同时还包括两个直接调用 Ollama 模型的独立示例：一个是 **直接输出**，另一个是 **流式输出**。通过这些示例，您可以学习如何使用 AI 模型生成代码并集成在 Python 程序中，体验不同的输出方式对应用的影响。

---

## 目录

1. [项目结构](#项目结构)
2. [安装前提](#安装前提)
3. [构建步骤](#构建步骤)
4. [运行应用](#运行应用)
5. [三种示例的功能说明](#三种示例的功能说明)
   - Flask 应用
   - 直接输出示例
   - 流式输出示例
6. [参考资源](#参考资源)

---

## 项目结构

最终项目文件夹结构如下：

```
ollama-chatbot/
│
├── chatbot.py                  # 主 Flask 应用，包含登录和聊天功能
├── hello_ollama.py             # 简单的 Ollama 调用示例
├── hello_ollama_stream.py      # 使用流式响应的 Ollama 调用示例
├── requirements.txt            # Python 依赖包
└── templates/                  # HTML 模板文件夹
    ├── base.html               # 基础模板，供其他页面继承
    ├── login.html              # 登录页面
    └── chat.html               # 聊天页面
```

## 安装前提

- **Ollama**：请确保您在本地安装了 Ollama，具体安装方法见 [Ollama 官方网站](https://ollama.com/)。
- **Python 3.7+**：项目使用 Python 3 及 Flask 框架。

---

## 构建步骤

> 请按照以下步骤逐步在本地搭建项目。

1. **创建项目文件夹**：在计算机上新建一个文件夹，命名为 `ollama-chatbot`。
2. **创建并填写 `requirements.txt`**：在 `ollama-chatbot` 文件夹中创建 `requirements.txt`，并添加所需依赖。
3. **创建 Flask 应用的主文件**：在 `ollama-chatbot` 文件夹中创建 `chatbot.py`，粘贴 Flask 应用代码。
4. **创建 Ollama 调用示例文件**：分别创建 `hello_ollama.py` 和 `hello_ollama_stream.py` 文件，粘贴相应的代码。
5. **创建 `templates` 文件夹和 HTML 模板**：在 `ollama-chatbot` 文件夹中创建 `templates` 子文件夹，并添加 HTML 文件。

请参考上方详细的文件和代码示例，逐步复制并粘贴代码到相应文件中。

---

## 运行应用

1. **安装依赖**：在项目根目录下运行以下命令安装所需依赖：
   ```bash
   pip install -r requirements.txt
   ```

2. **启动应用**：运行以下命令启动 Flask 应用：
   ```bash
   python chatbot.py
   ```

3. **访问应用**：在浏览器中打开 [http://127.0.0.1:5000](http://127.0.0.1:5000)，并使用用户名 `admin` 和密码 `password123` 登录，进入聊天页面。

---

## 三种示例的功能说明

### 1. Flask 应用：带有登录和聊天功能的 Web 应用

- **文件**：`chatbot.py`
- **描述**：这是一个基于 Flask 的 Web 应用，包含登录、聊天和登出功能。用户登录后可以访问聊天页面，通过与 Ollama 模型交互获得 AI 的回复。
- **用途**：展示了如何结合 Web 界面、会话管理和 Ollama AI 模型构建一个基础的聊天应用。

### 2. 直接输出示例：`hello_ollama.py`

- **文件**：`hello_ollama.py`
- **描述**：此脚本直接调用 Ollama 模型，发送一个问题并立即返回完整的回答。
- **示例代码**：
  ```python
  import ollama

  response = ollama.chat(model='llama3.2', messages=[
    {
      'role': 'user',
      'content': 'Why is the sky blue?',
    },
  ])
  print(response['message']['content'])
  ```
- **输出方式**：**直接输出**，即一次性输出整个回复。
- **适用场景**：直接输出适合处理较短的回答或简单的查询。这种方式更高效，因为它不会逐步输出，直接返回完整的响应。

### 3. 流式输出示例：`hello_ollama_stream.py`

- **文件**：`hello_ollama_stream.py`
- **描述**：此脚本使用流式响应模式（streaming）调用 Ollama 模型，逐块输出回复内容。
- **示例代码**：
  ```python
  import ollama

  stream = ollama.chat(
      model='llama3.2',
      messages=[{'role': 'user', 'content': 'Why is the sky blue?'}],
      stream=True,
  )

  for chunk in stream:
    print(chunk['message']['content'], end='', flush=True)
  ```
- **输出方式**：**流式输出**，即按数据块逐步输出内容，模拟实时响应。
- **适用场景**：流式输出适用于处理较长的回答或需要实时更新的情况。例如，当生成内容较长时，流式输出可以边生成边显示，让用户不必等待整个内容生成完毕，从而获得更好的交互体验。

### 为什么需要两种输出方式？

1. **直接输出**：
   - 更高效，适合生成短回答。
   - 由于不涉及分块输出，因此不适合处理需要逐步展示的长文本。
   - 适合简单的 API 请求或快速反馈的场景。

2. **流式输出**：
   - 适合较长或复杂的回答，可以边生成边展示，减少用户等待时间。
   - 尤其适合需要实时响应的场景，比如回答较长的问答或逐句生成内容。
   - 提供更自然的用户体验，让用户感觉内容是在动态生成的。

---

## 参考资源

- [Ollama 官方网站](https://ollama.com/)
- [Flask 官方文档](https://flask.palletsprojects.com/)
