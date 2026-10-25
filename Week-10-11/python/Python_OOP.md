# Python Object-Oriented Programming (OOP)

## Table of Contents

* [1. High-Level Overview](#1-high-level-overview)
* [2. The Four Pillars of OOP](#2-the-four-pillars-of-oop)
    * [2.1 Abstraction](#21-abstraction)
    * [2.2 Encapsulation](#22-encapsulation)
    * [2.3 Inheritance](#23-inheritance)
    * [2.4 Polymorphism](#24-polymorphism)
* [3. Summary Comparison](#3-summary-comparison)

***

## 1. High-Level Overview

**Object-Oriented Programming (OOP)** is a programming paradigm based on the concept of "**objects**," which can contain data (attributes) and code (methods). Instead of focusing on functions and logic (Procedural Programming), OOP focuses on the objects that developers want to manipulate.

By using OOP, developers can create modular, reusable, and scalable code by modeling real-world entities and their behaviors. This module covers the **Four Pillars of OOP**, which form the structural foundation of any robust object-oriented system.

[↑ Back to Table of Contents](#table-of-contents)

***

*Now that we understand the "What" of OOP, let's dive into the structural framework by exploring the first of the four pillars: Abstraction.*

## 2. The Four Pillars of OOP

The four pillars—**Abstraction**, **Encapsulation**, **Inheritance**, and **Polymorphism**—work together to provide the core benefits of OOP: security, reusability, and simplicity.

### 2.1 Abstraction

**Abstraction** is the process of hiding complex implementation details and showing only the necessary features of an object. It reduces complexity by allowing the user to interact with a high-level interface without needing to understand the "under-the-hood" mechanics.

In Python, abstraction is typically achieved using **Abstract Base Classes (ABCs)** from the `abc` module.

**How it Works:**
An abstract class acts as a blueprint. It defines a set of methods that *must* be implemented by any subclass, but it does not provide the implementation itself.

```python
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self):
        """Calculate the area of the shape."""
        pass

class Square(Shape):
    def __init__(self, side):
        self.side = side
    
    def area(self):
        return self.side * self.side

# shape = Shape() # This would raise an error: Can't instantiate abstract class
sq = Square(5)
print(sq.area()) # Output: 25
```

> [!TIP]
> Think of a **TV Remote**. You know that pressing the "Volume Up" button increases the sound. You don't need to know how the infrared signal is processed or how the internal circuitry communicates with the speakers. That is Abstraction.

[↑ Back to Table of Contents](#table-of-contents)

***

*While Abstraction hides complexity at the interface level, Encapsulation protects the data itself from unauthorized access.*

### 2.2 Encapsulation

**Encapsulation** is the practice of bundling data (attributes) and the methods that operate on that data into a single unit (a class) and restricting direct access to some of the object's components. This is often referred to as **Data Hiding**.

**How it Works:**
In Python, encapsulation is implemented using **access modifiers** (conventions) to indicate how "private" a member is:

| Access Level | Convention | Description |
| :--- | :--- | :--- |
| **Public** | `name` | Accessible from anywhere. |
| **Protected** | `_name` | Suggests the variable should only be accessed within the class and its subclasses. |
| **Private** | `__name` | Triggers **Name Mangling**, making it harder (but not impossible) to access from outside the class. |

> [!IMPORTANT]
> **Name Mangling:** When you prefix an attribute with two underscores (e.g., `__balance`), Python internally renames it to `_ClassName__attributeName`. This is not strictly "private" (as you could still access it via the mangled name), but it serves to prevent accidental name clashes in subclasses and discourages direct external access.

```python
class BankAccount:
    def __init__(self, balance):
        self.__balance = balance  # Private attribute

    def deposit(self, amount):
        if amount > 0:
            self.__balance += amount
            print(f"Deposited {amount}. New balance: {self.__balance}")

    def get_balance(self):
        return self.__balance

account = BankAccount(1000)
account.deposit(500)
# print(account.__balance) # This would raise an AttributeError
print(account.get_balance()) # Output: 1500
```

[↑ Back to Table of Contents](#table-of-contents)

***

*Encapsulation keeps our data safe; next, we look at how we can build upon existing structures using Inheritance.*

### 2.3 Inheritance

**Inheritance** allows a new class (the **Subclass** or **Child Class**) to acquire the properties and behaviors (methods) of an existing class (the **Superclass** or **Parent Class**). This promotes **Code Reusability**.

**How it Works:**
Instead of writing the same code for multiple similar objects, you define the common logic in a parent class and then specialize it in child classes.

```python
class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        print(f"{self.name} makes a sound.")

class Dog(Animal):
    def speak(self):
        # Overriding the parent method
        print(f"{self.name} barks!")

class Cat(Animal):
    def speak(self):
        print(f"{self.name} meows!")

dog = Dog("Buddy")
cat = Cat("Whiskers")

dog.speak() # Output: Buddy barks!
cat.speak() # Output: Whiskers meows!
```

[↑ Back to Table of Contents](#table-of-contents)

***

*Inheritance creates a hierarchy, but Polymorphism allows us to treat different objects in a uniform way.*

### 2.4 Polymorphism

**Polymorphism** (meaning "many forms") allows objects of different classes to be treated as objects of a common superclass. Most importantly, it allows a single interface (method name) to represent different underlying implementations.

**How it Works:**
In the context of inheritance, polymorphism is most commonly seen through **Method Overriding**, where different subclasses implement the same method name in their own way.

```python
animals = [Dog("Buddy"), Cat("Whiskers"), Dog("Rex")]

for animal in animals:
    # Even though they are different types, we call the same method name
    animal.speak() 
```

**Output:**
```text
Buddy barks!
Whiskers meows!
Rex barks!
```

### Special Polymorphism: Dunder Methods (Magic Methods)

Beyond standard method overriding, Python leverages **Dunder Methods** (Double Underscore methods) to implement polymorphism at the language level. These allow your custom objects to interact with built-in Python operations like addition, length checking, or printing.

By overriding these methods, you define how your object behaves when used with standard operators.

| Dunder Method | Purpose | Operator / Usage |
| :--- | :--- | :--- |
| `__str__` | Human-readable string representation | `print(obj)` or `str(obj)` |
| `__repr__` | Unambiguous "developer" representation | Inspecting in REPL / Debugging |
| `__len__` | Returns the size of the object | `len(obj)` |
| `__add__` | Defines behavior for the addition operator | `obj1 + obj2` |
| `__eq__` | Defines behavior for equality comparison | `obj1 == obj2` |

**Example of Dunder Overriding:**

```python
class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"Vector({self.x}, {self.y})"

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

v1 = Vector(2, 4)
v2 = Vector(1, 3)

print(v1)       # Uses __str__: Vector(2, 4)
print(v1 + v2)  # Uses __add__: Vector(3, 7)
```

[↑ Back to Table of Contents](#table-of-contents)

***

*To wrap up our exploration of the pillars, let's look at how they compare and interact.*

## 3. Summary Comparison

The following table provides a quick reference to differentiate the four pillars.

| Pillar | Primary Purpose | Key Concept | Analogy |
| :--- | :--- | :--- | :--- |
| **Abstraction** | Reduce Complexity | Hiding "how" it works via interfaces. | A TV Remote (Buttons vs. Circuitry). |
| **Encapsulation** | Data Security | Bundling data and restricting access. | A Capsule (Medicine inside a shell). |
| **Inheritance** | Code Reusability | Creating a hierarchy of classes. | A Child inheriting traits from a Parent. |
| **Polymorphism** | Flexibility | One interface, many implementations. | A "Play" button (Works for Music, Video, or Games). |

[↑ Back to Table of Contents](#table-of-contents)
