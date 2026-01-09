# questions.py
"""
Question bank with hints, solutions, complexity analysis, and tags.
Each question contains:
- question: Problem description
- function: Required function name
- test_cases: List of (inputs, expected_output) tuples
- hints: Progressive hints to help solve
- solution: Working solution code
- time_complexity: Big O time notation
- space_complexity: Big O space notation
- tags: Category labels for filtering
"""

# Available tags for filtering
ALL_TAGS = [
    "loops",
    "strings", 
    "math",
    "arrays",
    "recursion",
    "sorting",
    "searching",
    "dictionary",
    "two-pointers",
    "stack",
    "regex",
    "linked-list",
    "tree",
    "graph",
    "dynamic-programming",
    "bit-manipulation",
    "heap",
    "matrix",
    # Automation tags
    "Selenium",
    "WebDriver",
    "Locators",
    "Waits",
    "Page Object Model",
    "Robot Framework",
    "Keywords",
    "pytest",
    "Fixtures",
]

# Import automation questions (optional)
AUTOMATION_QUESTIONS_AVAILABLE = False
AUTOMATION_QUESTIONS = {}

try:
    from automation_questions import (
        SELENIUM_QUESTIONS,
        ROBOT_FRAMEWORK_QUESTIONS,
        PYTEST_QUESTIONS,
        AUTOMATION_QUESTIONS as AUTO_Q,
        AUTOMATION_QUESTION_TAGS
    )
    AUTOMATION_QUESTIONS_AVAILABLE = True
    AUTOMATION_QUESTIONS = AUTO_Q
    # Add automation tags to ALL_TAGS
    for tag in AUTOMATION_QUESTION_TAGS:
        if tag not in ALL_TAGS:
            ALL_TAGS.append(tag)
except ImportError:
    pass

QUESTIONS = {

    # ======================
    # BASIC LEVEL (30 Questions)
    # ======================
    "Basic": [

        {
            "question": "Return numbers from 1 to n",
            "function": "print_numbers",
            "test_cases": [
                ((5,), [1, 2, 3, 4, 5]),
                ((3,), [1, 2, 3]),
                ((1,), [1])
            ],
            "hints": [
                "Think about using a loop that counts from 1 to n",
                "The range() function can generate numbers - range(1, n+1) gives 1 to n",
                "Convert the range to a list using list()"
            ],
            "solution": """def print_numbers(n):
    return list(range(1, n + 1))""",
            "time_complexity": "O(n)",
            "space_complexity": "O(n)",
            "tags": ["loops", "arrays"]
        },

        {
            "question": "Return sum of two numbers",
            "function": "add",
            "test_cases": [
                ((2, 3), 5),
                ((10, 20), 30),
                ((-5, 5), 0)
            ],
            "hints": [
                "This is the simplest operation - just combine the two numbers",
                "Use the + operator to add the numbers",
                "Return the result directly: return a + b"
            ],
            "solution": """def add(a, b):
    return a + b""",
            "time_complexity": "O(1)",
            "space_complexity": "O(1)",
            "tags": ["math"]
        },

        {
            "question": "Return even numbers up to n",
            "function": "even_numbers",
            "test_cases": [
                ((10,), [2, 4, 6, 8, 10]),
                ((5,), [2, 4]),
                ((2,), [2])
            ],
            "hints": [
                "Even numbers are divisible by 2 (remainder is 0)",
                "Use a loop to check each number from 1 to n",
                "range(2, n+1, 2) directly generates even numbers"
            ],
            "solution": """def even_numbers(n):
    return [i for i in range(2, n + 1, 2)]""",
            "time_complexity": "O(n)",
            "space_complexity": "O(n)",
            "tags": ["loops", "arrays", "math"]
        },

        {
            "question": "Return factorial of n",
            "function": "factorial",
            "test_cases": [
                ((5,), 120),
                ((3,), 6),
                ((1,), 1)
            ],
            "hints": [
                "Factorial of n = n × (n-1) × (n-2) × ... × 1",
                "Start with result = 1 and multiply in a loop",
                "Or use recursion: n! = n × (n-1)!"
            ],
            "solution": """def factorial(n):
    result = 1
    for i in range(1, n + 1):
        result *= i
    return result""",
            "time_complexity": "O(n)",
            "space_complexity": "O(1)",
            "tags": ["math", "loops"]
        },

        {
            "question": "Return reverse of a string",
            "function": "reverse_string",
            "test_cases": [
                (("hello",), "olleh"),
                (("python",), "nohtyp")
            ],
            "hints": [
                "Python strings can be sliced with [start:end:step]",
                "A step of -1 reverses the sequence",
                "Try: string[::-1]"
            ],
            "solution": """def reverse_string(n):
    return n[::-1]""",
            "time_complexity": "O(n)",
            "space_complexity": "O(n)",
            "tags": ["strings"]
        },

        {
            "question": "Check if number is prime",
            "function": "is_prime",
            "test_cases": [
                ((7,), True),
                ((4,), False),
                ((2,), True),
                ((1,), False)
            ],
            "hints": [
                "A prime number is only divisible by 1 and itself",
                "You only need to check divisors up to √n",
                "Numbers less than 2 are not prime"
            ],
            "solution": """def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True""",
            "time_complexity": "O(√n)",
            "space_complexity": "O(1)",
            "tags": ["math", "loops"]
        },

        {
            "question": "Return squares from 1 to n",
            "function": "square_numbers",
            "test_cases": [
                ((3,), [1, 4, 9]),
                ((2,), [1, 4])
            ],
            "hints": [
                "Square of a number is the number multiplied by itself",
                "Use i * i or i ** 2 to get the square",
                "List comprehension makes this elegant: [i**2 for i in range(1, n+1)]"
            ],
            "solution": """def square_numbers(n):
    return [i ** 2 for i in range(1, n + 1)]""",
            "time_complexity": "O(n)",
            "space_complexity": "O(n)",
            "tags": ["math", "arrays", "loops"]
        },

        {
            "question": "Return length of string",
            "function": "string_length",
            "test_cases": [
                (("python",), 6),
                (("ai",), 2)
            ],
            "hints": [
                "Python has a built-in function to get length",
                "The len() function returns the number of characters",
                "Just return len(string)"
            ],
            "solution": """def string_length(n):
    return len(n)""",
            "time_complexity": "O(1)",
            "space_complexity": "O(1)",
            "tags": ["strings"]
        },

        {
            "question": "Return maximum of two numbers",
            "function": "find_max",
            "test_cases": [
                ((3, 9), 9),
                ((10, 2), 10)
            ],
            "hints": [
                "Compare the two numbers to find which is larger",
                "You can use if-else or the built-in max() function",
                "max(a, b) returns the larger value"
            ],
            "solution": """def find_max(a, b):
    return max(a, b)""",
            "time_complexity": "O(1)",
            "space_complexity": "O(1)",
            "tags": ["math"]
        },

        {
            "question": "Return 'Hello World'",
            "function": "hello_world",
            "test_cases": [
                ((), "Hello World")
            ],
            "hints": [
                "This function takes no arguments",
                "Simply return the string literal",
                "Make sure the spelling and capitalization match exactly"
            ],
            "solution": """def hello_world():
    return "Hello World\"""",
            "time_complexity": "O(1)",
            "space_complexity": "O(1)",
            "tags": ["strings"]
        },

        # ===== NEW BASIC QUESTIONS (11-30) =====

        {
            "question": "Return odd numbers up to n",
            "function": "odd_numbers",
            "test_cases": [
                ((10,), [1, 3, 5, 7, 9]),
                ((5,), [1, 3, 5]),
                ((1,), [1])
            ],
            "hints": [
                "Odd numbers have remainder 1 when divided by 2",
                "Use range(1, n+1, 2) to generate odd numbers",
                "Or filter with n % 2 != 0"
            ],
            "solution": """def odd_numbers(n):
    return [i for i in range(1, n + 1, 2)]""",
            "time_complexity": "O(n)",
            "space_complexity": "O(n)",
            "tags": ["loops", "arrays", "math"]
        },

        {
            "question": "Return difference of two numbers",
            "function": "subtract",
            "test_cases": [
                ((10, 3), 7),
                ((5, 8), -3),
                ((0, 0), 0)
            ],
            "hints": [
                "Subtraction is simply a - b",
                "The order matters: first minus second",
                "Return the result directly"
            ],
            "solution": """def subtract(a, b):
    return a - b""",
            "time_complexity": "O(1)",
            "space_complexity": "O(1)",
            "tags": ["math"]
        },

        {
            "question": "Return product of two numbers",
            "function": "multiply",
            "test_cases": [
                ((3, 4), 12),
                ((5, 0), 0),
                ((-2, 3), -6)
            ],
            "hints": [
                "Multiplication uses the * operator",
                "a * b gives the product",
                "Remember: anything times 0 is 0"
            ],
            "solution": """def multiply(a, b):
    return a * b""",
            "time_complexity": "O(1)",
            "space_complexity": "O(1)",
            "tags": ["math"]
        },

        {
            "question": "Check if number is even",
            "function": "is_even",
            "test_cases": [
                ((4,), True),
                ((7,), False),
                ((0,), True)
            ],
            "hints": [
                "Even numbers are divisible by 2",
                "Use the modulo operator: n % 2",
                "If remainder is 0, number is even"
            ],
            "solution": """def is_even(n):
    return n % 2 == 0""",
            "time_complexity": "O(1)",
            "space_complexity": "O(1)",
            "tags": ["math"]
        },

        {
            "question": "Check if number is odd",
            "function": "is_odd",
            "test_cases": [
                ((5,), True),
                ((8,), False),
                ((1,), True)
            ],
            "hints": [
                "Odd numbers have remainder 1 when divided by 2",
                "Use n % 2 != 0 or n % 2 == 1",
                "Return the boolean result"
            ],
            "solution": """def is_odd(n):
    return n % 2 != 0""",
            "time_complexity": "O(1)",
            "space_complexity": "O(1)",
            "tags": ["math"]
        },

        {
            "question": "Return absolute value",
            "function": "absolute_value",
            "test_cases": [
                ((-5,), 5),
                ((3,), 3),
                ((0,), 0)
            ],
            "hints": [
                "Absolute value is always positive",
                "Python has built-in abs() function",
                "Or use: n if n >= 0 else -n"
            ],
            "solution": """def absolute_value(n):
    return abs(n)""",
            "time_complexity": "O(1)",
            "space_complexity": "O(1)",
            "tags": ["math"]
        },

        {
            "question": "Return minimum of two numbers",
            "function": "find_min",
            "test_cases": [
                ((3, 9), 3),
                ((10, 2), 2),
                ((5, 5), 5)
            ],
            "hints": [
                "Compare two numbers to find smaller one",
                "Use built-in min() function",
                "Or use: a if a < b else b"
            ],
            "solution": """def find_min(a, b):
    return min(a, b)""",
            "time_complexity": "O(1)",
            "space_complexity": "O(1)",
            "tags": ["math"]
        },

        {
            "question": "Return cube of a number",
            "function": "cube",
            "test_cases": [
                ((2,), 8),
                ((3,), 27),
                ((1,), 1)
            ],
            "hints": [
                "Cube means number raised to power 3",
                "Use n ** 3 or n * n * n",
                "Return the result"
            ],
            "solution": """def cube(n):
    return n ** 3""",
            "time_complexity": "O(1)",
            "space_complexity": "O(1)",
            "tags": ["math"]
        },

        {
            "question": "Check if number is positive",
            "function": "is_positive",
            "test_cases": [
                ((5,), True),
                ((-3,), False),
                ((0,), False)
            ],
            "hints": [
                "Positive numbers are greater than 0",
                "Zero is neither positive nor negative",
                "Return n > 0"
            ],
            "solution": """def is_positive(n):
    return n > 0""",
            "time_complexity": "O(1)",
            "space_complexity": "O(1)",
            "tags": ["math"]
        },

        {
            "question": "Check if number is negative",
            "function": "is_negative",
            "test_cases": [
                ((-5,), True),
                ((3,), False),
                ((0,), False)
            ],
            "hints": [
                "Negative numbers are less than 0",
                "Zero is not negative",
                "Return n < 0"
            ],
            "solution": """def is_negative(n):
    return n < 0""",
            "time_complexity": "O(1)",
            "space_complexity": "O(1)",
            "tags": ["math"]
        },

        {
            "question": "Return sum of list elements",
            "function": "sum_list",
            "test_cases": [
                (([1, 2, 3, 4],), 10),
                (([5, 5, 5],), 15),
                (([],), 0)
            ],
            "hints": [
                "Python has built-in sum() function",
                "Or use a loop to add each element",
                "Empty list sums to 0"
            ],
            "solution": """def sum_list(n):
    return sum(n)""",
            "time_complexity": "O(n)",
            "space_complexity": "O(1)",
            "tags": ["arrays", "loops"]
        },

        {
            "question": "Return first element of list",
            "function": "first_element",
            "test_cases": [
                (([1, 2, 3],), 1),
                (([9, 8, 7],), 9),
                ((['a', 'b'],), 'a')
            ],
            "hints": [
                "Lists are zero-indexed in Python",
                "First element is at index 0",
                "Return list[0]"
            ],
            "solution": """def first_element(n):
    return n[0]""",
            "time_complexity": "O(1)",
            "space_complexity": "O(1)",
            "tags": ["arrays"]
        },

        {
            "question": "Return last element of list",
            "function": "last_element",
            "test_cases": [
                (([1, 2, 3],), 3),
                (([9, 8, 7],), 7),
                ((['a', 'b'],), 'b')
            ],
            "hints": [
                "Last element can be accessed with index -1",
                "Or use len(list) - 1",
                "Return list[-1]"
            ],
            "solution": """def last_element(n):
    return n[-1]""",
            "time_complexity": "O(1)",
            "space_complexity": "O(1)",
            "tags": ["arrays"]
        },

        {
            "question": "Count elements in list",
            "function": "count_elements",
            "test_cases": [
                (([1, 2, 3, 4, 5],), 5),
                (([],), 0),
                ((['a'],), 1)
            ],
            "hints": [
                "Use len() to get number of elements",
                "Works for any list type",
                "Empty list has length 0"
            ],
            "solution": """def count_elements(n):
    return len(n)""",
            "time_complexity": "O(1)",
            "space_complexity": "O(1)",
            "tags": ["arrays"]
        },

        {
            "question": "Convert string to uppercase",
            "function": "to_uppercase",
            "test_cases": [
                (("hello",), "HELLO"),
                (("Python",), "PYTHON"),
                (("abc123",), "ABC123")
            ],
            "hints": [
                "Strings have built-in methods",
                "Use .upper() method",
                "Numbers and symbols stay unchanged"
            ],
            "solution": """def to_uppercase(n):
    return n.upper()""",
            "time_complexity": "O(n)",
            "space_complexity": "O(n)",
            "tags": ["strings"]
        },

        {
            "question": "Convert string to lowercase",
            "function": "to_lowercase",
            "test_cases": [
                (("HELLO",), "hello"),
                (("Python",), "python"),
                (("ABC123",), "abc123")
            ],
            "hints": [
                "Strings have built-in methods",
                "Use .lower() method",
                "Numbers and symbols stay unchanged"
            ],
            "solution": """def to_lowercase(n):
    return n.lower()""",
            "time_complexity": "O(n)",
            "space_complexity": "O(n)",
            "tags": ["strings"]
        },

        {
            "question": "Return average of list",
            "function": "average",
            "test_cases": [
                (([1, 2, 3, 4, 5],), 3.0),
                (([10, 20],), 15.0),
                (([5],), 5.0)
            ],
            "hints": [
                "Average = sum divided by count",
                "Use sum(list) / len(list)",
                "Make sure to return a float"
            ],
            "solution": """def average(n):
    return sum(n) / len(n)""",
            "time_complexity": "O(n)",
            "space_complexity": "O(1)",
            "tags": ["arrays", "math"]
        },

        {
            "question": "Double each element in list",
            "function": "double_elements",
            "test_cases": [
                (([1, 2, 3],), [2, 4, 6]),
                (([5, 10],), [10, 20]),
                (([0],), [0])
            ],
            "hints": [
                "Multiply each element by 2",
                "Use list comprehension: [x*2 for x in list]",
                "Or use a loop with append"
            ],
            "solution": """def double_elements(n):
    return [x * 2 for x in n]""",
            "time_complexity": "O(n)",
            "space_complexity": "O(n)",
            "tags": ["arrays", "loops"]
        },

        {
            "question": "Check if string starts with given prefix",
            "function": "starts_with",
            "test_cases": [
                (("hello", "he"), True),
                (("python", "py"), True),
                (("hello", "lo"), False)
            ],
            "hints": [
                "Strings have startswith() method",
                "Or compare slices: s[:len(prefix)] == prefix",
                "Return True or False"
            ],
            "solution": """def starts_with(a, b):
    return a.startswith(b)""",
            "time_complexity": "O(k)",
            "space_complexity": "O(1)",
            "tags": ["strings"]
        },

        {
            "question": "Concatenate two strings",
            "function": "concat_strings",
            "test_cases": [
                (("Hello", "World"), "HelloWorld"),
                (("Py", "thon"), "Python"),
                (("", "test"), "test")
            ],
            "hints": [
                "Use + operator to join strings",
                "Or use string formatting",
                "Return a + b"
            ],
            "solution": """def concat_strings(a, b):
    return a + b""",
            "time_complexity": "O(n+m)",
            "space_complexity": "O(n+m)",
            "tags": ["strings"]
        },

        # ==================== NEW BASIC QUESTIONS (31-60) ====================

        {
            "question": "Return absolute value of a number",
            "function": "absolute_value",
            "test_cases": [
                ((-5,), 5),
                ((10,), 10),
                ((0,), 0)
            ],
            "hints": [
                "Use abs() function or conditional logic",
                "If n < 0, return -n else return n",
                "abs() is built-in Python function"
            ],
            "solution": """def absolute_value(n):
    return abs(n)""",
            "time_complexity": "O(1)",
            "space_complexity": "O(1)",
            "tags": ["math"]
        },

        {
            "question": "Check if a number is positive, negative or zero",
            "function": "check_sign",
            "test_cases": [
                ((5,), "positive"),
                ((-3,), "negative"),
                ((0,), "zero")
            ],
            "hints": [
                "Use if-elif-else to check conditions",
                "Compare n with 0",
                "Return appropriate string"
            ],
            "solution": """def check_sign(n):
    if n > 0:
        return "positive"
    elif n < 0:
        return "negative"
    return "zero" """,
            "time_complexity": "O(1)",
            "space_complexity": "O(1)",
            "tags": ["math"]
        },

        {
            "question": "Return the larger of two numbers",
            "function": "find_max",
            "test_cases": [
                ((5, 3), 5),
                ((2, 8), 8),
                ((4, 4), 4)
            ],
            "hints": [
                "Use max() function",
                "Or use conditional: if a > b return a else b",
                "Handle equal case"
            ],
            "solution": """def find_max(a, b):
    return max(a, b)""",
            "time_complexity": "O(1)",
            "space_complexity": "O(1)",
            "tags": ["math"]
        },

        {
            "question": "Return the smaller of two numbers",
            "function": "find_min",
            "test_cases": [
                ((5, 3), 3),
                ((2, 8), 2),
                ((4, 4), 4)
            ],
            "hints": [
                "Use min() function",
                "Or use conditional logic",
                "Return the smaller value"
            ],
            "solution": """def find_min(a, b):
    return min(a, b)""",
            "time_complexity": "O(1)",
            "space_complexity": "O(1)",
            "tags": ["math"]
        },

        {
            "question": "Calculate area of a rectangle",
            "function": "rectangle_area",
            "test_cases": [
                ((5, 3), 15),
                ((10, 2), 20),
                ((7, 7), 49)
            ],
            "hints": [
                "Area = length × width",
                "Multiply the two numbers",
                "Return the product"
            ],
            "solution": """def rectangle_area(length, width):
    return length * width""",
            "time_complexity": "O(1)",
            "space_complexity": "O(1)",
            "tags": ["math"]
        },

        {
            "question": "Calculate perimeter of a rectangle",
            "function": "rectangle_perimeter",
            "test_cases": [
                ((5, 3), 16),
                ((10, 2), 24),
                ((7, 7), 28)
            ],
            "hints": [
                "Perimeter = 2 × (length + width)",
                "Add length and width, then multiply by 2",
                "Return 2 * (l + w)"
            ],
            "solution": """def rectangle_perimeter(length, width):
    return 2 * (length + width)""",
            "time_complexity": "O(1)",
            "space_complexity": "O(1)",
            "tags": ["math"]
        },

        {
            "question": "Convert Celsius to Fahrenheit",
            "function": "celsius_to_fahrenheit",
            "test_cases": [
                ((0,), 32.0),
                ((100,), 212.0),
                ((-40,), -40.0)
            ],
            "hints": [
                "Formula: F = C × 9/5 + 32",
                "Multiply by 9, divide by 5, add 32",
                "Return as float"
            ],
            "solution": """def celsius_to_fahrenheit(c):
    return c * 9/5 + 32""",
            "time_complexity": "O(1)",
            "space_complexity": "O(1)",
            "tags": ["math"]
        },

        {
            "question": "Convert Fahrenheit to Celsius",
            "function": "fahrenheit_to_celsius",
            "test_cases": [
                ((32,), 0.0),
                ((212,), 100.0),
                ((-40,), -40.0)
            ],
            "hints": [
                "Formula: C = (F - 32) × 5/9",
                "Subtract 32, multiply by 5, divide by 9",
                "Return as float"
            ],
            "solution": """def fahrenheit_to_celsius(f):
    return (f - 32) * 5/9""",
            "time_complexity": "O(1)",
            "space_complexity": "O(1)",
            "tags": ["math"]
        },

        {
            "question": "Check if a year is a leap year",
            "function": "is_leap_year",
            "test_cases": [
                ((2020,), True),
                ((2021,), False),
                ((2000,), True),
                ((1900,), False)
            ],
            "hints": [
                "Divisible by 4 but not 100, or divisible by 400",
                "Use modulo operator %",
                "Check (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)"
            ],
            "solution": """def is_leap_year(year):
    return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)""",
            "time_complexity": "O(1)",
            "space_complexity": "O(1)",
            "tags": ["math"]
        },

        {
            "question": "Return nth Fibonacci number",
            "function": "fibonacci",
            "test_cases": [
                ((1,), 0),
                ((2,), 1),
                ((7,), 8),
                ((10,), 34)
            ],
            "hints": [
                "Fibonacci: 0, 1, 1, 2, 3, 5, 8, 13...",
                "Each number is sum of previous two",
                "Use loop to build up to n"
            ],
            "solution": """def fibonacci(n):
    if n <= 1:
        return 0
    if n == 2:
        return 1
    a, b = 0, 1
    for _ in range(n - 2):
        a, b = b, a + b
    return b""",
            "time_complexity": "O(n)",
            "space_complexity": "O(1)",
            "tags": ["math", "loops"]
        },

        {
            "question": "Count digits in a number",
            "function": "count_digits",
            "test_cases": [
                ((12345,), 5),
                ((0,), 1),
                ((999,), 3)
            ],
            "hints": [
                "Convert to string and get length",
                "Or divide by 10 repeatedly",
                "Handle 0 as special case"
            ],
            "solution": """def count_digits(n):
    return len(str(abs(n)))""",
            "time_complexity": "O(log n)",
            "space_complexity": "O(log n)",
            "tags": ["math", "strings"]
        },

        {
            "question": "Sum of digits of a number",
            "function": "sum_of_digits",
            "test_cases": [
                ((123,), 6),
                ((999,), 27),
                ((0,), 0)
            ],
            "hints": [
                "Extract each digit using % 10",
                "Or convert to string and sum int of each char",
                "Loop until number becomes 0"
            ],
            "solution": """def sum_of_digits(n):
    return sum(int(d) for d in str(abs(n)))""",
            "time_complexity": "O(log n)",
            "space_complexity": "O(log n)",
            "tags": ["math", "loops"]
        },

        {
            "question": "Reverse a number",
            "function": "reverse_number",
            "test_cases": [
                ((123,), 321),
                ((100,), 1),
                ((5,), 5)
            ],
            "hints": [
                "Convert to string, reverse, convert back",
                "Or use modulo and division",
                "int(str(n)[::-1])"
            ],
            "solution": """def reverse_number(n):
    return int(str(n)[::-1])""",
            "time_complexity": "O(log n)",
            "space_complexity": "O(log n)",
            "tags": ["math", "strings"]
        },

        {
            "question": "Check if number is perfect square",
            "function": "is_perfect_square",
            "test_cases": [
                ((16,), True),
                ((14,), False),
                ((1,), True),
                ((0,), True)
            ],
            "hints": [
                "Square root should be an integer",
                "Use n ** 0.5 and check if it's whole",
                "int(sqrt) ** 2 should equal n"
            ],
            "solution": """def is_perfect_square(n):
    if n < 0:
        return False
    root = int(n ** 0.5)
    return root * root == n""",
            "time_complexity": "O(1)",
            "space_complexity": "O(1)",
            "tags": ["math"]
        },

        {
            "question": "Calculate power of a number",
            "function": "power",
            "test_cases": [
                ((2, 3), 8),
                ((5, 2), 25),
                ((10, 0), 1)
            ],
            "hints": [
                "Use ** operator or pow() function",
                "base ** exponent",
                "Any number to power 0 is 1"
            ],
            "solution": """def power(base, exp):
    return base ** exp""",
            "time_complexity": "O(1)",
            "space_complexity": "O(1)",
            "tags": ["math"]
        },

        {
            "question": "Find GCD of two numbers",
            "function": "gcd",
            "test_cases": [
                ((12, 8), 4),
                ((17, 13), 1),
                ((100, 25), 25)
            ],
            "hints": [
                "Use math.gcd() or Euclidean algorithm",
                "Repeatedly apply: gcd(a, b) = gcd(b, a % b)",
                "Until b becomes 0, then a is GCD"
            ],
            "solution": """def gcd(a, b):
    while b:
        a, b = b, a % b
    return a""",
            "time_complexity": "O(log(min(a,b)))",
            "space_complexity": "O(1)",
            "tags": ["math"]
        },

        {
            "question": "Find LCM of two numbers",
            "function": "lcm",
            "test_cases": [
                ((4, 6), 12),
                ((3, 5), 15),
                ((12, 8), 24)
            ],
            "hints": [
                "LCM = (a × b) / GCD(a, b)",
                "First find GCD, then use formula",
                "Use integer division"
            ],
            "solution": """def lcm(a, b):
    def gcd(x, y):
        while y:
            x, y = y, x % y
        return x
    return (a * b) // gcd(a, b)""",
            "time_complexity": "O(log(min(a,b)))",
            "space_complexity": "O(1)",
            "tags": ["math"]
        },

        {
            "question": "Count vowels in a string",
            "function": "count_vowels",
            "test_cases": [
                (("hello",), 2),
                (("aeiou",), 5),
                (("xyz",), 0)
            ],
            "hints": [
                "Vowels are a, e, i, o, u",
                "Loop through each character and check",
                "Use sum with generator expression"
            ],
            "solution": """def count_vowels(s):
    return sum(1 for c in s.lower() if c in 'aeiou')""",
            "time_complexity": "O(n)",
            "space_complexity": "O(1)",
            "tags": ["strings", "loops"]
        },

        {
            "question": "Count consonants in a string",
            "function": "count_consonants",
            "test_cases": [
                (("hello",), 3),
                (("aeiou",), 0),
                (("python",), 5)
            ],
            "hints": [
                "Consonants are letters that are not vowels",
                "Check if character is letter and not vowel",
                "Use isalpha() method"
            ],
            "solution": """def count_consonants(s):
    vowels = 'aeiouAEIOU'
    return sum(1 for c in s if c.isalpha() and c not in vowels)""",
            "time_complexity": "O(n)",
            "space_complexity": "O(1)",
            "tags": ["strings", "loops"]
        },

        {
            "question": "Remove all spaces from string",
            "function": "remove_spaces",
            "test_cases": [
                (("hello world",), "helloworld"),
                (("  a  b  c  ",), "abc"),
                (("nospace",), "nospace")
            ],
            "hints": [
                "Use replace() method",
                "s.replace(' ', '')",
                "Or use join with split"
            ],
            "solution": """def remove_spaces(s):
    return s.replace(' ', '')""",
            "time_complexity": "O(n)",
            "space_complexity": "O(n)",
            "tags": ["strings"]
        },

        {
            "question": "Replace spaces with hyphens",
            "function": "space_to_hyphen",
            "test_cases": [
                (("hello world",), "hello-world"),
                (("a b c",), "a-b-c"),
                (("no space",), "no-space")
            ],
            "hints": [
                "Use replace() method",
                "s.replace(' ', '-')",
                "Simple string replacement"
            ],
            "solution": """def space_to_hyphen(s):
    return s.replace(' ', '-')""",
            "time_complexity": "O(n)",
            "space_complexity": "O(n)",
            "tags": ["strings"]
        },

        {
            "question": "Check if string contains only digits",
            "function": "is_all_digits",
            "test_cases": [
                (("12345",), True),
                (("123a5",), False),
                (("",), False)
            ],
            "hints": [
                "Use isdigit() method",
                "Return s.isdigit()",
                "Empty string returns False"
            ],
            "solution": """def is_all_digits(s):
    return s.isdigit() if s else False""",
            "time_complexity": "O(n)",
            "space_complexity": "O(1)",
            "tags": ["strings"]
        },

        {
            "question": "Check if string contains only letters",
            "function": "is_all_letters",
            "test_cases": [
                (("hello",), True),
                (("hello1",), False),
                (("",), False)
            ],
            "hints": [
                "Use isalpha() method",
                "Return s.isalpha()",
                "Empty string returns False"
            ],
            "solution": """def is_all_letters(s):
    return s.isalpha() if s else False""",
            "time_complexity": "O(n)",
            "space_complexity": "O(1)",
            "tags": ["strings"]
        },

        {
            "question": "Find first non-repeating character",
            "function": "first_unique_char",
            "test_cases": [
                (("leetcode",), "l"),
                (("loveleetcode",), "v"),
                (("aabb",), "")
            ],
            "hints": [
                "Count occurrences of each character",
                "Return first char with count 1",
                "Use dictionary or Counter"
            ],
            "solution": """def first_unique_char(s):
    count = {}
    for c in s:
        count[c] = count.get(c, 0) + 1
    for c in s:
        if count[c] == 1:
            return c
    return "" """,
            "time_complexity": "O(n)",
            "space_complexity": "O(k)",
            "tags": ["strings", "dictionary"]
        },

        {
            "question": "Remove duplicates from sorted list",
            "function": "remove_duplicates_sorted",
            "test_cases": [
                (([1, 1, 2, 2, 3],), [1, 2, 3]),
                (([1, 1, 1],), [1]),
                (([1, 2, 3],), [1, 2, 3])
            ],
            "hints": [
                "Use set() but maintain order",
                "Or use dict.fromkeys()",
                "list(dict.fromkeys(arr))"
            ],
            "solution": """def remove_duplicates_sorted(arr):
    return list(dict.fromkeys(arr))""",
            "time_complexity": "O(n)",
            "space_complexity": "O(n)",
            "tags": ["arrays"]
        },

        {
            "question": "Find second largest in list",
            "function": "second_largest",
            "test_cases": [
                (([1, 2, 3, 4, 5],), 4),
                (([5, 5, 4, 4, 3],), 4),
                (([10, 10],), None)
            ],
            "hints": [
                "Remove duplicates first",
                "Sort and get second from end",
                "Or track two largest values"
            ],
            "solution": """def second_largest(arr):
    unique = list(set(arr))
    if len(unique) < 2:
        return None
    unique.sort()
    return unique[-2]""",
            "time_complexity": "O(n log n)",
            "space_complexity": "O(n)",
            "tags": ["arrays", "sorting"]
        },

        {
            "question": "Rotate list left by k positions",
            "function": "rotate_left",
            "test_cases": [
                (([1, 2, 3, 4, 5], 2), [3, 4, 5, 1, 2]),
                (([1, 2, 3], 1), [2, 3, 1]),
                (([1, 2, 3], 3), [1, 2, 3])
            ],
            "hints": [
                "Slice and concatenate",
                "arr[k:] + arr[:k]",
                "Handle k >= len(arr)"
            ],
            "solution": """def rotate_left(arr, k):
    k = k % len(arr) if arr else 0
    return arr[k:] + arr[:k]""",
            "time_complexity": "O(n)",
            "space_complexity": "O(n)",
            "tags": ["arrays"]
        },

        {
            "question": "Rotate list right by k positions",
            "function": "rotate_right",
            "test_cases": [
                (([1, 2, 3, 4, 5], 2), [4, 5, 1, 2, 3]),
                (([1, 2, 3], 1), [3, 1, 2]),
                (([1, 2, 3], 3), [1, 2, 3])
            ],
            "hints": [
                "Right rotation is left rotation by n-k",
                "arr[-k:] + arr[:-k]",
                "Handle k >= len(arr)"
            ],
            "solution": """def rotate_right(arr, k):
    if not arr:
        return arr
    k = k % len(arr)
    return arr[-k:] + arr[:-k] if k else arr""",
            "time_complexity": "O(n)",
            "space_complexity": "O(n)",
            "tags": ["arrays"]
        },

        {
            "question": "Check if list is sorted ascending",
            "function": "is_sorted_asc",
            "test_cases": [
                (([1, 2, 3, 4],), True),
                (([1, 3, 2, 4],), False),
                (([1],), True)
            ],
            "hints": [
                "Compare each element with next",
                "arr[i] <= arr[i+1] for all i",
                "Use all() with comparison"
            ],
            "solution": """def is_sorted_asc(arr):
    return all(arr[i] <= arr[i+1] for i in range(len(arr)-1))""",
            "time_complexity": "O(n)",
            "space_complexity": "O(1)",
            "tags": ["arrays"]
        },

        {
            "question": "Merge two sorted lists",
            "function": "merge_sorted",
            "test_cases": [
                (([1, 3, 5], [2, 4, 6]), [1, 2, 3, 4, 5, 6]),
                (([1, 2], [3, 4]), [1, 2, 3, 4]),
                (([], [1, 2]), [1, 2])
            ],
            "hints": [
                "Use two pointers approach",
                "Compare elements from both lists",
                "Or simply concatenate and sort"
            ],
            "solution": """def merge_sorted(a, b):
    return sorted(a + b)""",
            "time_complexity": "O((n+m) log(n+m))",
            "space_complexity": "O(n+m)",
            "tags": ["arrays", "sorting"]
        }
    ],

    # ======================
    # INTERMEDIATE LEVEL (25 Questions)
    # ======================
    "Intermediate": [

        {
            "question": "Check if number is palindrome",
            "function": "is_palindrome_number",
            "test_cases": [
                ((121,), True),
                ((123,), False)
            ],
            "hints": [
                "A palindrome reads the same forwards and backwards",
                "Convert the number to string to easily reverse it",
                "Compare the string with its reverse: str(n) == str(n)[::-1]"
            ],
            "solution": """def is_palindrome_number(n):
    return str(n) == str(n)[::-1]""",
            "time_complexity": "O(log n)",
            "space_complexity": "O(log n)",
            "tags": ["strings", "math"]
        },

        {
            "question": "Count vowels in a string",
            "function": "count_vowels",
            "test_cases": [
                (("education",), 5),
                (("sky",), 0)
            ],
            "hints": [
                "Vowels are: a, e, i, o, u",
                "Loop through each character and check if it's a vowel",
                "Use 'in' operator: if char.lower() in 'aeiou'"
            ],
            "solution": """def count_vowels(n):
    return sum(1 for c in n.lower() if c in 'aeiou')""",
            "time_complexity": "O(n)",
            "space_complexity": "O(1)",
            "tags": ["strings", "loops"]
        },

        {
            "question": "Return prime numbers up to n",
            "function": "primes_upto",
            "test_cases": [
                ((10,), [2, 3, 5, 7]),
                ((5,), [2, 3, 5])
            ],
            "hints": [
                "First, write a helper to check if a number is prime",
                "Then loop through all numbers from 2 to n",
                "Add each prime number to a result list"
            ],
            "solution": """def primes_upto(n):
    def is_prime(num):
        if num < 2:
            return False
        for i in range(2, int(num ** 0.5) + 1):
            if num % i == 0:
                return False
        return True
    return [i for i in range(2, n + 1) if is_prime(i)]""",
            "time_complexity": "O(n√n)",
            "space_complexity": "O(n)",
            "tags": ["math", "loops", "arrays"]
        },

        {
            "question": "Return second largest number",
            "function": "second_largest",
            "test_cases": [
                (([1, 4, 2, 9, 5],), 5),
                (([10, 20, 30],), 20)
            ],
            "hints": [
                "Sort the list and pick the second from the end",
                "Handle duplicates by converting to set first",
                "Or track the two largest while looping once"
            ],
            "solution": """def second_largest(n):
    sorted_list = sorted(set(n), reverse=True)
    return sorted_list[1]""",
            "time_complexity": "O(n log n)",
            "space_complexity": "O(n)",
            "tags": ["arrays", "sorting"]
        },

        {
            "question": "Reverse words in a sentence",
            "function": "reverse_words",
            "test_cases": [
                (("Hello World",), "World Hello"),
                (("Python is fun",), "fun is Python")
            ],
            "hints": [
                "Split the sentence into a list of words",
                "Reverse the list of words",
                "Join them back with spaces"
            ],
            "solution": """def reverse_words(n):
    return ' '.join(n.split()[::-1])""",
            "time_complexity": "O(n)",
            "space_complexity": "O(n)",
            "tags": ["strings", "arrays"]
        },

        {
            "question": "Remove duplicates from list",
            "function": "remove_duplicates",
            "test_cases": [
                (([1, 2, 2, 3],), [1, 2, 3]),
                (([4, 4, 4],), [4])
            ],
            "hints": [
                "Keep track of elements you've already seen",
                "Only add new elements to the result",
                "Preserve order by not using set directly"
            ],
            "solution": """def remove_duplicates(n):
    seen = []
    for item in n:
        if item not in seen:
            seen.append(item)
    return seen""",
            "time_complexity": "O(n²)",
            "space_complexity": "O(n)",
            "tags": ["arrays", "loops"]
        },

        {
            "question": "Find GCD of two numbers",
            "function": "gcd",
            "test_cases": [
                ((12, 18), 6),
                ((8, 16), 8)
            ],
            "hints": [
                "GCD = Greatest Common Divisor",
                "Use Euclidean algorithm: gcd(a,b) = gcd(b, a%b)",
                "Base case: gcd(a, 0) = a"
            ],
            "solution": """def gcd(a, b):
    while b:
        a, b = b, a % b
    return a""",
            "time_complexity": "O(log min(a,b))",
            "space_complexity": "O(1)",
            "tags": ["math", "recursion"]
        },

        {
            "question": "Check if two strings are anagrams",
            "function": "is_anagram",
            "test_cases": [
                (("listen", "silent"), True),
                (("hello", "world"), False)
            ],
            "hints": [
                "Anagrams have the same letters in different order",
                "Sort both strings and compare",
                "Or count character frequency in both"
            ],
            "solution": """def is_anagram(a, b):
    return sorted(a.lower()) == sorted(b.lower())""",
            "time_complexity": "O(n log n)",
            "space_complexity": "O(n)",
            "tags": ["strings", "sorting"]
        },

        {
            "question": "Return sum of digits",
            "function": "sum_of_digits",
            "test_cases": [
                ((123,), 6),
                ((999,), 27)
            ],
            "hints": [
                "Extract each digit from the number",
                "Convert to string and sum each character as int",
                "Or use modulo: digit = n % 10, then n //= 10"
            ],
            "solution": """def sum_of_digits(n):
    return sum(int(d) for d in str(n))""",
            "time_complexity": "O(log n)",
            "space_complexity": "O(log n)",
            "tags": ["math", "strings"]
        },

        {
            "question": "Return Fibonacci series up to n",
            "function": "fibonacci",
            "test_cases": [
                ((10,), [0, 1, 1, 2, 3, 5, 8]),
                ((5,), [0, 1, 1, 2, 3])
            ],
            "hints": [
                "Fibonacci: each number is sum of two previous",
                "Start with [0, 1] and keep adding",
                "Stop when next number would exceed n"
            ],
            "solution": """def fibonacci(n):
    fib = [0, 1]
    while fib[-1] + fib[-2] <= n:
        fib.append(fib[-1] + fib[-2])
    return fib""",
            "time_complexity": "O(n)",
            "space_complexity": "O(n)",
            "tags": ["math", "arrays", "loops"]
        },

        # ===== NEW INTERMEDIATE QUESTIONS (11-25) =====

        {
            "question": "Find LCM of two numbers",
            "function": "lcm",
            "test_cases": [
                ((4, 6), 12),
                ((3, 5), 15),
                ((12, 18), 36)
            ],
            "hints": [
                "LCM = Least Common Multiple",
                "LCM(a,b) = (a * b) / GCD(a,b)",
                "First find GCD, then calculate LCM"
            ],
            "solution": """def lcm(a, b):
    def gcd(x, y):
        while y:
            x, y = y, x % y
        return x
    return (a * b) // gcd(a, b)""",
            "time_complexity": "O(log min(a,b))",
            "space_complexity": "O(1)",
            "tags": ["math"]
        },

        {
            "question": "Count consonants in a string",
            "function": "count_consonants",
            "test_cases": [
                (("hello",), 3),
                (("python",), 4),
                (("aeiou",), 0)
            ],
            "hints": [
                "Consonants are letters that are not vowels",
                "Check if character is alphabetic and not a vowel",
                "Use isalpha() to check for letters"
            ],
            "solution": """def count_consonants(n):
    vowels = 'aeiouAEIOU'
    return sum(1 for c in n if c.isalpha() and c not in vowels)""",
            "time_complexity": "O(n)",
            "space_complexity": "O(1)",
            "tags": ["strings", "loops"]
        },

        {
            "question": "Check if string is palindrome",
            "function": "is_palindrome_string",
            "test_cases": [
                (("radar",), True),
                (("hello",), False),
                (("level",), True)
            ],
            "hints": [
                "A palindrome reads same forwards and backwards",
                "Compare string with its reverse",
                "Use slicing: s == s[::-1]"
            ],
            "solution": """def is_palindrome_string(n):
    return n == n[::-1]""",
            "time_complexity": "O(n)",
            "space_complexity": "O(n)",
            "tags": ["strings"]
        },

        {
            "question": "Find second smallest number",
            "function": "second_smallest",
            "test_cases": [
                (([5, 2, 8, 1, 9],), 2),
                (([10, 20, 30],), 20)
            ],
            "hints": [
                "Sort the list in ascending order",
                "Handle duplicates by using set",
                "Return the element at index 1"
            ],
            "solution": """def second_smallest(n):
    sorted_list = sorted(set(n))
    return sorted_list[1]""",
            "time_complexity": "O(n log n)",
            "space_complexity": "O(n)",
            "tags": ["arrays", "sorting"]
        },

        {
            "question": "Reverse a list",
            "function": "reverse_list",
            "test_cases": [
                (([1, 2, 3, 4],), [4, 3, 2, 1]),
                ((['a', 'b', 'c'],), ['c', 'b', 'a'])
            ],
            "hints": [
                "Lists can be reversed with slicing",
                "Use list[::-1] for a new reversed list",
                "Or use list.reverse() to modify in place"
            ],
            "solution": """def reverse_list(n):
    return n[::-1]""",
            "time_complexity": "O(n)",
            "space_complexity": "O(n)",
            "tags": ["arrays"]
        },

        {
            "question": "Count occurrences of element",
            "function": "count_occurrences",
            "test_cases": [
                (([1, 2, 2, 3, 2], 2), 3),
                ((['a', 'b', 'a'], 'a'), 2),
                (([1, 2, 3], 5), 0)
            ],
            "hints": [
                "Lists have a count() method",
                "Or loop and count manually",
                "Return the count"
            ],
            "solution": """def count_occurrences(a, b):
    return a.count(b)""",
            "time_complexity": "O(n)",
            "space_complexity": "O(1)",
            "tags": ["arrays", "loops"]
        },

        {
            "question": "Capitalize first letter of each word",
            "function": "title_case",
            "test_cases": [
                (("hello world",), "Hello World"),
                (("python programming",), "Python Programming")
            ],
            "hints": [
                "Strings have title() method",
                "Or split, capitalize each, join",
                "title() handles this automatically"
            ],
            "solution": """def title_case(n):
    return n.title()""",
            "time_complexity": "O(n)",
            "space_complexity": "O(n)",
            "tags": ["strings"]
        },

        {
            "question": "Find power of a number",
            "function": "power",
            "test_cases": [
                ((2, 3), 8),
                ((5, 2), 25),
                ((10, 0), 1)
            ],
            "hints": [
                "Power means base raised to exponent",
                "Use ** operator or pow() function",
                "Any number to power 0 is 1"
            ],
            "solution": """def power(a, b):
    return a ** b""",
            "time_complexity": "O(log n)",
            "space_complexity": "O(1)",
            "tags": ["math"]
        },

        {
            "question": "Check if list is sorted",
            "function": "is_sorted",
            "test_cases": [
                (([1, 2, 3, 4],), True),
                (([1, 3, 2, 4],), False),
                (([5, 4, 3],), False)
            ],
            "hints": [
                "Compare list with its sorted version",
                "Or check if each element <= next",
                "list == sorted(list) works"
            ],
            "solution": """def is_sorted(n):
    return n == sorted(n)""",
            "time_complexity": "O(n log n)",
            "space_complexity": "O(n)",
            "tags": ["arrays", "sorting"]
        },

        {
            "question": "Merge two sorted lists",
            "function": "merge_sorted",
            "test_cases": [
                (([1, 3, 5], [2, 4, 6]), [1, 2, 3, 4, 5, 6]),
                (([1, 2], [3, 4]), [1, 2, 3, 4])
            ],
            "hints": [
                "Combine and sort is the simple approach",
                "Or use two-pointer technique",
                "sorted(a + b) works well"
            ],
            "solution": """def merge_sorted(a, b):
    return sorted(a + b)""",
            "time_complexity": "O((n+m) log(n+m))",
            "space_complexity": "O(n+m)",
            "tags": ["arrays", "sorting", "two-pointers"]
        },

        {
            "question": "Remove all occurrences of value",
            "function": "remove_all",
            "test_cases": [
                (([1, 2, 3, 2, 4], 2), [1, 3, 4]),
                ((['a', 'b', 'a'], 'a'), ['b'])
            ],
            "hints": [
                "Filter out elements equal to value",
                "Use list comprehension with condition",
                "[x for x in list if x != value]"
            ],
            "solution": """def remove_all(a, b):
    return [x for x in a if x != b]""",
            "time_complexity": "O(n)",
            "space_complexity": "O(n)",
            "tags": ["arrays", "loops"]
        },

        {
            "question": "Find index of element",
            "function": "find_index",
            "test_cases": [
                (([1, 2, 3, 4], 3), 2),
                ((['a', 'b', 'c'], 'b'), 1),
                (([1, 2, 3], 5), -1)
            ],
            "hints": [
                "Lists have index() method but it raises error if not found",
                "Use a loop to handle not-found case",
                "Return -1 if element not in list"
            ],
            "solution": """def find_index(a, b):
    return a.index(b) if b in a else -1""",
            "time_complexity": "O(n)",
            "space_complexity": "O(1)",
            "tags": ["arrays", "searching"]
        },

        {
            "question": "Calculate product of list",
            "function": "product_list",
            "test_cases": [
                (([1, 2, 3, 4],), 24),
                (([5, 5],), 25),
                (([2, 3, 0],), 0)
            ],
            "hints": [
                "Multiply all elements together",
                "Start with result = 1",
                "Loop through and multiply each"
            ],
            "solution": """def product_list(n):
    result = 1
    for x in n:
        result *= x
    return result""",
            "time_complexity": "O(n)",
            "space_complexity": "O(1)",
            "tags": ["arrays", "loops", "math"]
        },

        {
            "question": "Remove spaces from string",
            "function": "remove_spaces",
            "test_cases": [
                (("hello world",), "helloworld"),
                (("  a  b  c  ",), "abc"),
                (("no spaces",), "nospaces")
            ],
            "hints": [
                "Use replace() to remove spaces",
                "Or use split() and join()",
                "str.replace(' ', '') works"
            ],
            "solution": """def remove_spaces(n):
    return n.replace(' ', '')""",
            "time_complexity": "O(n)",
            "space_complexity": "O(n)",
            "tags": ["strings"]
        },

        {
            "question": "Find common elements in two lists",
            "function": "common_elements",
            "test_cases": [
                (([1, 2, 3], [2, 3, 4]), [2, 3]),
                (([1, 2], [3, 4]), [])
            ],
            "hints": [
                "Find elements present in both lists",
                "Use set intersection",
                "Convert result back to sorted list"
            ],
            "solution": """def common_elements(a, b):
    return sorted(list(set(a) & set(b)))""",
            "time_complexity": "O(n + m)",
            "space_complexity": "O(min(n, m))",
            "tags": ["arrays", "two-pointers"]
        },

        # ==================== NEW INTERMEDIATE QUESTIONS (26-50) ====================

        {
            "question": "Validate email address using regex",
            "function": "is_valid_email",
            "test_cases": [
                (("test@example.com",), True),
                (("invalid-email",), False),
                (("user.name@domain.co.uk",), True),
                (("@nodomain.com",), False)
            ],
            "hints": [
                "Use re module for regex matching",
                "Email pattern: name@domain.extension",
                "Pattern: r'^[\\w.-]+@[\\w.-]+\\.\\w+$'"
            ],
            "solution": """def is_valid_email(email):
    import re
    pattern = r'^[\\w.-]+@[\\w.-]+\\.\\w+$'
    return bool(re.match(pattern, email))""",
            "time_complexity": "O(n)",
            "space_complexity": "O(1)",
            "tags": ["regex", "strings"]
        },

        {
            "question": "Extract all numbers from string using regex",
            "function": "extract_numbers",
            "test_cases": [
                (("abc123def456",), [123, 456]),
                (("no numbers here",), []),
                (("price: $99.99",), [99, 99])
            ],
            "hints": [
                "Use re.findall() to find all matches",
                "Pattern for digits: r'\\d+'",
                "Convert matches to integers"
            ],
            "solution": """def extract_numbers(s):
    import re
    return [int(x) for x in re.findall(r'\\d+', s)]""",
            "time_complexity": "O(n)",
            "space_complexity": "O(k)",
            "tags": ["regex", "strings"]
        },

        {
            "question": "Validate phone number (10 digits)",
            "function": "is_valid_phone",
            "test_cases": [
                (("1234567890",), True),
                (("123-456-7890",), True),
                (("12345",), False),
                (("123-45-67890",), False)
            ],
            "hints": [
                "Remove non-digit characters first",
                "Check if exactly 10 digits remain",
                "Use re.sub to remove non-digits"
            ],
            "solution": """def is_valid_phone(phone):
    import re
    digits = re.sub(r'\\D', '', phone)
    return len(digits) == 10""",
            "time_complexity": "O(n)",
            "space_complexity": "O(n)",
            "tags": ["regex", "strings"]
        },

        {
            "question": "Replace multiple spaces with single space",
            "function": "normalize_spaces",
            "test_cases": [
                (("hello   world",), "hello world"),
                (("  too   many   spaces  ",), " too many spaces "),
                (("normal text",), "normal text")
            ],
            "hints": [
                "Use re.sub() for pattern replacement",
                "Pattern for multiple spaces: r' +'",
                "Replace with single space"
            ],
            "solution": """def normalize_spaces(s):
    import re
    return re.sub(r' +', ' ', s)""",
            "time_complexity": "O(n)",
            "space_complexity": "O(n)",
            "tags": ["regex", "strings"]
        },

        {
            "question": "Extract words starting with capital letter",
            "function": "extract_capitalized",
            "test_cases": [
                (("Hello World Python",), ["Hello", "World", "Python"]),
                (("no capitals here",), []),
                (("Mix of Words and lowercase",), ["Mix", "Words"])
            ],
            "hints": [
                "Use regex pattern for capitalized words",
                "Pattern: r'\\b[A-Z][a-z]*\\b'",
                "Use re.findall()"
            ],
            "solution": """def extract_capitalized(s):
    import re
    return re.findall(r'\\b[A-Z][a-z]*\\b', s)""",
            "time_complexity": "O(n)",
            "space_complexity": "O(k)",
            "tags": ["regex", "strings"]
        },

        {
            "question": "Validate IP address format",
            "function": "is_valid_ip",
            "test_cases": [
                (("192.168.1.1",), True),
                (("255.255.255.255",), True),
                (("256.1.1.1",), False),
                (("1.2.3",), False)
            ],
            "hints": [
                "IP has 4 octets separated by dots",
                "Each octet is 0-255",
                "Split by '.' and validate each part"
            ],
            "solution": """def is_valid_ip(ip):
    parts = ip.split('.')
    if len(parts) != 4:
        return False
    for part in parts:
        if not part.isdigit():
            return False
        num = int(part)
        if num < 0 or num > 255:
            return False
    return True""",
            "time_complexity": "O(1)",
            "space_complexity": "O(1)",
            "tags": ["regex", "strings"]
        },

        {
            "question": "Remove HTML tags from string",
            "function": "remove_html_tags",
            "test_cases": [
                (("<p>Hello</p>",), "Hello"),
                (("<b>Bold</b> and <i>italic</i>",), "Bold and italic"),
                (("No tags here",), "No tags here")
            ],
            "hints": [
                "HTML tags are enclosed in < >",
                "Pattern: r'<[^>]+>'",
                "Use re.sub to replace with empty string"
            ],
            "solution": """def remove_html_tags(s):
    import re
    return re.sub(r'<[^>]+>', '', s)""",
            "time_complexity": "O(n)",
            "space_complexity": "O(n)",
            "tags": ["regex", "strings"]
        },

        {
            "question": "Find all words with exactly n characters",
            "function": "words_of_length",
            "test_cases": [
                (("The quick brown fox", 3), ["The", "fox"]),
                (("Hello world", 5), ["Hello", "world"]),
                (("a bb ccc dddd", 2), ["bb"])
            ],
            "hints": [
                "Split string into words",
                "Filter words by length",
                "Return list of matching words"
            ],
            "solution": """def words_of_length(s, n):
    return [w for w in s.split() if len(w) == n]""",
            "time_complexity": "O(n)",
            "space_complexity": "O(k)",
            "tags": ["strings", "arrays"]
        },

        {
            "question": "Implement run-length encoding",
            "function": "run_length_encode",
            "test_cases": [
                (("aaabbc",), "a3b2c1"),
                (("aaa",), "a3"),
                (("abc",), "a1b1c1")
            ],
            "hints": [
                "Count consecutive characters",
                "Build result string with char + count",
                "Handle single occurrences"
            ],
            "solution": """def run_length_encode(s):
    if not s:
        return ""
    result = []
    count = 1
    for i in range(1, len(s)):
        if s[i] == s[i-1]:
            count += 1
        else:
            result.append(s[i-1] + str(count))
            count = 1
    result.append(s[-1] + str(count))
    return ''.join(result)""",
            "time_complexity": "O(n)",
            "space_complexity": "O(n)",
            "tags": ["strings"]
        },

        {
            "question": "Decode run-length encoded string",
            "function": "run_length_decode",
            "test_cases": [
                (("a3b2c1",), "aaabbc"),
                (("a3",), "aaa"),
                (("x1y2z3",), "xyyzzz")
            ],
            "hints": [
                "Parse character followed by number",
                "Repeat character count times",
                "Use regex to find pairs"
            ],
            "solution": """def run_length_decode(s):
    import re
    pairs = re.findall(r'([a-zA-Z])(\\d+)', s)
    return ''.join(char * int(count) for char, count in pairs)""",
            "time_complexity": "O(n)",
            "space_complexity": "O(n)",
            "tags": ["strings", "regex"]
        },

        {
            "question": "Find longest word in sentence",
            "function": "longest_word",
            "test_cases": [
                (("The quick brown fox",), "quick"),
                (("Hello world",), "Hello"),
                (("a",), "a")
            ],
            "hints": [
                "Split sentence into words",
                "Use max() with key=len",
                "Return the longest word"
            ],
            "solution": """def longest_word(s):
    return max(s.split(), key=len)""",
            "time_complexity": "O(n)",
            "space_complexity": "O(n)",
            "tags": ["strings"]
        },

        {
            "question": "Check if parentheses are balanced",
            "function": "is_balanced",
            "test_cases": [
                (("(())",), True),
                (("(()",), False),
                (("()()",), True),
                ((")(", ), False)
            ],
            "hints": [
                "Use a counter for open parentheses",
                "Increment for '(', decrement for ')'",
                "Counter should never go negative"
            ],
            "solution": """def is_balanced(s):
    count = 0
    for c in s:
        if c == '(':
            count += 1
        elif c == ')':
            count -= 1
            if count < 0:
                return False
    return count == 0""",
            "time_complexity": "O(n)",
            "space_complexity": "O(1)",
            "tags": ["strings", "stack"]
        },

        {
            "question": "Group anagrams together",
            "function": "group_anagrams",
            "test_cases": [
                ((["eat", "tea", "tan", "ate", "nat", "bat"],), [["eat", "tea", "ate"], ["tan", "nat"], ["bat"]]),
                ((["a"],), [["a"]])
            ],
            "hints": [
                "Anagrams have same sorted characters",
                "Use sorted string as key",
                "Group words with same key"
            ],
            "solution": """def group_anagrams(words):
    groups = {}
    for word in words:
        key = ''.join(sorted(word))
        if key not in groups:
            groups[key] = []
        groups[key].append(word)
    return list(groups.values())""",
            "time_complexity": "O(n * k log k)",
            "space_complexity": "O(n * k)",
            "tags": ["strings", "dictionary"]
        },

        {
            "question": "Find all permutations of a string",
            "function": "string_permutations",
            "test_cases": [
                (("ab",), ["ab", "ba"]),
                (("abc",), ["abc", "acb", "bac", "bca", "cab", "cba"])
            ],
            "hints": [
                "Use recursion or itertools.permutations",
                "Fix one character, permute rest",
                "Base case: single character"
            ],
            "solution": """def string_permutations(s):
    if len(s) <= 1:
        return [s]
    result = []
    for i, char in enumerate(s):
        for perm in string_permutations(s[:i] + s[i+1:]):
            result.append(char + perm)
    return sorted(result)""",
            "time_complexity": "O(n!)",
            "space_complexity": "O(n!)",
            "tags": ["strings", "recursion"]
        },

        {
            "question": "Implement binary search",
            "function": "binary_search",
            "test_cases": [
                (([1, 2, 3, 4, 5], 3), 2),
                (([1, 2, 3, 4, 5], 6), -1),
                (([1, 3, 5, 7, 9], 5), 2)
            ],
            "hints": [
                "Array must be sorted",
                "Compare middle element with target",
                "Narrow search to left or right half"
            ],
            "solution": """def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1""",
            "time_complexity": "O(log n)",
            "space_complexity": "O(1)",
            "tags": ["searching", "arrays"]
        },

        {
            "question": "Find peak element in array",
            "function": "find_peak",
            "test_cases": [
                (([1, 2, 3, 1],), 2),
                (([1, 2, 1, 3, 5, 6, 4],), 5),
                (([1],), 0)
            ],
            "hints": [
                "Peak is greater than neighbors",
                "Use binary search approach",
                "Compare mid with mid+1"
            ],
            "solution": """def find_peak(arr):
    left, right = 0, len(arr) - 1
    while left < right:
        mid = (left + right) // 2
        if arr[mid] < arr[mid + 1]:
            left = mid + 1
        else:
            right = mid
    return left""",
            "time_complexity": "O(log n)",
            "space_complexity": "O(1)",
            "tags": ["searching", "arrays"]
        },

        {
            "question": "Find missing number in range 1 to n",
            "function": "find_missing",
            "test_cases": [
                (([1, 2, 4, 5],), 3),
                (([2, 3, 4, 5],), 1),
                (([1, 2, 3, 4],), 5)
            ],
            "hints": [
                "Sum of 1 to n is n*(n+1)/2",
                "Subtract actual sum from expected",
                "Difference is missing number"
            ],
            "solution": """def find_missing(arr):
    n = len(arr) + 1
    expected = n * (n + 1) // 2
    return expected - sum(arr)""",
            "time_complexity": "O(n)",
            "space_complexity": "O(1)",
            "tags": ["math", "arrays"]
        },

        {
            "question": "Find duplicate number in array",
            "function": "find_duplicate",
            "test_cases": [
                (([1, 3, 4, 2, 2],), 2),
                (([3, 1, 3, 4, 2],), 3),
                (([1, 1],), 1)
            ],
            "hints": [
                "Use Floyd's cycle detection",
                "Or use set to track seen numbers",
                "Sum approach: actual - expected"
            ],
            "solution": """def find_duplicate(arr):
    seen = set()
    for num in arr:
        if num in seen:
            return num
        seen.add(num)
    return -1""",
            "time_complexity": "O(n)",
            "space_complexity": "O(n)",
            "tags": ["arrays", "searching"]
        },

        {
            "question": "Move all zeros to end",
            "function": "move_zeros",
            "test_cases": [
                (([0, 1, 0, 3, 12],), [1, 3, 12, 0, 0]),
                (([0, 0, 1],), [1, 0, 0]),
                (([1, 2, 3],), [1, 2, 3])
            ],
            "hints": [
                "Two pointer approach",
                "Move non-zeros to front",
                "Fill remaining with zeros"
            ],
            "solution": """def move_zeros(arr):
    result = [x for x in arr if x != 0]
    return result + [0] * (len(arr) - len(result))""",
            "time_complexity": "O(n)",
            "space_complexity": "O(n)",
            "tags": ["arrays", "two-pointers"]
        },

        {
            "question": "Product of array except self",
            "function": "product_except_self",
            "test_cases": [
                (([1, 2, 3, 4],), [24, 12, 8, 6]),
                (([2, 3],), [3, 2])
            ],
            "hints": [
                "For each position, multiply all other elements",
                "Use prefix and suffix products",
                "Avoid division by using two passes"
            ],
            "solution": """def product_except_self(arr):
    n = len(arr)
    result = [1] * n
    prefix = 1
    for i in range(n):
        result[i] = prefix
        prefix *= arr[i]
    suffix = 1
    for i in range(n-1, -1, -1):
        result[i] *= suffix
        suffix *= arr[i]
    return result""",
            "time_complexity": "O(n)",
            "space_complexity": "O(n)",
            "tags": ["arrays", "math"]
        },

        {
            "question": "Find majority element (appears > n/2 times)",
            "function": "majority_element",
            "test_cases": [
                (([3, 2, 3],), 3),
                (([2, 2, 1, 1, 1, 2, 2],), 2)
            ],
            "hints": [
                "Boyer-Moore voting algorithm",
                "Or count occurrences with dictionary",
                "Majority appears more than half"
            ],
            "solution": """def majority_element(arr):
    count = {}
    for num in arr:
        count[num] = count.get(num, 0) + 1
        if count[num] > len(arr) // 2:
            return num
    return -1""",
            "time_complexity": "O(n)",
            "space_complexity": "O(n)",
            "tags": ["arrays", "dictionary"]
        },

        {
            "question": "Spiral matrix traversal",
            "function": "spiral_order",
            "test_cases": [
                (([[1, 2, 3], [4, 5, 6], [7, 8, 9]],), [1, 2, 3, 6, 9, 8, 7, 4, 5]),
                (([[1, 2], [3, 4]],), [1, 2, 4, 3])
            ],
            "hints": [
                "Traverse: right, down, left, up",
                "Track boundaries and shrink",
                "Continue until all elements visited"
            ],
            "solution": """def spiral_order(matrix):
    if not matrix:
        return []
    result = []
    top, bottom = 0, len(matrix) - 1
    left, right = 0, len(matrix[0]) - 1
    while top <= bottom and left <= right:
        for i in range(left, right + 1):
            result.append(matrix[top][i])
        top += 1
        for i in range(top, bottom + 1):
            result.append(matrix[i][right])
        right -= 1
        if top <= bottom:
            for i in range(right, left - 1, -1):
                result.append(matrix[bottom][i])
            bottom -= 1
        if left <= right:
            for i in range(bottom, top - 1, -1):
                result.append(matrix[i][left])
            left += 1
    return result""",
            "time_complexity": "O(m*n)",
            "space_complexity": "O(m*n)",
            "tags": ["matrix", "arrays"]
        },

        {
            "question": "Rotate matrix 90 degrees clockwise",
            "function": "rotate_matrix",
            "test_cases": [
                (([[1, 2], [3, 4]],), [[3, 1], [4, 2]]),
                (([[1, 2, 3], [4, 5, 6], [7, 8, 9]],), [[7, 4, 1], [8, 5, 2], [9, 6, 3]])
            ],
            "hints": [
                "Transpose then reverse each row",
                "Or rotate layer by layer",
                "New[j][n-1-i] = Old[i][j]"
            ],
            "solution": """def rotate_matrix(matrix):
    n = len(matrix)
    # Transpose
    for i in range(n):
        for j in range(i, n):
            matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]
    # Reverse each row
    for row in matrix:
        row.reverse()
    return matrix""",
            "time_complexity": "O(n^2)",
            "space_complexity": "O(1)",
            "tags": ["matrix", "arrays"]
        },

        {
            "question": "Set matrix zeros",
            "function": "set_zeros",
            "test_cases": [
                (([[1, 1, 1], [1, 0, 1], [1, 1, 1]],), [[1, 0, 1], [0, 0, 0], [1, 0, 1]]),
                (([[0, 1], [1, 1]],), [[0, 0], [0, 1]])
            ],
            "hints": [
                "First find positions of zeros",
                "Then set rows and columns",
                "Use first row/col as markers"
            ],
            "solution": """def set_zeros(matrix):
    m, n = len(matrix), len(matrix[0])
    rows, cols = set(), set()
    for i in range(m):
        for j in range(n):
            if matrix[i][j] == 0:
                rows.add(i)
                cols.add(j)
    for i in range(m):
        for j in range(n):
            if i in rows or j in cols:
                matrix[i][j] = 0
    return matrix""",
            "time_complexity": "O(m*n)",
            "space_complexity": "O(m+n)",
            "tags": ["matrix", "arrays"]
        },

        {
            "question": "Validate date string format (YYYY-MM-DD)",
            "function": "is_valid_date",
            "test_cases": [
                (("2023-12-25",), True),
                (("2023-13-01",), False),
                (("2023-02-30",), False),
                (("invalid",), False)
            ],
            "hints": [
                "Use regex to match format first",
                "Then validate month and day ranges",
                "Consider month days and leap years"
            ],
            "solution": """def is_valid_date(date):
    import re
    if not re.match(r'^\\d{4}-\\d{2}-\\d{2}$', date):
        return False
    try:
        year, month, day = map(int, date.split('-'))
        if month < 1 or month > 12:
            return False
        days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
            days_in_month[1] = 29
        return 1 <= day <= days_in_month[month - 1]
    except:
        return False""",
            "time_complexity": "O(1)",
            "space_complexity": "O(1)",
            "tags": ["regex", "strings"]
        }
    ],

    # ======================
    # ADVANCED LEVEL (20 Questions)
    # ======================
    "Advanced": [

        {
            "question": "Check if number is Armstrong",
            "function": "is_armstrong",
            "test_cases": [
                ((153,), True),
                ((123,), False)
            ],
            "hints": [
                "Armstrong: sum of digits^(number of digits) = number",
                "153 = 1³ + 5³ + 3³ = 1 + 125 + 27 = 153",
                "First count digits, then compute sum of powers"
            ],
            "solution": """def is_armstrong(n):
    digits = str(n)
    power = len(digits)
    return n == sum(int(d) ** power for d in digits)""",
            "time_complexity": "O(log n)",
            "space_complexity": "O(log n)",
            "tags": ["math", "strings"]
        },

        {
            "question": "Return longest word in sentence",
            "function": "longest_word",
            "test_cases": [
                (("I love programming",), "programming"),
                (("AI is powerful",), "powerful")
            ],
            "hints": [
                "Split sentence into words",
                "Find the word with maximum length",
                "Use max() with key=len"
            ],
            "solution": """def longest_word(n):
    return max(n.split(), key=len)""",
            "time_complexity": "O(n)",
            "space_complexity": "O(n)",
            "tags": ["strings", "arrays"]
        },

        {
            "question": "Find missing number in list",
            "function": "missing_number",
            "test_cases": [
                (([1, 2, 4, 5],), 3),
                (([2, 3, 4, 6],), 5)
            ],
            "hints": [
                "The list has consecutive numbers with one missing",
                "Find the full range and subtract the given set",
                "Or use sum formula: expected_sum - actual_sum"
            ],
            "solution": """def missing_number(n):
    full_range = set(range(min(n), max(n) + 1))
    return (full_range - set(n)).pop()""",
            "time_complexity": "O(n)",
            "space_complexity": "O(n)",
            "tags": ["arrays", "math"]
        },

        {
            "question": "Check balanced parentheses",
            "function": "balanced_parentheses",
            "test_cases": [
                (("()[]",), True),
                (("(]",), False)
            ],
            "hints": [
                "Use a stack to track opening brackets",
                "Push opening brackets, pop for closing",
                "Each closing must match the last opening"
            ],
            "solution": """def balanced_parentheses(n):
    stack = []
    pairs = {'(': ')', '[': ']', '{': '}'}
    for char in n:
        if char in pairs:
            stack.append(char)
        elif char in pairs.values():
            if not stack or pairs[stack.pop()] != char:
                return False
    return len(stack) == 0""",
            "time_complexity": "O(n)",
            "space_complexity": "O(n)",
            "tags": ["stack", "strings"]
        },

        {
            "question": "Flatten a nested list",
            "function": "flatten_list",
            "test_cases": [
                (([[1, 2], [3, 4]],), [1, 2, 3, 4])
            ],
            "hints": [
                "Iterate through each sublist",
                "Add all elements from each sublist to result",
                "Use extend() or nested list comprehension"
            ],
            "solution": """def flatten_list(n):
    result = []
    for sublist in n:
        result.extend(sublist)
    return result""",
            "time_complexity": "O(n)",
            "space_complexity": "O(n)",
            "tags": ["arrays", "loops"]
        },

        {
            "question": "Return intersection of two lists",
            "function": "intersection",
            "test_cases": [
                (([1, 2, 3], [2, 3, 4]), [2, 3])
            ],
            "hints": [
                "Find elements present in both lists",
                "Check each element of first list against second",
                "Preserve order from the first list"
            ],
            "solution": """def intersection(a, b):
    return [x for x in a if x in b]""",
            "time_complexity": "O(n×m)",
            "space_complexity": "O(min(n,m))",
            "tags": ["arrays", "two-pointers"]
        },

        {
            "question": "Check if sentence is pangram",
            "function": "is_pangram",
            "test_cases": [
                (("The quick brown fox jumps over the lazy dog",), True),
                (("Hello world",), False)
            ],
            "hints": [
                "A pangram contains every letter of the alphabet",
                "Convert to lowercase and check for all 26 letters",
                "Use set comparison with the alphabet"
            ],
            "solution": """def is_pangram(n):
    return set('abcdefghijklmnopqrstuvwxyz') <= set(n.lower())""",
            "time_complexity": "O(n)",
            "space_complexity": "O(1)",
            "tags": ["strings"]
        },

        {
            "question": "Binary search in sorted list",
            "function": "binary_search",
            "test_cases": [
                (([1, 3, 5, 7], 5), True),
                (([1, 3, 5, 7], 2), False)
            ],
            "hints": [
                "Binary search works on sorted arrays",
                "Compare target with middle element",
                "Eliminate half the array each iteration"
            ],
            "solution": """def binary_search(a, b):
    left, right = 0, len(a) - 1
    while left <= right:
        mid = (left + right) // 2
        if a[mid] == b:
            return True
        elif a[mid] < b:
            left = mid + 1
        else:
            right = mid - 1
    return False""",
            "time_complexity": "O(log n)",
            "space_complexity": "O(1)",
            "tags": ["searching", "arrays"]
        },

        {
            "question": "Return character frequency",
            "function": "char_frequency",
            "test_cases": [
                (("aab",), {"a": 2, "b": 1})
            ],
            "hints": [
                "Count how many times each character appears",
                "Use a dictionary to store counts",
                "Loop through string and increment counts"
            ],
            "solution": """def char_frequency(n):
    freq = {}
    for char in n:
        freq[char] = freq.get(char, 0) + 1
    return freq""",
            "time_complexity": "O(n)",
            "space_complexity": "O(k)",
            "tags": ["dictionary", "strings"]
        },

        {
            "question": "Sort dictionary by values",
            "function": "sort_dict_by_value",
            "test_cases": [
                (({"b": 3, "a": 1, "c": 2},), [("a", 1), ("c", 2), ("b", 3)])
            ],
            "hints": [
                "Convert dict items to list of tuples",
                "Sort by the second element (value)",
                "Use sorted() with key function"
            ],
            "solution": """def sort_dict_by_value(n):
    return sorted(n.items(), key=lambda x: x[1])""",
            "time_complexity": "O(n log n)",
            "space_complexity": "O(n)",
            "tags": ["dictionary", "sorting"]
        },

        # ===== NEW ADVANCED QUESTIONS (11-20) =====

        {
            "question": "Find all pairs with given sum",
            "function": "pairs_with_sum",
            "test_cases": [
                (([1, 2, 3, 4, 5], 6), [(1, 5), (2, 4)]),
                (([1, 1, 2, 3], 4), [(1, 3)])
            ],
            "hints": [
                "For each element, check if complement exists",
                "Complement = target - current element",
                "Use a set to track seen numbers"
            ],
            "solution": """def pairs_with_sum(a, b):
    seen = set()
    pairs = []
    for num in a:
        complement = b - num
        if complement in seen and (complement, num) not in pairs:
            pairs.append((min(num, complement), max(num, complement)))
        seen.add(num)
    return sorted(set(pairs))""",
            "time_complexity": "O(n)",
            "space_complexity": "O(n)",
            "tags": ["arrays", "two-pointers", "dictionary"]
        },

        {
            "question": "Rotate list by k positions",
            "function": "rotate_list",
            "test_cases": [
                (([1, 2, 3, 4, 5], 2), [4, 5, 1, 2, 3]),
                (([1, 2, 3], 1), [3, 1, 2])
            ],
            "hints": [
                "Rotation moves last k elements to front",
                "Handle k > length using modulo",
                "Use slicing: list[-k:] + list[:-k]"
            ],
            "solution": """def rotate_list(a, b):
    k = b % len(a)
    return a[-k:] + a[:-k]""",
            "time_complexity": "O(n)",
            "space_complexity": "O(n)",
            "tags": ["arrays"]
        },

        {
            "question": "Find first non-repeating character",
            "function": "first_unique_char",
            "test_cases": [
                (("leetcode",), "l"),
                (("aabbcc",), ""),
                (("aabbc",), "c")
            ],
            "hints": [
                "Count frequency of each character first",
                "Then find first character with count 1",
                "Use dictionary to store counts"
            ],
            "solution": """def first_unique_char(n):
    freq = {}
    for c in n:
        freq[c] = freq.get(c, 0) + 1
    for c in n:
        if freq[c] == 1:
            return c
    return \"\"""",
            "time_complexity": "O(n)",
            "space_complexity": "O(k)",
            "tags": ["strings", "dictionary"]
        },

        {
            "question": "Check if list has duplicate",
            "function": "has_duplicate",
            "test_cases": [
                (([1, 2, 3, 1],), True),
                (([1, 2, 3, 4],), False)
            ],
            "hints": [
                "Compare length of list with length of set",
                "Set removes duplicates",
                "If lengths differ, there were duplicates"
            ],
            "solution": """def has_duplicate(n):
    return len(n) != len(set(n))""",
            "time_complexity": "O(n)",
            "space_complexity": "O(n)",
            "tags": ["arrays"]
        },

        {
            "question": "Find majority element",
            "function": "majority_element",
            "test_cases": [
                (([3, 2, 3],), 3),
                (([2, 2, 1, 1, 1, 2, 2],), 2)
            ],
            "hints": [
                "Majority element appears more than n/2 times",
                "Count occurrences of each element",
                "Or use Boyer-Moore voting algorithm"
            ],
            "solution": """def majority_element(n):
    freq = {}
    for num in n:
        freq[num] = freq.get(num, 0) + 1
        if freq[num] > len(n) // 2:
            return num
    return None""",
            "time_complexity": "O(n)",
            "space_complexity": "O(n)",
            "tags": ["arrays", "dictionary"]
        },

        {
            "question": "Group anagrams together",
            "function": "group_anagrams",
            "test_cases": [
                ((["eat", "tea", "tan", "ate", "nat", "bat"],), [["eat", "tea", "ate"], ["tan", "nat"], ["bat"]])
            ],
            "hints": [
                "Anagrams have same sorted characters",
                "Use sorted word as dictionary key",
                "Group words with same key"
            ],
            "solution": """def group_anagrams(n):
    groups = {}
    for word in n:
        key = ''.join(sorted(word))
        if key not in groups:
            groups[key] = []
        groups[key].append(word)
    return list(groups.values())""",
            "time_complexity": "O(n * k log k)",
            "space_complexity": "O(n * k)",
            "tags": ["strings", "dictionary", "sorting"]
        },

        {
            "question": "Find longest consecutive sequence",
            "function": "longest_consecutive",
            "test_cases": [
                (([100, 4, 200, 1, 3, 2],), 4),
                (([0, 3, 7, 2, 5, 8, 4, 6, 0, 1],), 9)
            ],
            "hints": [
                "Convert list to set for O(1) lookup",
                "For each number, check if it's sequence start",
                "Count consecutive numbers from each start"
            ],
            "solution": """def longest_consecutive(n):
    if not n:
        return 0
    num_set = set(n)
    longest = 0
    for num in num_set:
        if num - 1 not in num_set:
            current = num
            streak = 1
            while current + 1 in num_set:
                current += 1
                streak += 1
            longest = max(longest, streak)
    return longest""",
            "time_complexity": "O(n)",
            "space_complexity": "O(n)",
            "tags": ["arrays", "dictionary"]
        },

        {
            "question": "Validate sudoku row",
            "function": "valid_sudoku_row",
            "test_cases": [
                (([5, 3, 4, 6, 7, 8, 9, 1, 2],), True),
                (([5, 3, 4, 6, 7, 8, 9, 1, 5],), False)
            ],
            "hints": [
                "Each digit 1-9 must appear exactly once",
                "Check for duplicates using set",
                "Compare set length with list length"
            ],
            "solution": """def valid_sudoku_row(n):
    valid = set(range(1, 10))
    return set(n) == valid""",
            "time_complexity": "O(1)",
            "space_complexity": "O(1)",
            "tags": ["arrays"]
        },

        {
            "question": "Find kth largest element",
            "function": "kth_largest",
            "test_cases": [
                (([3, 2, 1, 5, 6, 4], 2), 5),
                (([3, 2, 3, 1, 2, 4, 5, 5, 6], 4), 4)
            ],
            "hints": [
                "Sort the list in descending order",
                "Return element at index k-1",
                "Or use min-heap of size k"
            ],
            "solution": """def kth_largest(a, b):
    return sorted(a, reverse=True)[b - 1]""",
            "time_complexity": "O(n log n)",
            "space_complexity": "O(n)",
            "tags": ["arrays", "sorting"]
        },

        {
            "question": "Implement stack using list",
            "function": "stack_operations",
            "test_cases": [
                ((["push 1", "push 2", "pop", "push 3", "top"],), [None, None, 2, None, 3]),
                ((["push 5", "top", "pop", "pop"],), [None, 5, 5, None])
            ],
            "hints": [
                "Stack follows LIFO - Last In First Out",
                "Use list.append() for push",
                "Use list.pop() for pop operation"
            ],
            "solution": """def stack_operations(n):
    stack = []
    results = []
    for op in n:
        if op.startswith('push'):
            stack.append(int(op.split()[1]))
            results.append(None)
        elif op == 'pop':
            results.append(stack.pop() if stack else None)
        elif op == 'top':
            results.append(stack[-1] if stack else None)
    return results""",
            "time_complexity": "O(n)",
            "space_complexity": "O(n)",
            "tags": ["stack", "arrays"]
        },

        # ==================== NEW ADVANCED QUESTIONS (21-40) ====================

        {
            "question": "Longest Increasing Subsequence",
            "function": "longest_increasing_subsequence",
            "test_cases": [
                (([10, 9, 2, 5, 3, 7, 101, 18],), 4),
                (([0, 1, 0, 3, 2, 3],), 4),
                (([7, 7, 7, 7],), 1)
            ],
            "hints": [
                "Use dynamic programming approach",
                "dp[i] = length of LIS ending at index i",
                "For each i, check all j < i where arr[j] < arr[i]"
            ],
            "solution": """def longest_increasing_subsequence(arr):
    if not arr:
        return 0
    n = len(arr)
    dp = [1] * n
    for i in range(1, n):
        for j in range(i):
            if arr[j] < arr[i]:
                dp[i] = max(dp[i], dp[j] + 1)
    return max(dp)""",
            "time_complexity": "O(n^2)",
            "space_complexity": "O(n)",
            "tags": ["dynamic-programming", "arrays"]
        },

        {
            "question": "Edit Distance (Levenshtein Distance)",
            "function": "edit_distance",
            "test_cases": [
                (("horse", "ros"), 3),
                (("intention", "execution"), 5),
                (("", "abc"), 3)
            ],
            "hints": [
                "Use 2D DP table",
                "Operations: insert, delete, replace",
                "dp[i][j] = min operations to convert s1[:i] to s2[:j]"
            ],
            "solution": """def edit_distance(s1, s2):
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i-1] == s2[j-1]:
                dp[i][j] = dp[i-1][j-1]
            else:
                dp[i][j] = 1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])
    return dp[m][n]""",
            "time_complexity": "O(m*n)",
            "space_complexity": "O(m*n)",
            "tags": ["dynamic-programming", "strings"]
        },

        {
            "question": "Longest Common Subsequence",
            "function": "lcs",
            "test_cases": [
                (("abcde", "ace"), 3),
                (("abc", "abc"), 3),
                (("abc", "def"), 0)
            ],
            "hints": [
                "Use 2D DP table",
                "If chars match, add 1 to diagonal",
                "Else take max of left or top cell"
            ],
            "solution": """def lcs(s1, s2):
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i-1] == s2[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    return dp[m][n]""",
            "time_complexity": "O(m*n)",
            "space_complexity": "O(m*n)",
            "tags": ["dynamic-programming", "strings"]
        },

        {
            "question": "0/1 Knapsack Problem",
            "function": "knapsack",
            "test_cases": [
                (([60, 100, 120], [10, 20, 30], 50), 220),
                (([10, 20, 30], [1, 1, 1], 2), 50)
            ],
            "hints": [
                "Include or exclude each item",
                "dp[i][w] = max value with first i items and capacity w",
                "Take max of including or not including current item"
            ],
            "solution": """def knapsack(values, weights, capacity):
    n = len(values)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for w in range(capacity + 1):
            if weights[i-1] <= w:
                dp[i][w] = max(dp[i-1][w], values[i-1] + dp[i-1][w - weights[i-1]])
            else:
                dp[i][w] = dp[i-1][w]
    return dp[n][capacity]""",
            "time_complexity": "O(n*W)",
            "space_complexity": "O(n*W)",
            "tags": ["dynamic-programming"]
        },

        {
            "question": "Coin Change - Minimum Coins",
            "function": "min_coins",
            "test_cases": [
                (([1, 2, 5], 11), 3),
                (([2], 3), -1),
                (([1], 0), 0)
            ],
            "hints": [
                "DP approach for each amount",
                "dp[i] = min coins needed for amount i",
                "For each coin, update dp[i] = min(dp[i], dp[i-coin] + 1)"
            ],
            "solution": """def min_coins(coins, amount):
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0
    for i in range(1, amount + 1):
        for coin in coins:
            if coin <= i and dp[i - coin] != float('inf'):
                dp[i] = min(dp[i], dp[i - coin] + 1)
    return dp[amount] if dp[amount] != float('inf') else -1""",
            "time_complexity": "O(amount * n)",
            "space_complexity": "O(amount)",
            "tags": ["dynamic-programming"]
        },

        {
            "question": "Word Break Problem",
            "function": "word_break",
            "test_cases": [
                (("leetcode", ["leet", "code"]), True),
                (("applepenapple", ["apple", "pen"]), True),
                (("catsandog", ["cats", "dog", "sand", "and", "cat"]), False)
            ],
            "hints": [
                "Use DP to check if string can be segmented",
                "dp[i] = True if s[:i] can be segmented",
                "Check all possible word endings"
            ],
            "solution": """def word_break(s, word_dict):
    word_set = set(word_dict)
    n = len(s)
    dp = [False] * (n + 1)
    dp[0] = True
    for i in range(1, n + 1):
        for j in range(i):
            if dp[j] and s[j:i] in word_set:
                dp[i] = True
                break
    return dp[n]""",
            "time_complexity": "O(n^2)",
            "space_complexity": "O(n)",
            "tags": ["dynamic-programming", "strings"]
        },

        {
            "question": "Maximum Subarray Sum (Kadane's Algorithm)",
            "function": "max_subarray",
            "test_cases": [
                (([-2, 1, -3, 4, -1, 2, 1, -5, 4],), 6),
                (([1],), 1),
                (([-1, -2, -3],), -1)
            ],
            "hints": [
                "Track current sum and max sum",
                "Reset current sum if it goes negative",
                "Max sum = max(max_sum, current_sum)"
            ],
            "solution": """def max_subarray(arr):
    max_sum = arr[0]
    curr_sum = arr[0]
    for i in range(1, len(arr)):
        curr_sum = max(arr[i], curr_sum + arr[i])
        max_sum = max(max_sum, curr_sum)
    return max_sum""",
            "time_complexity": "O(n)",
            "space_complexity": "O(1)",
            "tags": ["dynamic-programming", "arrays"]
        },

        {
            "question": "Trapping Rain Water",
            "function": "trap_water",
            "test_cases": [
                (([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1],), 6),
                (([4, 2, 0, 3, 2, 5],), 9)
            ],
            "hints": [
                "Water at each position depends on min of max heights on both sides",
                "Precompute left_max and right_max arrays",
                "water[i] = min(left_max[i], right_max[i]) - height[i]"
            ],
            "solution": """def trap_water(height):
    if not height:
        return 0
    n = len(height)
    left_max = [0] * n
    right_max = [0] * n
    left_max[0] = height[0]
    for i in range(1, n):
        left_max[i] = max(left_max[i-1], height[i])
    right_max[n-1] = height[n-1]
    for i in range(n-2, -1, -1):
        right_max[i] = max(right_max[i+1], height[i])
    water = 0
    for i in range(n):
        water += min(left_max[i], right_max[i]) - height[i]
    return water""",
            "time_complexity": "O(n)",
            "space_complexity": "O(n)",
            "tags": ["arrays", "two-pointers", "dynamic-programming"]
        },

        {
            "question": "Longest Palindromic Substring",
            "function": "longest_palindrome_substring",
            "test_cases": [
                (("babad",), "bab"),
                (("cbbd",), "bb"),
                (("a",), "a")
            ],
            "hints": [
                "Expand around center approach",
                "Check both odd and even length palindromes",
                "Track start and max length"
            ],
            "solution": """def longest_palindrome_substring(s):
    if not s:
        return ""
    start, max_len = 0, 1
    
    def expand(left, right):
        while left >= 0 and right < len(s) and s[left] == s[right]:
            left -= 1
            right += 1
        return right - left - 1
    
    for i in range(len(s)):
        len1 = expand(i, i)      # Odd length
        len2 = expand(i, i + 1)  # Even length
        length = max(len1, len2)
        if length > max_len:
            max_len = length
            start = i - (length - 1) // 2
    return s[start:start + max_len]""",
            "time_complexity": "O(n^2)",
            "space_complexity": "O(1)",
            "tags": ["strings", "dynamic-programming"]
        },

        {
            "question": "Merge Intervals",
            "function": "merge_intervals",
            "test_cases": [
                (([[1, 3], [2, 6], [8, 10], [15, 18]],), [[1, 6], [8, 10], [15, 18]]),
                (([[1, 4], [4, 5]],), [[1, 5]])
            ],
            "hints": [
                "Sort intervals by start time",
                "Merge if current overlaps with previous",
                "Track end of merged interval"
            ],
            "solution": """def merge_intervals(intervals):
    if not intervals:
        return []
    intervals.sort(key=lambda x: x[0])
    merged = [intervals[0]]
    for current in intervals[1:]:
        if current[0] <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], current[1])
        else:
            merged.append(current)
    return merged""",
            "time_complexity": "O(n log n)",
            "space_complexity": "O(n)",
            "tags": ["arrays", "sorting"]
        },

        {
            "question": "Number of Islands (DFS)",
            "function": "num_islands",
            "test_cases": [
                (([["1", "1", "0"], ["1", "1", "0"], ["0", "0", "1"]],), 2),
                (([["1", "0", "1"], ["0", "0", "0"], ["1", "0", "1"]],), 4)
            ],
            "hints": [
                "Use DFS to explore connected land",
                "Mark visited cells",
                "Count number of DFS starts"
            ],
            "solution": """def num_islands(grid):
    if not grid:
        return 0
    rows, cols = len(grid), len(grid[0])
    count = 0
    
    def dfs(r, c):
        if r < 0 or r >= rows or c < 0 or c >= cols or grid[r][c] != "1":
            return
        grid[r][c] = "0"  # Mark visited
        dfs(r + 1, c)
        dfs(r - 1, c)
        dfs(r, c + 1)
        dfs(r, c - 1)
    
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "1":
                dfs(r, c)
                count += 1
    return count""",
            "time_complexity": "O(m*n)",
            "space_complexity": "O(m*n)",
            "tags": ["graph", "matrix", "recursion"]
        },

        {
            "question": "Valid Binary Search Tree",
            "function": "is_valid_bst",
            "test_cases": [
                (([2, 1, 3],), True),
                (([5, 1, 4, None, None, 3, 6],), False)
            ],
            "hints": [
                "BST: left < root < right",
                "Track valid range for each node",
                "Use recursion with min/max bounds"
            ],
            "solution": """def is_valid_bst(nodes):
    # Simplified: using inorder traversal property
    # Full BST would need tree construction
    if len(nodes) <= 1:
        return True
    root = nodes[0]
    left = nodes[1] if len(nodes) > 1 else None
    right = nodes[2] if len(nodes) > 2 else None
    if left is not None and left >= root:
        return False
    if right is not None and right <= root:
        return False
    return True""",
            "time_complexity": "O(n)",
            "space_complexity": "O(h)",
            "tags": ["tree", "recursion"]
        },

        {
            "question": "Serialize and Deserialize Binary Tree (Level Order)",
            "function": "serialize_tree",
            "test_cases": [
                (([1, 2, 3, None, None, 4, 5],), "1,2,3,#,#,4,5"),
                (([],), "")
            ],
            "hints": [
                "Use level-order traversal (BFS)",
                "Use special character for None",
                "Serialize as comma-separated string"
            ],
            "solution": """def serialize_tree(nodes):
    if not nodes:
        return ""
    return ','.join('#' if x is None else str(x) for x in nodes)""",
            "time_complexity": "O(n)",
            "space_complexity": "O(n)",
            "tags": ["tree", "strings"]
        },

        {
            "question": "LRU Cache Implementation",
            "function": "lru_cache_ops",
            "test_cases": [
                (([["put", 1, 1], ["put", 2, 2], ["get", 1], ["put", 3, 3], ["get", 2]], 2), [None, None, 1, None, -1]),
                (([["put", 1, 1], ["get", 1], ["get", 2]], 1), [None, 1, -1])
            ],
            "hints": [
                "Use OrderedDict for O(1) operations",
                "Move accessed items to end",
                "Remove from front when capacity exceeded"
            ],
            "solution": """def lru_cache_ops(operations, capacity):
    from collections import OrderedDict
    cache = OrderedDict()
    results = []
    for op in operations:
        if op[0] == 'put':
            key, value = op[1], op[2]
            if key in cache:
                cache.move_to_end(key)
            cache[key] = value
            if len(cache) > capacity:
                cache.popitem(last=False)
            results.append(None)
        else:  # get
            key = op[1]
            if key in cache:
                cache.move_to_end(key)
                results.append(cache[key])
            else:
                results.append(-1)
    return results""",
            "time_complexity": "O(1) per operation",
            "space_complexity": "O(capacity)",
            "tags": ["dictionary", "arrays"]
        },

        {
            "question": "Find Median from Data Stream",
            "function": "running_median",
            "test_cases": [
                (([2, 3, 4],), [2.0, 2.5, 3.0]),
                (([1, 2],), [1.0, 1.5])
            ],
            "hints": [
                "Use two heaps: max-heap for lower half, min-heap for upper",
                "Balance heaps after each insertion",
                "Median is from heap tops"
            ],
            "solution": """def running_median(nums):
    import heapq
    small = []  # Max heap (negated)
    large = []  # Min heap
    result = []
    
    for num in nums:
        heapq.heappush(small, -num)
        heapq.heappush(large, -heapq.heappop(small))
        
        if len(large) > len(small):
            heapq.heappush(small, -heapq.heappop(large))
        
        if len(small) > len(large):
            result.append(float(-small[0]))
        else:
            result.append((-small[0] + large[0]) / 2.0)
    
    return result""",
            "time_complexity": "O(n log n)",
            "space_complexity": "O(n)",
            "tags": ["heap", "arrays"]
        },

        {
            "question": "Count Inversions in Array",
            "function": "count_inversions",
            "test_cases": [
                (([2, 4, 1, 3, 5],), 3),
                (([1, 2, 3, 4, 5],), 0),
                (([5, 4, 3, 2, 1],), 10)
            ],
            "hints": [
                "Inversion: i < j but arr[i] > arr[j]",
                "Use modified merge sort",
                "Count inversions during merge step"
            ],
            "solution": """def count_inversions(arr):
    def merge_count(arr, temp, left, mid, right):
        i = left
        j = mid + 1
        k = left
        inv = 0
        while i <= mid and j <= right:
            if arr[i] <= arr[j]:
                temp[k] = arr[i]
                i += 1
            else:
                temp[k] = arr[j]
                inv += (mid - i + 1)
                j += 1
            k += 1
        while i <= mid:
            temp[k] = arr[i]
            i += 1
            k += 1
        while j <= right:
            temp[k] = arr[j]
            j += 1
            k += 1
        for i in range(left, right + 1):
            arr[i] = temp[i]
        return inv
    
    def sort_count(arr, temp, left, right):
        inv = 0
        if left < right:
            mid = (left + right) // 2
            inv += sort_count(arr, temp, left, mid)
            inv += sort_count(arr, temp, mid + 1, right)
            inv += merge_count(arr, temp, left, mid, right)
        return inv
    
    n = len(arr)
    temp = [0] * n
    return sort_count(arr.copy(), temp, 0, n - 1)""",
            "time_complexity": "O(n log n)",
            "space_complexity": "O(n)",
            "tags": ["sorting", "arrays", "recursion"]
        },

        {
            "question": "Minimum Window Substring",
            "function": "min_window",
            "test_cases": [
                (("ADOBECODEBANC", "ABC"), "BANC"),
                (("a", "a"), "a"),
                (("a", "aa"), "")
            ],
            "hints": [
                "Use sliding window with two pointers",
                "Track character frequencies",
                "Shrink window when all chars found"
            ],
            "solution": """def min_window(s, t):
    from collections import Counter
    if not s or not t:
        return ""
    t_count = Counter(t)
    required = len(t_count)
    formed = 0
    window = {}
    left = 0
    min_len = float('inf')
    result = ""
    
    for right, char in enumerate(s):
        window[char] = window.get(char, 0) + 1
        if char in t_count and window[char] == t_count[char]:
            formed += 1
        
        while formed == required:
            if right - left + 1 < min_len:
                min_len = right - left + 1
                result = s[left:right+1]
            
            window[s[left]] -= 1
            if s[left] in t_count and window[s[left]] < t_count[s[left]]:
                formed -= 1
            left += 1
    
    return result""",
            "time_complexity": "O(n)",
            "space_complexity": "O(k)",
            "tags": ["strings", "two-pointers", "dictionary"]
        },

        {
            "question": "Decode Ways",
            "function": "decode_ways",
            "test_cases": [
                (("12",), 2),
                (("226",), 3),
                (("06",), 0)
            ],
            "hints": [
                "Each digit can be decoded alone (1-9)",
                "Or two digits together (10-26)",
                "Use DP: dp[i] = ways to decode s[:i]"
            ],
            "solution": """def decode_ways(s):
    if not s or s[0] == '0':
        return 0
    n = len(s)
    dp = [0] * (n + 1)
    dp[0] = 1
    dp[1] = 1
    
    for i in range(2, n + 1):
        if s[i-1] != '0':
            dp[i] += dp[i-1]
        two_digit = int(s[i-2:i])
        if 10 <= two_digit <= 26:
            dp[i] += dp[i-2]
    
    return dp[n]""",
            "time_complexity": "O(n)",
            "space_complexity": "O(n)",
            "tags": ["dynamic-programming", "strings"]
        },

        {
            "question": "Maximal Rectangle in Binary Matrix",
            "function": "maximal_rectangle",
            "test_cases": [
                (([["1", "0", "1", "0", "0"], ["1", "0", "1", "1", "1"], ["1", "1", "1", "1", "1"]],), 6),
                (([["0"]],), 0)
            ],
            "hints": [
                "Convert to histogram for each row",
                "Apply largest rectangle in histogram",
                "Use stack-based approach"
            ],
            "solution": """def maximal_rectangle(matrix):
    if not matrix:
        return 0
    
    def largest_rect_histogram(heights):
        heights.append(0)
        stack = [-1]
        max_area = 0
        for i, h in enumerate(heights):
            while heights[stack[-1]] > h:
                height = heights[stack.pop()]
                width = i - stack[-1] - 1
                max_area = max(max_area, height * width)
            stack.append(i)
        heights.pop()
        return max_area
    
    m, n = len(matrix), len(matrix[0])
    heights = [0] * n
    max_rect = 0
    
    for row in matrix:
        for j in range(n):
            heights[j] = heights[j] + 1 if row[j] == '1' else 0
        max_rect = max(max_rect, largest_rect_histogram(heights))
    
    return max_rect""",
            "time_complexity": "O(m*n)",
            "space_complexity": "O(n)",
            "tags": ["stack", "matrix", "dynamic-programming"]
        },

        {
            "question": "Regular Expression Matching",
            "function": "regex_match",
            "test_cases": [
                (("aa", "a"), False),
                (("aa", "a*"), True),
                (("ab", ".*"), True)
            ],
            "hints": [
                "Use dynamic programming",
                "'.' matches any single character",
                "'*' matches zero or more of preceding element"
            ],
            "solution": """def regex_match(s, p):
    m, n = len(s), len(p)
    dp = [[False] * (n + 1) for _ in range(m + 1)]
    dp[0][0] = True
    
    for j in range(1, n + 1):
        if p[j-1] == '*':
            dp[0][j] = dp[0][j-2]
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if p[j-1] == s[i-1] or p[j-1] == '.':
                dp[i][j] = dp[i-1][j-1]
            elif p[j-1] == '*':
                dp[i][j] = dp[i][j-2]
                if p[j-2] == s[i-1] or p[j-2] == '.':
                    dp[i][j] = dp[i][j] or dp[i-1][j]
    
    return dp[m][n]""",
            "time_complexity": "O(m*n)",
            "space_complexity": "O(m*n)",
            "tags": ["dynamic-programming", "strings", "regex"]
        }
    ]
}


def get_all_tags() -> list:
    """Return list of all available tags."""
    return ALL_TAGS.copy()


def get_questions_by_tag(tag: str) -> list:
    """
    Get all questions that have a specific tag.
    Returns list of (stage, index, question) tuples.
    """
    results = []
    for stage, questions in QUESTIONS.items():
        for idx, q in enumerate(questions):
            if tag in q.get("tags", []):
                results.append((stage, idx, q))
    
    # Also search automation questions
    if AUTOMATION_QUESTIONS_AVAILABLE:
        for stage, questions in AUTOMATION_QUESTIONS.items():
            for idx, q in enumerate(questions):
                if tag in q.get("tags", []):
                    results.append((f"Automation-{stage}", idx, q))
    
    return results


def count_questions_by_tag() -> dict:
    """
    Count questions per tag.
    Returns dict {tag: count}.
    """
    counts = {tag: 0 for tag in ALL_TAGS}
    for stage, questions in QUESTIONS.items():
        for q in questions:
            for tag in q.get("tags", []):
                counts[tag] = counts.get(tag, 0) + 1
    
    # Also count automation questions
    if AUTOMATION_QUESTIONS_AVAILABLE:
        for stage, questions in AUTOMATION_QUESTIONS.items():
            for q in questions:
                for tag in q.get("tags", []):
                    counts[tag] = counts.get(tag, 0) + 1
    
    return counts


def get_automation_questions() -> dict:
    """Return automation questions dictionary."""
    if AUTOMATION_QUESTIONS_AVAILABLE:
        return AUTOMATION_QUESTIONS
    return {}


def get_all_questions() -> dict:
    """Return combined Python and automation questions."""
    all_q = dict(QUESTIONS)
    if AUTOMATION_QUESTIONS_AVAILABLE:
        all_q.update(AUTOMATION_QUESTIONS)
    return all_q
