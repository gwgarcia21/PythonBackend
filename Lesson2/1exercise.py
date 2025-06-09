"""1. Logging Decorator: Create a decorator that logs 
the input arguments and return value of a function."""
def logger(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        print(f"Function {func.__name__} called with args={args}, kwargs={kwargs}, returned {result}")
        return result
    return wrapper

@logger
def sum(a: int, b: int):
    return a + b

sum(1, 2)