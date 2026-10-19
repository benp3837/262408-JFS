# Spring Cloud

## Table of Contents

* [1. High-Level Overview](#1-high-level-overview)
* [2. Service Discovery](#2-service-discovery)
    * [2.1 Netflix Eureka](#21-netflix-eureka)
    * [2.2 HashiCorp Consul](#22-hashicorp-consul)
* [3. Edge & Communication](#3-edge--communication)
    * [3.1 API Gateway](#31-api-gateway)
    * [3.2 Feign Client](#32-feign-client)
* [4. Resilience & Stability](#4-resilience--stability)
    * [4.1 Load Balancing](#41-load-balancing)
    * [4.2 Spring Cloud Circuit Breaker](#42-spring-cloud-circuit-breaker)
* [5. Infrastructure & Observability](#5-infrastructure--observability)
    * [5.1 Config Server](#51-config-server)
    * [5.2 Distributed Tracing](#52-distributed-tracing)
    * [5.3 Monitoring Tools](#53-monitoring-tools)

***

## 1. High-Level Overview

In a microservices architecture, managing dozens or hundreds of independent services becomes impossible using static configurations. **Spring Cloud** provides a suite of tools that address the fundamental challenges of distributed systems: how services find each other, how they communicate reliably, how they handle failures, and how they are monitored.

Rather than solving a single problem, Spring Cloud provides a **Distributed System Chassis**—a set of patterns that allow developers to focus on business logic while the infrastructure handles the complexity of the network.

[↑ Back to Table of Contents](#table-of-contents)
***

*With the high-level landscape established, let's look at the first pillar of microservices: how services find each other in a dynamic environment.*

## 2. Service Discovery

In a cloud environment, service instances are ephemeral; they spin up and shut down constantly, often with changing IP addresses. **Service Discovery** acts as a "phone book" for your microservices.

### 2.1 Netflix Eureka

**Netflix Eureka** is a REST-based service discovery component. It follows a **Client/Server** model where service instances register themselves upon startup.

*   **Eureka Server:** The central registry that maintains the list of active service instances.
*   **Eureka Client:** The individual microservices that register with the server and periodically send "heartbeats" to prove they are still alive.

| Feature | Description |
| :--- | :--- |
| **Registration** | Services tell the server: "I am `Order-Service` at `10.0.0.5:8080`." |
| **Heartbeats** | Services send signals every 30s. If a signal is missed, Eureka removes the instance. |
| **Self-Preservation** | If many heartbeats fail at once (e.g., network glitch), Eureka enters "Self-Preservation" mode to avoid mass-evicting healthy services. |

### 2.2 HashiCorp Consul

While Eureka is a dedicated discovery tool, **HashiCorp Consul** is a more comprehensive service mesh and discovery tool.

**Consul vs. Eureka**

| Feature | Netflix Eureka | HashiCorp Consul |
| :--- | :--- | :--- |
| **Primary Focus** | Service Discovery only. | Discovery, KV Store, and Service Mesh. |
| **Health Checking** | Basic (Heartbeat based). | Advanced (HTTP, TCP, Script-based checks). |
| **Consistency Model** | **AP** (Availability/Partition Tolerance) - Prioritizes availability. | **CP** (Consistency/Partition Tolerance) - Prioritizes strong consistency. |
| **Ecosystem** | Deeply integrated with Spring Cloud. | Language-agnostic; works with any tech stack. |

> [!TIP]
> Choose **Eureka** if you are building a pure Spring Boot ecosystem and want simple, high-availability discovery. Choose **Consul** if you need a centralized Configuration/KV store or if you have a polyglot (non-Java) environment.

[↑ Back to Table of Contents](#table-of-contents)
***

*Now that services can find each other, we need a single entry point to manage client requests and orchestrate how they reach those services.*

## 3. Edge & Communication

Once discovery is in place, we must manage how external clients (Web/Mobile) enter our system and how internal services talk to one another.

### 3.1 API Gateway

An **API Gateway** acts as the "Front Door" to your entire microservices ecosystem. Instead of clients calling 50 different services, they call one Gateway.

**Key Responsibilities:**
*   **Routing:** Mapping an incoming request (e.g., `/orders/**`) to the correct service.
*   **Cross-Cutting Concerns:** Handling Authentication, Authorization, SSL termination, and Rate Limiting in one central place.
*   **Request Transformation:** Modifying headers or paths before passing the request along.

### 3.2 Feign Client

While the Gateway handles external traffic, **Feign Client** simplifies internal communication. It is a **Declarative REST Client**.

Instead of writing complex code using `RestTemplate` to call another service, you simply define an **Interface** and annotate it.

**Example Implementation:**
```java
@FeignClient(name = "inventory-service")
public interface InventoryClient {

    @GetMapping("/api/inventory/{productId}")
    boolean checkStock(@PathVariable("productId") String productId);
}
```

**Why use Feign?**
*   **Abstraction:** You write Java interfaces, not HTTP logic.
*   **Integration:** It integrates natively with Load Balancing and Circuit Breakers.

[↑ Back to Table of Contents](#table-of-contents)
***

*Communication is easy when everything is working, but in a distributed system, network failures are inevitable. We must build for resilience.*

## 4. Resilience & Stability

In a microservices world, one slow service can cause a "Cascading Failure" that brings down the entire system. We prevent this through Load Balancing and Circuit Breaking.

### 4.1 Load Balancing

**Load Balancing** ensures that traffic is distributed evenly across multiple instances of a single service, preventing any one instance from being overwhelmed.

*   **Client-Side Load Balancing (Spring Cloud LoadBalancer):** The client (the service calling another) knows about all available instances (via Eureka) and decides which one to call. This is more efficient than a centralized hardware load balancer because it eliminates an extra "hop."

### 4.2 Spring Cloud Circuit Breaker

A **Circuit Breaker** prevents a client from repeatedly trying to call a failing service, which saves resources and allows the failing service time to recover.

It operates like an electrical circuit breaker in your home:

| State | Behavior |
| :--- | :--- |
| **CLOSED** | Everything is normal. Requests flow through to the service. |
| **OPEN** | The service is failing. The circuit "trips," and requests are **immediately rejected** with a "fallback" response (e.g., a cached value or a default error). |
| **HALF-OPEN** | After a timeout, the circuit allows a few "test" requests to see if the service has recovered. If they succeed, it closes; if they fail, it opens again. |

> [!IMPORTANT]
> **The Fallback Pattern:** Always implement a fallback method in your Circuit Breaker. If the `Inventory-Service` is down, the fallback might return `true` (assume stock is available) or a generic message, ensuring the user experience doesn't simply crash.

[↑ Back to Table of Contents](#table-of-contents)
***

*With resilience built in, we move to the final layer: managing the complexity of configurations and keeping an eye on the health of the entire system.*

## 5. Infrastructure & Observability

The final pillar involves managing environmental settings and gaining visibility into how requests flow through the complex web of services.

### 5.1 Config Server

In a microservice environment, you cannot manually update `.properties` files in 50 different containers. **Spring Cloud Config Server** provides a centralized, externalized configuration repository.

*   **Centralized Management:** All configuration (for Dev, Test, and Prod) is stored in one place (usually a Git repository).
*   **Dynamic Refresh:** Using `@RefreshScope`, you can update configuration values in the Config Server and trigger the microservices to reload them **without restarting the application**.

### 5.2 Distributed Tracing

When a user gets a `500 Internal Server Error`, and that request touched 10 different services, finding the root cause is like finding a needle in a haystack. **Distributed Tracing** solves this by attaching a unique **Trace ID** to the request as it enters the system.

*   **Trace ID:** Represents the entire journey of a single user request across all services.
*   **Span ID:** Represents a single unit of work within one specific service.

By looking at the Trace ID, you can see exactly which service in the chain failed or was slow.

### 5.3 Monitoring Tools

Observability is completed by real-time monitoring and metrics collection.

| Tool | Purpose |
| :--- | :--- |
| **Spring Boot Actuator** | Provides "health checks" and internal metrics (CPU, Memory, HTTP requests) via HTTP endpoints. |
| **Prometheus** | A time-series database that "scrapes" (pulls) metrics from your services. |
| **Grafana** | The visualization layer. It turns Prometheus data into beautiful, real-time dashboards for your operations team. |

[↑ Back to Table of Contents](#table-of-contents)
