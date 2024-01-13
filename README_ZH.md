# StableOpenai

StableOpenai 是一个增强的 OpenAI 轻量级框架。目的是提供更稳定、高效的 API 请求管理。它允许使用多个 API
密钥，增加每分钟和每天的请求次数，并确保线程安全。

## 特点

- **多密钥管理**：轻松管理多个 OpenAI API 密钥。
- **线程安全**：支持多线程环境下的稳定请求。
- **自动请求回退**：当 API 限制触发时自动尝试其他密钥。

## 安装

使用 pip 安装 StableOpenai：

```bash
pip install stable-openai
```

## 快速开始

快速开始使用 StableOpenai 库的过程可以分为以下三个步骤：

### 步骤1: 初始化 KeyManager

首先，您需要初始化 `KeyManager` 并添加您的 API 密钥列表。这一步骤在开始任何 API 请求之前完成。

```python
from stable_openai import KeyManager

# 替换成您的 API 密钥列表
api_keys = ["your_api_key1", "your_api_key2", ...]
KeyManager(api_keys)
```

### 步骤2: 使用装饰器

在调用 OpenAI API 的函数上使用 `stable` 装饰器。这将确保每个请求都通过 `KeyManager` 进行管理，以便在多个 API
密钥间进行切换。

```python
from stable_openai import stable


@stable  # 在调用 OpenAI API 的函数上加上此装饰器
def completions_with_backoff(model, messages):
    pass
```

### 步骤3: 添加 api_key 参数

在使用装饰器的函数中，添加一个 `api_key` 参数。这个参数是必需的，因为它将接收从 `KeyManager` 分配的 API 密钥，并将其传递给
OpenAI 客户端。

```python
from stable_openai import stable
import openai
@stable
def completions_with_backoff(model, messages, api_key):  # api_key 参数接收分配的 API 密钥
    # 使用指定的 API 密钥创建客户端
    client = openai.OpenAI(api_key=api_key)  # 将 api_key 传递给 OpenAI 客户端

    # 向 OpenAI API 发送请求并返回响应
    response = client.chat.completions.create(
            model=model,
            messages=messages
    )
    return response.choices[0].message.content
```

通过遵循这三个步骤，您可以高效地使用 StableOpenai 库，确保 API 请求的稳定性和效率。 

## 完整示例

使用 `completions_with_backoff` 函数获取模型响应：

```python
import threading
import openai
from stable_openai import KeyManager, stable

# 初始化KeyManager并添加API密钥
api_keys = ["your_api_key1", "your_api_key2", ...]  # 替换成你的API密钥列表
KeyManager(api_keys)


@stable
def completions_with_backoff(model, messages, api_key):
    # 使用指定的API密钥创建客户端
    client = openai.OpenAI(api_key=api_key)

    # 向OpenAI API发送请求并返回响应
    response = client.chat.completions.create(
            model=model,
            messages=messages
    )
    return response.choices[0].message.content


# 定义一个多线程运行的函数
def thread_function(thread_id):
    for i in range(5):  # 假设每个线程运行5次
        try:
            # 生成测试提示
            test_prompt = f"Thread {thread_id}, Test {i + 1}: 你好，世界！"
            messages = [{"role": "user", "content": test_prompt}]

            # 调用API
            response = completions_with_backoff(
                    model="gpt-3.5-turbo",
                    messages=messages,
            )
            print(f"线程 {thread_id}, 请求 {i + 1}/5: 成功，响应：{response}")
        except Exception as e:
            print(f"线程 {thread_id}, 请求 {i + 1}/5: 失败，错误：{e}")


# 创建并启动线程
threads = []
for i in range(10):  # 假设启动10个线程
    t = threading.Thread(target=thread_function, args=(i + 1,))
    threads.append(t)
    t.start()

# 等待所有线程完成
for t in threads:
    t.join()

```

