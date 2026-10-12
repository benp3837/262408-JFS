# Swagger UI & OpenAPI in Spring Boot

## Table of Contents

* [1. High-Level Overview](#1-high-level-overview)
* [2. The Structural Framework: OpenAPI vs. Swagger](#2-the-structural-framework-openapi-vs-swagger)
* [3. Implementation: SpringDoc OpenAPI for Spring Boot](#3-implementation-springdoc-openapi-for-spring-boot)
    * [3.1 Dependencies](#31-dependencies)
    * [3.2 Automatic Documentation](#32-automatic-documentation)
    * [3.3 Customizing the UI](#33-customizing-the-ui)
* [4. Nuance & Integration: Security and Advanced Config](#4-nuance--integration-security-and-advanced-config)

***

## 1. High-Level Overview

In modern API-driven development, documentation is not a luxury; it is a requirement. **Swagger UI** is a powerful tool that provides a visual, interactive interface for discovering and interacting with an API's resources. Instead of reading static PDF or Markdown files, developers can use Swagger UI to "try out" API endpoints directly from their browser, seeing real-time request and response data.

In the context of **Spring Boot**, Swagger UI is typically implemented to automatically generate documentation based on your REST controllers, ensuring that your documentation always stays in sync with your actual code.

[↑ Back to Table of Contents](#table-of-contents)
***

## 2. The Structural Framework: OpenAPI vs. Swagger

It is common to use the terms "Swagger" and "OpenAPI" interchangeably, but they refer to different things. Understanding this distinction is critical for choosing the right tools.

| Concept | Definition | Purpose |
| :--- | :--- | :--- |
| **OpenAPI Specification (OAS)** | A formal, language-agnostic standard for describing RESTful APIs. | The **Contract**: A JSON/YAML file that defines paths, parameters, and schemas. |
| **Swagger UI** | An open-source tool that visualizes an OpenAPI specification. | The **Interface**: A web-based UI that renders the specification into an interactive page. |
| **Swagger Codegen** | A tool that generates client libraries or server stubs from an OAS file. | The **Automation**: Translates the contract into usable code. |

**OpenAPI vs. Swagger**
The relationship is best described as **Standard vs. Implementation**. **OpenAPI** is the "rulebook" (the specification), while **Swagger** is the set of tools (UI, Codegen, Editor) built by SmartBear to work with that rulebook.

[↑ Back to Table of Contents](#table-of-contents)
***

*Now that we have clarified the definitions, let's move from theory to implementation by integrating these tools into a Spring Boot application.*

## 3. Implementation: SpringDoc OpenAPI for Spring Boot

While there are several ways to implement Swagger, the industry standard for Spring Boot applications today is **SpringDoc OpenAPI**. It has largely superseded the older *Springfox* library, which is no longer actively maintained.

### 3.1 Dependencies

To get started, you need to add the `springdoc-openapi-starter-webmvc-ui` dependency to your `pom.xml` (Maven) or `build.gradle` (Gradle). This dependency includes both the OpenAPI generator and the Swagger UI itself.

**Maven Example:**
```xml
<dependency>
    <groupId>org.springdoc</groupId>
    <artifactId>springdoc-openapi-starter-webmvc-ui</artifactId>
    <version>2.3.0</version>
</dependency>
```

**Gradle Example:**
```groovy
implementation 'org.springdoc:springdoc-openapi-starter-webmvc-ui:2.3.0'
```

### 3.2 Automatic Documentation

Once the dependency is added, SpringDoc automatically scans your application for `@RestController` and `@RequestMapping` annotations. 

By default, once your application starts, you can access the Swagger UI at:
`http://localhost:8080/swagger-ui/index.html`

**How it works:**
1. **Scanning:** SpringDoc inspects your Spring beans.
2. **Metadata Extraction:** It reads your annotations (e.g., `@GetMapping`, `@RequestParam`, `@RequestBody`).
3. **Spec Generation:** It produces an OpenAPI JSON file (usually at `/v3/api-docs`).
4. **UI Rendering:** Swagger UI fetches that JSON and renders the interactive dashboard.

### 3.3 Customizing the UI

You often need to change the default behavior, such as the URL path or the API title. This is done via your `application.properties` or `application.yml`.

**Properties Configuration:**
```properties
# Change the path to the Swagger UI
springdoc.swagger-ui.path=/api-docs.html

# Change the path to the OpenAPI Spec (JSON)
springdoc.api-docs.path=/api-spec

# Enable/Disable Swagger UI
springdoc.swagger-ui.enabled=true
```

**Code-based Configuration (Bean Definition):**
To add metadata like versioning or descriptions, define an `OpenAPI` Bean:

```java
@Configuration
public class OpenApiConfig {

    @Bean
    public OpenAPI customOpenAPI() {
        return new OpenAPI()
                .info(new Info()
                        .title("My Awesome API")
                        .version("1.0")
                        .description("This is a sample Spring Boot RESTful service using SpringDoc."));
    }
}
```

[↑ Back to Table of Contents](#table-of-contents)
***

*Implementing the UI is one thing, but in a real-world enterprise application, you must ensure that this documentation is not exposed to the public internet.*

## 4. Nuance & Integration: Security and Advanced Config

### 4.1 Spring Security Integration

If your application uses **Spring Security**, Swagger UI will likely be blocked by default. You must explicitly permit access to the Swagger endpoints in your `SecurityFilterChain` configuration.

> [!IMPORTANT]
> **Security Warning:** Never leave Swagger UI wide open in a Production environment unless it is specifically intended for public API consumers. Use role-based access control to restrict visibility.

**Example Security Configuration:**
```java
@Bean
public SecurityFilterChain securityFilterChain(HttpSecurity http) throws Exception {
    http.authorizeHttpRequests(auth -> auth
        .requestMatchers("/v3/api-docs/**", "/swagger-ui/**", "/swagger-ui.html").permitAll()
        .anyRequest().authenticated()
    );
    return http.build();
}
```

### 4.2 Handling JWT Authentication

If your API uses Bearer Tokens (JWT), you need to tell Swagger UI how to send the `Authorization` header so you can actually "Try it out."

**Configuring Security Schemes:**
```java
@Configuration
public class OpenApiConfig {

    @Bean
    public OpenAPI customOpenAPI() {
        return new OpenAPI()
                .info(new Info().title("Secure API").version("1.0"))
                .addSecurityItem(new SecurityRequirement().addList("Bearer Authentication"))
                .components(new Components()
                        .addSecuritySchemes("Bearer Authentication", createAPIKeyScheme()));
    }

    private SecurityScheme createAPIKeyScheme() {
        return new SecurityScheme().type(SecurityScheme.Type.HTTP)
                .bearerFormat("JWT")
                .scheme("bearer");
    }
}
```

**Result:** After this configuration, a "Authorize" button will appear in Swagger UI, allowing you to paste your JWT and include it in all subsequent requests.

[↑ Back to Table of Contents](#table-of-contents)
