# Docker Setup

## Table of Contents

* [1. High-Level Overview](#1-high-level-overview)
* [2. Understanding Docker Containers](#2-understanding-docker-containers)
* [3. Installing Docker](#3-installing-docker)
* [4. Containerization & Orchestration](#4-containerization--orchestration)
* [5. Basic Docker CLI Commands](#5-basic-docker-cli-commands)

***

## 1. High-Level Overview

In modern software development, the "it works on my machine" problem is a significant bottleneck. **Docker** provides a solution by allowing developers to package applications with all their dependencies into standardized units called **Containers**. This module covers the fundamental concepts of Docker, from understanding what a container is to installing the engine and mastering the essential command-line interface (CLI) tools.

[↑ Back to Table of Contents](#table-of-contents)

***

*Now that we understand the purpose of Docker, let's dive into the core unit of execution: the Container.*

## 2. Understanding Docker Containers

To master Docker, one must distinguish between the **Image** (the blueprint) and the **Container** (the living instance).

### 2.1 Images vs. Containers

| Concept | Analogy | Definition | Persistence |
| :--- | :--- | :--- | :--- |
| **Docker Image** | **The Blueprint / Recipe** | A read-only, static template containing the OS, libraries, and application code. | Immutable (cannot be changed once built). |
| **Docker Container** | **The Building / Finished Dish** | A running, isolated instance of an image. It adds a thin "writable layer" on top of the image. | Ephemeral (changes are lost if not using volumes). |

### 2.2 Why Containerization?

**Containerization** is the process of isolating an application and its environment. This provides several key benefits:
* **Isolation:** Processes inside a container cannot interfere with the host or other containers.
* **Portability:** A container running on your laptop will run identically on a production server.
* **Efficiency:** Unlike Virtual Machines (VMs), containers share the host OS kernel, making them much lighter and faster to start.

**Containers vs. Virtual Machines (VMs)**

| Feature | Docker Containers | Virtual Machines (VMs) |
| :--- | :--- | :--- |
| **Architecture** | Share the host OS kernel. | Each has its own full Guest OS. |
| **Size** | Megabytes (MB). | Gigabytes (GB). |
| **Startup Time** | Seconds. | Minutes. |
| **Resource Usage** | Very Low. | High (due to OS overhead). |

[↑ Back to Table of Contents](#table-of-contents)

***

*With the conceptual foundation laid, the next step is getting the tools onto your machine.*

## 3. Installing Docker

The installation process depends heavily on your operating system. Most users will interact with **Docker Desktop** on Windows or macOS, or **Docker Engine** on Linux.

### 3.1 Installation Pathways

| Environment | Recommended Tool | Key Requirement |
| :--- | :--- | :--- |
| **Windows** | **Docker Desktop** | Requires **WSL 2** (Windows Subsystem for Linux) for optimal performance. |
| **macOS** | **Docker Desktop** | Works on both Intel and Apple Silicon (M1/M2/M3). |
| **Linux** | **Docker Engine** | Installed via native package managers (`apt`, `yum`). |

> [!IMPORTANT]
> **WSL 2 on Windows:** For the best experience on Windows, ensure you have WSL 2 enabled. Docker Desktop uses a specialized Linux utility VM powered by WSL 2 to run the Docker engine, providing much better speed and compatibility than the older Hyper-V backend.

### 3.2 Verifying Installation

Once installed, you must verify that the Docker daemon is running and accessible via your terminal. Run the following command:

```bash
docker --version
```

To test if you can actually run containers, try the "Hello World" test:

```bash
docker run hello-world
```

If successful, Docker will pull a tiny image, run it, print a message, and exit.

[↑ Back to Table of Contents](#table-of-contents)

***

*Running a single container is easy, but modern applications often require multiple services to talk to each other. This brings us to orchestration.*

## 4. Containerization & Orchestration

As applications grow, you move from managing single containers to managing entire ecosystems of services (e.g., a web server, a database, and a cache).

### 4.1 The Scaling Problem

When you have dozens or hundreds of containers, manual management becomes impossible. You need to handle:
* **Scaling:** Running more instances of a service to handle traffic.
* **Self-healing:** Automatically restarting containers if they crash.
* **Service Discovery:** Helping containers find and talk to each other.

### 4.2 Orchestration Tools

**Orchestration** is the automated management, scaling, and networking of containerized applications.

* **Docker Compose:** A tool for defining and running **multi-container** Docker applications. You use a `docker-compose.yml` file to configure your application's services. It is ideal for development environments.
* **Kubernetes (K8s):** The industry standard for **production-grade** orchestration. It manages clusters of machines and is designed for massive, high-availability workloads.

**Compose vs. Kubernetes**

| Feature | Docker Compose | Kubernetes |
| :--- | :--- | :--- |
| **Primary Goal** | Single-host, multi-container setup. | Multi-host, cluster-wide orchestration. |
| **Complexity** | Low (Easy to learn). | High (Steep learning curve). |
| **Best Use Case** | Local development & testing. | Large-scale production environments. |

[↑ Back to Table of Contents](#table-of-contents)

***

*Now that we understand the ecosystem, let's master the primary way we interact with it: the CLI.*

## 5. Basic Docker CLI Commands

The Docker Command Line Interface (CLI) is your primary tool for managing images, containers, and networks.

### 5.1 Lifecycle Commands

These commands manage the "state" of your containers.

| Action | Command | Description |
| :--- | :--- | :--- |
| **Run Container** | `docker run <image>` | Creates and starts a new container from an image. |
| **List Running** | `docker ps` | Shows all currently active containers. |
| **List All** | `docker ps -a` | Shows all containers, including those that have exited. |
| **Stop Container** | `docker stop <id/name>` | Gracefully shuts down a running container. |
| **Start Container** | `docker start <id/name>` | Restarts a stopped container. |
| **Remove Container**| `docker rm <id/name>` | Deletes a stopped container. |

### 5.2 Image Management

| Action | Command | Description |
| :--- | :--- | :--- |
| **List Images** | `docker images` | Shows all images currently stored locally. |
| **Build Image** | `docker build -t <name> .` | Creates an image from a `Dockerfile` in the current directory. |
| **Pull Image** | `docker pull <image>` | Downloads an image from a registry (like Docker Hub). |
| **Remove Image** | `docker rmi <image>` | Deletes a local image. |

### 5.3 Inspection & Debugging

When things go wrong, use these tools to peek inside the container.

* **`docker logs <id/name>`**: View the standard output (STDOUT) of a container. Essential for seeing application errors.
* **`docker exec -it <id/name> sh`**: Opens an interactive shell *inside* a running container. This is like "SSH-ing" into the container.
* **`docker inspect <id/name>`**: Returns a massive JSON object containing every detail about the container (IP address, mounts, environment variables, etc.).

> [!TIP]
> **The `-d` Flag:** When running a container, use `docker run -d <image>` (detached mode). This runs the container in the background, allowing you to keep using your terminal.
