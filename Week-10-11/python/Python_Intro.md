# Python Introduction

## Table of Contents

* [1. High-Level Overview](#1-high-level-overview)
* [2. Language Features](#2-language-features)
* [3. Python Syntax](#3-python-syntax)
* [4. Variables](#4-variables)
* [5. Data Types](#5-data-types)

***

## 1. High-Level Overview

**Python** is a high-level, interpreted, general-purpose programming language. Designed with an emphasis on code readability, it uses significant indentation to define structure rather than curly braces or keywords. It is an industry standard for web development, data science, artificial intelligence, and automation.

[↑ Back to Table of Contents](#table-of-contents)
***

*Now that we understand what Python is, let's explore the specific characteristics that make it unique.*

## 2. Language Features

Python is defined by several key characteristics that influence how developers write and maintain code.

| Feature | Description | Benefit |
| :--- | :--- | :--- |
| **Interpreted** | Code is executed line-by-line by the Python interpreter. | Faster development cycle; easier debugging. |
| **Dynamically Typed** | Variable types are determined at runtime, not declared explicitly. | Increased flexibility and faster prototyping. |
| **High-Level** | Provides high-level abstractions and handles memory management (Garbage Collection) automatically. | Allows developers to focus on logic rather than hardware management. |
| **Multi-paradigm** | Supports Procedural, Object-Oriented (OOP), and Functional programming styles. | Versatility for different problem-solving approaches. |

**Interpreted vs. Compiled**
While **Compiled** languages (like C++) translate code into machine-level instructions before execution, **Interpreted** languages (like Python) use an intermediary step where the interpreter reads and executes the code on the fly. This makes Python more portable across different operating systems but generally slower for heavy computation.

[↑ Back to Table of Contents](#table-of-contents)
***

*With its core features established, we can now look at the rules governing how Python code is actually written.*

## 3. Python Syntax

Python syntax is famously clean and "executable pseudocode." Its primary differentiator is the use of **Whitespace/Indentation**.

### 3.1 Indentation and Blocks
In most languages, `{}` braces define a block of code. In Python, **indentation** (usually 4 spaces) is mandatory and defines the scope of loops, functions, and classes.

```python
# Example of correct indentation
if True:
    print("This is inside the block")
    if True:
        print("This is a nested block")
print("This is outside the block")
```

> [!WARNING]
> **Inconsistent Indentation:** Mixing tabs and spaces, or using inconsistent numbers of spaces, will trigger an `IndentationError`. Always stick to a single standard (PEP 8 recommends 4 spaces).

### 3.2 Comments
Comments are used to explain code and are ignored by the interpreter.
*   **Single-line:** Use the `#` symbol.
*   **Multi-line (Docstrings):** While technically strings, triple quotes `"""` are often used for multi-line documentation.

```python
# This is a single-line comment

"""
This is a multi-line string,
often used as a docstring to document
functions or classes.
"""
```

[↑ Back to Table of Contents](#table-of-contents)
***

*The structure of the code provides the framework, but we need variables to hold the actual data.*

## 4. Variables

A **Variable** is a reserved memory location to store values. In Python, you do not need to declare a variable's type; you simply assign a value using the `=` operator.

### 4.1 Variable Assignment
```python
x = 10          # An integer assignment
name = "Alice"  # A string assignment
is_active = True # A boolean assignment
```

### 4.2 Naming Conventions (PEP 8)
To ensure your code is "Pythonic," follow these naming standards:
*   **snake_case:** Use lowercase words separated by underscores for variables and functions (e.g., `user_score`).
*   **PascalCase:** Use capitalized words for Classes (e.g., `UserProfile`).
*   **UPPER_CASE:** Use for constants (e.g., `PI = 3.14`).

**Rules for Names:**
1. Must start with a letter or an underscore `_`.
2. Cannot start with a number.
3. Can only contain alpha-numeric characters and underscores (`A-z`, `0-9`, and `_`).
4. Are case-sensitive (`age` and `Age` are different variables).

[↑ Back to Table of Contents](#table-of-contents)
***

*Variables serve as containers, but the "content" inside them is categorized into specific types known as Data Types.*

## 5. Data Types

Because Python is **Dynamically Typed**, a variable's type is determined by the value it holds. You can check a variable's type using the `type()` function.

### 5.1 Primary Data Types
| Category | Type | Example | Description |
| :--- | :--- | :--- | :--- |
| **Numeric** | `int` | `5`, `-2` | Whole numbers without decimals. |
| **Numeric** | `float` | `3.14`, `2.0` | Numbers containing decimal points. |
| **Text** | `str` | `"Hello"` | A sequence of Unicode characters. |
| **Boolean** | `bool` | `True`, `False` | Represents logical truth values. |

### 5.2 Sequence Types (Collections)
Python provides several ways to group multiple items together.

| Type | Syntax | Characteristics | Use Case |
| :--- | :--- | :--- | :--- |
| **List** | `[a, b]` | **Mutable** (changeable), Ordered. | A collection of items you need to modify often. |
| **Tuple** | `(a, b)` | **Immutable** (un-changeable), Ordered. | A fixed collection of items (e.g., coordinates). |
| **Set** | `{a, b}` | **Mutable**, Unordered, **Unique** items only. | Removing duplicates or mathematical sets. |
| **Dictionary** | `{"k": "v"}` | **Mutable**, Key-Value pairs. | Mapping unique keys to specific values. |

**List vs. Tuple**
The fundamental difference is **mutability**. Once a **List** is created, you can add, remove, or change items. A **Tuple** is "locked" once created; this makes tuples faster and safer for data that should never change during the program's execution.

```python
# List Example (Mutable)
fruits = ["apple", "banana"]
fruits[0] = "cherry" # Works!

# Tuple Example (Immutable)
coordinates = (10, 20)
# coordinates[0] = 15 # Raises a TypeError
```

> [!TIP]
> Use **Lists** for most collections, but reach for **Tuples** when you want to guarantee that the data remains constant, preventing accidental bugs.

[↑ Back to Table of Contents](#table-of-contents)
