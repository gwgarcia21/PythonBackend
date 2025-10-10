"""2. Retry Decorator: Create a decorator that 
retries a function a certain number of times if 
it raises an exception."""
import random

def retry(num_times):
    def decorator_repeat(func):
        def wrapper(*args, **kwargs):
            last_exception = None
            for i in range(num_times):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    print(f"Error! Retrying ({i+1})...")
            raise last_exception
        return wrapper
    return decorator_repeat
    
@retry(num_times=3)
def random_error(chance=0.5):
    if random.random() < chance:
        raise ValueError("Random error occurred!")
    print("Success!")
    return

random_error(0.9)