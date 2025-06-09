class MyContextManager:
    def __enter__(self):
        print("Entering the context")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("Exiting the context")
        if exc_type:
            print(f"Exception occurred: {exc_type}, {exc_val}")
        return True  # Suppress the exception

    def do_something(self):
        print("Doing something within the context")

with MyContextManager() as manager:
    manager.do_something()
    # Raise an exception to test exception handling
    # raise ValueError("Something went wrong")

print("After the context")