# Spring ORM (Object-Relational Mapping)

## Table of Contents

* [1. High-Level Overview](#1-high-level-overview)
* [2. The Core Concepts](#2-the-core-concepts)
    * [2.1 Object-Relational Mapping (ORM)](#21-object-relational-mapping-orm)
    * [2.2 Class vs. Schema](#22-class-vs-schema)
* [3. The Implementation Ecosystem](#3-the-implementation-ecosystem)
    * [3.1 Spring Data ORM Providers](#31-spring-data-orm-providers)
    * [3.2 Hibernate](#32-hibernate)
* [4. Configuration & Model Definition](#4-configuration--model-definition)
    * [4.1 Annotations for Model Classes](#41-annotations-for-model-classes)
    * [4.2 hibernate.cfg.xml](#42-hibernatecfgxml)
* [5. Data Persistence Patterns](#5-data-persistence-patterns)
    * [5.1 Inheritance Hierarchies](#51-inheritance-hierarchies)
    * [5.2 Caching](#52-caching)
* [6. Querying the Database](#6-querying-the-database)
    * [6.1 HQL (Hibernate Query Language)](#61-hql-hibernate-query-language)
    * [6.2 JPQL (Java Persistence Query Language)](#62-jpql-java-persistence-query-language)
    * [6.3 Native SQL](#63-native-sql)
    * [6.4 Criteria API](#64-criteria-api)

***

## 1. High-Level Overview

In modern enterprise applications, there is a fundamental mismatch between the way data is structured in **Object-Oriented Programming (OOP)** and the way it is stored in **Relational Databases (RDBMS)**. This mismatch is known as the **Object-Relational Impedance Mismatch**.

**Object-Relational Mapping (ORM)** provides a layer of abstraction that allows developers to interact with a database using Java objects instead of writing manual SQL for every operation. By automating the mapping between objects and tables, it increases developer productivity, reduces boilerplate code, and enhances maintainability.

[↑ Back to Table of Contents](#table-of-contents)
***

*To understand how this abstraction works, we must first look at the fundamental concept of mapping and how code structures relate to database structures.*

## 2. The Core Concepts

### 2.1 Object-Relational Mapping (ORM)

**Object-Relational Mapping (ORM)** is a programming technique for converting data between incompatible type systems in object-oriented programming languages and relational databases.

*   **In Java:** You work with **Classes**, **Fields**, and **Object Instances**.
*   **In the Database:** You work with **Tables**, **Columns**, and **Rows**.

An **ORM framework** acts as the "translator," automatically mapping a Java class to a database table and its properties to specific columns.

### 2.2 Class vs. Schema

While often used interchangeably in casual conversation, they represent different layers of the application.

| Feature | Class (Java Side) | Schema (Database Side) |
| :--- | :--- | :--- |
| **Definition** | A blueprint for creating objects in code. | The logical structure of the database. |
| **Elements** | **Classes**, **Fields**, **Methods**, **Types**. | **Tables**, **Columns**, **Constraints**, **Indexes**. |
| **Nature** | Defines behavior and data structure. | Defines data integrity and relationships. |
| **Mapping** | The **Entity** class. | The **Table** definition. |

**Relationship:** The **ORM framework** ensures that the **Class** structure remains synchronized with the **Schema** structure.

[↑ Back to Table of Contents](#table-of-contents)
***

*Now that we understand the core concepts, let's explore the specific tools and providers that Spring uses to bridge these worlds.*

## 3. The Implementation Ecosystem

### 3.1 Spring Data ORM Providers

Spring does not implement the ORM logic itself. Instead, it provides a unified programming model (like Spring Data JPA) that can work with various underlying **ORM Providers**.

An **ORM Provider** is the engine that actually performs the heavy lifting of generating SQL, managing connections, and tracking **object states**.

### 3.2 Hibernate

**Hibernate** is the most widely used ORM provider in the Java ecosystem and is the default provider used by Spring Boot for **JPA (Java Persistence API)** implementations.

*   **Role:** It implements the **JPA specification**.
*   **Key Feature:** It provides high-performance data access through advanced features like **lazy loading**, **dirty checking**, and **multi-level caching**.

[↑ Back to Table of Contents](#table-of-contents)
***

*With a provider like Hibernate in place, we need to define how our Java models actually look and how they are configured.*

## 4. Configuration & Model Definition

### 4.1 Annotations for Model Classes

In Spring ORM (specifically **JPA/Hibernate**), we use **Annotations** to metadata-tag Java classes, turning them into **Entities**.

| Annotation | Purpose |
| :--- | :--- |
| `@Entity` | Marks the class as a persistent entity mapped to a table. |
| `@Table(name="...")` | Specifies the exact name of the database table. |
| `@Id` | Designates the primary key of the entity. |
| `@GeneratedValue` | Defines the strategy for primary key generation (e.g., `IDENTITY`, `SEQUENCE`). |
| `@Column(name="...")` | Maps a specific field to a specific database column. |
| `@OneToMany` / `@ManyToOne` | Defines relationships between entities. |

### 4.2 hibernate.cfg.xml

In traditional Hibernate setups, `hibernate.cfg.xml` is the central configuration file. It tells Hibernate:
1.  **Database Connection Details:** URL, username, password, driver.
2.  **Dialect:** Which SQL "dialect" to use (e.g., `MySQL8Dialect`, `PostgreSQLDialect`) so Hibernate knows how to write vendor-specific SQL.
3.  **Mapping Files:** Where to find the entity classes.

> [!TIP]
> In modern **Spring Boot** applications, explicit `hibernate.cfg.xml` files are often replaced by properties defined in `application.properties` or `application.yml`, which Spring then uses to configure the Hibernate `SessionFactory` automatically.

[↑ Back to Table of Contents](#table-of-contents)
***

*Once the models are defined and configured, we can manage complex data structures and optimize performance.*

## 5. Data Persistence Patterns

### 5.1 Inheritance Hierarchies

Relational databases do not have a native concept of "inheritance" like Java does. To solve this, ORM providers offer several strategies to map Java inheritance to database tables:

1.  **Single Table Strategy:** All classes in the hierarchy are stored in **one single table**. A "Discriminator Column" is used to tell which class a specific row belongs to.
    *   *Pro:* Fast queries (no joins).
    *   *Con:* Many columns will be NULL for certain subclasses.
2.  **Joined Table Strategy:** Each class has its **own table**, containing only its specific fields. Subclass tables are linked to the parent table via **Foreign Keys**.
    *   *Pro:* Highly normalized and clean.
    *   *Con:* Requires expensive `JOIN` operations to fetch data.
3.  **Table Per Class Strategy:** Every concrete class has its own table containing *all* fields (including inherited ones).
    *   *Pro:* Simple for individual class queries.
    *   *Con:* Difficult to perform **polymorphic queries** (queries across the whole hierarchy).

### 5.2 Caching

To avoid hitting the database repeatedly for the same data, ORM providers implement **Caching**.

| Level | Scope | Description |
| :--- | :--- | :--- |
| **First-Level Cache** | **Session/Transaction** | Mandatory. It lives within the current Hibernate `Session`. If you request the same object twice in one transaction, Hibernate returns the cached instance. |
| **Second-Level Cache** | **SessionFactory/Application** | Optional. It lives across multiple sessions. This allows different users/transactions to share cached data, significantly reducing database load. |

[↑ Back to Table of Contents](#table-of-contents)
***

*The final stage of ORM is learning how to retrieve the data we have persisted, ranging from high-level abstractions to low-level SQL.*

## 6. Querying the Database

### 6.1 HQL (Hibernate Query Language)

**HQL** is an object-oriented query language, proprietary to Hibernate. Instead of querying tables and columns, you query **Objects and Properties**.

*   **Example:** `FROM User u WHERE u.email = :email`
*   **Key Trait:** It is aware of the object model and relationships.

### 6.2 JPQL (Java Persistence Query Language)

**JPQL** is the standard specification version of HQL. While HQL is Hibernate-specific, JPQL is part of the JPA standard. They are very similar, but JPQL is designed to be vendor-neutral.

| Feature | HQL | JPQL |
| :--- | :--- | :--- |
| **Standardization** | Proprietary to Hibernate. | Part of the JPA Standard. |
| **Capability** | Often includes Hibernate-specific extensions. | Follows strict JPA rules. |
| **Portability** | Tied to Hibernate. | Highly portable across any JPA provider. |

### 6.3 Native SQL

Sometimes, ORM abstractions are too restrictive or inefficient for highly complex, vendor-specific queries. In these cases, you can use **Native SQL**.

*   **How:** You write raw SQL strings directly in your repository or query.
*   **Trade-off:** You lose database portability and the benefits of object-oriented querying, but you gain maximum control and performance for complex operations.

### 6.4 Criteria API

The **Criteria API** provides a way to build queries **programmatically** using Java code rather than strings.

*   **Type-Safe:** Because it uses Java methods and classes, the compiler can catch errors (unlike HQL/JPQL strings).
*   **Dynamic:** It is perfect for building complex search screens where the user might choose any combination of filters at runtime.

**Example Concept:**
Instead of `WHERE name = 'John'`, you write `cb.equal(root.get("name"), "John")`.

[↑ Back to Table of Contents](#table-of-contents)
