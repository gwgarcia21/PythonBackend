def divide(x, y):
    try:
        result = x / y
    except ZeroDivisionError:
        print("Cannot divide by zero.")
    else:
        print("Division successful.")
        return result
    finally:
        print("Executing finally block.")

print(divide(10, 2))
print(divide(10, 0))