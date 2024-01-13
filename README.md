# StableOpenai
**English** | [中文](README_ZH.md)

StableOpenai is an enhanced lightweight framework for OpenAI. It aims to provide more stable and efficient API request
management. It allows the use of multiple API keys to increase the number of requests per minute and per day, while
ensuring thread safety.

## Features

- **Multi-Key Management**: Easily manage multiple OpenAI API keys.
- **Thread Safety**: Supports stable requests in a multi-threaded environment.
- **Automatic Request Fallback**: Automatically tries other keys when API limits are triggered.

## Installation

Install StableOpenai using pip:

```bash
pip install stable-openai
```
## Quick Start

The process to quickly start using the StableOpenai library can be broken down into the following three steps:

### Step 1: Initialize KeyManager

First, you need to initialize `KeyManager` and add your list of API keys. This step should be completed before beginning any API requests.

```python
from stable_openai import KeyManager

# Replace with your list of API keys
api_keys = ["your_api_key1", "your_api_key2", ...]  
KeyManager(api_keys)
```

### Step 2: Use the Decorator

Use the `stable` decorator on the function that calls the OpenAI API. This ensures that each request is managed by `KeyManager` for switching between multiple API keys.

```python
from stable_openai import stable

@stable  # Add this decorator to the function calling the OpenAI API
def completions_with_backoff(model, messages):
    pass
    # The function body will be filled in the next step
```

### Step 3: Add the api_key Parameter

In the function using the decorator, add an `api_key` parameter. This parameter is necessary as it will receive the API key assigned by `KeyManager` and pass it to the OpenAI client.

```python
from stable_openai import stable
import openai
@stable
def completions_with_backoff(model, messages, api_key):  # api_key parameter receives the assigned API key
    # Create a client with the specified API key
    client = openai.OpenAI(api_key=api_key)  # Pass the api_key to the OpenAI client

    # Send a request to the OpenAI API and return the response
    response = client.chat.completions.create(
        model=model,
        messages=messages
    )
    return response.choices[0].message.content
```

By following these three steps, you can efficiently use the StableOpenai library, ensuring the stability and efficiency of your API requests.

## Complete Example

Use the `completions_with_backoff` function to get a model response:

```python
import threading
import openai
from stable_openai import KeyManager, stable

# Initialize KeyManager and add API keys
api_keys = ["your_api_key1", "your_api_key2", ...]  # Replace with your list of API keys
KeyManager(api_keys)


@stable
def completions_with_backoff(model, messages, api_key):
    # Create a client using the specified API key
    client = openai.OpenAI(api_key=api_key)

    # Send a request to the OpenAI API and return the response
    response = client.chat.completions.create(
            model=model,
            messages=messages
    )
    return response.choices[0].message.content


# Define a function for multi-threaded execution
def thread_function(thread_id):
    for i in range(5):  # Assuming each thread runs 5 times
        try:
            # Generate a test prompt
            test_prompt = f"Thread {thread_id}, Test {i + 1}: Hello, world!"
            messages = [{"role": "user", "content": test_prompt}]

            # Call the API
            response = completions_with_backoff(
                    model="gpt-3.5-turbo",
                    messages=messages,
            )
            print(f"Thread {thread_id}, Request {i + 1}/5: Success, Response: {response}")
        except Exception as e:
            print(f"Thread {thread_id}, Request {i + 1}/5: Failed, Error: {e}")


# Create and start threads
threads = []
for i in range(10):  # Assuming 10 threads are started
    t = threading.Thread(target=thread_function, args=(i + 1,))
    threads.append(t)
    t.start()

# Wait for all threads to complete
for t in threads:
    t.join()
```
