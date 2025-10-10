"""Singleton with Metaclass: Implement the singleton pattern 
using a metaclass instead of a decorator. Compare the 
advantages and disadvantages of each approach."""

class SingleInstance(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]
    
class Machine(metaclass=SingleInstance):
    def __init__(self):
        self.version = "1.0"

machine1 = Machine()
machine1.version = "2.0"
machine2 = Machine()
print("Version machine 1: ", machine1.version)
print("Version machine 2: ", machine2.version)
if (machine1 is machine2):
    print("Singleton is correct")
else:
    print("Singleton is NOT correct")