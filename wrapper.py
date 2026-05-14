import time
import functools

def retry(max_retries=3, initial_delay=1, exceptions=(Exception,)):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            wait = initial_delay
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    if attempt == max_retries - 1:
                        raise
                    time.sleep(wait)
                    wait *= 2  # Exponential backoff
        return wrapper
    return decorator

@retry(max_retries=3, initial_delay=1, exceptions=(ConnectionError,))
def call_llm_api():
    # Simulate an API call that may fail
    import random
    if random.random() < 0.5:  # 50% chance of failure
        raise ConnectionError("Failed to connect to LLM API")
    return "LLM API response"

if __name__ == "__main__":
    try:
        response = call_llm_api()
        print(response)
    except Exception as e:
        print(f"Error: {e}")