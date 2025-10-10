"""Exception Chaining: Modify the process_data function 
to catch TypeError if the input data is not a number and 
raise a custom exception InvalidDataTypeError with the 
original TypeError chained to it."""

class CustomError(Exception):
    pass

class InvalidDataTypeError(CustomError):
    pass

def process_data(data):
    try:
        result = 10 / data
        return result
    except ZeroDivisionError as e:
        raise ValueError("Invalid data provided") from e
    except TypeError as e:
        raise InvalidDataTypeError("Invalid type provided") from e

try:
    process_data("c")
except ValueError as e:
    print(f"Error: {e}")
    print(f"Original exception: {e.__cause__}")
except InvalidDataTypeError as e:
    print(f"Error: {e}")
    print(f"Original exception: {e.__cause__}")