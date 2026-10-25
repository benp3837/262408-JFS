# Python Basics

## Table of Contents

* [1. High-Level Overview](#1-high-level-overview)
* [2. Operators](#2-operators)
    * [2.1 Arithmetic Operators](#21-arithmetic-operators)
    * [2.2 Comparison Operators](#22-comparison-operators)
    * [2.3 Logical Operators](#23-logical-operators)
    * [2.4 Assignment Operators](#24-assignment-operators)
* [3. Control Flow](#3-control-flow)
    * [3.1 Conditional Statements (if, elif, else)](#31-conditional-statements-if-elif-else)
    * [3.2 Loops (for, while)](#32-loops-for-while)
    * [3.3 Loop Control (break, continue, pass)](#33-loop-control-break-continue-pass)
* [4. Functions](#4-functions)
    * [4.1 Defining and Calling Functions](#41-defining-and-calling-functions)
    * [4.2 Arguments and Parameters](#42-arguments-and-parameters)
    * [4.3 Return Values](#43-return-values)
* [5. Exception Handling](#5-exception-handling)
    * [5.1 Try-Except Blocks](#51-try-except-blocks)
    * [5.2 Finally and Else](#52-finally-and-else)
    * [5.3 Raising Exceptions](#53-raising-exceptions)
* [6. Summary Comparison: Control Flow Structures](#6-summary-comparison-control-flow-structures)

***

## 1. High-Level Overview

Python is a high-level, interpreted language known for its readability and simplicity. To write effective logic, a programmer must master how data is manipulated (**Operators**), how the execution path is decided (**Control Flow**), how logic is encapsulated for reuse (**Functions**), and how to handle unexpected errors gracefully (**Exception Handling**).

This module follows the dependency architecture, moving from basic data manipulation to complex logical structures and error management.

[↑ Back to Table of Contents](#table-of-contents)
***

## 2. Operators

**Operators** are special symbols in Python that perform operations on variables and values. They are the fundamental building blocks of any expression.

### 2.1 Arithmetic Operators
Used to perform common mathematical operations.

| Operator | Name | Description | Example (`a=10, b=3`) |
| :--- | :--- | :--- | :--- |
| `+` | Addition | Adds two values | `a + b` $\rightarrow$ `13` |
| `-` | Subtraction | Subtracts right operand from left | `a - b` $\rightarrow$ `7` |
| `*` | Multiplication | Multiplies two values | `a * b` $\rightarrow$ `30` |
| `/` | Division | Divides left operand by right (always returns a float) | `a / b` $\rightarrow$ `3.333...` |
| `%` | Modulus | Returns the remainder of division | `a % b` $\rightarrow$ `1` |
| `**` | Exponentiation | Left operand raised to the power of right | `a ** b` $\rightarrow$ `1000` |
| `//` | Floor Division | Divides and returns the largest integer | `a // b` $\rightarrow$ `3` |

### 2.2 Comparison Operators
Used to compare two values. They always return a **Boolean** value (`True` or `False`).

| Operator | Name | Example (`a=10, b=3`) |
| :--- | :--- | :--- |
| `==` | Equal | `a == b` $\rightarrow$ `False` |
| `!=` | Not Equal | `a != b` $\rightarrow$ `True` |
| `>` | Greater Than | `a > b` $\rightarrow$ `True` |
| `<` | Less Than | `a < b` $\rightarrow$ `False` |
| `>=` | Greater or Equal | `a >= 10` $\rightarrow$ `True` |
| `<=` | Less or Equal | `b <= 2` $\rightarrow$ `False` |

### 2.3 Logical Operators
Used to combine conditional statements.

| Operator | Description | Example |
| :--- | :--- | :--- |
| `and` | Returns `True` if both statements are true | `(5 > 3 and 10 > 5)` $\rightarrow$ `True` |
| `or` | Returns `True` if one of the statements is true | `(5 > 3 or 10 < 5)` $\rightarrow$ `True` |
| `not` | Reverse the result, returns `False` if the result is true | `not(5 > 3)` $\rightarrow$ `False` |

### 2.4 Assignment Operators
Used to assign values to variables.

| Operator | Example | Equivalent To |
| :--- | :--- | :--- |
| `=` | `x = 5` | `x = 5` |
| `+=` | `x += 3` | `x = x + 3` |
| `-=` | `x -= 3` | `x = x - 3` |
| `*=` | `x *= 3` | `x = x * 3` |

[↑ Back to Table of Contents](#table-of-contents)
***

*Now that we know how to manipulate individual values, we need a way to direct the program's path based on those values using **Control Flow**.*

## 3. Control Flow

**Control Flow** refers to the order in which individual statements, instructions, or function calls are executed. In Python, this is primarily achieved through conditional branching and looping.

### 3.1 Conditional Statements (if, elif, else)

Conditionals allow the program to execute certain blocks of code only if a specific condition is met.

```python
age = 18

if age < 13:
    print("Child")
elif age < 20:
    print("Teenager")
else:
    print("Adult")
```

*   **`if`**: The initial test.
*   **`elif`** (short for else if): Checks another condition if the previous ones were `False`.
*   **`else`**: The fallback; executes if no previous conditions were met.

### 3.2 Loops (for, while)

Loops are used to repeat a block of code multiple times.

#### The `for` Loop
Used for iterating over a sequence (like a list, tuple, string, or range).

```python
# Iterating through a range
for i in range(5):
    print(f"Iteration {i}")

# Iterating through a list
fruits = ["apple", "banana", "cherry"]
for fruit in fruits:
    print(fruit)
```

#### The `while` Loop
Repeats a block of code as long as a condition remains `True`.

```python
count = 0
while count < 5:
    print(count)
    count += 1
```

> [!WARNING]
> **Infinite Loops:** If the condition in a `while` loop never becomes `False`, the program will run indefinitely, potentially consuming all system resources. Always ensure the loop has a mechanism to terminate.

### 3.3 Loop Control (break, continue, pass)

Sometimes you need to alter the behavior of a loop while it is running.

| Keyword | Action | Use Case |
| :--- | :--- | :--- |
| `break` | Exits the loop entirely. | Stopping a search once an item is found. |
| `continue` | Skips the current iteration and moves to the next. | Skipping invalid data in a dataset. |
| `pass` | Does nothing; acts as a placeholder. | When syntax requires a statement but you aren't ready to write the logic. |

[↑ Back to Table of Contents](#table-of-contents)
***

*Repeated logic is fine, but modularizing that logic into reusable chunks is what makes code maintainable. This leads us to **Functions**.*

## 4. Functions

A **Function** is a reusable block of code that performs a specific task. Functions help in achieving **DRY** (Don't Repeat Yourself) principles.

### 4.1 Defining and Calling Functions

You define a function using the `def` keyword, followed by the function name and parentheses.

```python
def greet():
    print("Hello, World!")

# Calling the function
greet()
```

### 4.2 Arguments and Parameters

To use functions effectively, it is crucial to distinguish between the definition and the invocation.

**Parameters vs. Arguments**

| Term | Definition | Context | Example |
| :--- | :--- | :--- | :--- |
| **Parameter** | The named variable in the function definition. | **Declaration** | `def greet(name):` |
| **Argument** | The actual value passed to the function. | **Invocation** | `greet("Alice")` |

```python
def greet_user(name): # 'name' is a parameter
    print(f"Hello, {name}!")

greet_user("Alice") # "Alice" is an argument
```

### 4.3 Return Values

Functions can send data back to the caller using the `return` statement. Once a `return` is executed, the function exits immediately.

```python
def add(a, b):
    return a + b

result = add(10, 5)
print(result) # Output: 15
```

[↑ Back to Table of Contents](#table-of-contents)
***

*Even the best-written functions can encounter errors (e.g., dividing by zero or missing files). To prevent these errors from crashing the entire program, we use **Exception Handling**.*

## 5. Exception Handling

**Exception Handling** is the process of responding to occurrences of abnormal conditions during the execution of a program.

### 5.1 Try-Except Blocks

The `try` block lets you test a block of code for errors, and the `except` block lets you handle the error.

```python
try:
    number = int(input("Enter a number: "))
    result = 10 / number
    print(result)
except ValueError:
    print("Error: Invalid input. Please enter an integer.")
except ZeroDivisionError:
    print("Error: You cannot divide by zero.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
```

### 5.2 Finally and Else

*   **`else`**: Executes if **no** exceptions were raised in the `try` block.
*   **`finally`**: Executes **regardless** of whether an exception occurred or not. It is commonly used for cleanup (e.g., closing a file).

> [!TIP]
> **Graceful Cleanup:** Always use a `finally` block (or a `with` statement for context managers) to ensure resources like files or network connections are closed, even if an error occurs.

```python
try:
    file = open("example.txt", "r")
    content = file.read()
except FileNotFoundError:
    print("File not found.")
else:
    print("File read successfully.")
finally:
    print("Closing resources...")
    # In a real scenario, you'd close the file here if it was opened
```

### 5.3 Raising Exceptions

You can manually trigger an exception using the `raise` keyword if a specific condition in your logic is met.

```python
def check_age(age):
    if age < 0:
        raise ValueError("Age cannot be negative!")
    return age

try:
    check_age(-5)
except ValueError as e:
    print(e)
```

> [!TIP]
> **Exception Specificity:** Avoid catching the generic `Exception` class whenever possible. Instead, catch specific errors (like `ValueError` or `KeyError`). This prevents you from accidentally "swallowing" unexpected bugs that should actually crash the program so you can fix them.

[↑ Back to Table of Contents](#table-of-contents)
***

### 6. Summary Comparison: Control Flow Structures

To wrap up, let's compare the two main ways we control the flow of logic in Python using a decision matrix.

| Feature | `if/elif/else` | `for` Loop | `while` Loop |
| :--- | :--- | :--- | :--- |
| **Primary Purpose** | Decision making (branching). | Iteration over a known sequence. | Iteration based on a condition. |
| **Execution** | Runs once per check. | Runs $N$ times (where $N$ is sequence length). | Runs until the condition is `False`. |
| **Best Use Case** | Choosing between paths. | Processing lists, ranges, or strings. | Running a process until a state changes. |
| **Risk** | None. | Generally safe. | Risk of infinite loops. |

[↑ Back to Table of Contents](#table-of-contents)
