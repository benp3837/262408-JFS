# FastAPI

## Table of Contents

* [1. High-Level Overview](#1-high-level-overview)
* [2. Core Architecture & Fundamentals](#2-core-architecture--fundamentals)
    * [2.1 Fast API Introduction](#21-fast-api-introduction)
    * [2.2 Pydantic Models](#22-pydantic-models)
* [3. The Request-Response Cycle](#3-the-request-response-cycle)
    * [3.1 Creating REST Endpoints](#31-creating-rest-endpoints)
    * [3.2 Path and Query Parameters](#32-path-and-query-parameters)
    * [3.3 Request and Response Models](#33-request-and-response-models)
* [4. Advanced Patterns & Scaling](#4-advanced-patterns--scaling)
    * [4.1 Dependency Injection](#41-dependency-injection)
    * [4.2 Routers (APIRouter)](#42-routers-apirouter)
    * [4.3 Middleware](#43-middleware)
* [5. Integration & Documentation](#5-integration--documentation)
    * [5.1 OpenAPI Integration](#51-openapi-integration)

***

## 1. High-Level Overview

**FastAPI** is a modern, high-performance web framework for building APIs with Python 3.8+ based on standard Python type hints. It is designed to be easy to use, incredibly fast (on par with NodeJS and Go), and robust, thanks to its heavy reliance on **Pydantic** for data validation and **Starlette** for web capabilities.

FastAPI streamlines the entire development lifecycle—from defining data structures to generating interactive documentation—by leveraging the power of asynchronous programming and strict type safety.

[↑ Back to Table of Contents](#table-of-contents)
***

*Now that we have a high-level understanding of what FastAPI is, let's look at the underlying engine that makes its data handling so powerful: Pydantic.*

## 2. Core Architecture & Fundamentals

### 2.1 Fast API Introduction

FastAPI stands out because it is built on two foundational pillars:

1.  **Starlette:** A lightweight **ASGI** framework/toolkit, which handles the web parts (routing, requests, responses, WebSockets).
2.  **Pydantic:** A data validation and settings management library, which handles the data parts (parsing, validation, **serialization**).

This combination allows FastAPI to provide **automatic data validation**, **type conversion**, and **interactive documentation** out of the box.

### 2.2 Pydantic Models

At the heart of FastAPI's data handling is **Pydantic**. While Starlette handles the "envelope" (the HTTP request), Pydantic handles the "letter" (the data inside).

**Pydantic Models** are Python classes that inherit from `pydantic.BaseModel`. They define the exact shape, type, and constraints of the data your application expects.

| Feature | Benefit |
| :--- | :--- |
| **Type Validation** | Ensures an `int` is an `int`, an `email` is a valid email, etc. |
| **Data Parsing** | Automatically converts incoming strings (e.g., from a URL) into the correct Python types. |
| **Error Reporting** | Generates clear, structured error messages when validation fails. |
| **Serialization** | Easily converts Python objects back into JSON for responses. |

> [!TIP]
> **Type Hints are the Key:** FastAPI uses Python's native type hinting system. If you define a parameter as `item_id: int`, FastAPI knows to look for an integer and will return a 422 error if it receives a string that cannot be converted.

[↑ Back to Table of Contents](#table-of-contents)
***

*With the data models defined, we can now begin constructing the actual communication points of our API: the endpoints.*

## 3. The Request-Response Cycle

### 3.1 Creating REST Endpoints

In FastAPI, an **endpoint** is a function decorated with an HTTP method (like `@app.get()`, `@app.post()`, etc.). These functions represent the different "actions" your API can perform.

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}
```

### 3.2 Path and Query Parameters

Data can be passed to an endpoint in several ways. The two most common for simple lookups are **Path Parameters** and **Query Parameters**.

| Parameter Type | Purpose | Example URL | FastAPI Implementation |
| :--- | :--- | :--- | :--- |
| **Path Parameter** | Identifies a *specific resource*. | `/items/42` | `def read_item(item_id: int):` |
| **Query Parameter** | *Filters or modifies* the result. | `/items?limit=10` | `def read_items(limit: int = 10):` |

**Path Parameter vs. Query Parameter**
*   Use **Path Parameters** when the value is an integral part of the resource's identity (e.g., a specific User ID).
*   Use **Query Parameters** for optional modifiers, such as sorting, pagination, or filtering (e.g., `?sort=desc`).

### 3.3 Request and Response Models

To handle complex data structures, FastAPI uses **Pydantic** models as both **Request Models** (the body of an incoming POST/PUT request) and **Response Models** (the shape of the data returned to the client).

#### Request Model vs. Response Model

| Feature | Request Model | Response Model |
| :--- | :--- | :--- |
| **Primary Role** | **Input Validation**: Ensures the client sent all required fields in the correct format. | **Output Filtering**: Ensures the API only returns the specific fields you want to expose. |
| **Security** | Prevents malformed or malicious data from entering the application. | Prevents accidental data leakage (e.g., returning a `password_hash`). |
| **Implementation** | Parsed from the HTTP request body. | Serialized from the return value of the endpoint function. |

```python
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    price: float
    is_offer: bool | None = None

@app.post("/items/")
async def create_item(item: Item):
    return item
```

[↑ Back to Table of Contents](#table-of-contents)
***

*Endpoints handle individual requests, but as your application grows, you need ways to manage complexity, share logic, and secure your routes.*

## 4. Advanced Patterns & Scaling

### 4.1 Dependency Injection

**Dependency Injection (DI)** is a design pattern where a function (the "dependency") is "injected" into your endpoint. FastAPI has a built-in system for this using the `Depends` function.

**Use Cases for DI:**
*   **Database Connections:** Sharing a single DB session across multiple endpoints.
*   **Security/Authentication:** Verifying a JWT token before allowing access to a route.
*   **Common Logic:** Sharing pagination or filtering logic.

> [!TIP]
> **Testability:** DI makes testing significantly easier. Instead of hardcoding a database connection, you can "inject" a mock database during tests, allowing you to test your logic in isolation without needing a real database.

```python
from fastapi import Depends

async def common_params(q: str | None = None, skip: int = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}

@app.get("/items/")
async def read_items(params: dict = Depends(common_params)):
    return params
```

### 4.2 Routers (APIRouter)

As your API grows, putting every endpoint in a single `main.py` file becomes unmanageable. **`APIRouter`** allows you to split your API into multiple files (modules), organized by feature or resource.

*   `users.py` $\rightarrow$ contains all `/users/...` routes.
*   `items.py` $\rightarrow$ contains all `/items/...` routes.
*   `main.py` $\rightarrow$ includes all routers via `app.include_router()`.

### 4.3 Middleware

**Middleware** is a function that runs for *every single request* that enters your application and *every single response* that leaves it.

> [!TIP]
> **The Onion Model:** Think of middleware as layers of an onion. When a request comes in, it passes through each layer from the outside in. When the response is sent back, it passes through the same layers in **reverse order** (from the inside out).

**Common Middleware tasks:**
*   **CORS (Cross-Origin Resource Sharing):** Allowing your API to be called from different domains.
*   **Logging:** Recording every request for auditing.
*   **GZip Compression:** Automatically compressing response bodies to save bandwidth.

[↑ Back to Table of Contents](#table-of-contents)
***

*Finally, one of FastAPI's most powerful "magic" features is its ability to document itself automatically as you write code.*

## 5. Integration & Documentation

### 5.1 OpenAPI Integration

FastAPI is built to be **OpenAPI-compliant**. This means that as you write your code and define your Pydantic models, FastAPI automatically generates a massive, standardized JSON schema describing your entire API.

Because this schema is standardized, FastAPI provides two incredible interactive tools out of the box:

1.  **Swagger UI (`/docs`):** An interactive web interface that allows you to browse all your endpoints and **test them directly in your browser** by sending real requests.
2.  **ReDoc (`/redoc`):** A highly organized, professional-looking documentation layout focused on readability and easy navigation.

> [!IMPORTANT]
> **Documentation is a Side Effect of Good Typing:** In FastAPI, your documentation is not a separate manual that gets outdated; it is a real-time reflection of your code's type hints and Pydantic models.
