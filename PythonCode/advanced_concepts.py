# advanced_concepts.py
"""
Advanced Python Concepts - Modern Python 3.7+ Features
Contains comprehensive explanations for advanced Python topics.
"""

# =============================================================================
# ADVANCED PYTHON CONCEPTS DICTIONARY
# =============================================================================

ADVANCED_CONCEPTS = {
    
    "async": """## ⚡ Async/Await in Python

**Definition:** Asynchronous programming allows concurrent execution of I/O-bound operations without blocking the main thread.

### Basic Async Function
```python
import asyncio

async def fetch_data():
    print("Start fetching...")
    await asyncio.sleep(2)  # Simulate I/O operation
    print("Done fetching!")
    return "Data"

# Run async function
result = asyncio.run(fetch_data())
print(result)  # "Data"
```

### Running Multiple Tasks Concurrently
```python
async def task1():
    await asyncio.sleep(1)
    return "Task 1 done"

async def task2():
    await asyncio.sleep(2)
    return "Task 2 done"

async def main():
    # Run concurrently - takes 2 seconds total, not 3!
    results = await asyncio.gather(task1(), task2())
    print(results)  # ['Task 1 done', 'Task 2 done']

asyncio.run(main())
```

### Real-World Example: Concurrent API Calls
```python
import asyncio
import aiohttp

async def fetch_url(session, url):
    async with session.get(url) as response:
        return await response.json()

async def fetch_all_users():
    urls = [
        'https://api.example.com/user/1',
        'https://api.example.com/user/2',
        'https://api.example.com/user/3'
    ]
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_url(session, url) for url in urls]
        results = await asyncio.gather(*tasks)
        return results

# Fetch all 3 users concurrently!
users = asyncio.run(fetch_all_users())
```

### When to Use Async
| Use Case | Async? | Why |
|----------|--------|-----|
| API calls | ✅ Yes | I/O-bound, waiting for network |
| File I/O | ✅ Yes | Waiting for disk operations |
| Database queries | ✅ Yes | Waiting for DB response |
| Heavy computation | ❌ No | CPU-bound, use multiprocessing |
| Simple scripts | ❌ No | Adds complexity unnecessarily |

### Async vs Threading vs Multiprocessing
| Feature | Async | Threading | Multiprocessing |
|---------|-------|-----------|-----------------|
| Best for | I/O-bound | I/O-bound | CPU-bound |
| GIL blocked | No | Yes | No (separate processes) |
| Memory | Low | Medium | High |
| Complexity | Medium | High | Medium |

### Common Async Patterns
```python
# Pattern 1: Timeout
try:
    result = await asyncio.wait_for(long_task(), timeout=5.0)
except asyncio.TimeoutError:
    print("Task took too long!")

# Pattern 2: Create task and continue
task = asyncio.create_task(background_work())
# Do other stuff while task runs
await task  # Wait when needed

# Pattern 3: Async context manager
async with aiofiles.open('file.txt') as f:
    content = await f.read()

# Pattern 4: Async iterator
async for item in async_generator():
    await process(item)
```

### Key Concepts
- **async def**: Defines a coroutine function
- **await**: Suspends execution until awaitable completes
- **asyncio.run()**: Entry point for async programs
- **asyncio.gather()**: Run multiple coroutines concurrently
- **asyncio.create_task()**: Schedule coroutine for execution

**💡 Rule of Thumb:** Use async for I/O-bound operations where you're waiting for external resources (network, disk, database).""",

    "await": """## ⚡ Async/Await in Python

**Definition:** The `await` keyword suspends execution of an async function until the awaited operation completes.

### How await Works
```python
async def example():
    print("Before await")
    result = await some_async_operation()  # Pauses here
    print("After await")  # Resumes when operation completes
    return result
```

### Key Points
- Can only be used inside `async def` functions
- Suspends the coroutine, allowing other tasks to run
- Returns the result of the awaited operation
- Works with coroutines, Tasks, and Futures

See 'async' for comprehensive async/await documentation.""",

    "asyncio": """## ⚡ asyncio Module

**Definition:** Python's built-in library for writing asynchronous code using async/await syntax.

### Key Functions
| Function | Purpose |
|----------|---------|
| `asyncio.run(coro)` | Run the main coroutine |
| `asyncio.gather(*coros)` | Run coroutines concurrently |
| `asyncio.create_task(coro)` | Schedule coroutine as Task |
| `asyncio.sleep(seconds)` | Async sleep |
| `asyncio.wait_for(coro, timeout)` | Add timeout to coroutine |

### Example
```python
import asyncio

async def main():
    # Create tasks for concurrent execution
    task1 = asyncio.create_task(fetch_data())
    task2 = asyncio.create_task(process_data())
    
    # Wait for both to complete
    results = await asyncio.gather(task1, task2)
    return results

asyncio.run(main())
```

See 'async' for comprehensive async/await documentation.""",

    "dataclass": """## 📦 Dataclasses in Python

**Definition:** Automatically generate special methods like `__init__`, `__repr__`, `__eq__` for classes (Python 3.7+).

### Basic Dataclass
```python
from dataclasses import dataclass

@dataclass
class Person:
    name: str
    age: int
    city: str = "Unknown"  # Default value

# Automatic __init__
person = Person("Alice", 30)
print(person)  # Person(name='Alice', age=30, city='Unknown')

# Automatic __eq__
person2 = Person("Alice", 30)
print(person == person2)  # True
```

### Dataclass vs Regular Class
```python
# Regular Class - Lots of boilerplate!
class PersonRegular:
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age
    
    def __repr__(self):
        return f"PersonRegular(name={self.name!r}, age={self.age!r})"
    
    def __eq__(self, other):
        if not isinstance(other, PersonRegular):
            return NotImplemented
        return self.name == other.name and self.age == other.age

# Dataclass - Clean and simple!
@dataclass
class PersonData:
    name: str
    age: int
    # All above methods auto-generated!
```

### Advanced Features
```python
from dataclasses import dataclass, field

# Frozen (Immutable)
@dataclass(frozen=True)
class Point:
    x: int
    y: int
    # point.x = 5  # Error! Immutable

# Ordered (for sorting)
@dataclass(order=True)
class Score:
    points: int
    name: str = field(compare=False)  # Exclude from comparison

# Mutable default values
@dataclass
class Inventory:
    items: list = field(default_factory=list)  # Safe mutable default
    count: int = field(init=False, default=0)  # Not in __init__
    
    def __post_init__(self):
        self.count = len(self.items)
```

### Field Options
| Option | Purpose | Example |
|--------|---------|---------|
| `default` | Default value | `field(default=0)` |
| `default_factory` | Callable for mutable defaults | `field(default_factory=list)` |
| `init=False` | Exclude from __init__ | `field(init=False)` |
| `repr=False` | Exclude from __repr__ | `field(repr=False)` |
| `compare=False` | Exclude from comparisons | `field(compare=False)` |

### Decorator Options
```python
@dataclass(
    init=True,        # Generate __init__ (default: True)
    repr=True,        # Generate __repr__ (default: True)
    eq=True,          # Generate __eq__ (default: True)
    order=False,      # Generate __lt__, __le__, etc. (default: False)
    frozen=False,     # Make immutable (default: False)
)
class Config:
    setting: str
    value: int
```

### Post-Init Processing
```python
@dataclass
class Rectangle:
    width: float
    height: float
    area: float = field(init=False)
    
    def __post_init__(self):
        # Called after __init__
        self.area = self.width * self.height

rect = Rectangle(10, 5)
print(rect.area)  # 50.0
```

### When to Use Dataclasses
| Use Dataclass | Use Regular Class |
|---------------|-------------------|
| Data containers | Complex behavior |
| Configuration objects | Heavy inheritance |
| API responses | Database models (use ORM) |
| Value objects | Active objects with logic |

**💡 Benefit:** Dataclasses reduce boilerplate code by 60-80% for simple data-holding classes!""",

    "pathlib": """## 📁 Pathlib in Python

**Definition:** Object-oriented file path handling (Python 3.4+), cleaner and more intuitive than os.path.

### Basic Usage
```python
from pathlib import Path

# Current directory and home
current = Path('.')
home = Path.home()
cwd = Path.cwd()

# Create paths with / operator
file_path = Path('data') / 'users' / 'info.txt'
print(file_path)  # data/users/info.txt

# Check existence
if file_path.exists():
    print("File exists")
if file_path.is_file():
    print("It's a file")
if file_path.is_dir():
    print("It's a directory")
```

### Path Properties
```python
path = Path('/home/user/documents/report.pdf')

print(path.name)       # 'report.pdf'
print(path.stem)       # 'report'
print(path.suffix)     # '.pdf'
print(path.suffixes)   # ['.pdf']
print(path.parent)     # '/home/user/documents'
print(path.parents[0]) # '/home/user/documents'
print(path.parents[1]) # '/home/user'
print(path.anchor)     # '/'
print(path.parts)      # ('/', 'home', 'user', 'documents', 'report.pdf')
```

### Reading and Writing Files
```python
from pathlib import Path

path = Path('data.txt')

# Write and read text
path.write_text("Hello, World!")
content = path.read_text()
print(content)  # Hello, World!

# Write and read bytes
path.write_bytes(b'\\x00\\x01\\x02')
data = path.read_bytes()

# Read lines
lines = path.read_text().splitlines()
```

### Path Operations
```python
path = Path('data/file.txt')

# Change extension
new_path = path.with_suffix('.csv')  # data/file.csv

# Change name
renamed = path.with_name('newfile.txt')  # data/newfile.txt

# Change stem (keep extension)
changed = path.with_stem('renamed')  # data/renamed.txt

# Resolve to absolute
absolute = path.resolve()

# Relative path
relative = path.relative_to(Path.cwd())
```

### Directory Operations
```python
from pathlib import Path

# Create directory (with parents)
Path('new_folder/sub').mkdir(parents=True, exist_ok=True)

# List files
for item in Path('.').iterdir():
    print(item)

# Glob patterns
for txt_file in Path('.').glob('*.txt'):
    print(txt_file)

# Recursive glob
for py_file in Path('.').rglob('*.py'):
    print(py_file)
```

### Pathlib vs os.path
| Task | Pathlib | os.path |
|------|---------|---------|
| Join paths | `Path('a') / 'b'` | `os.path.join('a', 'b')` |
| Get name | `path.name` | `os.path.basename(path)` |
| Get parent | `path.parent` | `os.path.dirname(path)` |
| Get extension | `path.suffix` | `os.path.splitext(path)[1]` |
| Check exists | `path.exists()` | `os.path.exists(path)` |
| Is file | `path.is_file()` | `os.path.isfile(path)` |
| Is directory | `path.is_dir()` | `os.path.isdir(path)` |
| Absolute | `path.resolve()` | `os.path.abspath(path)` |
| Home | `Path.home()` | `os.path.expanduser('~')` |

### Real-World Example
```python
from pathlib import Path
import json

def process_config_files(config_dir):
    config_path = Path(config_dir)
    
    if not config_path.exists():
        config_path.mkdir(parents=True)
    
    configs = []
    for json_file in config_path.glob('*.json'):
        data = json.loads(json_file.read_text())
        configs.append(data)
        print(f"Loaded: {json_file.name}")
    
    return configs
```

**💡 Best Practice:** Use Pathlib for all new code. It's more Pythonic, readable, and cross-platform!""",

    "functools": """## 🛠️ Functools Module

**Definition:** Higher-order functions and operations on callable objects. Essential for functional programming in Python.

### @lru_cache - Memoization
```python
from functools import lru_cache

@lru_cache(maxsize=128)
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

# First call: calculates
print(fibonacci(100))  # Fast! Results cached

# Check cache stats
print(fibonacci.cache_info())
# CacheInfo(hits=98, misses=101, maxsize=128, currsize=101)

# Clear cache if needed
fibonacci.cache_clear()
```

### @cache - Simple Unlimited Cache (Python 3.9+)
```python
from functools import cache

@cache  # Unlimited cache size
def expensive_function(n):
    # Some expensive computation
    return n ** 2

print(expensive_function(5))  # Computed
print(expensive_function(5))  # Cached!
```

### @wraps - Preserve Function Metadata
```python
from functools import wraps

def my_decorator(func):
    @wraps(func)  # Preserves __name__, __doc__, etc.
    def wrapper(*args, **kwargs):
        print("Before")
        result = func(*args, **kwargs)
        print("After")
        return result
    return wrapper

@my_decorator
def greet(name):
    '''Greet someone by name.'''
    return f"Hello, {name}"

print(greet.__name__)  # 'greet' (not 'wrapper')
print(greet.__doc__)   # 'Greet someone by name.'
```

### partial - Partial Function Application
```python
from functools import partial
from operator import mul

# Create specialized functions
double = partial(mul, 2)
triple = partial(mul, 3)

print(double(5))  # 10
print(triple(5))  # 15

# With keyword arguments
def power(base, exponent):
    return base ** exponent

square = partial(power, exponent=2)
cube = partial(power, exponent=3)

print(square(5))  # 25
print(cube(3))    # 27
```

### reduce - Cumulative Operations
```python
from functools import reduce

numbers = [1, 2, 3, 4, 5]

# Sum
total = reduce(lambda x, y: x + y, numbers)
print(total)  # 15

# Product
product = reduce(lambda x, y: x * y, numbers)
print(product)  # 120

# Find maximum
maximum = reduce(lambda a, b: a if a > b else b, numbers)
print(maximum)  # 5

# Flatten nested list
nested = [[1, 2], [3, 4], [5, 6]]
flat = reduce(lambda a, b: a + b, nested)
print(flat)  # [1, 2, 3, 4, 5, 6]
```

### @singledispatch - Function Overloading
```python
from functools import singledispatch

@singledispatch
def process(data):
    raise NotImplementedError("Unsupported type")

@process.register(int)
def _(data):
    return f"Processing int: {data * 2}"

@process.register(str)
def _(data):
    return f"Processing string: {data.upper()}"

@process.register(list)
def _(data):
    return f"Processing list: {len(data)} items"

print(process(5))        # Processing int: 10
print(process("hello"))  # Processing string: HELLO
print(process([1,2,3]))  # Processing list: 3 items
```

### @total_ordering - Generate Comparison Methods
```python
from functools import total_ordering

@total_ordering
class Student:
    def __init__(self, name, grade):
        self.name = name
        self.grade = grade
    
    def __eq__(self, other):
        return self.grade == other.grade
    
    def __lt__(self, other):
        return self.grade < other.grade
    # __le__, __gt__, __ge__ auto-generated!

students = [Student("Alice", 85), Student("Bob", 92)]
print(sorted(students, key=lambda s: s.grade))
```

### Functools Summary
| Function | Purpose | Use Case |
|----------|---------|----------|
| `lru_cache` | Memoization | Expensive recursive functions |
| `cache` | Unlimited cache | Simple caching |
| `wraps` | Preserve metadata | Writing decorators |
| `partial` | Fix arguments | Specialized functions |
| `reduce` | Cumulative ops | Aggregations |
| `singledispatch` | Type dispatch | Function overloading |
| `total_ordering` | Comparisons | Sortable classes |

**💡 Performance Tip:** `lru_cache` can speed up recursive functions by 100x or more!""",

    "iterator": """## 🔄 Iterators in Python

**Definition:** An iterator is an object that implements `__iter__()` and `__next__()` methods, allowing sequential access to elements.

### Understanding Iteration
```python
# What happens behind a for loop
my_list = [1, 2, 3]
for item in my_list:
    print(item)

# Is actually:
iterator = iter(my_list)  # Calls __iter__()
while True:
    try:
        item = next(iterator)  # Calls __next__()
        print(item)
    except StopIteration:
        break
```

### Creating a Custom Iterator
```python
class Counter:
    def __init__(self, start, end):
        self.current = start
        self.end = end
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.current > self.end:
            raise StopIteration
        self.current += 1
        return self.current - 1

counter = Counter(1, 5)
for num in counter:
    print(num)  # 1, 2, 3, 4, 5
```

### Iterable vs Iterator
| Iterable | Iterator |
|----------|----------|
| Has `__iter__()` | Has both `__iter__()` and `__next__()` |
| Can be looped over | Produces values one at a time |
| List, tuple, string, dict | iter(list), file objects |
| Can create many iterators | Single pass only |

```python
# List is iterable
my_list = [1, 2, 3]  # Iterable
iterator = iter(my_list)  # Iterator

print(next(iterator))  # 1
print(next(iterator))  # 2
print(next(iterator))  # 3
# next(iterator)  # StopIteration!
```

### Iterator vs Generator
```python
# Iterator Class - More code
class Fibonacci:
    def __init__(self, n):
        self.n = n
        self.a, self.b = 0, 1
        self.count = 0
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.count >= self.n:
            raise StopIteration
        result = self.a
        self.a, self.b = self.b, self.a + self.b
        self.count += 1
        return result

# Generator Function - Much simpler!
def fibonacci(n):
    a, b = 0, 1
    for _ in range(n):
        yield a
        a, b = b, a + b

# Both work the same
for num in Fibonacci(10):
    print(num)

for num in fibonacci(10):
    print(num)
```

### Built-in Iterators from itertools
```python
from itertools import count, cycle, repeat, chain

# count - Infinite counter
counter = count(start=10, step=2)
print(next(counter))  # 10
print(next(counter))  # 12

# cycle - Repeat sequence infinitely
colors = cycle(['red', 'green', 'blue'])
for _ in range(5):
    print(next(colors))  # red, green, blue, red, green

# repeat - Repeat value
threes = repeat(3, times=4)
print(list(threes))  # [3, 3, 3, 3]

# chain - Combine iterables
combined = chain([1, 2], [3, 4], [5, 6])
print(list(combined))  # [1, 2, 3, 4, 5, 6]
```

### Real-World Example: File Reader
```python
class ChunkReader:
    '''Read file in chunks for memory efficiency.'''
    def __init__(self, filename, chunk_size=1024):
        self.filename = filename
        self.chunk_size = chunk_size
        self.file = None
    
    def __iter__(self):
        self.file = open(self.filename, 'r')
        return self
    
    def __next__(self):
        chunk = self.file.read(self.chunk_size)
        if not chunk:
            self.file.close()
            raise StopIteration
        return chunk

# Process large file without loading into memory
for chunk in ChunkReader('large_file.txt'):
    process(chunk)
```

### When to Use
| Use Iterator | Use Generator | Use List |
|--------------|---------------|----------|
| Complex state | Simple iteration | Small data |
| Reusable class | One-time use | Need indexing |
| Object-oriented | Functional | Multiple passes |

**💡 Memory Efficiency:** Iterators process one item at a time, never storing the entire sequence in memory!""",

    "property": """## 🎛️ Property Decorators in Python

**Definition:** Properties provide getter, setter, and deleter methods for attributes while maintaining a clean interface.

### Basic Property
```python
class Circle:
    def __init__(self, radius):
        self._radius = radius
    
    @property
    def radius(self):
        '''Getter for radius.'''
        return self._radius
    
    @radius.setter
    def radius(self, value):
        '''Setter with validation.'''
        if value < 0:
            raise ValueError("Radius cannot be negative")
        self._radius = value
    
    @radius.deleter
    def radius(self):
        '''Delete the radius.'''
        del self._radius
    
    @property
    def area(self):
        '''Computed property (read-only).'''
        return 3.14159 * self._radius ** 2

circle = Circle(5)
print(circle.radius)  # 5 (calls getter)
circle.radius = 10    # Calls setter with validation
print(circle.area)    # 314.159 (computed)
# circle.area = 100   # Error! No setter defined
del circle.radius     # Calls deleter
```

### Read-Only Properties
```python
class Person:
    def __init__(self, first_name, last_name):
        self._first = first_name
        self._last = last_name
    
    @property
    def full_name(self):
        '''Read-only computed property.'''
        return f"{self._first} {self._last}"
    
    @property
    def initials(self):
        return f"{self._first[0]}.{self._last[0]}."

person = Person("John", "Doe")
print(person.full_name)  # John Doe
print(person.initials)   # J.D.
# person.full_name = "Jane"  # Error! Read-only
```

### Property with Validation
```python
class Temperature:
    def __init__(self, celsius):
        self._celsius = celsius
    
    @property
    def celsius(self):
        return self._celsius
    
    @celsius.setter
    def celsius(self, value):
        if value < -273.15:
            raise ValueError("Below absolute zero!")
        self._celsius = value
    
    @property
    def fahrenheit(self):
        return self._celsius * 9/5 + 32
    
    @fahrenheit.setter
    def fahrenheit(self, value):
        self.celsius = (value - 32) * 5/9

temp = Temperature(25)
print(temp.fahrenheit)  # 77.0
temp.fahrenheit = 86
print(temp.celsius)     # 30.0
```

### Lazy Property (Computed Once)
```python
class DataLoader:
    def __init__(self, filename):
        self.filename = filename
        self._data = None
    
    @property
    def data(self):
        '''Load data only when first accessed.'''
        if self._data is None:
            print("Loading data...")
            with open(self.filename) as f:
                self._data = f.read()
        return self._data

loader = DataLoader('big_file.txt')
# Data not loaded yet
print(loader.data)  # Loading data... (first access)
print(loader.data)  # Returns cached (no loading)
```

### Property vs Java-style Getters/Setters
```python
# Java-style (verbose)
class PersonOld:
    def get_name(self):
        return self._name
    def set_name(self, value):
        self._name = value

person.set_name("Alice")  # Verbose!

# Pythonic with property
class PersonNew:
    @property
    def name(self):
        return self._name
    @name.setter
    def name(self, value):
        self._name = value

person.name = "Alice"  # Clean!
```

### When to Use Properties
| Use Property | Use Method |
|--------------|------------|
| Attribute-like access | Complex operations |
| Computed values | Multiple return values |
| Validation on set | Side effects expected |
| Backward compatibility | Long-running tasks |

**💡 Best Practice:** Use properties to maintain a clean interface while adding validation or computation logic.""",

    "descriptor": """## 🔍 Descriptors in Python

**Definition:** Descriptors define how attribute access is handled through `__get__`, `__set__`, and `__delete__` methods.

### Basic Descriptor
```python
class Descriptor:
    def __init__(self, name=None):
        self.name = name
    
    def __set_name__(self, owner, name):
        '''Called when descriptor is assigned to class.'''
        self.name = name
    
    def __get__(self, instance, owner):
        '''Called when attribute is accessed.'''
        if instance is None:
            return self
        return instance.__dict__.get(self.name)
    
    def __set__(self, instance, value):
        '''Called when attribute is set.'''
        print(f"Setting {self.name} to {value}")
        instance.__dict__[self.name] = value
    
    def __delete__(self, instance):
        '''Called when attribute is deleted.'''
        del instance.__dict__[self.name]

class MyClass:
    attr = Descriptor()

obj = MyClass()
obj.attr = 42    # Setting attr to 42
print(obj.attr)  # 42
```

### Validator Descriptor
```python
class Validator:
    def __init__(self, min_val=None, max_val=None):
        self.min_val = min_val
        self.max_val = max_val
    
    def __set_name__(self, owner, name):
        self.name = name
    
    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__.get(self.name)
    
    def __set__(self, instance, value):
        if self.min_val is not None and value < self.min_val:
            raise ValueError(f"{self.name} must be >= {self.min_val}")
        if self.max_val is not None and value > self.max_val:
            raise ValueError(f"{self.name} must be <= {self.max_val}")
        instance.__dict__[self.name] = value

class Person:
    age = Validator(0, 150)
    height = Validator(0, 300)
    
    def __init__(self, age, height):
        self.age = age
        self.height = height

person = Person(25, 175)  # OK
# person.age = 200  # ValueError: age must be <= 150
```

### Type Checking Descriptor
```python
class TypedProperty:
    def __init__(self, expected_type):
        self.expected_type = expected_type
    
    def __set_name__(self, owner, name):
        self.name = name
    
    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__.get(self.name)
    
    def __set__(self, instance, value):
        if not isinstance(value, self.expected_type):
            raise TypeError(f"{self.name} must be {self.expected_type.__name__}")
        instance.__dict__[self.name] = value

class User:
    name = TypedProperty(str)
    age = TypedProperty(int)
    
    def __init__(self, name, age):
        self.name = name
        self.age = age

user = User("Alice", 30)  # OK
# user.age = "thirty"  # TypeError: age must be int
```

### Descriptor Types
| Type | Has `__set__` | Behavior |
|------|---------------|----------|
| Data Descriptor | ✅ Yes | Takes precedence over instance dict |
| Non-Data Descriptor | ❌ No | Instance dict takes precedence |

### How Properties Use Descriptors
```python
# @property is actually a descriptor!
class property_like:
    def __init__(self, fget=None, fset=None):
        self.fget = fget
        self.fset = fset
    
    def __get__(self, instance, owner):
        if instance is None:
            return self
        return self.fget(instance)
    
    def __set__(self, instance, value):
        if self.fset is None:
            raise AttributeError("can't set attribute")
        self.fset(instance, value)
    
    def setter(self, fset):
        return type(self)(self.fget, fset)
```

**💡 Advanced Insight:** Descriptors are the mechanism behind properties, methods, staticmethods, and classmethods!""",

    "metaclass": """## 🎭 Metaclasses in Python

**Definition:** A metaclass is a class of a class that defines how classes behave. Classes are instances of metaclasses.

### Understanding Metaclasses
```python
# Everything is an object in Python
x = 5
print(type(x))  # <class 'int'>

# Classes are objects too!
class MyClass:
    pass

print(type(MyClass))  # <class 'type'>
# 'type' is the default metaclass!

# type() can also create classes dynamically
MyClass = type('MyClass', (object,), {'x': 5})
```

### Basic Metaclass
```python
class Meta(type):
    def __new__(cls, name, bases, dct):
        print(f"Creating class: {name}")
        return super().__new__(cls, name, bases, dct)
    
    def __init__(cls, name, bases, dct):
        print(f"Initializing class: {name}")
        super().__init__(name, bases, dct)

class MyClass(metaclass=Meta):
    pass

# Output:
# Creating class: MyClass
# Initializing class: MyClass
```

### Singleton Pattern with Metaclass
```python
class Singleton(type):
    _instances = {}
    
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class Database(metaclass=Singleton):
    def __init__(self):
        print("Connecting to database...")

db1 = Database()  # Connecting to database...
db2 = Database()  # (no output - returns same instance)
print(db1 is db2)  # True
```

### Auto-Registration Metaclass
```python
class PluginRegistry(type):
    plugins = {}
    
    def __new__(cls, name, bases, dct):
        new_class = super().__new__(cls, name, bases, dct)
        # Register all non-base classes
        if bases:  # Skip the base Plugin class
            cls.plugins[name] = new_class
        return new_class

class Plugin(metaclass=PluginRegistry):
    pass

class PDFPlugin(Plugin):
    pass

class ImagePlugin(Plugin):
    pass

print(PluginRegistry.plugins)
# {'PDFPlugin': <class 'PDFPlugin'>, 'ImagePlugin': <class 'ImagePlugin'>}
```

### Validation Metaclass
```python
class ValidatedMeta(type):
    def __new__(cls, name, bases, dct):
        # Enforce that all methods have docstrings
        for key, value in dct.items():
            if callable(value) and not key.startswith('_'):
                if not value.__doc__:
                    raise TypeError(f"Method {key} must have a docstring")
        return super().__new__(cls, name, bases, dct)
```

### Metaclass vs Decorator
```python
# Metaclass - affects class creation
class Meta(type):
    def __new__(cls, name, bases, dct):
        dct['meta_added'] = True
        return super().__new__(cls, name, bases, dct)

# Decorator - simpler for most cases!
def add_attribute(cls):
    cls.decorator_added = True
    return cls

@add_attribute
class MyClass:
    pass

# Decorator is simpler for most use cases!
```

### When to Use Metaclasses
| Use Metaclass | Use Alternative |
|---------------|-----------------|
| Framework development | Decorators for most cases |
| API validation | Class decorators |
| Auto-registration | Registry pattern |
| ORM frameworks | Simpler approaches |

**💡 Tim Peters Quote:** "Metaclasses are deeper magic than 99% of users should ever worry about. If you wonder whether you need them, you don't."

**Real Use Cases:**
- ✅ Django ORM (model registration)
- ✅ SQLAlchemy (declarative base)
- ✅ Plugin systems
- ❌ Most application code""",

    "collections": """## 📚 Collections Module

**Definition:** Specialized container datatypes providing alternatives to Python's built-in list, dict, set, and tuple.

### Counter - Count Elements
```python
from collections import Counter

# Count words
words = ["apple", "banana", "apple", "cherry", "banana", "apple"]
counter = Counter(words)
print(counter)  # Counter({'apple': 3, 'banana': 2, 'cherry': 1})

# Most common
print(counter.most_common(2))  # [('apple', 3), ('banana', 2)]

# Count characters
text = "mississippi"
char_count = Counter(text)
print(char_count)  # Counter({'i': 4, 's': 4, 'p': 2, 'm': 1})

# Arithmetic operations
c1 = Counter(a=3, b=1)
c2 = Counter(a=1, b=2)
print(c1 + c2)  # Counter({'a': 4, 'b': 3})
print(c1 - c2)  # Counter({'a': 2})
```

### defaultdict - Default Values
```python
from collections import defaultdict

# Group by first letter
words = ["apple", "ant", "banana", "bear", "cherry"]
groups = defaultdict(list)
for word in words:
    groups[word[0]].append(word)

print(dict(groups))
# {'a': ['apple', 'ant'], 'b': ['banana', 'bear'], 'c': ['cherry']}

# Count occurrences (no KeyError!)
counts = defaultdict(int)
for char in "hello":
    counts[char] += 1
print(dict(counts))  # {'h': 1, 'e': 1, 'l': 2, 'o': 1}

# Nested defaultdict
tree = lambda: defaultdict(tree)
users = tree()
users['john']['age'] = 30
users['john']['city'] = 'NYC'
```

### deque - Double-Ended Queue
```python
from collections import deque

# Efficient operations on both ends
dq = deque([1, 2, 3])
dq.append(4)        # Right: [1, 2, 3, 4]
dq.appendleft(0)    # Left: [0, 1, 2, 3, 4]
dq.pop()            # Remove right: [0, 1, 2, 3]
dq.popleft()        # Remove left: [1, 2, 3]

# Rotation
dq = deque([1, 2, 3, 4, 5])
dq.rotate(2)   # Rotate right: [4, 5, 1, 2, 3]
dq.rotate(-1)  # Rotate left: [5, 1, 2, 3, 4]

# Fixed-size queue (auto-drops oldest)
recent = deque(maxlen=3)
recent.extend([1, 2, 3])  # [1, 2, 3]
recent.append(4)          # [2, 3, 4] - 1 dropped
```

### namedtuple - Named Tuples
```python
from collections import namedtuple

# Define structure
Point = namedtuple('Point', ['x', 'y'])
p = Point(10, 20)

# Access by name or index
print(p.x, p.y)    # 10 20
print(p[0], p[1])  # 10 20

# Immutable (like regular tuple)
# p.x = 15  # Error!

# Great for CSV data
Person = namedtuple('Person', 'name age city')
people = [
    Person('Alice', 30, 'NYC'),
    Person('Bob', 25, 'LA'),
]
for p in people:
    print(f"{p.name}: {p.age}")
```

### OrderedDict - Ordered Dictionary
```python
from collections import OrderedDict

# Note: Regular dicts are ordered in Python 3.7+
# OrderedDict has extra features

ordered = OrderedDict()
ordered['first'] = 1
ordered['second'] = 2
ordered['third'] = 3

# Move to end
ordered.move_to_end('first')
print(list(ordered.keys()))  # ['second', 'third', 'first']

# Move to beginning
ordered.move_to_end('third', last=False)
print(list(ordered.keys()))  # ['third', 'second', 'first']
```

### ChainMap - Multiple Dictionaries
```python
from collections import ChainMap

# Combine dicts with fallback
defaults = {'color': 'blue', 'size': 'medium'}
user_prefs = {'size': 'large'}
config = ChainMap(user_prefs, defaults)

print(config['color'])  # 'blue' (from defaults)
print(config['size'])   # 'large' (from user_prefs)

# Use case: configuration with fallbacks
cli_args = {'verbose': True}
env_vars = {'debug': True}
defaults = {'verbose': False, 'debug': False}
config = ChainMap(cli_args, env_vars, defaults)
```

### Collections Summary
| Type | Purpose | Key Feature |
|------|---------|-------------|
| `Counter` | Count elements | Arithmetic operations |
| `defaultdict` | Default values | No KeyError |
| `deque` | Double-ended queue | O(1) both ends |
| `namedtuple` | Named fields | Immutable, lightweight |
| `OrderedDict` | Ordered dict | move_to_end() |
| `ChainMap` | Multiple dicts | Fallback lookups |

**💡 Performance Tip:** deque is much faster than list for left-side operations (appendleft, popleft)!""",

    "enumerate": """## 🔢 Enumerate Function

**Definition:** Add a counter to an iterable, yielding (index, value) tuples.

### Basic Usage
```python
fruits = ['apple', 'banana', 'cherry']

# Basic enumeration
for index, fruit in enumerate(fruits):
    print(f"{index}: {fruit}")
# 0: apple
# 1: banana
# 2: cherry

# Custom start index
for index, fruit in enumerate(fruits, start=1):
    print(f"{index}. {fruit}")
# 1. apple
# 2. banana
# 3. cherry
```

### Common Patterns
```python
# Pattern 1: Find index of element
names = ['Alice', 'Bob', 'Charlie', 'David']
for i, name in enumerate(names):
    if name == 'Charlie':
        print(f"Found at index {i}")  # Found at index 2

# Pattern 2: Modify list with index
numbers = [10, 20, 30, 40]
for i, num in enumerate(numbers):
    numbers[i] = num * 2
print(numbers)  # [20, 40, 60, 80]

# Pattern 3: Index in list comprehension
squares = [x**2 for i, x in enumerate([1, 2, 3, 4]) if i % 2 == 0]
print(squares)  # [1, 9] (indices 0 and 2)

# Pattern 4: Count lines in file
with open('file.txt') as f:
    for line_num, line in enumerate(f, start=1):
        print(f"Line {line_num}: {line.strip()}")
```

### Enumerate vs range(len())
```python
items = ['a', 'b', 'c']

# ❌ Don't do this
for i in range(len(items)):
    print(i, items[i])

# ✅ Do this instead
for i, item in enumerate(items):
    print(i, item)
```

### Converting to Dict
```python
fruits = ['apple', 'banana', 'cherry']

# Index as key
fruit_dict = dict(enumerate(fruits))
print(fruit_dict)  # {0: 'apple', 1: 'banana', 2: 'cherry'}

# With custom start
fruit_dict = dict(enumerate(fruits, start=1))
print(fruit_dict)  # {1: 'apple', 2: 'banana', 3: 'cherry'}
```

### With zip for Multiple Lists
```python
names = ['Alice', 'Bob', 'Charlie']
scores = [85, 92, 78]

for i, (name, score) in enumerate(zip(names, scores), start=1):
    print(f"#{i}: {name} scored {score}")
# #1: Alice scored 85
# #2: Bob scored 92
# #3: Charlie scored 78
```

**💡 Best Practice:** Always use `enumerate()` instead of `range(len())` for cleaner, more Pythonic code!""",

    "zip": """## 🤐 Zip Function

**Definition:** Combine multiple iterables element-wise, yielding tuples of corresponding elements.

### Basic Usage
```python
names = ['Alice', 'Bob', 'Charlie']
ages = [25, 30, 35]
cities = ['NYC', 'LA', 'Chicago']

# Combine iterables
for name, age, city in zip(names, ages, cities):
    print(f"{name}, {age}, from {city}")
# Alice, 25, from NYC
# Bob, 30, from LA
# Charlie, 35, from Chicago
```

### Create Dictionary
```python
keys = ['name', 'age', 'city']
values = ['Alice', 25, 'NYC']

person = dict(zip(keys, values))
print(person)  # {'name': 'Alice', 'age': 25, 'city': 'NYC'}
```

### Unzip (Transpose)
```python
pairs = [(1, 'a'), (2, 'b'), (3, 'c')]

# Unzip using * operator
numbers, letters = zip(*pairs)
print(numbers)  # (1, 2, 3)
print(letters)  # ('a', 'b', 'c')

# Convert to lists
numbers = list(numbers)
letters = list(letters)
```

### Zip Stops at Shortest
```python
short = [1, 2, 3]
long = [10, 20, 30, 40, 50]

result = list(zip(short, long))
print(result)  # [(1, 10), (2, 20), (3, 30)]
# Stops at length 3!

# Use zip_longest for all elements
from itertools import zip_longest
result = list(zip_longest(short, long, fillvalue=0))
print(result)  # [(1, 10), (2, 20), (3, 30), (0, 40), (0, 50)]
```

### Common Patterns
```python
# Pattern 1: Sum corresponding elements
list1 = [1, 2, 3, 4]
list2 = [10, 20, 30, 40]
sums = [a + b for a, b in zip(list1, list2)]
print(sums)  # [11, 22, 33, 44]

# Pattern 2: Filter based on condition
names = ['Alice', 'Bob', 'Charlie', 'David']
ages = [25, 17, 30, 15]
adults = [name for name, age in zip(names, ages) if age >= 18]
print(adults)  # ['Alice', 'Charlie']

# Pattern 3: Build lookup table
fruits = ['apple', 'banana', 'cherry']
prices = [1.5, 0.5, 2.0]
price_lookup = dict(zip(fruits, prices))
print(price_lookup['banana'])  # 0.5

# Pattern 4: Parallel iteration with index
for i, (name, score) in enumerate(zip(names, ages)):
    print(f"#{i+1}: {name}")
```

### Transpose Matrix
```python
matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]

transposed = list(zip(*matrix))
print(transposed)
# [(1, 4, 7), (2, 5, 8), (3, 6, 9)]

# Convert to list of lists
transposed = [list(row) for row in zip(*matrix)]
```

### Performance Note
```python
# zip returns an iterator (memory efficient)
result = zip([1, 2, 3], [10, 20, 30])
print(next(result))  # (1, 10)
print(next(result))  # (2, 20)

# Convert to list only if needed
result = list(zip([1, 2, 3], [10, 20, 30]))
```

**💡 Key Point:** zip() stops at the shortest iterable. Use `itertools.zip_longest()` if you need all elements!""",

    "f-string": """## 🎨 F-Strings (Formatted String Literals)

**Definition:** Modern string formatting syntax (Python 3.6+), faster and more readable than format() and % formatting.

### Basic Usage
```python
name = "Alice"
age = 30

# Simple substitution
print(f"My name is {name} and I'm {age} years old")
# My name is Alice and I'm 30 years old
```

### Expressions Inside F-Strings
```python
x = 10
y = 20

# Math expressions
print(f"{x} + {y} = {x + y}")  # 10 + 20 = 30
print(f"Is {x} even? {x % 2 == 0}")  # Is 10 even? True

# Function calls
def square(n):
    return n ** 2

print(f"Square of 5 is {square(5)}")  # Square of 5 is 25

# Method calls
text = "hello"
print(f"{text.upper()}")  # HELLO

# List comprehension
numbers = [1, 2, 3, 4, 5]
print(f"Squares: {[n**2 for n in numbers]}")
# Squares: [1, 4, 9, 16, 25]
```

### Number Formatting
```python
pi = 3.14159265359

# Decimal places
print(f"{pi:.2f}")   # 3.14
print(f"{pi:.4f}")   # 3.1416

# Padding and width
num = 42
print(f"{num:5d}")   # '   42' (width 5)
print(f"{num:05d}")  # '00042' (zero-padded)

# Thousands separator
big_num = 1000000
print(f"{big_num:,}")  # 1,000,000
print(f"{big_num:_}")  # 1_000_000

# Percentage
ratio = 0.756
print(f"{ratio:.1%}")  # 75.6%

# Scientific notation
large = 1234567890
print(f"{large:e}")    # 1.234568e+09
print(f"{large:.2e}")  # 1.23e+09

# Binary, Octal, Hex
num = 42
print(f"{num:b}")  # 101010 (binary)
print(f"{num:o}")  # 52 (octal)
print(f"{num:x}")  # 2a (hex)
print(f"{num:X}")  # 2A (HEX)
```

### Alignment and Padding
```python
text = "Python"

# Left align (default for strings)
print(f"{text:<10}")   # 'Python    '

# Right align
print(f"{text:>10}")   # '    Python'

# Center align
print(f"{text:^10}")   # '  Python  '

# With fill character
print(f"{text:*<10}")  # 'Python****'
print(f"{text:=>10}")  # '====Python'
print(f"{text:-^10}")  # '--Python--'
```

### Debugging (Python 3.8+)
```python
x = 10
y = 20
z = x + y

# Old way
print(f"x: {x}, y: {y}, z: {z}")

# New way with = operator
print(f"{x=}, {y=}, {z=}")     # x=10, y=20, z=30
print(f"{x + y=}")              # x + y=30
print(f"{len('hello')=}")       # len('hello')=5
```

### Date and Time
```python
from datetime import datetime

now = datetime.now()

print(f"{now:%Y-%m-%d}")           # 2026-01-16
print(f"{now:%Y-%m-%d %H:%M:%S}")  # 2026-01-16 14:30:45
print(f"{now:%B %d, %Y}")          # January 16, 2026
print(f"{now:%A}")                 # Friday
print(f"{now:%I:%M %p}")           # 02:30 PM
```

### Dictionary Access
```python
person = {'name': 'Alice', 'age': 30}

# Direct access
print(f"{person['name']} is {person['age']}")
# Alice is 30
```

### Escape Braces
```python
# Use double braces
print(f"{{x}} = {5}")  # {x} = 5
```

### F-String vs Other Methods
```python
name = "Alice"
age = 30

# % formatting (old)
msg = "Name: %s, Age: %d" % (name, age)

# str.format() (old)
msg = "Name: {}, Age: {}".format(name, age)

# F-string (modern, fastest!)
msg = f"Name: {name}, Age: {age}"
```

### Performance Comparison
| Method | Speed | Readability |
|--------|-------|-------------|
| f-string | ⭐⭐⭐ Fastest | ⭐⭐⭐ Best |
| str.format() | ⭐⭐ Medium | ⭐⭐ Good |
| % formatting | ⭐ Slowest | ⭐ Poor |

**💡 Best Practice:** Use f-strings for all string formatting in Python 3.6+. They're the fastest and most readable option!""",

    "fstring": """## 🎨 F-Strings (Formatted String Literals)

See 'f-string' for comprehensive documentation.

### Quick Reference
```python
name = "Alice"
num = 42
pi = 3.14159

# Basic
f"{name}"           # Alice

# Width and alignment
f"{name:>10}"       # '     Alice'
f"{name:<10}"       # 'Alice     '
f"{name:^10}"       # '  Alice   '

# Numbers
f"{num:05d}"        # 00042
f"{pi:.2f}"         # 3.14
f"{num:,}"          # 1,000,000

# Debug (3.8+)
f"{name=}"          # name='Alice'
```

**💡 Key Point:** F-strings are the modern, fastest, and most readable way to format strings in Python 3.6+.""",
}

# =============================================================================
# TAGS FOR SEARCH AND CATEGORIZATION
# =============================================================================

ADVANCED_TAGS = [
    # Async programming
    "async", "await", "asyncio", "coroutine", "async/await",
    
    # Modern features
    "dataclass", "dataclasses",
    
    # Path handling
    "pathlib", "path",
    
    # Functools
    "functools", "lru_cache", "cache", "wraps", "partial", "reduce",
    "singledispatch", "total_ordering", "cmp_to_key",
    
    # Iterators
    "iterator", "iterable", "__iter__", "__next__",
    
    # Properties and descriptors
    "property", "descriptor", "getter", "setter",
    
    # Metaclasses
    "metaclass", "type", "__new__", "__init__",
    
    # Collections
    "collections", "counter", "defaultdict", "deque", "namedtuple",
    "ordereddict", "chainmap",
    
    # Built-in functions
    "enumerate", "zip", "zip_longest",
    
    # String formatting
    "f-string", "fstring", "format string", "string formatting",
]
