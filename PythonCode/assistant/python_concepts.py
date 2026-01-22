# assistant/python_concepts.py
"""
Python concept library with comprehensive explanations.
Contains definitions, examples, and learning resources for Python concepts.
"""

from typing import Dict, Optional


# Core Python concepts with detailed explanations
CONCEPTS: Dict[str, str] = {
    # ==========================================================================
    # BASIC TYPES
    # ==========================================================================
    
    "class": """## 🏗️ Classes in Python

**Definition:** A class is a blueprint for creating objects. Objects have attributes (data) and methods (functions).

### Basic Class Structure
```python
class Dog:
    \"\"\"A simple class representing a dog.\"\"\"
    
    def __init__(self, name, age):
        \"\"\"Initialize name and age attributes.\"\"\"
        self.name = name
        self.age = age
    
    def sit(self):
        \"\"\"Simulate a dog sitting.\"\"\"
        print(f"{self.name} is now sitting.")
    
    def roll_over(self):
        \"\"\"Simulate rolling over.\"\"\"
        print(f"{self.name} rolled over!")
```

### Creating Instances
```python
# Create an instance (object)
my_dog = Dog('Willie', 6)

# Access attributes
print(my_dog.name)  # 'Willie'
print(my_dog.age)   # 6

# Call methods
my_dog.sit()        # Willie is now sitting.
my_dog.roll_over()  # Willie rolled over!
```

### Key Concepts
| Concept | Description |
|---------|-------------|
| `class` | Keyword to define a class |
| `__init__` | Constructor method, runs when creating instance |
| `self` | Reference to the current instance |
| Attribute | Variable belonging to an object |
| Method | Function belonging to a class |

### Why Use Classes?
- **Organization** - Group related data and functions
- **Reusability** - Create multiple objects from one class
- **Inheritance** - Build on existing classes
- **Encapsulation** - Hide internal details""",

    "object": """## 📦 Objects in Python

**Definition:** An object is an instance of a class. Everything in Python is an object!

### Creating Objects
```python
class Car:
    def __init__(self, brand, model):
        self.brand = brand
        self.model = model
    
    def describe(self):
        return f"{self.brand} {self.model}"

# Create objects (instances)
car1 = Car("Toyota", "Camry")
car2 = Car("Honda", "Civic")

print(car1.describe())  # Toyota Camry
print(car2.describe())  # Honda Civic
```

### Everything is an Object
```python
# Numbers are objects
x = 42
print(type(x))  # <class 'int'>

# Strings are objects
s = "hello"
print(s.upper())  # HELLO

# Lists are objects
lst = [1, 2, 3]
print(type(lst))  # <class 'list'>
```

### Object Identity and Equality
```python
a = [1, 2, 3]
b = [1, 2, 3]
c = a

print(a == b)   # True (equal values)
print(a is b)   # False (different objects)
print(a is c)   # True (same object)
```""",

    "function": """## 🔧 Functions in Python

**Definition:** A function is a reusable block of code that performs a specific task.

### Basic Function
```python
def greet(name):
    \"\"\"Return a greeting message.\"\"\"
    return f"Hello, {name}!"

message = greet("Alice")
print(message)  # Hello, Alice!
```

### Parameters and Arguments
```python
# Positional arguments
def add(a, b):
    return a + b

print(add(2, 3))  # 5

# Default parameters
def greet(name, greeting="Hello"):
    return f"{greeting}, {name}!"

print(greet("Bob"))           # Hello, Bob!
print(greet("Bob", "Hi"))     # Hi, Bob!

# Keyword arguments
def describe_pet(name, animal_type):
    print(f"I have a {animal_type} named {name}")

describe_pet(animal_type="dog", name="Max")
```

### *args and **kwargs
```python
# Variable positional arguments
def sum_all(*args):
    return sum(args)

print(sum_all(1, 2, 3, 4))  # 10

# Variable keyword arguments
def print_info(**kwargs):
    for key, value in kwargs.items():
        print(f"{key}: {value}")

print_info(name="Alice", age=25, city="NYC")
```

### Return Values
```python
# Return single value
def square(n):
    return n * n

# Return multiple values (tuple)
def get_stats(numbers):
    return min(numbers), max(numbers), sum(numbers)

low, high, total = get_stats([1, 2, 3, 4, 5])
```""",

    "list": """## 📋 Lists in Python

**Definition:** A list is an ordered, mutable collection that can hold items of any type.

### Creating Lists
```python
# Empty list
empty = []

# List with items
fruits = ["apple", "banana", "cherry"]
numbers = [1, 2, 3, 4, 5]
mixed = [1, "hello", 3.14, True]
```

### Accessing Elements
```python
fruits = ["apple", "banana", "cherry", "date"]

# Indexing (0-based)
print(fruits[0])   # "apple"
print(fruits[-1])  # "date" (last item)

# Slicing
print(fruits[1:3])  # ["banana", "cherry"]
print(fruits[:2])   # ["apple", "banana"]
print(fruits[2:])   # ["cherry", "date"]
```

### Common Methods
```python
fruits = ["apple", "banana"]

# Add items
fruits.append("cherry")       # Add to end
fruits.insert(0, "apricot")   # Insert at index
fruits.extend(["date", "fig"]) # Add multiple

# Remove items
fruits.remove("banana")       # Remove by value
popped = fruits.pop()         # Remove and return last
del fruits[0]                 # Remove by index

# Other methods
fruits.sort()                 # Sort in place
fruits.reverse()              # Reverse in place
count = fruits.count("apple") # Count occurrences
index = fruits.index("cherry") # Find index
```

### List Comprehensions
```python
# Create list from another
squares = [x**2 for x in range(10)]
# [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]

# With condition
evens = [x for x in range(20) if x % 2 == 0]
# [0, 2, 4, 6, 8, 10, 12, 14, 16, 18]
```""",

    "dictionary": """## 📖 Dictionaries in Python

**Definition:** A dictionary is a collection of key-value pairs, providing O(1) average lookup time.

### Creating Dictionaries
```python
# Empty dict
empty = {}

# With items
person = {"name": "Alice", "age": 25, "city": "NYC"}

# Using dict()
person = dict(name="Alice", age=25, city="NYC")
```

### Accessing Values
```python
person = {"name": "Alice", "age": 25}

# Using key
print(person["name"])  # "Alice"

# Using get() (safer)
print(person.get("age"))        # 25
print(person.get("job", "N/A")) # "N/A" (default)
```

### Common Methods
```python
person = {"name": "Alice", "age": 25}

# Get all keys, values, items
person.keys()    # dict_keys(['name', 'age'])
person.values()  # dict_values(['Alice', 25])
person.items()   # dict_items([('name', 'Alice'), ('age', 25)])

# Add/Update
person["job"] = "Engineer"  # Add new
person["age"] = 26          # Update existing
person.update({"city": "NYC", "age": 27})

# Remove
del person["city"]          # Remove key
value = person.pop("job")   # Remove and return
person.clear()              # Remove all
```

### Dictionary Comprehensions
```python
# Create from range
squares = {x: x**2 for x in range(5)}
# {0: 0, 1: 1, 2: 4, 3: 9, 4: 16}

# Filter
original = {'a': 1, 'b': 2, 'c': 3, 'd': 4}
filtered = {k: v for k, v in original.items() if v > 2}
# {'c': 3, 'd': 4}
```""",

    "loop": """## 🔄 Loops in Python

**Definition:** Loops allow you to repeat code multiple times.

### For Loop
```python
# Iterate over list
fruits = ["apple", "banana", "cherry"]
for fruit in fruits:
    print(fruit)

# Iterate over range
for i in range(5):
    print(i)  # 0, 1, 2, 3, 4

# With enumerate
for index, fruit in enumerate(fruits):
    print(f"{index}: {fruit}")

# With zip
names = ["Alice", "Bob"]
ages = [25, 30]
for name, age in zip(names, ages):
    print(f"{name} is {age}")
```

### While Loop
```python
count = 0
while count < 5:
    print(count)
    count += 1

# With break
while True:
    user_input = input("Enter 'quit' to exit: ")
    if user_input == 'quit':
        break
```

### Loop Control
```python
# break - exit loop
for i in range(10):
    if i == 5:
        break  # Exit at 5
    print(i)

# continue - skip iteration
for i in range(10):
    if i % 2 == 0:
        continue  # Skip even numbers
    print(i)

# else clause (runs if no break)
for i in range(5):
    print(i)
else:
    print("Loop completed!")
```""",

    "decorator": """## 🎀 Decorators in Python

**Definition:** A decorator is a function that modifies the behavior of another function or class.

### Basic Decorator
```python
def my_decorator(func):
    def wrapper():
        print("Before function call")
        func()
        print("After function call")
    return wrapper

@my_decorator
def say_hello():
    print("Hello!")

say_hello()
# Before function call
# Hello!
# After function call
```

### Decorator with Arguments
```python
def my_decorator(func):
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__}")
        result = func(*args, **kwargs)
        print(f"Finished {func.__name__}")
        return result
    return wrapper

@my_decorator
def add(a, b):
    return a + b

print(add(2, 3))
# Calling add
# Finished add
# 5
```

### Common Built-in Decorators
```python
class MyClass:
    @staticmethod
    def static_method():
        print("No self needed")
    
    @classmethod
    def class_method(cls):
        print(f"Class: {cls.__name__}")
    
    @property
    def my_property(self):
        return self._value
```

### Practical Example: Timing
```python
import time

def timer(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} took {end-start:.4f}s")
        return result
    return wrapper

@timer
def slow_function():
    time.sleep(1)
```""",

    "exception": """## ⚠️ Exception Handling in Python

**Definition:** Exceptions are errors that occur during program execution. Exception handling lets you manage these errors gracefully.

### Try-Except
```python
try:
    result = 10 / 0
except ZeroDivisionError:
    print("Cannot divide by zero!")
```

### Multiple Exceptions
```python
try:
    value = int("not a number")
except ValueError:
    print("Invalid number format")
except TypeError:
    print("Type error occurred")
except Exception as e:
    print(f"Unexpected error: {e}")
```

### Try-Except-Else-Finally
```python
try:
    file = open("data.txt", "r")
    content = file.read()
except FileNotFoundError:
    print("File not found")
else:
    print("File read successfully")
    print(content)
finally:
    print("Cleanup complete")
    # Always runs
```

### Raising Exceptions
```python
def validate_age(age):
    if age < 0:
        raise ValueError("Age cannot be negative")
    if age > 150:
        raise ValueError("Age seems unrealistic")
    return age

try:
    validate_age(-5)
except ValueError as e:
    print(f"Validation error: {e}")
```

### Custom Exceptions
```python
class InvalidEmailError(Exception):
    def __init__(self, email):
        self.email = email
        super().__init__(f"Invalid email: {email}")

def validate_email(email):
    if "@" not in email:
        raise InvalidEmailError(email)
```""",

    "recursion": """## 🔁 Recursion in Python

**Definition:** Recursion is when a function calls itself to solve a problem by breaking it into smaller subproblems.

### Basic Structure
```python
def recursive_function(input):
    # Base case (stopping condition)
    if base_condition:
        return base_value
    
    # Recursive case
    return recursive_function(smaller_input)
```

### Classic Examples

**Factorial:**
```python
def factorial(n):
    if n <= 1:  # Base case
        return 1
    return n * factorial(n - 1)  # Recursive case

print(factorial(5))  # 120
```

**Fibonacci:**
```python
def fibonacci(n):
    if n <= 1:  # Base cases
        return n
    return fibonacci(n-1) + fibonacci(n-2)

print(fibonacci(10))  # 55
```

**Sum of List:**
```python
def sum_list(lst):
    if not lst:  # Base case: empty list
        return 0
    return lst[0] + sum_list(lst[1:])
```

### Tips for Recursion
1. **Always have a base case** - prevents infinite recursion
2. **Progress toward base case** - each call should be smaller
3. **Trust the recursion** - assume recursive calls work
4. **Consider memoization** - cache results for efficiency

### Memoization Example
```python
from functools import lru_cache

@lru_cache(maxsize=None)
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
```""",

    "data type": """## 📊 Data Types in Python

Python has several built-in data types organized into categories:

### Numeric Types
```python
# Integer (int) - whole numbers
x = 42
big = 10**100  # Arbitrary precision

# Float - decimal numbers
y = 3.14
scientific = 2.5e-3  # 0.0025

# Complex - complex numbers
z = 3 + 4j
```

### Sequence Types
```python
# String (str) - text
name = "Python"
multiline = \"\"\"Multiple
lines\"\"\"

# List - mutable ordered collection
numbers = [1, 2, 3, 4, 5]

# Tuple - immutable ordered collection
point = (10, 20)
```

### Mapping Type
```python
# Dictionary (dict) - key-value pairs
person = {"name": "Alice", "age": 25}
```

### Set Types
```python
# Set - unordered unique elements
unique = {1, 2, 3}

# Frozenset - immutable set
frozen = frozenset([1, 2, 3])
```

### Boolean Type
```python
# bool - True or False
is_valid = True
is_empty = False
```

### None Type
```python
# NoneType - represents absence of value
result = None
```

### Type Checking
```python
x = 42
print(type(x))        # <class 'int'>
print(isinstance(x, int))  # True
print(isinstance(x, (int, float)))  # True
```""",

    "oop": """## 🎭 Object-Oriented Programming (OOP)

OOP is a programming paradigm based on the concept of "objects" with data and behavior.

### The Four Pillars of OOP

#### 1. Encapsulation
Bundling data and methods that work on that data within a single unit.
```python
class BankAccount:
    def __init__(self, balance):
        self._balance = balance  # Protected attribute
    
    def deposit(self, amount):
        if amount > 0:
            self._balance += amount
    
    def get_balance(self):
        return self._balance
```

#### 2. Inheritance
Creating new classes based on existing classes.
```python
class Animal:
    def speak(self):
        pass

class Dog(Animal):
    def speak(self):
        return "Woof!"

class Cat(Animal):
    def speak(self):
        return "Meow!"
```

#### 3. Polymorphism
Objects of different classes responding to the same method call.
```python
def animal_sound(animal):
    print(animal.speak())

animal_sound(Dog())  # Woof!
animal_sound(Cat())  # Meow!
```

#### 4. Abstraction
Hiding complex implementation details behind simple interfaces.
```python
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self):
        pass

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius
    
    def area(self):
        return 3.14 * self.radius ** 2
```

### Advanced OOP Concepts

**Multiple Inheritance:**
```python
class A:
    def method(self):
        return "A"

class B:
    def method(self):
        return "B"

class C(A, B):  # Inherits from both
    pass
```

**Method Resolution Order (MRO):**
```python
print(C.__mro__)  # Shows inheritance order
```""",

    "regex": """## 🔍 Regular Expressions (Regex)

Regular expressions are powerful patterns for matching and manipulating text.

### Basic Patterns
```python
import re

text = "Contact: john@email.com or jane@email.com"

# Find first match
match = re.search(r'\\w+@\\w+\\.\\w+', text)
print(match.group())  # john@email.com

# Find all matches
emails = re.findall(r'\\w+@\\w+\\.\\w+', text)
print(emails)  # ['john@email.com', 'jane@email.com']
```

### Common Patterns
| Pattern | Meaning |
|---------|---------|
| `.` | Any character except newline |
| `\\d` | Digit (0-9) |
| `\\w` | Word character (a-z, A-Z, 0-9, _) |
| `\\s` | Whitespace |
| `*` | 0 or more |
| `+` | 1 or more |
| `?` | 0 or 1 |
| `{n}` | Exactly n times |
| `[abc]` | a, b, or c |
| `^` | Start of string |
| `$` | End of string |

### Example 1: Validate Phone Number
```python
def validate_phone(phone):
    pattern = r'^\\d{3}-\\d{3}-\\d{4}$'
    return bool(re.match(pattern, phone))

print(validate_phone("123-456-7890"))  # True
print(validate_phone("12-456-7890"))   # False
```

### Example 2: Extract Information
```python
text = "Order #12345 was placed on 2024-01-15"

# Extract order number
order = re.search(r'#(\\d+)', text)
print(order.group(1))  # 12345

# Extract date
date = re.search(r'(\\d{4}-\\d{2}-\\d{2})', text)
print(date.group(1))  # 2024-01-15
```

### Substitution
```python
text = "Hello World"
result = re.sub(r'World', 'Python', text)
print(result)  # Hello Python
```""",
}


def get_concept_explanation(topic: str) -> Optional[str]:
    """
    Get explanation for a Python concept.
    
    Args:
        topic: The concept to look up (case-insensitive)
        
    Returns:
        Explanation string if found, None otherwise
    """
    topic_lower = topic.lower().strip()
    
    # Direct match
    if topic_lower in CONCEPTS:
        return CONCEPTS[topic_lower]
    
    # Try common variations
    variations = {
        'classes': 'class',
        'objects': 'object',
        'functions': 'function',
        'lists': 'list',
        'dictionaries': 'dictionary',
        'dicts': 'dictionary',
        'loops': 'loop',
        'for loop': 'loop',
        'while loop': 'loop',
        'decorators': 'decorator',
        'exceptions': 'exception',
        'error handling': 'exception',
        'data types': 'data type',
        'datatypes': 'data type',
        'types': 'data type',
        'object oriented programming': 'oop',
        'object-oriented programming': 'oop',
        'oops': 'oop',
        'regular expressions': 'regex',
        'regexp': 'regex',
        're': 'regex',
        'pattern matching': 'regex',
    }
    
    if topic_lower in variations:
        return CONCEPTS.get(variations[topic_lower])
    
    # Partial match
    for key in CONCEPTS:
        if key in topic_lower or topic_lower in key:
            return CONCEPTS[key]
    
    return None


# List of all available concepts
AVAILABLE_CONCEPTS = list(CONCEPTS.keys())

