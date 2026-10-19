# AWS Introduction

## Table of Contents
* [1. High-Level Overview](#1-high-level-overview)
* [2. AWS Global Infrastructure](#2-aws-global-infrastructure)
    * [2.1 AWS Regions](#21-aws-regions)
    * [2.2 Availability Zones](#22-availability-zones)
* [3. AWS Common Services](#3-aws-common-services)
    * [3.1 Compute Services](#31-compute-services)
    * [3.2 Storage Services](#32-storage-services)
    * [3.3 Networking Services](#33-networking-services)
    * [3.4 Database Services](#34-database-services)
    * [3.5 Hands-on with AWS CLI](#35-hands-on-with-aws-cli)

***

## 1. High-Level Overview
**Amazon Web Services (AWS)** is the world's most comprehensive and broadly adopted cloud platform, offering over 200 fully featured services from data centers globally. Instead of buying, owning, and maintaining physical data centers and servers, you can access technology services, such as computing power, storage, and databases, on an as-needed basis from AWS.

[↑ Back to Table of Contents](#table-of-contents)
***

*Now that we understand the scale of AWS, let's look at the physical foundation that makes it possible: its global infrastructure.*

## 2. AWS Global Infrastructure

AWS operates on a highly redundant and resilient physical infrastructure designed to provide high availability and fault tolerance.

### 2.1 AWS Regions
An **AWS Region** is a physical location in the world where AWS has multiple **Availability Zones**. 

*   **Isolation:** Each **Region** is completely independent and isolated from other **Regions**. This ensures that a failure in one **Region** does not affect others.
*   **Compliance & Proximity:** You choose a **Region** based on your data residency requirements (compliance) and to minimize latency by being close to your users.

### 2.2 Availability Zones (AZs)
An **Availability Zone (AZ)** consists of one or more discrete data centers, each with redundant power, networking, and connectivity, located within an **AWS Region**.

| Feature | AWS Region | Availability Zone (AZ) |
| :--- | :--- | :--- |
| **Scope** | A geographic area (e.g., US East (N. Virginia)). | A specific cluster of data centers within a Region. |
| **Purpose** | Provides global reach and regulatory compliance. | Provides high availability and fault tolerance. |
| **Relationship** | Contains multiple AZs. | Resides within a single Region. |

**AZ vs. Region: The High Availability Concept**
To build a **Highly Available (HA)** application, you should deploy your resources across multiple **Availability Zones**. If one **AZ** experiences a localized failure (e.g., power outage or flood), your application can continue to run from the other **AZs** in the same **Region**.

[↑ Back to Table of Contents](#table-of-contents)
***

*With the physical infrastructure in place, we can now explore the core services that run on top of this foundation.*

## 3. AWS Common Services

AWS services are categorized by their function. Understanding these categories is essential for designing efficient cloud architectures.

### 3.1 Compute Services
Compute services provide the "brains" of your applications.

| Service | Type | Best Use Case |
| :--- | :--- | :--- |
| **Amazon EC2** | **Infrastructure as a Service (IaaS)** | Full control over virtual servers; custom OS and software. |
| **AWS Lambda** | **Function as a Service (FaaS/Serverless)** | Running code in response to events without managing servers. |
| **AWS Fargate** | **Container as a Service (CaaS)** | Running containers without managing the underlying EC2 instances. |

**EC2 vs. Lambda: Operational Differences**
The primary difference lies in the **abstraction of management**.
* **Amazon EC2** provides maximum control; you manage the Operating System, patching, and scaling logic. It is best for long-running, predictable workloads.
* **AWS Lambda** is fully managed; you only provide the code. AWS handles all underlying infrastructure, scaling, and high availability. It is best for event-driven, bursty, or intermittent workloads.

### 3.2 Storage Services
Storage services provide the "memory" for your data.

| Service | Type | Best Use Case |
| :--- | :--- | :--- |
| **Amazon S3** | **Object Storage** | Storing unstructured data (images, videos, backups) with high durability. |
| **Amazon EBS** | **Block Storage** | Providing persistent storage volumes for EC2 instances (like a virtual hard drive). |
| **Amazon EFS** | **File Storage** | Shared file systems that can be mounted by multiple EC2 instances simultaneously. |

### 3.3 Networking Services
Networking services provide the "nervous system" that connects your resources.

* **Amazon VPC (Virtual Private Cloud):** A logically isolated section of the AWS Cloud where you can launch AWS resources in a virtual network that you define.
* **Amazon Route 53:** A scalable **Domain Name System (DNS)** web service designed to route users to Internet applications.
* **AWS Direct Connect:** A cloud service solution that makes it easy to establish a dedicated network connection from your premises to AWS.

### 3.4 Database Services
Database services provide structured and semi-structured data storage.

| Service | Type | Key Characteristic |
| :--- | :--- | :--- |
| **Amazon RDS** | **Relational (SQL)** | Managed service for engines like MySQL, PostgreSQL, and SQL Server. |
| **Amazon DynamoDB** | **NoSQL** | A key-value and document database that delivers single-digit millisecond performance at any scale. |
| **Amazon Aurora** | **Relational (Cloud-Native)** | A high-performance, MySQL and PostgreSQL-compatible relational database built for the cloud. |

### 3.5 Hands-on with AWS CLI
The **AWS Command Line Interface (CLI)** allows you to interact with AWS services directly from your terminal.

**1. Listing S3 Buckets**
To view all storage buckets in your account:
```bash
aws s3 ls
```

**2. Describing EC2 Instances**
To get details about your running virtual servers:
```bash
aws ec2 describe-instances --query 'Reservations[*].Instances[*].[InstanceId,State.Name]' --output table
```

> [!IMPORTANT]
> **The "Serverless" Trend:** When choosing between services like EC2 (Server) and Lambda (Serverless), consider your management overhead. Serverless services (Lambda, S3, DynamoDB) allow you to focus on code and data while AWS handles the infrastructure scaling and patching.

> [!WARNING]
> **The Cost Trap:** Cloud resources are billed by usage. Always remember to terminate unused **Amazon EC2** instances and delete unattached **Amazon EBS** volumes to prevent unexpected charges.

[↑ Back to Table of Contents](#table-of-contents)
