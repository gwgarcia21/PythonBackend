"""3. Context Manager for Files: Create a context manager 
that automatically opens and closes a file. The context 
manager should take the file path and mode as input."""
class FileContextManager():
    def __init__(self, file_path, mode):
        self.file_path = file_path
        self.mode = mode
        self.file_stream = None

    def __enter__(self):
        """Opens the file"""
        print("Opening file")
        try:
            self.file_stream = open(file=self.file_path, mode=self.mode)
            return self
        except Exception as e:
            raise Exception("Open file error") from e
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Close the file"""
        print("Closing file")
        try:
            if self.file_stream:
                self.file_stream.close()
        except Exception as e:
            raise Exception("Close file error") from e
        if exc_type:
            print(f"Exception occurred: {exc_type}, {exc_val}")
        return False
    
    def print_content(self):
        if self.file_stream:
            content = self.file_stream.read()
            print(content)
    
with FileContextManager(file_path="2exercise.py", mode="r") as manager:
    manager.print_content()