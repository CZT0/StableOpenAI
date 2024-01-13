import backoff
import logging
import openai

from stable_openai.key import KeyManager

logging.getLogger('backoff').setLevel(logging.WARNING)


# This decorator enhances a function with retry and API key management capabilities.
def stable(func):
    # Apply exponential backoff with a maximum backoff time of 20 seconds and a maximum of 5 tries.
    @backoff.on_predicate(backoff.expo, max_value=20, max_tries=5)
    def wrapper(*args, **kwargs):
        global api_key
        try:
            # Retrieve an API key using the KeyManager.
            api_key = KeyManager().get_key()
            # Call the original function with the retrieved API key and other arguments.
            response = func(*args, **kwargs, api_key=api_key)
            return response
        except openai.RateLimitError:
            # If a rate limit error is encountered, set the TTL of the key to 60 seconds.
            KeyManager().set_ttl(api_key, 60)
            # Log the rate limit issue and the retry mechanism.
            logging.info(
                    f"{api_key} Rate limit reached. Will retry this key after 60 seconds.")
        except Exception as e:
            # Log any other exceptions that occur during the function execution.
            logging.error(f"An error occurred: {e}")

    # Return the wrapper function.
    return wrapper
