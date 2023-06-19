import time
import random
import openai


def retry_on_error(max_retries=5, backoff_factor=2):
    def decorator(func):
        def wrapper(*args, **kwargs):
            retries = 0
            while retries <= max_retries:
                try:
                    return func(*args, **kwargs)
                except openai.error.ServiceUnavailableError:
                    print("Service is temporarily unavailable. Retrying...")
                    retries += 1
                    delay = backoff_factor ** retries + random.uniform(0, 1)
                    time.sleep(delay)

            print("Failed to complete the request after multiple retries.")
            return None

        return wrapper

    return decorator