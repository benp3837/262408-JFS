# Spring AI

## Table of Contents

* [1. High-Level Overview](#1-high-level-overview)
* [2. Structural Framework: Core Concepts](#2-structural-framework-core-concepts)
    * [2.1 ChatClient Overview](#21-chatclient-overview)
    * [2.2 Sending Prompts](#22-sending-prompts)
    * [2.3 Prompt Templates](#23-prompt-templates)
    * [2.4 System vs. User Prompts](#24-system-vs-user-prompts)
* [3. Granular Implementation: Integration & Deployment](#3-granular-implementation-integration--deployment)
    * [3.1 Exposing AI via Spring Boot REST APIs](#31-exposing-ai-via-spring-boot-rest-apis)
    * [3.2 Integrating AI into Enterprise Applications](#32-integrating-ai-into-enterprise-applications)

***

## 1. High-Level Overview

**Spring AI** is an application framework for building AI-powered applications. It aims to provide a consistent, portable API for interacting with various Artificial Intelligence models, effectively abstracting the complexities of individual model providers (like OpenAI, Azure, or Ollama) away from the developer.

By following the **Spring Programming Model**, it allows developers to integrate generative AI capabilities into their existing Java ecosystems with the same ease as adding a database or a messaging service.

[↑ Back to Table of Contents](#table-of-contents)
***

*Now that we understand the purpose of Spring AI, let's dive into the core components that drive interaction with the models.*

## 2. Structural Framework: Core Concepts

The interaction with any LLM (Large Language Model) in Spring AI revolves around the concept of the **Prompt** and the **Client**.

### 2.1 ChatClient Overview

The **`ChatClient`** is the primary entry point for interacting with AI models in Spring AI. It serves as a high-level abstraction that wraps the underlying model implementation.

| Feature | Description |
| :--- | :--- |
| **Abstraction** | Allows you to switch between providers (e.g., **OpenAI** to **Bedrock**) with minimal code changes. |
| **Fluent API** | Provides a modern, builder-style API for constructing complex requests. |
| **Integrated Capabilities** | Combines **prompting**, **context management**, and **output parsing** into a single interface. |

A **Prompt** is the input sent to the AI. In Spring AI, you don't just send strings; you interact with structured objects that allow for sophisticated control.

**Basic Usage Example:**
```java
// Simple string-based prompt
String response = chatClient.call("Tell me a joke about Java.");
```

### 2.3 Prompt Templates

To avoid hardcoding text, Spring AI uses **`PromptTemplate`**. This allows you to create reusable "blueprints" where specific variables can be injected at runtime.

**Template Definition:**
```text
You are a helpful assistant that explains {topic} to a {audience} level.
```

**Implementation:**
```java
PromptTemplate template = new PromptTemplate("You are a helpful assistant that explains {topic} to a {audience} level.");
Prompt prompt = template.create(Map.of("topic", "Spring AI", "audience", "beginner"));
ChatResponse response = chatClient.call(prompt);
```

### 2.4 System vs. User Prompts

Understanding the distinction between these two roles is crucial for controlling the "personality" and "constraints" of the AI.

| Prompt Type | Role | Purpose |
| :--- | :--- | :--- |
| **System Prompt** | The "Instruction" | Defines the **persona**, **rules**, **tone**, and **boundaries** of the AI (e.g., "You are a formal legal expert"). |
| **User Prompt** | The "Question" | Represents the specific request or query from the end-user (e.g., "What is a contract?"). |

> [!TIP]
> **Best Practice:** Always use a **System Prompt** to ground the model's behavior and prevent "jailbreaking" or off-topic responses.

### 2.5 RAG vs. Direct Prompting

While direct prompting is sufficient for simple tasks, complex enterprise needs often require **Retrieval-Augmented Generation (RAG)**.

| Feature | Direct Prompting | RAG (Retrieval-Augmented Generation) |
| :--- | :--- | :--- |
| **Knowledge Source** | The model's internal training data. | External, private, or real-time data sources. |
| **Context Window** | Limited to what the user provides in the prompt. | Dynamically expanded by injecting relevant document snippets. |
| **Hallucination Risk** | Higher, as the model may "fill in gaps" with fabricated info. | Lower, as the model is grounded in retrieved, verifiable facts. |
| **Best Use Case** | General knowledge, reasoning, creative writing. | Q&A on private docs, technical support, real-time data queries. |

[↑ Back to Table of Contents](#table-of-contents)
***

*With the core interaction patterns mastered, we can now explore how to bring these capabilities into a production-grade environment.*

## 3. Granular Implementation: Integration & Deployment

### 3.1 Exposing AI via Spring Boot REST APIs

The most common way to expose AI capabilities is through a standard Spring Boot REST controller. This turns your AI logic into a consumable microservice.

> [!WARNING]
> **Security Warning:** Exposing AI endpoints directly to the internet can lead to **Prompt Injection** attacks or excessive token usage. Always implement rate limiting and strict input validation via **Spring Security**.

**Standard Workflow:**
1. **Inject `ChatClient`** into your Controller.
2. **Create a Request DTO** to capture user input.
3. **Map the Request to a Prompt.**
4. **Return the Response** as a JSON object.

**Example Controller:**
```java
@RestController
@RequestMapping("/api/ai")
public class AiController {

    private final ChatClient chatClient;

    public AiController(ChatClient.Builder builder) {
        this.chatClient = builder.build();
    }

    @PostMapping("/chat")
    public String chat(@RequestBody String userMessage) {
        return chatClient.prompt()
                .user(userMessage)
                .call()
                .content();
    }
}
```

### 3.2 Integrating AI into Enterprise Applications

Integrating AI into large-scale enterprise environments requires more than just a simple API call. It necessitates addressing data security, context, and reliability.

**Key Integration Patterns:**

1.  **RAG (Retrieval-Augmented Generation):**
    *   **Problem:** LLMs have a knowledge cutoff and don't know your private enterprise data.
    *   **Solution:** Use Spring AI's **Vector Store** integration to retrieve relevant snippets from your own documents and inject them into the **Prompt** context before calling the model.

2.  **Function Calling (Tool Use):**
    *   **Problem:** AI can "talk" but cannot "do" (e.g., it can't check an inventory database).
    *   **Solution:** Define Java functions and register them with the **`ChatClient`**. The model can then request to execute these functions to fetch real-time data or trigger business workflows.

3.  **Observability & Monitoring:**
    *   **Strategy:** Use **Spring Boot Actuator** and **Micrometer** to track **token usage**, **latency**, and **error rates** of your AI calls. This is vital for cost management and SLA compliance in enterprise settings.

4.  **Security & Governance:**
    *   **Strategy:** Implement strict input validation to prevent **Prompt Injection** and use **Spring Security** to manage who can access specific AI capabilities and which data can be sent to third-party providers.

[↑ Back to Table of Contents](#table-of-contents)
