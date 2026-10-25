# Agents

## Table of Contents

* [1. High-Level Overview](#1-high-level-overview)
* [2. Understanding AI Agents](#2-understanding-ai-agents)
* [3. Agentic Workflows](#3-agentic-workflows)
* [4. Planning vs. Reactive Agents](#4-planning-vs-reactive-agents)
* [5. Human-in-the-Loop (HITL)](#5-human-in-the-loop-hitl)
* [6. Multi-Step Reasoning](#6-multi-step-reasoning)
* [7. Challenges & Constraints](#7-challenges--constraints)

***

## 1. High-Level Overview

In the rapidly evolving landscape of Artificial Intelligence, we are moving from passive models that simply respond to prompts toward active systems capable of autonomous action. This module explores the concept of **AI Agents**—systems designed to perceive, reason, and act to achieve specific goals. We will cover the fundamental architectures, the shift from single-step to agentic workflows, and the critical role of human oversight.

[↑ Back to Table of Contents](#table-of-contents)
***

*To understand how these systems operate, we must first define exactly what constitutes an "Agent" in the context of LLMs.*

## 2. Understanding AI Agents

An **AI Agent** is an autonomous or semi-autonomous system that uses a Large Language Model (LLM) as its "reasoning engine" to interact with the world. Unlike a standard chatbot, which primarily generates text, an agent can use **tools** (APIs, code execution, web search) to bridge the gap between thought and action.

### Core Components of an Agent
| Component | Function | Analogy |
| :--- | :--- | :--- |
| **Brain (LLM)** | Processes information, reasons through problems, and decides on actions. | The Mind |
| **Planning** | Breaks down complex goals into smaller, manageable sub-tasks. | The Strategy |
| **Memory** | Stores past experiences and context to inform future decisions. | The Experience |
| **Tools/Action** | External capabilities used to interact with the environment (e.g., a calculator, a browser). | The Hands |

[↑ Back to Table of Contents](#table-of-contents)
***

*While a single agent can perform tasks, the true power of modern AI lies in how those tasks are structured through workflows.*

## 3. Agentic Workflows

An **Agentic Workflow** refers to the iterative process where an agent doesn't just produce a single output, but instead engages in a loop of drafting, critiquing, and refining.

In a traditional "Zero-Shot" workflow, you give a prompt and get a result. In an **Agentic Workflow**, the system follows a cycle:
1. **Plan:** Decompose the request.
2. **Act:** Execute a tool or generate a draft.
3. **Observe:** Evaluate the result of the action.
4. **Refine:** Adjust the plan based on observations and repeat until the goal is met.

> [!TIP]
> **Agentic vs. Non-Agentic:** The key differentiator is **iteration**. If the system can "think about its own work" and correct itself, it is operating in an agentic workflow.

[↑ Back to Table of Contents](#table-of-contents)
***

*The way an agent decides its next move depends heavily on whether it follows a rigid path or a flexible, reasoning-based approach.*

## 4. Planning vs. Reactive Agents

Agents generally fall into two categories based on how they handle complexity and unpredictability.

### Planning Agents
**Planning Agents** attempt to look ahead. They create a comprehensive roadmap before taking significant actions. This is ideal for complex, multi-stage tasks where the steps are logically sequenced.
* **Method:** Task Decomposition (e.g., Chain of Thought, Tree of Thoughts).
* **Strength:** High coherence and goal alignment.
* **Weakness:** Can be computationally expensive and may struggle if the environment changes unexpectedly.

### Reactive Agents
**Reactive Agents** operate on a stimulus-response basis. They take an action, observe the immediate environment, and react to that observation without a long-term pre-defined plan.
* **Method:** ReAct (Reason + Act) patterns.
* **Strength:** Highly adaptable to dynamic or unpredictable environments.
* **Weakness:** Can get stuck in local optima or "loops" if they lack a sense of long-term direction.

| Feature | Planning Agents | Reactive Agents |
| :--- | :--- | :--- |
| **Primary Focus** | Long-term goal achievement | Immediate environmental response |
| **Complexity Handling** | High (breaks down large tasks) | Moderate (handles step-by-step) |
| **Adaptability** | Lower (plans may become stale) | Higher (adjusts per observation) |

[↑ Back to Table of Contents](#table-of-contents)
***

*Even the most autonomous agents benefit from—and often require—the guidance of a human operator.*

## 5. Human-in-the-Loop (HITL)

**Human-in-the-Loop (HITL)** is a design pattern where a human interacts with the agentic workflow at critical decision points. This is essential for safety, accuracy, and complex judgment calls.

### Common HITL Patterns
* **Approval Gates:** The agent proposes an action (e.g., "I want to delete this file" or "I want to send this email"), and the human must click "Approve" before it proceeds.
* **Feedback Loops:** The human provides qualitative feedback (e.g., "This response is too formal") which the agent uses to refine its next attempt.
* **Intervention:** A human manually takes control to steer the agent away from a mistake or a hallucination.

> [!IMPORTANT]
> **The Autonomy Trade-off:** Increasing autonomy increases efficiency but also increases the risk of catastrophic errors. HITL is the primary mechanism for managing this risk.

[↑ Back to Table of Contents](#table-of-contents)
***

*At the heart of both planning and reactive agents lies the capability to perform sophisticated, multi-step reasoning.*

## 6. Multi-Step Reasoning

**Multi-Step Reasoning** is the cognitive process that allows an agent to move from a high-level goal to a low-level execution through a series of logical inferences.

Instead of jumping from **Goal $\rightarrow$ Result**, the agent performs **Goal $\rightarrow$ Step 1 $\rightarrow$ Observation $\rightarrow$ Step 2 $\rightarrow$ Observation $\\rightarrow$ Result**.

### Key Reasoning Techniques
* **Chain of Thought (CoT):** Encouraging the model to "show its work" by outputting intermediate reasoning steps.
* **Self-Reflection:** The agent reviews its own previous outputs to identify errors or areas for improvement.
* **Tree of Thoughts (ToT):** Exploring multiple reasoning paths simultaneously and evaluating which one is most likely to lead to the solution.

[↑ Back to Table of Contents](#table-of-contents)
***

## 7. Challenges & Constraints

As agentic systems move from research prototypes to production environments, they encounter significant "real-world" friction. Understanding these constraints is crucial for designing reliable systems.

### Common Failure Modes

| Failure Mode | Description | Mitigation Strategy |
| :--- | :--- | :--- |
| **Infinite Reasoning Loops** | The agent becomes stuck in a repetitive cycle of the same failed action/observation. | Implement **Max Iterations** and mandatory "break" conditions. |
| **Context Contamination** | Long-term memory or previous observations "pollute" the current reasoning window. | Use **Summarization** or **Vector Retrieval** to inject only relevant context. |
| **Goal Drift / Misalignment** | The agent interprets a high-level goal too literally or deviates during long reasoning chains. | Use **HITL (Human-in-the-Loop)** and strict **System Prompts**. |

> [!WARNING]
> **The "Unintended Agency" Risk:** An autonomous agent might achieve a goal in a way that violates implicit constraints. For example, an agent tasked with "optimizing server costs" might decide the most efficient path is to shut down all active services. Always define **Guardrails** to prevent such catastrophic "successes."

[↑ Back to Table of Contents](#table-of-contents)
