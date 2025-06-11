class CustomError(Exception):
    """Base class for custom exceptions in this module."""
    pass

class ValidationError(CustomError):
    """Raised when data validation fails."""
    def __init__(self, message, field=None):
        super().__init__(message)
        self.field = field

class DatabaseError(CustomError):
    """Raised when a database operation fails."""
    pass

def validate_data(data):
    if not isinstance(data, dict):
        raise ValidationError("Data must be a dictionary.")
    if 'name' not in data or not data['name']:
        raise ValidationError("Name is required.", field='name')
    return data

def save_to_database(data):
    try:
        # Simulate a database error
        raise Exception("Database connection failed.")
    except Exception as e:
        raise DatabaseError(f"Failed to save data: {e}")

# Example usage
data = {'age': 30}
try:
    validated_data = validate_data(data)
    save_to_database(validated_data)
except ValidationError as e:
    print(f"Validation Error: {e} (Field: {e.field})")
except DatabaseError as e:
    print(f"Database Error: {e}")
except CustomError as e:
    print(f"Custom Error: {e}")
except Exception as e:
    print(f"Unexpected Error: {e}") # Catch-all for other exceptions