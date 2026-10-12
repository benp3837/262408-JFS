# Spring Data Transaction Management

## Table of Contents
* [1. High-Level Overview](#1-high-level-overview)
* [2. The Foundation: ACID Properties](#2-the-foundation-acid-properties)
* [3. Declarative Transaction Management: @Transactional](#3-declarative-transaction-management-transactional)
* [4. Transaction Propagation Strategies](#4-transaction-propagation-strategies)

***

## 1. High-Level Overview
In enterprise applications, maintaining data integrity during complex operations is critical. **Spring Data Transaction Management** provides a robust abstraction layer that allows developers to manage database transactions declaratively. This ensures that a series of database operations either all succeed (commit) or all fail (rollback), preventing "partial updates" that could leave the system in an inconsistent state.

This module covers the fundamental principles of transactions (**ACID**), the primary mechanism for applying them in Spring (**@Transactional**), the role of the **ResponseEntity** in web responses, and the complex ways transactions interact with each other (**Propagation**).

[↑ Back to Table of Contents](#table-of-contents)
***

*Before we look at how Spring implements transactions, we must understand the fundamental mathematical and logical rules that all database transactions must obey: the ACID properties.*

## 2. The Foundation: ACID Properties
To ensure reliable processing, every transaction must adhere to the **ACID** model. These four properties guarantee that database transactions are processed reliably.

| Property | Name | Description | Example Scenario |
| :--- | :--- | :--- | :--- |
| **A** | **Atomicity** | The "All or Nothing" rule. A transaction is treated as a single unit. | If a bank transfer fails halfway through, the money is not deducted from account A without being added to account B. |
| **C** | **Consistency** | Ensures a transaction brings the database from one valid state to another, maintaining all predefined rules (constraints, triggers). | A transaction cannot complete if it would result in a negative balance in an account where a `CHECK` constraint forbids it. |
| **I** | **Isolation** | Ensures that concurrent transactions do not interfere with each other. The results of an incomplete transaction are invisible to others. | Two people buying the last seat on a plane at the same time; isolation ensures only one succeeds. |
| **D** | **Durability** | Once a transaction is committed, it remains committed even in the event of a system failure (power outage, crash). | Once the "Transfer Successful" message appears, the data is written to permanent storage (disk). |

> [!IMPORTANT]
> **Atomicity** is the most frequently discussed property in application development, as it is the primary defense against "half-finished" business logic.

[↑ Back to Table of Contents](#table-of-contents)
***

*With the theoretical foundation of ACID established, we can now move to how Spring makes applying these principles effortless through declarative programming.*

## 3. Declarative Transaction Management: @Transactional
Spring simplifies transaction handling through **Declarative Transaction Management** using the `@Transactional` annotation. Instead of writing manual `begin`, `commit`, and `rollback` code (which is error-prone), you simply annotate a method or class.

### 3.1 How it Works: The Proxy Pattern
When you annotate a method with `@Transactional`, Spring does not execute your method directly. Instead, it creates a **Proxy** around your bean.

1. **Proxy Interception:** When a caller invokes the method, the Spring Proxy intercepts the call.
2. **Transaction Start:** The proxy starts a new transaction via the `TransactionManager`.
3. **Business Logic:** The proxy then calls your actual method.
4. **Outcome Handling:**
    * **Success:** If the method completes without an exception, the proxy **commits** the transaction.
    * **Failure:** If a `RuntimeException` (or configured exception) is thrown, the proxy triggers a **rollback**.

### 3.2 Configuration Nuances
| Feature | Implementation | Note |
| :--- | :--- | :--- |
| **Rollback Rules** | `rollbackFor = Exception.class` | By default, Spring only rolls back for **Unchecked Exceptions** (`RuntimeException` and `Error`). |
| **ReadOnly** | `readOnly = true` | Optimization hint for the database; prevents accidental modifications. |

#### Example: Standard Transactional Service
```java
@Service
public class UserService {

    @Autowired
    private UserRepository userRepository;

    @Transactional
    public void registerUser(User user) {
        // If any exception occurs here, the user is not saved
        userRepository.save(user);
        
        // Imagine another database operation here...
        // If this fails, the entire method rolls back.
        performAdditionalSetup(user);
    }

    @Transactional(readOnly = true)
    public User getUser(Long id) {
        return userRepository.findById(id).orElseThrow();
    }
}
```

> [!WARNING]
> **Self-Invocation Pitfall:** If a method inside a class calls another `@Transactional` method in the *same class* using `this.method()`, the transaction will **not** work. This is because the call bypasses the Spring Proxy.


[↑ Back to Table of Contents](#table-of-contents)
***

*Managing how multiple transactional methods behave when they call each other is a much more complex problem: Transaction Propagation.*

## 4. Transaction Propagation Strategies
**Propagation** defines the "boundary" of a transaction. It determines whether a method should join an existing transaction, start a new one, or behave differently when called from within an active transaction.

### 4.1 Common Propagation Types
Spring provides several strategies via the `propagation` attribute of `@Transactional`.

| Propagation | Name | Behavior |
| :--- | :--- | :--- |
| `REQUIRED` | **Required (Default)** | Joins the existing transaction if one exists; otherwise, starts a new one. |
| `REQUIRES_NEW` | **Requires New** | Always starts a new, independent transaction. If a transaction is already running, it is **suspended** until the new one finishes. |
| `NESTED` | **Nested** | Creates a "Savepoint" within the current transaction. If the nested transaction fails, it rolls back to the savepoint without failing the entire outer transaction. |
| `SUPPORTS` | **Supports** | If a transaction exists, it joins it. If not, it executes non-transactionally. |
| `MANDATORY` | **Mandatory** | Must be called within an existing transaction. Throws an exception if no transaction is active. |
| `NOT_SUPPORTED`| **Not Supported** | Always executes non-transactionally. If a transaction is active, it is suspended. |
| `NEVER` | **Never** | Must NOT be called within a transaction. Throws an exception if a transaction is active. |

### 4.2 Propagation: REQUIRED vs. REQUIRES_NEW
This is the most critical distinction for developers to understand.

**Scenario: A User Registration Process**
1.  **Method A (Outer):** `registerUser()` (Marked `@Transactional(propagation = REQUIRED)`)
2.  **Method B (Inner):** `logAuditTrail()` (Marked `@Transactional(propagation = REQUIRES_NEW)`)

*   **With `REQUIRED` (Both methods):** If `logAuditTrail()` fails and throws an exception, the **entire** transaction (including `registerUser`) rolls back. The user is not created, and the audit log is not saved.
*   **With `REQUIRES_NEW` (On Method B):** If `logAuditTrail()` fails, its transaction rolls back, but the **outer** `registerUser()` transaction can catch that exception and still proceed to commit the user creation. The audit log attempt is independent.

> [!TIP]
> Use `REQUIRES_NEW` for logging or auditing tasks where you want the record of the *attempt* to persist even if the main business logic fails.

[↑ Back to Table of Contents](#table-of-contents)
