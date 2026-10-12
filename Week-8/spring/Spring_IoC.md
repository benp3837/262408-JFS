# Spring IoC (Inversion of Control)

## Table of Contents

* [1. High-Level Overview](#1-high-level-overview)
* [2. Inversion of Control (IoC) Fundamentals](#2-inversion-of-control-ioc-fundamentals)
* [3. The Spring IoC Container](#3-the-spring-ioc-container)
* [4. Spring Bean Management](#4-spring-bean-management)
    * [4.1 Bean Definition and Instantiation](#41-bean-definition-and-instantiation)
    * [4.2 The Bean Lifecycle](#42-the-bean-lifecycle)
    * [4.3 Bean Scopes](#43-bean-scopes)

***

## 1. High-Level Overview

In traditional programming, a developer is responsible for creating objects, managing their dependencies, and controlling the flow of execution. In the **Spring Framework**, this responsibility is shifted away from the developer and handed over to the framework. This module explores the concept of **Inversion of Control (IoC)**, how the **Spring IoC Container** manages objects known as **Beans**, and the lifecycle and scopes that govern their existence.

[↑ Back to Table of Contents](#table-of-contents)
***

*Understanding the philosophy of "Inversion" is the first step toward mastering Spring. Let's dive into the core concept.*

## 2. Inversion of Control (IoC) Fundamentals

**Inversion of Control (IoC)** is a design principle in which the control of objects or portions of a program is transferred to a container or framework. 

### 2.1 The "Traditional" vs. "IoC" Approach

To understand IoC, we must compare how objects are managed in standard programming versus the Spring way.

| Feature | Traditional Approach (Manual Control) | IoC Approach (Framework Control) |
| :--- | :--- | :--- |
| **Object Creation** | The application code uses `new ClassName()` to create objects. | The **IoC Container** creates and manages objects. |
| **Dependency Management** | The developer manually passes dependencies into constructors or setters. | Dependencies are "injected" automatically by the framework (**Dependency Injection**). |
| **Control Flow** | Your code calls library functions. | The framework calls your code (the "Hollywood Principle"). |
| **Coupling** | High coupling; classes are tightly bound to specific implementations. | Low coupling; classes depend on abstractions (interfaces). |

> [!TIP]
> **The Hollywood Principle:** "Don't call us, we'll call you." This is the essence of IoC. Instead of your code asking for a service, the framework provides the service to your code when it is needed.

**IoC vs. Dependency Injection (DI)**

While often used interchangeably, they are not the same:
* **IoC** is the broad **design principle** (the concept of delegating control).
* **Dependency Injection** is a specific **pattern** used to implement IoC. DI is the mechanism by which the IoC container provides an object with its required dependencies.

[↑ Back to Table of Contents](#table-of-contents)
***

*Now that we understand the concept of shifting control, let's look at the engine that makes this happen in Spring: The Container.*

## 3. The Spring IoC Container

The **Spring IoC Container** is the heart of the Spring Framework. It is responsible for instantiating, configuring, and assembling objects (Beans) by reading configuration metadata.

### 3.1 Core Responsibilities

The container acts as the "orchestrator" for your application:
1.  **Instantiating Beans:** Creating the actual objects.
2.  **Dependency Injection:** Wiring objects together so they can work as a cohesive system.
3.  **Lifecycle Management:** Managing the entire existence of a bean from creation to destruction.

### 3.2 Types of Containers

Spring provides two main types of containers, depending on how you provide your configuration:

| Container Type | Configuration Source | Use Case |
| :--- | :--- | :--- |
| **BeanFactory** | XML or programmatic configuration. | The most basic container. Provides lightweight access to bean management. Used in resource-constrained environments (rare in modern apps). |
| **ApplicationContext** | XML, Java Annotations, or Java Config. | An advanced `BeanFactory`. Includes all `BeanFactory` features plus enterprise integration (AOP, internationalization, event propagation). **This is the standard for modern Spring applications.** |

**BeanFactory vs. ApplicationContext**

The primary difference is **capability**. While `BeanFactory` provides the fundamental "plumbing" for IoC, `ApplicationContext` adds a massive layer of "intelligence," such as automatic integration with other Spring modules and easier testing capabilities.

[↑ Back to Table of Contents](#table-of-contents)
***

*With the container understood, we can now look at the individual units of work within it: the Beans.*

## 4. Spring Bean Management

In Spring, a **Bean** is simply an object that is instantiated, assembled, and managed by the Spring IoC container.

### 4.1 Bean Definition and Instantiation

Before a bean can exist, the container must know how to create it. This is defined in the **Bean Definition**.

**1. Bean Definition**
A definition tells the container:
*   What class to instantiate.
*   What properties to set (dependencies).
*   What scope the bean should have.
*   What lifecycle callbacks to run.

You can provide these definitions via:
*   **XML Configuration:** `<bean id="myService" class="com.example.MyServiceImpl" />`
*   **Java Configuration:** `@Bean public MyService myService() { ... }`
*   **Annotation-based:** Using `@Component`, `@Service`, `@Repository`, etc., on the class itself.

**2. Instantiation Process**
When the container starts, it follows these steps for every definition:
1.  **Read Metadata:** Parse the configuration.
2.  **Instantiate:** Create the object instance (usually via reflection).
3.  **Populate Properties:** Perform Dependency Injection (injecting required beans).

### 4.2 The Bean Lifecycle

A bean's life is more than just "born and died." Spring provides hooks at various stages to allow for custom logic (like opening a database connection when a bean is born).

| Stage | Action | Description |
| :--- | :--- | :--- |
| **1. Instantiation** | Create Object | The bean instance is created in memory. |
| **2. Populate Properties** | Dependency Injection | The container injects all required dependencies into the bean. |
| **3. Initialization** | `init-method` / `@PostConstruct` | Custom logic is executed after the bean is fully "ready" but before it is used. |
| **4. Ready for Use** | In Service | The bean is now live and available to the application. |
| **5. Destruction** | `destroy-method` / `@PreDestroy` | Custom logic is executed before the bean is removed from the container (e.g., closing connections). |

> [!IMPORTANT]
> **The Initialization Hook:** Always use `@PostConstruct` or the `InitializingBean` interface for logic that depends on injected dependencies being present. If you try to use a dependency in the constructor, it may still be `null` because injection happens *after* construction.

### 4.3 Bean Scopes

**Scope** defines how long a bean lives and how many instances of it the container creates.

| Scope | Description | Lifetime |
| :--- | :--- | :--- |
| **Singleton** (Default) | Only **one instance** of the bean is created per Spring IoC container. | Created once at startup; shared by all callers. |
| **Prototype** | A **new instance** is created every time the bean is requested from the container. | Created upon request; caller is responsible for cleanup. |
| **Request** (Web Only) | A new instance is created for every single HTTP request. | Lives for the duration of one HTTP request. |
| **Session** (Web Only) | A single instance is created for the entire duration of an HTTP session. | Lives as long as the user's session is active. |

**Singleton vs. Prototype**

The choice between Singleton and Prototype is fundamental to application performance and state management.
*   **Singleton** is highly efficient because the object is reused, but you must ensure it is **stateless** (thread-safe).
*   **Prototype** is safer for objects that hold "user-specific" or "transaction-specific" state, but it incurs the overhead of frequent object creation.

### Implementation Example

Here is how you define these scopes using Spring annotations:

```java
// A Singleton bean (the default behavior)
@Component
@Scope("singleton")
public class DatabaseService {
    // Shared by all callers
}

// A Prototype bean
@Component
@Scope("prototype")
public class UserSessionTracker {
    // A new instance is created every time it is injected or requested
}
```

[↑ Back to Table of Contents](#table-of-contents)
