"""Logging: Configure the logging module to log 
messages to a file named my_app.log. Log a DEBUG 
message when a function is called, an INFO message 
when a user logs in, a WARNING message when a user 
enters invalid data, an ERROR message when a database 
connection fails, and a CRITICAL message when the application crashes."""

import inspect
import logging
import random

logging.basicConfig(filename='my_app.log',
                    level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def log_function_name(func):
    def wrapper(*args, **kwargs):
        self = args[0]  # o 'self' da instância
        logger : logging.Logger = getattr(self, "logger", None)
        if logger:
            logger.debug(f"Method {func.__name__} called")
        return func(*args, **kwargs)
    return wrapper

class MyApp():
    def __init__(self, logger:logging.Logger=None):
        self.user = None
        self.logger = logger

    @log_function_name
    def login(self, user):
        self.user = user
        self.logger and self.logger.info(f"User logged in: {self.user}")
    
    @log_function_name
    def divide(self, x, y):
        try:
            result = x / y
            return result
        except Exception as e:
            self.logger and self.logger.warning(e)

    @log_function_name
    def connect_database(self):
        success = random.random() < 0.2
        if success:
            self.logger and self.logger.info("Successful connection to database.")
        else:
            self.logger and self.logger.error("Connection to database failed.")

    @log_function_name
    def crash(self):
        try:
            raise RuntimeError("Crash proposital")
        except Exception as e:
            self.logger and self.logger.critical(e)
        
if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    app = MyApp(logger)
    app.login("Jack")
    app.divide(1, 0)
    app.connect_database()
    app.crash()