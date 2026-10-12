# Spring Security

## Table of Contents

* [1. High-Level Overview](#1-high-level-overview)
* [2. Authentication: The Identity Layer](#2-authentication-the-identity-layer)
    * [2.1 Authentication vs. Authorization](#21-authentication-vs-authorization)
    * [2.2 Authentication Providers](#22-authentication-providers)
* [3. Authorization: The Access Control Layer](#3-authorization-the-access-control-layer)
    * [3.1 RBAC (Role-Based Access Control)](#31-rbac-role-based-access-control)
* [4. The Security Architecture](#4-the-security-architecture)
    * [4.1 The SecurityFilterChain](#41-the-securityfilterchain)
* [5. Stateless Authentication & REST APIs](#5-stateless-authentication--securing-rest-apis-with-jwt)
    * [5.1 JSON Web Tokens (JWT)](#51-json-web-tokens-jwt)
    * [5.2 Securing REST APIs with JWT](#52-securing-rest-apis-with-jwt)

***

## 1. High-Level Overview

In a modern web application, security is not just a single feature but a multi-layered defense mechanism. **Spring Security** is a powerful, highly customizable authentication and access-control framework that provides non-invasive security for Spring applications. It focuses on protecting against common attacks (like CSRF, Session Fixation, and Clickjacking) while providing a robust model for managing identities and permissions.

[↑ Back to Table of Contents](#table-of-contents)
***

*Before we can decide what a user can do, we must first establish who they are.*

## 2. Authentication: The Identity Layer

**Authentication** is the process of verifying that a user (or system) is who they claim to be. In Spring Security, this is the first line of defense.

### 2.1 Authentication vs. Authorization

The two terms are often used interchangeably, but in security engineering, they represent distinct phases of the security lifecycle.

| Concept | Question Answered | Analogy |
| :--- | :--- | :--- |
| **Authentication** | "Who are you?" | Showing your Passport at an airport. |
| **Authorization** | "What are you allowed to do?" | Having a Boarding Pass that allows you into a specific gate. |

**The fundamental distinction:** Authentication happens *first*. You cannot determine what a user is allowed to do (Authorization) until you have verified their identity (Authentication).

[↑ Back to Table of Contents](#table-of-contents)
***

*Once identity is established, Spring Security needs a mechanism to validate the provided credentials.*

### 2.2 Authentication Providers

An **AuthenticationProvider** is a specialized component in Spring Security responsible for performing a specific type of authentication logic. 

Spring Security uses a modular approach: instead of one giant "login" function, it delegates the work to various providers based on the credentials provided.

*   **DaoAuthenticationProvider:** The most common provider. It retrieves user details from a `UserDetailsService` (usually a database) and compares them against the provided password (using a `PasswordEncoder`).
*   **LdapAuthenticationProvider:** Used for authenticating against an LDAP (Lightweight Directory Access Protocol) server.
*   **JwtAuthenticationProvider:** Specifically designed to validate and process JWTs.
*   **OAuth2LoginAuthenticationProvider:** Handles the complex flow of OAuth2/OpenID Connect social logins (e.g., "Login with Google").

**How it works:** When a user attempts to log in, the `AuthenticationManager` iterates through its configured `AuthenticationProviders`. The first provider that "supports" the specific type of token (e.g., a username/password token) will attempt to validate it.

[↑ Back to Table of Contents](#table-of-contents)
***

*Now that we know how to verify an identity, we must define the rules for what that identity can actually access.*

## 3. Authorization: The Access Control Layer

**Authorization** is the process of determining whether an authenticated principal (user/service) has the necessary permissions to perform a specific action or access a specific resource.

### 3.1 RBAC (Role-Based Access Control)

The most common model implemented in Spring Security is **RBAC**. In this model, permissions are not assigned directly to users. Instead, permissions are assigned to **Roles**, and users are assigned to those roles.

**The RBAC Hierarchy:**
1.  **Permissions/Privileges:** Granular actions (e.g., `READ_USER`, `WRITE_USER`).
2.  **Roles:** Groups of permissions (e.g., `ROLE_ADMIN`, `ROLE_USER`).
3.  **Users:** Assigned one or more roles.

**Why use RBAC?**
*   **Scalability:** It is much easier to manage 10 roles than to manage 1,000 individual user permissions.
*   **Efficiency:** When a user's responsibilities change, you simply change their role rather than hunting down every individual permission.

> [!TIP]
> In Spring Security, roles are traditionally prefixed with `ROLE_` (e.g., `ROLE_ADMIN`). When using method security like `@PreAuthorize("hasRole('ADMIN')")`, Spring automatically looks for the `ROLE_` prefix.

[↑ Back to Table of Contents](#table-of-contents)
***

*With identities and permissions defined, we need an engine to intercept every request and enforce these rules.*

## 4. The Security Architecture

The "engine" of Spring Security is a chain of filters that every incoming request must pass through before reaching your controllers.

### 4.1 The SecurityFilterChain

The **SecurityFilterChain** is a collection of Servlet Filters that are applied to a request in a specific order. This is known as the **Filter Chain Pattern**.

When a request hits your server, it doesn't go straight to your code. It enters the **FilterChainProxy**, which delegates the request to a specific **SecurityFilterChain**.

**The Flow of a Request:**
1.  **Request Arrival:** An HTTP request (e.g., `GET /api/admin/dashboard`) enters the filter chain.
2.  **Interception:** Filters intercept the request.
    *   A **JwtAuthenticationFilter** might look for a **Bearer** token in the headers.
    *   A **CsrfFilter** might check for a valid CSRF token.
    *   An **AuthorizationFilter** checks if the current user has **ROLE_ADMIN**.
3.  **Decision:** 
    *   **Success:** If all filters pass, the request reaches your `@RestController`.
    *   **Failure:** If a filter fails (e.g., invalid token or insufficient roles), the chain is broken, and an error (like `401 Unauthorized` or `403 Forbidden`) is returned immediately.

[↑ Back to Table of Contents](#table-of-contents)
***

*Traditional web apps use sessions, but modern APIs require a different approach to handle scale and decentralization.*

## 5. Stateless Authentication & Securing REST APIs with JWT

In traditional monolithic applications, the server keeps a **Session** in memory to remember who a user is. However, for RESTful microservices, this "Stateful" approach creates problems: if you have 10 instances of a service, which one holds the session?

To solve this, we use **Stateless Authentication**.

### 5.1 JSON Web Tokens (JWT)

A **JWT** is a compact, URL-safe means of representing claims to be transferred between two parties. It is a "self-contained" token, meaning it carries all the necessary user information within itself.

**The Anatomy of a JWT:**
A JWT consists of three parts separated by dots (`.`): `Header.Payload.Signature`

1.  **Header:** Contains metadata about the token (e.g., the algorithm used: `HS256`).
2.  **Payload:** Contains the **Claims**. This is the actual data (e.g., `sub: "user123"`, `roles: ["ROLE_USER"]`, `exp: 1723456789`).
3.  **Signature:** Created by taking the encoded header, the encoded payload, a secret key, and the algorithm specified in the header. This ensures the token hasn't been tampered with.

| Feature | Session-Based (Stateful) | JWT-Based (Stateless) |
| :--- | :--- | :--- |
| **Storage** | Server memory/Database | Client-side (Browser/Mobile) |
| **Scalability** | Harder (Requires Session Clustering) | Easier (No server state needed) |
| **Complexity** | Low (Built-in to most frameworks) | Higher (Requires token management/refresh) |
| **Revocation** | Easy (Delete session from server) | Hard (Tokens are valid until they expire) |

### 5.2 Securing REST APIs with JWT

When securing a REST API with JWT, the lifecycle follows this pattern:

1.  **Authentication:** The user sends credentials (username/password) to a `/login` endpoint.
2.  **Token Issuance:** The server validates the credentials and generates a signed JWT. This token is returned to the client.
3.  **Client Storage:** The client (React, Mobile App, etc.) stores the token (e.g., in `localStorage` or an `HttpOnly` cookie).
4.  **Subsequent Requests:** For every protected request, the client attaches the token in the `Authorization` header:

```http
Authorization: Bearer <token>
```

5.  **Server Validation:** 
*   The **SecurityFilterChain** intercepts the request.
*   The **JwtAuthenticationFilter** extracts the token.
*   The server verifies the **Signature** using its secret key.
*   The server checks the **Expiration** (`exp`).
*   If valid, the user's identity and roles are loaded into the **SecurityContext**.

> [!IMPORTANT]
> **Never store sensitive information (like passwords) in the JWT Payload.** The Payload is only Base64 encoded, not encrypted. Anyone who intercepts the token can read the contents. The Signature only prevents *tampering*, not *reading*.

[↑ Back to Table of Contents](#table-of-contents)
