# Docker Images & Registry Ecosystem

## Table of Contents

* [1. High-Level Overview](#1-high-level-overview)
* [2. The Blueprint: Dockerfile](#2-the-blueprint-dockerfile)
    * [2.1 Anatomy of a Dockerfile](#21-anatomy-of-a-dockerfile)
    * [2.2 Common Instructions](#22-common-instructions)
* [3. The Artifact: Docker Images](#3-the-artifact-docker-images)
    * [3.1 Layered File System](#31-layered-file-system)
    * [3.2 Image vs. Container](#32-image-vs-container)
* [4. The Ecosystem: Container Registries](#4-the-ecosystem-container-registries)
    * [4.1 Docker Hub](#41-docker-hub)
    * [4.2 Amazon ECR](#42-amazon-ecr)
    * [4.3 Comparison: Docker Hub vs. Amazon ECR](#43-comparison-docker-hub-vs-amazon-ecr)

***

## 1. High-Level Overview

In the world of containerization, if a **Container** is a running process, then a **Docker Image** is the static, read-only template from which it is instantiated. This module explores how these images are defined using a **Dockerfile**, how they are structured as a series of layers, and how they are stored and distributed using **Container Registries**.

[↑ Back to Table of Contents](#table-of-contents)
***

## 2. The Blueprint: Dockerfile

A **Dockerfile** is a text document that contains all the commands a user could call on the command line to assemble an image. It serves as the "source code" for your infrastructure.

### 2.1 Anatomy of a Dockerfile

A Dockerfile is read from top to bottom. Each instruction creates a new layer in the resulting image.

### 2.2 Common Instructions

| Instruction | Purpose | Example |
| :--- | :--- | :--- |
| **`FROM`** | Sets the **Base Image** upon which you are building. | `FROM python:3.9-slim` |
| **`WORKDIR`** | Sets the working directory for subsequent instructions. | `WORKDIR /app` |
| **`COPY`** | Copies files/directories from the host to the image. | `COPY . .` |
| **`RUN`** | Executes commands in a new layer during the build process. | `RUN pip install -r requirements.txt` |
| **`ENV`** | Sets environment variables. | `ENV APP_COLOR=blue` |
| **`EXPOSE`** | Informs Docker that the container listens on specific network ports. | `EXPOSE 8080` |
| **`ENTRYPOINT`** | Configures a container that will run as an executable. | `ENTRYPOINT ["python", "app.py"]` |
| **`CMD`** | The default command or parameters passed to the ENTRYPOINT. | `CMD ["--help"]` |

> [!IMPORTANT]
> **`RUN` vs. `CMD`:** `RUN` is executed during the **build time** to prepare the image. `CMD` is executed during the **runtime** when the container is actually launched.
>
> **`ENTRYPOINT` vs. `CMD`:**
> * **`ENTRYPOINT`** defines the main executable of the container. It is difficult to override at runtime.
> * **`CMD`** provides default arguments for the `ENTRYPOINT`. It is easily overridden by passing arguments at the end of the `docker run` command.
> * **Combined:** When used together, `ENTRYPOINT` sets the command, and `CMD` sets the default parameters.

[↑ Back to Table of Contents](#table-of-contents)
***

*Now that we understand how to write the blueprint, let's look at the resulting artifact: the Docker Image.*

## 3. The Artifact: Docker Images

A **Docker Image** is a lightweight, standalone, executable package that includes everything needed to run a piece of software: code, runtime, system tools, libraries, and settings.

### 3.1 Layered File System

Docker images are composed of **Layers**. Each instruction in a Dockerfile (like `RUN` or `COPY`) creates a new layer. These layers are read-only and are stacked on top of each other.

* **Efficiency:** Layers are cached. If you change a line at the bottom of your Dockerfile, Docker reuses the cached layers from the top, making builds extremely fast.
* **Storage:** Layers are shared. If two different images both use `FROM ubuntu:22.04`, they share the same underlying Ubuntu layers on your disk.

### 3.2 Image vs. Container

It is critical to distinguish between the template and the instance.

| Concept | State | Analogy |
| :--- | :--- | :--- |
| **Docker Image** | Static / Read-Only | A Recipe |
| **Docker Container** | Dynamic / Writable | The cooked Meal |

[↑ Back to Table of Contents](#table-of-contents)
***

*Images are useless if they stay on your local machine; we need a way to share them. This brings us to Container Registries.*

## 4. The Ecosystem: Container Registries

A **Container Registry** is a centralized service for storing and distributing Docker images. Think of it as "GitHub, but for images."

### 4.1 Docker Hub

**Docker Hub** is the world's largest public registry. It is the default registry used by the Docker CLI.

* **Public Images:** Anyone can download (pull) official images like `nginx`, `postgres`, or `python`.
* **Private Images:** You can host your own proprietary images (usually requires a paid tier).
* **Ease of Use:** Zero configuration needed; it works "out of the box" with Docker.

### 4.2 Amazon ECR (Elastic Container Registry)

**Amazon ECR** is a fully managed Docker container registry service provided by AWS. It is designed for enterprise-grade security and integration within the AWS ecosystem.

* **IAM Integration:** Uses AWS Identity and Access Management (IAM) for granular control over who can push/pull images.
* **VPC Support:** Images can be kept entirely within your private AWS network.
* **Scanning:** Automatically scans images for software vulnerabilities.

### 4.3 Comparison: Docker Hub vs. Amazon ECR

Choosing between these depends on where your application is running and your security requirements.

| Feature | Docker Hub | Amazon ECR |
| :--- | :--- | :--- |
| **Primary Use Case** | Public sharing & general development. | Production workloads on AWS. |
| **Security Model** | Simple User/Pass or Token. | Robust AWS IAM roles/policies. |
| **Network** | Public Internet. | Can be entirely private (VPC). |
| **Pricing** | Free (limited) / Subscription. | Pay-as-you-go (Storage + Data Transfer). |

> [!TIP]
> **The Hybrid Workflow:** Many teams use **Docker Hub** for testing and sharing open-source tools, but use **Amazon ECR** to host their production-ready application images to ensure maximum security and speed within their AWS environment.

[↑ Back to Table of Contents](#table-of-contents)
