# LangGraph

## Table of Contents

* [1. High-Level Overview](#1-high-level-overview)
* [2. Structural Framework: The Graph Architecture](#2-structural-framework-the-graph-architecture)
    * [2.1 Core Components](#21-core-components)
    * [2.2 State Management](#22-state-management)
* [3. Graph-based Agent Workflows](#3-graph-based-agent-workflows)
    * [3.1 The Agentic Loop](#31-the-agentic-loop)
    * [3.2 Control Flow vs. Sequential Chains](#32-control-flow-vs-sequential-chains)
* [4. Implementation Pattern](#4-implementation-pattern)
* [5. Nuance & Best Practices](#5-nuance--best-practices)

***

## 1. High-Level Overview

**LangGraph** is a library built on top of LangChain designed to create complex, stateful, and multi-actor applications with LLMs. While standard LangChain chains are typically linear and directed acyclic graphs (DAGs), LangGraph enables the creation of **cyclic graphs**, allowing for iterative reasoning, loops, and complex agentic behaviors.

[↑ Back to Table of Contents](#table-of-contents)
***

*While the high-level purpose of LangGraph is to enable cycles, understanding how these cycles are governed requires looking at the underlying structural framework.*

## 2. Structural Framework: The Graph Architecture

LangGraph treats an agentic workflow as a state machine. The workflow is represented as a graph consisting of nodes and edges.

### 2.1 Core Components

| Component | Definition | Role in the Workflow |
| :--- | :--- | :--- |
| **Nodes** | Functions or units of work. | Execute specific logic (e.g., "call LLM", "search tool", "format response"). |
| **Edges** | Connections between nodes. | Define the path of execution from one node to the next. |
| **Conditional Edges** | Logic-based routing. | Use functions to decide which node to visit next based on the current state (e.g., "if LLM says 'finish', go to END; otherwise, go to 'tools'"). |

### 2.2 State Management

The defining feature of LangGraph is its approach to **State Management**. In a traditional chain, data is passed from one step to the next in a linear flow. In LangGraph, a single, shared **State Object** is passed through the entire graph.

*   **Persistence:** The state acts as the "short-term memory" of the agent. Every node receives the current state, modifies it, and returns the updated state.
*   **Reducers:** LangGraph uses **Reducers** to determine how to update the state. Instead of simply overwriting the state, a reducer can define how to *append* to a list (e.g., adding a new message to a `messages` list) rather than replacing it.

> [!IMPORTANT]
> **State is the Source of Truth:** Because every node contributes to and reads from the same state object, the entire history and context of the agent's reasoning are preserved and accessible throughout the cycle.

[↑ Back to Table of Contents](#table-of-contents)
***

*With the structural components of nodes, edges, and state in place, we can now examine how these elements combine to form sophisticated agentic workflows.*

## 3. Graph-based Agent Workflows

The transition from "Chains" to "Graphs" represents a fundamental shift in how we build AI agents.

### 3.1 The Agentic Loop

Most advanced agents operate in a loop:
1.  **Perceive:** The LLM receives the current **State** (including history).
2.  **Reason/Act:** The LLM decides on an action (e.g., calling a tool).
3.  **Execute:** A **Node** executes the tool and updates the **State**.
4.  **Evaluate:** A **Conditional Edge** checks the new state. If the task is incomplete, the graph loops back to step 1.

### 3.2 Control Flow vs. Sequential Chains

The following table highlights the fundamental difference between standard LangChain execution and LangGraph execution.

| Feature | LangChain (Chains) | LangGraph (Agents) |
| :--- | :--- | :--- |
| **Topology** | Directed Acyclic Graph (DAG) | Cyclic Graph |
| **Flow** | Linear / Pre-defined | Iterative / Dynamic |
| **State** | Passed step-by-step (often ephemeral) | Shared, persistent State Object |
| **Complexity** | Best for predictable, multi-step tasks. | Best for unpredictable, reasoning-heavy tasks. |

**LangChain vs. LangGraph**
The core distinction is **predictability**. If you know exactly what steps must occur in what order, a **Chain** is more efficient. If the next step depends on the *outcome* of the previous step (e.g., "try this tool, and if it fails, try a different one"), you require the cyclic capabilities of **LangGraph**.

[↑ Back to Table of Contents](#table-of-contents)
***

*Having understood the logic of the agentic loop, let's look at how this translates into actual code.*

## 4. Implementation Pattern

To build a graph, you follow a standard lifecycle: defining the state, creating the graph object, adding nodes/edges, and compiling.

```python
from typing import Annotated, TypedDict
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages

# 1. Define the State
# We use Annotated with a reducer (add_messages) so new messages 
# are appended to history rather than overwriting it.
class State(TypedDict):
    messages: Annotated[list, add_messages]

# 2. Define Nodes
def chatbot(state: State):
    # Logic for the LLM would go here
    return {"messages": ["Hello! I am your agent."]}

def tool_executor(state: State):
    # Logic for tool usage would go here
    return {"messages": ["Tool output: Success."]}

# 3. Construct the Graph
workflow = StateGraph(State)

# Add nodes to the graph
workflow.add_node("agent", chatbot)
workflow.add_node("tools", tool_executor)

# Define edges
workflow.set_entry_point("agent")
workflow.add_edge("agent", "tools")
workflow.add_edge("tools", "agent") # Creating the cycle

# 4. Compile
app = workflow.compile()
```

[↑ Back to Table of Contents](#table-of-contents)
***

*While the implementation pattern provides the mechanics, mastering LangGraph requires understanding specific nuances in state handling and execution.*

## 5. Nuance & Best Practices

### 5.1 Advanced State Management: Reducers

In Section 2.2, we touched on **Reducers**. In a production environment, you rarely want to overwrite the entire state. 

> [!TIP]
> **Use `add_messages` for Chat History:** When defining your `State` object, use `Annotated[list, add_messages]` for your message key. This tells LangGraph to use the `add_messages` reducer, which automatically appends new messages to the existing list instead of replacing it.

### 5.2 The Immutability Rule

A common mistake when starting with LangGraph is attempting to mutate the state object directly inside a node.

> [!WARNING]
> **Never Mutate State In-Place:** Nodes must return a *new* dictionary containing the specific keys they wish to update. LangGraph handles the merging of these updates into the global state. Attempting to modify `state['messages'].append(...)` inside a node will often result in unpredictable behavior or errors.

[↑ Back to Table of Contents](#table-of-contents)