# Spring Introduction

## Table of Contents

* [1. High-Level Overview](#1-high-level-overview)
* [2. Dependency Injection (DI)](#2-dependency-injection-di)
    * [2.1 What is DI?](#21-what-is-di)
    * [2.2 Types of Dependency Injection](#22-types-of-dependency-injection)
        * [2.2.1 XML-Based Configuration](#221-xml-based-configuration)
        * [2.2.2 Java-Based Configuration](#222-java-based-configuration)

***

## 1. High-Level Overview

**Spring Framework** is the most popular application framework for Java development. At its core, Spring is designed to simplify the complexity of enterprise-level application development by providing a comprehensive programming and configuration model.

The primary goal of Spring is to enable developers to write cleaner, more modular, and more testable code. It achieves this primarily through **Inversion of Control (IoC)** and **Dependency Injection (DI)**, which decouple the creation of objects from their actual usage.

[↑ Back to Table of Contents](#table-of-contents)

***

*Now that we understand the high-level purpose of Spring, let's dive into its most fundamental mechanism: Dependency Injection.*

## 2. Dependency Injection (DI)

**Dependency Injection (DI)** is a design pattern used to implement **Inversion of Control (IoC)**. In a traditional program, an object is responsible for creating its own dependencies (the other objects it needs to function). In Spring, this responsibility is "inverted" and handed over to the **Spring IoC Container**.

### 2.1 What is DI?

In a standard "Manual" approach, you might see code like this:

```java
public class Car {
    private Engine engine;

    public Car() {
        this.engine = new GasolineEngine(); // Car is responsible for creating the Engine
    }
}
```

In this example, `Car` is **tightly coupled** to `GasolineEngine`. If you want to change to an `ElectricEngine`, you must modify the `Car` class.

With **Dependency Injection**, the `Car` simply asks for an `Engine`, and Spring provides it:

```java
public class Car {
    private Engine engine;

    // The engine is "injected" from the outside
    public Car(Engine engine) {
        this.engine = engine;
    }
}
```

This makes the `Car` class **loosely coupled**, highly flexible, and much easier to unit test using mocks.

[↑ Back to Table of Contents](#table-of-contents)

***

*Understanding DI is essential, but how do we actually tell Spring which objects to create and how to connect them? We do this through Configuration.*

## 2.2 Types of Dependency Injection

Spring offers several ways to define your **beans** (objects) and their relationships. While there are many methods, the two most significant evolutionary stages are **XML-Based Configuration** and **Java-Based Configuration**.

### 2.2.1 XML-Based Configuration

In the early days of Spring, all configuration was handled in external **XML files**. This approach completely separates the configuration from the Java source code.

**How it works:**
You define your beans and their dependencies in an `.xml` file located in your resources folder.

**Example Configuration (`applicationContext.xml`):**

```xml
<beans xmlns="http://www.springframework.org/schema/beans"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xsi:schemaLocation="http://www.springframework.org/schema/beans
       http://www.springframework.org/schema/beans/spring-beans.xsd">

    <!-- Define the Engine bean -->
    <bean id="myEngine" class="com.example.GasolineEngine" />

    <!-- Define the Car bean and inject the engine via Constructor Injection -->
    <bean id="myCar" class="com.example.Car">
        <constructor-arg ref="myEngine" />
    </bean>

</beans>
```

| Feature | XML-Based Configuration |
| :--- | :--- |
| **Separation** | Maximum; no configuration exists in Java code. |
| **Type Safety** | **Low**; errors in class names or property names are only caught at runtime. |
| **Refactoring** | **Difficult**; renaming a class requires manually updating XML strings. |
| **Modern Usage** | Primarily found in **legacy systems**. |

[↑ Back to Table of Contents](#table-of-contents)

***

*While XML was the foundation, modern Spring development has moved toward a more integrated, type-safe approach using Java code.*

### 2.2.2 Java-Based Configuration

**Java-Based Configuration** uses annotated Java classes to define **beans**. This is the modern standard in **Spring** and **Spring Boot** development. It leverages the power of the Java compiler to catch errors early.

**How it works:**
You create a class annotated with `@Configuration` and define methods annotated with `@Bean`. 

**Example Configuration:**

```java
@Configuration
public class AppConfig {

    @Bean
    public Engine myEngine() {
        return new GasolineEngine();
    }

    @Bean
    public Car myCar() {
        // We inject the engine by calling the method
        return new Car(myEngine());
    }
}
```

**XML vs. Java-Based Configuration**

| Comparison Point | XML-Based Configuration | Java-Based Configuration |
| :--- | :--- | :--- |
| **Complexity** | High (verbose XML syntax) | Low (standard Java syntax) |
| **Type Safety** | **Weak** (String-based) | **Strong** (Compile-time checked) |
| **IDE Support** | Limited autocomplete | Full IDE support (refactoring, navigation) |
| **Flexibility** | Can change config without recompiling | Requires recompilation to change config |

> [!TIP]
> **Modern Standard:** For almost all new projects, prefer **Java-Based Configuration** (or even better, **Annotation-Based Configuration** using `@Component` and `@Autowired`) to ensure type safety and developer productivity.

[↑ Back to Table of Contents](#table-of-contents)
