import random
import threading
import unittest

import openai

from stable_openai.backoff import stable
from stable_openai.key import KeyManager
from tests.config import api_base, api_keys


class TestBackoff(unittest.TestCase):
    # Define a static method to test the backoff functionality with OpenAI completions
    @staticmethod
    @stable
    def completions_with_backoff(model, messages, api_key):
        # Create a client with the provided API key and other parameters
        client = openai.OpenAI(api_key=api_key, base_url=api_base, max_retries=2)
        # Send a request to the OpenAI chat API and return the response
        response = client.chat.completions.create(
                model=model,
                response_format={"type": "text"},
                messages=messages,
                seed=0,
                max_tokens=2
        )
        return response.choices[0].message.content

    # Test method to execute the API call in multiple threads
    def test_completions_thread(self):
        # Initialize the KeyManager with API keys
        KeyManager(api_keys)

        # Define a function to run in each thread
        def run_thread(thread_id):
            test_instance = TestBackoff()
            for i in range(5):  # Assume each thread runs 5 times
                try:
                    # Generate a test prompt
                    test_prompt = f"Thread {thread_id}, Test {i + 1}: " + random.choice(
                            ["Hello, world!"])
                    messages = [
                        {"role": "system", "content": ""},
                        {"role": "assistant", "content": ""},
                        {"role": "user", "content": test_prompt}
                    ]
                    # Call the API with backoff functionality
                    response = test_instance.completions_with_backoff(model="gpt-3.5-turbo-1106", messages=messages)
                    self.assertIsNotNone(response)  # Use unittest assertion
                    print(f"Thread {thread_id}, Request {i + 1}/5: Success")
                except Exception as e:
                    # Print and fail the test if an exception occurs
                    print(f"Thread {thread_id}, Request {i + 1}/5: Failed with error: {e}")
                    self.fail(f"Thread {thread_id}, Request {i + 1}/5: Failed with error: {e}")

        # Create and start threads
        threads = []
        for i in range(5):  # Assume launching 10 threads
            t = threading.Thread(target=run_thread, args=(i + 1,))
            threads.append(t)
            t.start()

        # Join threads to ensure they complete before exiting
        for t in threads:
            t.join()


# Standard boilerplate to run the test suite
if __name__ == '__main__':
    unittest.main()
