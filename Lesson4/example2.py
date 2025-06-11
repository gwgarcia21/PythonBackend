def process_data(data):
    try:
        result = 10 / data
        return result
    except ZeroDivisionError as e:
        raise ValueError("Invalid data provided") from e

try:
    process_data(0)
except ValueError as e:
    print(f"Error: {e}")
    print(f"Original exception: {e.__cause__}")