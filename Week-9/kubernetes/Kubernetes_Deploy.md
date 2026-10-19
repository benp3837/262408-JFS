# Deploying Kubernetes & Amazon EKS

## Table of Contents

* [1. High-Level Overview](#1-high-level-overview)
* [2. Amazon EKS Overview](#2-amazon-eks-overview)
* [3. Amazon CloudWatch: Monitoring & Logging](#3-amazon-cloudwatch-monitoring--logging)
    * [3.1 Metrics](#31-metrics)
    * [3.2 Alarms](#32-alarms)
    * [3.3 Dashboards](#33-dashboards)
* [4. Summary Comparison: EKS vs. Self-Managed Kubernetes](#4-summary-comparison-eks-vs-self-managed-kubernetes)

***

## 1. High-Level Overview

Deploying a production-grade Kubernetes cluster involves more than just orchestrating containers; it requires a robust ecosystem for observability, security, and management. In the AWS ecosystem, this typically means leveraging **Amazon Elastic Kubernetes Service (EKS)** integrated with **Amazon CloudWatch** to ensure the health and performance of your workloads.

This module covers the structural components of Amazon EKS and the observability framework provided by CloudWatch to monitor, alert, and visualize your cluster's state.

[↑ Back to Table of Contents](#table-of-contents)
***

*Now that we have the high-level context, let's dive into the core service that powers managed Kubernetes on AWS: Amazon EKS.*

## 2. Amazon EKS Overview

**Amazon Elastic Kubernetes Service (EKS)** is a managed service that makes it easy to run Kubernetes on AWS without needing to install, operate, and maintain your own Kubernetes control plane or nodes.

### 2.1 Core Components

EKS automates the heavy lifting of managing the Kubernetes **Control Plane**, providing high availability and scalability.

| Component | Responsibility | Managed by AWS? |
| :--- | :--- | :--- |
| **Control Plane** | Manages the API server, etcd (cluster state), scheduler, and controller manager. | **Yes** (Highly available across AZs) |
| **Data Plane (Nodes)** | The worker nodes where your actual containerized applications run. | **Optional** (Can use EKS Managed Node Groups or Fargate) |
| **Kubernetes API** | The primary interface for interacting with the cluster via `kubectl`. | **Yes** |

### 2.2 Deployment Models

When deploying the data plane in EKS, you generally choose between two primary models:

1.  **Managed Node Groups:** AWS automes the provisioning and lifecycle of EC2 instances. It handles patching and updates for the underlying OS and Kubernetes components.
2.  **AWS Fargate (Serverless):** A "serverless" compute engine for containers. You don't manage EC2 instances at all; you simply define your pod requirements, and Fargate provisions the necessary compute on-demand.

> [!TIP]
> **When to choose Fargate:** Use Fargate when you want to reduce operational overhead and only pay for the exact CPU/Memory resources your pods consume, without managing any underlying infrastructure.
>
> **Use Fargate when:**
> * **Intermittent Workloads:** You have jobs that run periodically (e.g., CronJobs) where scaling up and down to zero is critical for cost-savings.
> * **Bursting Traffic:** Your application has unpredictable traffic patterns that require rapid, hands-off scaling.
> * **Low Operational Capacity:** Your team lacks the bandwidth to manage OS patching, AMI updates, or node scaling policies.
>
> **Avoid Fargate when:**
> * **Extreme Performance Tuning:** You require custom kernel modules, specific OS optimizations, or low-level hardware access.
> * **Cost-Efficiency at High Scale:** For massive, steady-state workloads, using Reserved Instances or Savings Plans on EC2 Managed Node Groups is often more cost-effective than Fargate's premium.
> * **GPU Requirements:** Your workloads require specialized hardware like NVIDIA GPUs (Fargate is currently focused on general-purpose compute).

[↑ Back to Table of Contents](#table-of-contents)
***

*A cluster is only as good as your ability to see what is happening inside it. We now transition from orchestration to observability using Amazon CloudWatch.*

## 3. Amazon CloudWatch: Monitoring & Logging

In a distributed system like Kubernetes, traditional monitoring is insufficient. **Amazon CloudWatch** provides the centralized observability required to track the health of your EKS cluster, nodes, and applications.

### 3.1 Metrics

**Metrics** are numerical representations of data measured over time. In the context of EKS, CloudWatch collects several types of metrics:

*   **Infrastructure Metrics:** CPU utilization, Memory usage, and Network I/O for your worker nodes.
*   **Container Metrics:** Resource consumption at the Pod and Container level (often via the Container Insights add-on).
*   **Control Plane Metrics:** API server latency, etcd health, and scheduler performance.

### 3.2 Alarms

**CloudWatch Alarms** allow you to automate responses to changes in your metrics. An alarm watches a single metric over a specified time period and performs one of two actions:

1.  **EC2 Action:** Stop, Terminate, or Recover an instance.
2.  **SNS Action:** Send a notification to an **Amazon Simple Notification Service (SNS)** topic (e.g., sending an email or triggering a Lambda function).

**Common Use Case:** An alarm that triggers an SNS notification to the DevOps team if the `CPUUtilization` of a node exceeds 80% for more than 5 minutes.

### 3.3 Dashboards

**CloudWatch Dashboards** provide a visual interface to monitor your entire ecosystem in a single pane of glass. 

*   **Customization:** You can create bespoke dashboards that combine metrics from EKS, EC2, RDS, and even custom application metrics.
*   **Visibility:** Dashboards allow you to see correlations—for example, seeing if a spike in application latency (from your logs) correlates with a spike in CPU usage (from your metrics).

[↑ Back to Table of Contents](#table-of-contents)
***

*To wrap up, let's compare the managed approach of EKS against the alternative of managing your own Kubernetes cluster.*

## 4. Summary Comparison: EKS vs. Self-Managed Kubernetes

| Feature | Amazon EKS (Managed) | Self-Managed Kubernetes (on EC2) |
| :--- | :--- | :--- |
| **Control Plane Management** | Fully managed by AWS; highly available by default. | You must install, configure, and maintain etcd and API servers. |
| **Operational Overhead** | **Low.** AWS handles patching, scaling, and availability. | **High.** You are responsible for the entire stack. |
| **Scalability** | Highly automated via Managed Node Groups or Fargate. | Requires manual configuration of Auto Scaling Groups and cluster autoscalers. |
| **Customization** | Limited to what the AWS API and Kubernetes allow. | Total control over every component and configuration. |
| **Best For...** | Production workloads where reliability and low ops are priorities. | Highly specialized use cases requiring deep kernel or control plane tweaks. |

[↑ Back to Table of Contents](#table-of-contents)
