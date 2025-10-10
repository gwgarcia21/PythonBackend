"""Circular References: Create a scenario with circular references 
between objects. Use gc.collect() and sys.getrefcount() to demonstrate 
how the garbage collector handles these references."""
import gc
import sys

class Dog():
    def __init__(self, name):
        self.name = name
        print(f"Dog {self.name} created")
        return
    
    def __del__(self):
        print(f"Dog {self.name} deleted")
        return
    
gc.enable()
cheetosName = "cheetos"
yorkieName = "yorkie"
cheetos = Dog(cheetosName)
print(f"Reference count of {cheetosName}: {sys.getrefcount(cheetos)}")
yorkie = Dog(yorkieName)
print(f"Reference count of {yorkieName}: {sys.getrefcount(yorkie)}")
anotherCheetos = cheetos
print(f"Reference count of {cheetosName}: {sys.getrefcount(anotherCheetos)}")

del(cheetos)
print(f"Reference count of {cheetosName}: {sys.getrefcount(anotherCheetos)}")
del(yorkie)
del(anotherCheetos)

gc.collect()