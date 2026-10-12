# Spring MVC: Mastering Web Development with Spring Boot

## Table of Contents

* [1. High-Level Overview](#1-high-level-overview)
* [2. The Spring MVC Architecture](#2-the-spring-mvc-architecture)
* [3. The Controller Layer](#3-the-controller-layer)
    * [3.1 MVC Annotations](#31-mvc-annotations)
    * [3.2 HTTP Method Annotations](#32-http-method-annotations)
* [4. Data Extraction (Request Handling)](#4-data-extraction-request-handling)
    * [4.1 Path Variables](#41-path-variables)
    * [4.2 Request Parameters](#42-request-parameters)
    * [4.3 Request Body](#43-request-body)
* [5. Error Handling](#5-error-handling)
    * [5.1 Exception Handler](#51-exception-handler)
* [6. RESTful API Development](#6-restful-api-development)

***

## 1. High-Level Overview

**Spring MVC (Model-View-Controller)** is a robust, web-based framework designed to simplify the creation of highly scalable, loosely coupled web applications. Within a **Spring Boot** ecosystem, Spring MVC provides the foundational layer for handling HTTP requests, managing application flow, and delivering responses (either as HTML views or JSON/XML data).

In the modern era of development, Spring MVC is most commonly used to build **RESTful APIs** that serve as the backend for single-page applications (SPAs) or mobile apps.

[↑ Back to Table of Contents](#table-of-contents)
***

## 2. **The Spring MVC Architecture**

Spring MVC follows the classic **Model-View-Controller** design pattern, which separates the application into three main components to ensure a clean separation of concerns.

| Component | Responsibility | Role in Spring MVC |
| :--- | :--- | :--- |
| **Model** | Data & Business Logic | Represents the state of the application and the data being passed between components. |
| **View** | Presentation Layer | Responsible for rendering the **Model** data into a format the user can see (e.g., **HTML**, **JSON**, **XML**). |
| **Controller** | Orchestration Layer | Intercepts incoming **HTTP requests**, interacts with the **Model**, and selects the appropriate **View**. |

**The Flow of a Request:**
1. The client sends an **HTTP Request**.
2. The **DispatcherServlet** (the **Front Controller**) intercepts the request.
3. The **DispatcherServlet** consults **Handler Mappings** to find the right **Controller**.
4. The **Controller** processes the request and returns a **ModelAndView** (or just the data).
5. The **View Resolver** identifies the correct **View**.
6. The **View** is rendered and sent back as an **HTTP Response**.

[↑ Back to Table of Contents](#table-of-contents)
***

*Now that we understand the structural architecture, let's dive into the component responsible for handling the actual logic: the Controller.*

## 3. The Controller Layer

The **Controller** is the entry point for your web logic. It acts as the "brain" that decides what happens when a specific URL is hit.

### 3.1 MVC Annotations

To turn a standard Java class into a web-capable component, Spring provides several specialized annotations.

| Annotation | Description |
| :--- | :--- |
| **`@Controller`** | Marks a class as a web controller. Typically used when returning **Views** (e.g., **HTML** or **Thymeleaf**). |
| **`@RestController`** | A specialized version of **`@Controller`** that combines **`@Controller`** and **`@ResponseBody`**. It is the standard for building **RESTful APIs** where every method returns data (e.g., **JSON** or **XML**) directly to the response body. |

### 3.2 HTTP Method Annotations

Spring provides specific annotations to map **HTTP verbs** to Java methods, ensuring your API follows **REST** principles.

*   **`@GetMapping`**: Handles `GET` requests (Fetching data).
*   **`@PostMapping`**: Handles `POST` requests (Creating data).
*   **`@PutMapping`**: Handles `PUT` requests (Updating/Replacing data).
*   **`@DeleteMapping`**: Handles `DELETE` requests (Removing data).
*   **`@PatchMapping`**: Handles `PATCH` requests (Partial updates).

[↑ Back to Table of Contents](#table-of-contents)
***

*Once a request reaches a method, we need a way to extract the specific information sent by the client. This is where Data Extraction comes in.*

## 4. Data Extraction (Request Handling)

Spring provides several ways to "pull" data out of an incoming HTTP request, depending on where that data is located.

### 4.1 Path Variables

**Path Variables** are used when the data is part of the **URL path** itself. This is a hallmark of **RESTful design**.

**Example URL:** `/api/users/42`

```java
@GetMapping("/api/users/{id}")
public User getUserById(@PathVariable("id") Long userId) {
    return userService.findById(userId);
}
```
> [!TIP]
> If the variable name in the path `{id}` matches the method parameter name `id`, you can simply use **`@PathVariable Long id`**.

### 4.2 Request Parameters

**Request Parameters** (often called **Query Params**) are appended to the end of a **URL** after a question mark. They are typically used for **filtering**, **sorting**, or **pagination**.

**Example URL:** `/api/users?role=admin&page=1`

```java
@GetMapping("/api/users")
public List<User> getUsers(
    @RequestParam(name = "role", required = false) String role,
    @RequestParam(name = "page", defaultValue = "0") int page
) {
    return userService.findByRole(role, page);
}
```

### 4.3 Request Body

The **Request Body** is used when the client sends a large, complex payload (usually a **JSON object**) inside the body of the **HTTP request**. This is most common in **`POST`** and **`PUT`** operations.

**Example JSON:** `{"name": "John Doe", "email": "john@example.com"}`

```java
@PostMapping("/api/users")
public User createUser(@RequestBody User newUser) {
    return userService.save(newUser);
}
```

[↑ Back to Table of Contents](#table-of-contents)
***

*Applications inevitably encounter errors. To prevent a complete system crash and provide meaningful feedback, we must implement a robust Exception Handling strategy.*

## 5. Error Handling

### 5.1 Exception Handler

Instead of letting raw stack traces leak to the client (which is a security risk), Spring allows you to intercept exceptions and transform them into clean, structured responses.

| Approach | Scope | Best Use Case |
| :--- | :--- | :--- |
| **`@ExceptionHandler`** | **Local:** Only works within the specific **Controller** where it is defined. | Handling errors unique to one specific controller. |
| **`@ControllerAdvice`** | **Global:** Intercepts exceptions thrown by *any* controller in the application. | Centralized, consistent error responses across the whole **API**. |

**Example: Global Exception Handling**

```java
@ControllerAdvice
public class GlobalExceptionHandler {

    @ExceptionHandler(UserNotFoundException.class)
    public ResponseEntity<ErrorResponse> handleUserNotFound(UserNotFoundException ex) {
        ErrorResponse error = new ErrorResponse("USER_NOT_FOUND", ex.getMessage());
        return new ResponseEntity<>(error, HttpStatus.NOT_FOUND);
    }
}
```

[↑ Back to Table of Contents](#table-of-contents)
***

*Now that we have mastered the individual components, let's synthesize them into the ultimate goal: building a RESTful API.*

## 6. RESTful API Development

**REST (Representational State Transfer)** is an architectural style for designing networked applications. A RESTful API uses standard HTTP methods to perform CRUD (Create, Read, Update, Delete) operations on **Resources**.

### The RESTful Mapping Pattern

To build a standard **RESTful service**, map your business logic to these patterns:

| HTTP Method | Endpoint Pattern | CRUD Operation | Description |
| :--- | :--- | :--- | :--- |
| `GET` | `/users` | **R**ead (List) | Fetch all users. |
| `GET` | `/users/{id}` | **R**ead (Single) | Fetch a specific user by ID. |
| `POST` | `/users` | **C**reate | Create a new user. |
| `PUT` | `/users/{id}` | **U**pdate | Replace an existing user entirely. |
| `PATCH` | `/users/{id}` | **U**pdate | Partially update a user (e.g., change just the email). |
| `DELETE` | `/users/{id}` | **D**elete | Remove a user. |

### Key Principles of RESTful Design
1.  **Statelessness:** Each request must contain all the information needed to understand it. The server does not store "session" state about the client.
2.  **Resource-Based URLs:** Use nouns, not verbs. Use `/users`, not `/getAllUsers`.
3.  **Standard Status Codes:** Always return appropriate **HTTP codes** (e.g., `201 Created` for successful **POST**s, `404 Not Found` for missing resources, `400 Bad Request` for validation errors).

[↑ Back to Table of Contents](#table-of-contents)
