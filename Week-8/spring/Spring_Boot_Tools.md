# Spring Boot Tools

## Table of Contents

* [1. High-Level Overview](#1-high-level-overview)
* [2. Spring Boot DevTools](#2-spring-boot-devtools)
* [3. Spring Environments](#3-spring-environments)
* [4. Spring Boot Actuator](#4-spring-boot-actuator)
    * [4.1 Actuator Overview](#41-actuator-overview)
    * [4.2 Built-In Actuator Endpoints](#42-built-in-actuator-endpoints)
* [5. Comparison: DevTools vs. Actuator](#5-comparison-devtools-vs-actuator)

***

## 1. High-Level Overview

Spring Boot is designed to reduce the boilerplate and configuration required to build production-ready applications. To achieve this, it provides a suite of specialized **Tools** that assist throughout the development lifecycle—from improving developer productivity during coding to providing deep observability in production.

This module covers three pillars of the Spring Boot ecosystem:
1.  **Spring Boot DevTools:** Optimizing the local development experience.
2.  **Spring Environments:** Managing configuration across different deployment stages.
3.  **Spring Boot Actuator:** Providing operational visibility and monitoring in production.

[↑ Back to Table of Contents](#table-of-contents)
***

*While DevTools makes the "inner loop" of coding faster, we still need a way to manage how our application behaves in different stages of its lifecycle.*

## 2. Spring Boot DevTools

**Spring Boot DevTools** is a set of tools designed to make the development process faster and more efficient by automating repetitive tasks.

### 2.1 Core Features

| Feature | Function | Benefit |
| :--- | :--- | :--- |
| **Automatic Restart** | Detects changes in classpath files and restarts the application context. | Eliminates the need for manual restarts after every code change. |
| **LiveReload** | A browser extension that triggers a page refresh when resources change. | Allows you to see UI/Static resource changes immediately. |
| **Configuration Defaults** | Disables caching (e.g., Thymeleaf templates) to ensure changes are visible. | Ensures you aren't seeing "stale" views due to template caching. |
| **Remote Development** | Supports pushing changes to a remote application (advanced). | Enables a "hot-reload" feel even when working on remote servers. |

### Implementation: Adding DevTools
To use DevTools, add the following dependency to your `pom.xml`:

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-devtools</artifactId>
    <scope>runtime</scope>
    <optional>true</optional>
</dependency>
```
> **Automatic Restart vs. Traditional Restarts:** Unlike a full application restart, DevTools uses a two-classloader approach. It keeps "base" libraries (like Spring Framework itself) in one classloader and your "application" code in another. When you change code, it only restarts the application classloader, making the process significantly faster.

[↑ Back to Table of Contents](#table-of-contents)
***

*Once the development loop is optimized, we must address the challenge of configuration: ensuring the app knows whether it is running on your laptop, a test server, or in the cloud.*

## 3. Spring Environments

A **Spring Environment** is an abstraction that represents the current running context of the application. It is the central place where Spring manages **Profiles** and **Properties**.

### 3.1 The Environment Components

The Environment is composed of two primary elements:
1.  **Profiles:** Logical groupings of configuration (e.g., `dev`, `test`, `prod`).
2.  **Property Sources:** Key-value pairs (from `application.properties`, environment variables, etc.).

### 3.2 Property Precedence (The Hierarchy)

Spring Boot uses a specific order of precedence to decide which property value "wins" if the same key is defined in multiple places.

| Precedence | Source | Description |
| :--- | :--- | :--- |
| **Highest** | Command Line Arguments | `--server.port=9090` |
| | JVM System Properties | `-Dserver.port=9090` |
| | OS Environment Variables | `SERVER_PORT=9090` |
| | Application Properties | `application.properties` or `application.yml` |
| **Lowest** | Default Properties | Hardcoded defaults in the code. |

### Implementation: Profile-Specific Configuration

Spring uses a naming convention for profile-specific properties: `application-{profile}.properties`.

**src/main/resources/application-dev.properties**
```properties
app.message=Welcome to the DEVELOPMENT environment
spring.datasource.url=jdbc:h2:mem:devdb
```

**src/main/resources/application-prod.properties**
```properties
app.message=Welcome to the PRODUCTION environment
spring.datasource.url=jdbc:postgresql://prod-db-server:5432/myapp
```

### Using `@Profile` in Code

You can use the `@Profile` annotation to register beans only when a specific profile is active.

```java
@Configuration
public class DataConfig {

    @Bean
    @Profile("dev")
    public DataSource devDataSource() {
        return new EmbeddedDatabaseBuilder()
                .setType(EmbeddedDatabaseType.H2)
                .build();
    }

    @Bean
    @Profile("prod")
    public DataSource prodDataSource() {
        // Real connection logic for production
        return new DriverManagerDataSource(...);
    }
}
```

> [!IMPORTANT]
> **Environment Variables for Cloud Native Apps:** Because environment variables have higher precedence than `application.properties`, they are the preferred way to inject secrets (like DB passwords) in Docker and Kubernetes environments without hardcoding them in your source code.

[↑ Back to Table of Contents](#table-of-contents)
***

*With configuration managed, we can now turn our attention to production readiness: how do we know our app is actually healthy and performing as expected?*

## 4. Spring Boot Actuator

**Spring Boot Actuator** is a sub-project that provides production-ready features to help you monitor and manage your application.

### 4.1 Actuator Overview

In a production environment, you cannot simply "debug" a running server. You need "windows" into the application's internal state. Actuator provides these windows via **Endpoints**—specialized URLs that expose metrics, health, and metadata.

### 4.2 Built-In Actuator Endpoints

Actuator provides a wide range of endpoints. By default, most are **hidden** for security reasons and must be explicitly enabled.

| Endpoint | Function | Example Use Case |
| :--- | :--- | :--- |
| **`/health`** | Shows application health information. | Used by Kubernetes liveness/readiness probes. |
| **`/info`** | Displays arbitrary application info. | Showing the current app version or build time. |
| **`/metrics`** | Shows various metrics (memory, CPU, etc.). | Feeding data into Prometheus or Grafana. |
| **`/env`** | Displays current environment properties. | Verifying which configuration profile is active. |
| **`/loggers`** | Allows viewing and changing log levels. | Changing `DEBUG` level on the fly without a restart. |
| **`/beans`** | Shows a complete list of all Spring Beans. | Debugging dependency injection issues. |
| **`/threaddump`** | Performs a thread dump. | Diagnosing deadlocks or performance bottlenecks. |

### Implementation: Actuator Configuration

By default, most Actuator endpoints are hidden for security. You must explicitly expose them in your `application.properties`.

```properties
# Expose specific endpoints
management.endpoints.web.exposure.include=health,info,metrics,env
```

### Extending Actuator: Custom Health Indicator

You can create your own health checks to monitor external dependencies (like a 3rd party API) via the `/health` endpoint.

```java
@Component
public class ExternalServiceHealthIndicator implements HealthIndicator {

    @Override
    public Health health() {
        boolean isServiceUp = checkExternalService(); // Your logic here
        
        if (isServiceUp) {
            return Health.up().withDetail("External API", "Available").build();
        } else {
            return Health.down().withDetail("External API", "Unavailable").build();
        }
    }

    private boolean checkExternalService() {
        // Simulate a connection check
        return true; 
    }
}
```

> [!WARNING]
> **Security Warning:** Many Actuator endpoints (like `/env`, `/beans`, or `/heapdump`) can leak sensitive information or system internals. **Never** expose these endpoints to the public internet without proper Spring Security protection.

[↑ Back to Table of Contents](#table-of-contents)
***

*To wrap up, let's compare the two primary "tooling" categories we've covered: one for the developer's desk and one for the production server.*

## 5. Comparison: DevTools vs. Actuator

While both are "tools," they serve opposite ends of the application lifecycle.

| Feature | **Spring Boot DevTools** | **Spring Boot Actuator** |
| :--- | :--- | :--- |
| **Primary Goal** | Developer Productivity (Speed) | Operational Visibility (Monitoring) |
| **Lifecycle Stage** | Development / Local | Production / Staging |
| **Key Action** | Restarting the app on change | Exposing internal state via HTTP |
| **Security Risk** | Very Low (Local only) | **High** (Can leak secrets/internals) |
| **Typical User** | Software Engineer | DevOps / SRE / Platform Engineer |

[↑ Back to Table of Contents](#table-of-contents)
