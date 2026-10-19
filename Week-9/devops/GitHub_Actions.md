# GitHub Actions & Introduction to IaC

## Table of Contents

* [1. High-Level Overview](#1-high-level-overview)
* [2. GitHub Actions Fundamentals](#2-github-actions-fundamentals)
    * [2.1 Core Components](#21-core-components)
    * [2.2 The Workflow Lifecycle](#22-the-workflow-lifecycle)
* [3. YAML Workflow Creation](#3-yaml-workflow-creation)
    * [3.1 Workflow Anatomy](#31-workflow-anatomy)
    * [3.2 Example: A Simple CI Pipeline](#32-example-a-simple-ci-pipeline)
* [4. Introduction to IaC: Terraform](#4-introduction-to-iac-terraform)
    * [4.1 What is IaC?](#41-what-is-iac)
    * [4.2 Terraform Fundamentals](#42-terraform-fundamentals)
    * [4.3 Terraform vs. Manual Configuration](#43-terraform-vs-manual-configuration)

***

## 1. High-Level Overview

In modern DevOps, manual processes are the enemy of reliability and scale. **GitHub Actions** is a Continuous Integration and Continuous Deployment (CI/CD) platform that allows you to automate your software development workflows directly within your GitHub repository. 

By using GitHub Actions, you can automatically build, test, and deploy your code every time a change is made. To manage the infrastructure that these processes run on, we use **Infrastructure as Code (IaC)**, specifically **Terraform**, to ensure our environments are predictable, repeatable, and version-controlled.

[↑ Back to Table of Contents](#table-of-contents)
***

*Now that we understand the high-level goal of automation, let's dive into the engine that powers it: GitHub Actions.*

## 2. GitHub Actions Fundamentals

GitHub Actions is an event-driven automation platform. It listens for specific "events" in your repository and triggers "workflows" to respond to them.

### 2.1 Core Components

To master GitHub Actions, you must understand its hierarchical structure. It moves from the trigger (Event) to the execution environment (Runner) through a series of organized steps.

| Component | Definition | Responsibility |
| :--- | :--- | :--- |
| **Event** | A specific activity that triggers a workflow. | The "When" (e.g., `push`, `pull_request`, `workflow_dispatch`). |
| **Workflow** | A configurable automated process. | The "What" (an organized collection of jobs). |
| **Job** | A set of steps that execute on the same runner. | The "Where" (defines a unit of work). |
| **Step** | An individual task within a job. | The "How" (runs a command or an action). |
| **Action** | A standalone, reusable extension. | The "Tool" (pre-packaged logic, e.g., `actions/checkout`). |
| **Runner** | A server that executes the jobs. | The "Engine" (the machine running your code). |

### 2.2 The Workflow Lifecycle

A typical workflow follows this logical progression:
1.  **Trigger:** An **Event** occurs (e.g., you push code to `main`).
2.  **Dispatch:** GitHub identifies the relevant **Workflow** file.
3.  **Allocation:** GitHub assigns a **Runner** (virtual machine) to the **Jobs**.
4.  **Execution:** The Runner executes each **Step** sequentially within the job.
5.  **Completion:** The workflow reports success or failure back to the GitHub UI.

> [!TIP]
> **Jobs run in parallel by default.** If you have multiple jobs in one workflow, they will all start at the same time unless you explicitly define dependencies using the `needs` keyword.

[↑ Back to Table of Contents](#table-of-contents)
***

*With the automation engine understood, we must now learn how to write the instructions that govern it using YAML.*

## 3. YAML Workflow Creation

GitHub Actions workflows are defined using **YAML (YAML Ain't Markup Language)**. YAML is a human-readable data serialization language that relies on indentation to define structure.

### 3.1 Workflow Anatomy

A standard workflow file (located in `.github/workflows/*.yml`) consists of several key top-level keys:

*   `name`: The name of the workflow as it appears in the GitHub Actions tab.
*   `on`: The list of **Events** that trigger the workflow.
*   `jobs`: The collection of jobs to be executed.
    *   `runs-on`: Defines the type of **Runner** (e.g., `ubuntu-latest`).
    *   `steps`: The list of tasks to perform.
        *   `uses`: Specifies an **Action** to run.
        *   `run`: Executes a shell command.

### 3.2 Example: A Simple CI Pipeline

Below is a standard configuration for a Continuous Integration (CI) workflow that triggers on every push to the `main` branch.

```yaml
name: Node.js CI

# 1. The Event (The "When")
on:
  push:
    branches: [ "main" ]
  pull_request:
    branches: [ "main" ]

# 2. The Jobs (The "What")
jobs:
  build-and-test:
    # 3. The Runner (The "Where")
    runs-on: ubuntu-latest

    # 4. The Steps (The "How")
    steps:
      # Step 1: Checkout the code using a pre-built Action
      - name: Checkout Repository
        uses: actions/checkout@v4

      # Step 2: Set up the environment
      - name: Set up Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'

      # Step 3: Run actual shell commands
      - name: Install Dependencies
        run: npm install

      - name: Run Tests
        run: npm test
```

[↑ Back to Table of Contents](#table-of-contents)
***

*Automation handles the software lifecycle, but to ensure the underlying infrastructure is just as reliable, we turn to Infrastructure as Code.*

## 4. Introduction to IaC: Terraform

As applications scale, managing servers, databases, and networks manually becomes impossible. **Infrastructure as Code (IaC)** solves this by treating infrastructure setup like software development.

### 4.1 What is IaC?

**Infrastructure as Code (IaC)** is the managing and provisioning of infrastructure through machine-readable definition files, rather than physical hardware configuration or interactive configuration tools.

**Key Benefits of IaC:**
*   **Idempotency:** You can run the same code multiple times and always get the same result.
*   **Version Control:** Since infrastructure is just code, you can track changes, perform code reviews, and roll back to previous versions.
*   **Consistency:** Eliminates "**Configuration Drift**" where environments (Dev vs. Prod) slowly become different due to manual tweaks.

### 4.2 Terraform Fundamentals

**Terraform** is an open-source IaC tool created by HashiCorp. It uses a declarative language called **HCL (HashiCorp Configuration Language)**.

**The Terraform Workflow:**
1.  **Write:** Define your infrastructure in `.tf` files.
2.  **Init (`terraform init`):** Prepare the working directory and download necessary providers (e.g., AWS, Azure, Google Cloud).
3.  **Plan (`terraform plan`):** Preview the changes Terraform will make. This is a "dry run" that shows exactly what will be created, modified, or destroyed.
4.  **Apply (`terraform apply`):** Execute the plan to provision the infrastructure.

> [!IMPORTANT]
> **The State File (`terraform.tfstate`):** Terraform keeps track of your real-world infrastructure in a JSON file called the "State File." **Never delete or manually edit this file.** It is the single source of truth that allows Terraform to know what currently exists.

### 4.3 Terraform vs. Manual Configuration

| Feature | Manual Configuration (ClickOps) | Terraform (IaC) |
| :--- | :--- | :--- |
| **Speed** | Slow; requires human interaction for every step. | Fast; automated execution of large environments. |
| **Repeatability** | Low; prone to human error and "forgetting" steps. | High; identical environments every single time. |
| **Documentation** | Often non-existent or outdated. | The code *is* the documentation. |
| **Scalability** | Extremely difficult to scale. | Highly scalable through modules and loops. |
| **Auditability** | Hard to track "Who changed what and when." | Full audit trail via Git history. |

[↑ Back to Table of Contents](#table-of-contents)
