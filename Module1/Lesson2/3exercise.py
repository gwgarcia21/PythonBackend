"""3. Attribute Validation Metaclass: Create a 
metaclass that ensures all classes using it have 
a specific set of attributes with specific types."""

class Animal(type):
    required_attrs = {
        "name": str,
        "weight": float,
    }

    def __new__(cls, name, bases, attrs):
        for attr, typ in cls.required_attrs.items():
            # Verifica se o atributo existe na classe ou em suas bases
            if not any(hasattr(base, attr) for base in (bases or [])) and attr not in attrs:
                raise ValueError(f"Class '{name}' must define '{attr}' (directly or via inheritance)")
        return super().__new__(cls, name, bases, attrs)

class Mammal(metaclass=Animal):
    name = "Unidentified mammal"
    weight = 0.0

class Dog(Mammal):
    def __init__(self):
        self.name = "Dog"
        self.weight = 10.0

class Cat(Mammal):
    def __init__(self):
        self.name = "Cat"
        self.weight = 5.0

dog = Dog()
cat = Cat()
print(f"{dog.name} - {dog.weight}")
print(f"{cat.name} - {cat.weight}")