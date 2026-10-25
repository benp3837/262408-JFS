# Introduction to Pytest

## Table of Contents

* [1. High-Level Overview](#1-high-level-overview)
* [2. The Foundations](#2-the-foundations)
* [3. Core Mechanics](#3-core-mechanics)
* [4. Intermediate & Advanced Patterns](#4-intermediate--advanced-patterns)
* [5. Professional Workflow](#5-professional-workflow)

***

## 1. High-Level Overview

In modern software development, writing code is only half the battle; ensuring that code works reliably over time is the other half. **Testing** is the practice of verifying that a software component behaves as expected. This module explores **pytest**, the industry-standard framework for writing and running Python tests.

### 1.1 The Purpose of Testing

Testing is generally categorized by the scope of the code being verified:

| Test Type | Scope | Goal |
| :--- | :--- | :--- |
| **Unit Test** | A single function or class. | Verify logic in isolation. |
| **Integration Test** | Multiple modules or components. | Verify that different parts work together. |
| **End-to-End (E2E)** | The entire application flow. | Verify the system works from a user's perspective. |

### 1.2 Why Pytest?

While Python includes a built-in module called `unittest`, `pytest` has become the preferred tool for most professional developers due to its simplicity and powerful feature set.

**`unittest` vs. `pytest`**

| Feature | `unittest` (Standard Library) | `pytest` |
| :--- | :--- | :--- |
| **Style** | Object-Oriented (requires classes). | Functional (plain functions). |
| **Assertions** | Requires specific methods (e.g., `self.assertEqual`). | Uses standard Python `assert` statements. |
| **Complexity** | Verbose and boilerplate-heavy. | Concise and highly readable. |
| **Fixtures** | Uses `setUp`/`tearDown` methods. | Uses powerful, injectable **Fixtures**. |
| **Ecosystem** | Limited. | Massive (hundreds of plugins). |

***

*Now that we understand the "Why" behind testing, let's move into the "How" by exploring the most basic mechanics of running a test.*

## 2. The Foundations

### 2.1 The Pytest Ecosystem

To begin, you must install the framework via your package manager:

```bash
pip install pytest
```

**Test Discovery:** 
Pytest automatically finds tests by looking for files that match the patterns `test_*.py` or `*_test.py`. Inside these files, it looks for functions prefixed with `test_`.

### 2.2 Writing Your First Test

Unlike `unittest`, which requires you to inherit from a class, a `pytest` test can be a simple function.

```python
# test_math.py

def add(a, b):
    return a + b

def test_add_success():
    # Pytest uses standard Python asserts
    assert add(2, 3) == 5

def test_add_failure():
    # This will fail and provide a detailed error report
    assert add(2, 3) == 6
```

**The Power of `assert`:**
When a test fails, `pytest` performs **Assertion Rewriting**. Instead of just telling you `AssertionError`, it inspects the values and provides a detailed breakdown of exactly what the expression evaluated to (e.g., showing that `5 != 6`).

***

*While simple assertions are useful, real-world testing often requires setting up complex data or environments before the test runs. This is where Fixtures come in.*

## 3. Core Mechanics

### 3.1 Fixtures: Dependency Injection

**Fixtures** are functions that provide a fixed baseline (data, connections, objects) for your tests. They are "injected" into your test functions by name.

**Fixture Scopes:**
The "scope" determines how often a fixture is executed and how long it lives.

| Scope | Lifecycle | Best Use Case |
| :--- | :--- | :--- |
| `function` | Created for every single test function. | Small, isolated data objects. |
| `class` | Created once per test class. | Grouping tests that share a setup. |
| `module` | Created once per `.py` file. | Database connections for a specific module. |
| `session` | Created once for the entire test run. | Starting a web server or heavy external service. |

**Example: Yield Fixtures (Setup & Teardown)**
Use `yield` instead of `return` to allow for cleanup code (teardown).

```python
import pytest

@pytest.fixture
def db_connection():
    # SETUP: Connect to database
    db = {"connection": "active", "data": []}
    print("\nConnecting to DB...")
    
    yield db  # The test runs here
    
    # TEARDOWN: Close connection
    print("\nClosing DB connection...")
    db["connection"] = "closed"

def test_db_insert(db_connection):
    db_connection["data"].append("test_record")
    assert len(db_connection["data"]) == 1
    assert db_connection["connection"] == "active"
```

### 3.2 Parametrization: Eliminating Boilerplate

Instead of writing five different tests for five different inputs, use `@pytest.mark.parametrize` to run the same test logic against multiple datasets.

```python
import pytest

@pytest.mark.parametrize("input_a, input_b, expected", [
    (1, 2, 3),
    (5, 5, 10),
    (10, -2, 8),
    (0, 0, 0),
])
def test_add_multiple_cases(input_a, input_b, expected):
    assert input_a + input_b == expected
```

### 3.3 Marking and Filtering

You can tag tests with **Marks** to control which ones run in specific environments.

*   `@pytest.mark.skip(reason="...")`: Skips the test entirely.
*   `@pytest.mark.xfail`: Tells pytest the test is *expected* to fail.
*   `@pytest.mark.slow`: A custom mark for long-running tests.

**Running filtered tests via CLI:**
```bash
pytest -m "not slow"  # Runs everything EXCEPT tests marked as 'slow'
```

***

*Mastering fixtures and parametrization allows us to write clean tests. Now, let's look at how to handle complex real-world scenarios like errors and external dependencies.*

## 4. Intermediate & Advanced Patterns

### 4.1 Handling Exceptions

To verify that your code fails correctly when given bad input, use `pytest.raises`.

```python
import pytest

def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

def test_divide_by_zero():
    with pytest.raises(ValueError) as excinfo:
        divide(10, 0)
    
    # You can even check the error message
    assert "Cannot divide by zero" in str(excinfo.value)
```

### 4.2 The `conftest.py` File

If you have fixtures that need to be shared across many different files, you don't need to import them. Simply place them in a file named `conftest.py` in your test directory. Pytest automatically discovers and makes these fixtures available to all tests in that directory and its subdirectories.

### 4.3 Mocking and Patching

In unit testing, you want to isolate your code from the "outside world" (like an API or a Database). We use **Mocking** to replace real objects with "fake" ones that simulate behavior.

Using the `pytest-mock` plugin (which provides the `mocker` fixture):

```python
# service.py
import requests

def get_user_data(user_id):
    response = requests.get(f"https://api.example.com/users/{user_id}")
    return response.json()

# test_service.py
def test_get_user_data(mocker):
    # Mock the 'requests.get' call so we don't actually hit the internet
    mock_get = mocker.patch("service.requests.get")
    
    # Define what the fake response should look like
    mock_get.return_value.json.return_value = {"id": 1, "name": "John Doe"}
    
    from service import get_user_data
    result = get_user_data(1)
    
    assert result["name"] == "John Doe"
    mock_get.assert_called_once_with("https://api.example.com/users/1")
```

***

*Having the tools to write tests is only useful if you know how to integrate them into a professional development workflow.*

## 5. Professional Workflow

### 5.1 Running Tests Efficiently

When working on a large codebase, you don't want to run every test every time. Use these CLI flags:

*   `-x`: **Exit immediately** on the first failure.
*   `-v`: **Verbose** mode; shows more detail about which tests are running.
*   `--lf`: **Last Failed**; only runs the tests that failed during the previous run.
*   `-k "pattern"`: Run only tests that match a specific string in their name.

### 5.2 Code Coverage

To see how much of your code is actually being tested, use `pytest-cov`.

**Installation:**
```bash
pip install pytest-cov
```

**Usage:**
```bash
pytest --cov=my_package tests/
```
This generates a report showing the percentage of lines in `my_package` that were executed during the test suite.

### 5.3 CI/CD Integration

In a professional environment, tests are not just run on your machine; they are run automatically in a **CI/CD pipeline** (e.g., GitHub Actions). Every time you push code, the pipeline runs:
1.  `pip install -r requirements.txt`
2.  `pytest --cov=...`

If any test fails, the "Build" fails, preventing broken code from ever reaching production.
