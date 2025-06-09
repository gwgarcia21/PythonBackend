def my_decorator(func):
    def wrapper():
        print("Before the function call.")
        func()
        print("After the function call.")
    return wrapper

@my_decorator
def say_hello():
    print("Hello!")

say_hello()

####

def repeat(num_times):
    def decorator_repeat(func):
        def wrapper(*args, **kwargs):
            for i in range(num_times):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator_repeat

@repeat(num_times=3)
def greet(name):
    print(f"Hello, {name}!")

greet("Alice")

####

def add_attribute(cls):
    cls.new_attribute = "Added by decorator"
    return cls

@add_attribute
class MyClass:
    pass

instance = MyClass()
print(instance.new_attribute)

####

def singleton(cls):
    instances = {}
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return get_instance

@singleton
class DatabaseConnection:
    def __init__(self, db_url):
        self.db_url = db_url

db1 = DatabaseConnection("url1")
db2 = DatabaseConnection("url2")
print(db1 is db2)