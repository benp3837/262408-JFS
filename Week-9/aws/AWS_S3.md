# AWS S3 (Simple Storage Service)

## Table of Contents

* [1. High-Level Overview](#1-high-level-overview)
* [2. Core Concepts & Architecture](#2-core-concepts--architecture)
    * [2.1 The S3 Object Model](#21-the-s3-object-model)
    * [2.2 Bucket Properties & Configuration](#22-bucket-properties--configuration)
* [3. S3 Bucket Configuration Deep Dive](#3-s3-bucket-configuration-deep-dive)
    * [3.1 Access Control & Security](#31-access-control--security)
    * [3.2 Storage Classes](#32-storage-classes)
    * [3.3 Versioning & Lifecycle Management](#33-versioning--lifecycle-management)
* [4. Hosting Static Websites on S3](#4-hosting-static-websites-on-s3)
    * [4.1 Use Cases vs. Alternatives](#41-use-cases-vs-alternatives)
    * [4.2 Implementation Workflow](#42-implementation-workflow)
* [5. Comparison: S3 vs. EBS vs. EFS](#5-comparison-s3-vs-ebs-vs-efs)

***

## 1. High-Level Overview

**Amazon S3 (Simple Storage Service)** is an object storage service that offers industry-leading scalability, data availability, security, and performance. Unlike a traditional file system that organizes data in a hierarchy of folders, S3 is designed to store and retrieve any amount of data from anywhere on the web. It is the "foundational" storage layer for many cloud-native applications, used for everything from hosting website assets to massive data lakes.

[↑ Back to Table of Contents](#table-of-contents)
***

*Now that we have defined what S3 is, let's look at the fundamental building blocks that make it function.*

## 2. Core Concepts & Architecture

To master S3, you must distinguish between the "container" and the "content."

### 2.1 The S3 Object Model

S3 is an **Object Storage** service, which differs significantly from **Block Storage** (like EBS) or **File Storage** (like EFS). In S3, data is stored as **Objects** within **Buckets**.

| Component | Description | Key Attributes |
| :--- | :--- | :--- |
| **Bucket** | A container for objects. Think of it as a top-level namespace. | Must have a **globally unique name**. |
| **Object** | The fundamental entity stored in S3. | Comprised of **Data** (the file) and **Metadata** (attributes). |
| **Key** | The unique identifier for an object within a bucket. | Acts as the "file path" (e.g., `images/logo.png`). |

> [!IMPORTANT]
> **Global Namespace:** S3 bucket names are shared across *all* AWS accounts globally. If someone else has a bucket named `my-backup`, you cannot use that name.

[↑ Back to Table of Contents](#table-of-contents)
***

*Understanding the object model is the first step; the next is learning how to configure these buckets to ensure they are secure and cost-effective.*

## 3. S3 Bucket Configuration Deep Dive

Configuring a bucket involves balancing three critical pillars: **Security**, **Availability**, and **Cost**.

### 3.1 Access Control & Security

By default, all new S3 buckets are **private**. AWS implements a "Deny by Default" posture.

*   **IAM Policies:** Used to grant permissions to specific users or roles within your AWS account.
*   **Bucket Policies:** Resource-based policies attached directly to the bucket to manage access for the entire bucket (including cross-account access).
*   **ACLs (Access Control Lists):** A legacy method of managing access. *Note: AWS now recommends using Bucket Policies over ACLs for most modern use cases.*
*   **Block Public Access (BPA):** A critical safety layer. When enabled, it overrides any policy that might accidentally grant public access.

### 3.2 Storage Classes

S3 offers various "tiers" to optimize costs based on how frequently you access your data.

| Storage Class | Durability/Availability | Best For... | Cost Profile |
| :--- | :--- | :--- | :--- |
| **S3 Standard** | High | Frequently accessed data (active apps, websites). | Highest storage cost, lowest access cost. |
| **S3 Intelligent-Tiering** | High | Data with unpredictable or changing access patterns. | Automatic cost savings via AI. |
| **S3 Standard-IA** (Infrequent Access) | High | Long-lived data that is rarely accessed but needs instant retrieval. | Lower storage cost, higher retrieval cost. |
| **S3 One Zone-IA** | Lower (Single AZ) | Non-critical, reproducible data. | Even lower cost, but less resilient. |
| **S3 Glacier Instant Retrieval** | High | Archival data that still needs millisecond access. | Low storage, higher retrieval. |
| **S3 Glacier Flexible/Deep Archive** | High | Long-term backups/compliance (retrieval in minutes to hours). | Lowest storage cost, highest retrieval cost/time. |

### 3.3 Versioning & Lifecycle Management

*   **Versioning:** When enabled, S3 keeps multiple variants of an object in the same bucket. This is a primary defense against accidental `DELETE` operations or overwrites.
*   **Lifecycle Policies:** Automated rules that transition objects between storage classes or expire (delete) them after a set period.
    *   *Example Workflow:* Move data from `Standard` $\rightarrow$ `Standard-IA` after 30 days $\rightarrow$ `Glacier` after 90 days $\rightarrow$ `Delete` after 365 days.

[↑ Back to Table of Contents](#table-of-contents)
***

*With a secure and optimized bucket in place, we can now explore one of S3's most popular web-facing features: static website hosting.*

## 4. Hosting Static Websites on S3

S3 can function as a highly scalable, low-cost web server for content that does not require server-side processing (e.g., HTML, CSS, JS, images).

### 4.1 Use Cases vs. Alternatives

| Feature | S3 Static Hosting | EC2 / Lambda (Dynamic) |
| :--- | :--- | :--- |
| **Compute** | None (Client-side only). | Full server-side logic. |
| **Scalability** | Virtually infinite/Automatic. | Requires Auto-Scaling Groups. |
| **Complexity** | Very Low. | High (OS, Runtime, Networking). |
| **Best For** | SPAs (React/Vue), Documentation, Marketing sites. | APIs, CMS (WordPress), Databases. |

### 4.2 Implementation Workflow

To host a site, follow these steps:

1.  **Upload Assets:** Upload your `index.html`, `error.html`, and assets to the bucket.
2.  **Enable Static Website Hosting:** In the Bucket Properties, toggle "Static website hosting" and specify your `index.html`.
3.  **Configure Public Access:**
    *   Disable "Block Public Access" for the bucket.
    *   Attach a **Bucket Policy** that allows `s3:GetObject` to `Principal: *`.
4.  **Access via Endpoint:** S3 provides a unique URL (e.g., `http://my-bucket.s3-website-us-east-1.amazonaws.com`).

> [!TIP]
> For production sites, always use **Amazon CloudFront** (CDN) in front of your S3 bucket. This enables HTTPS, improves global latency, and allows you to use a custom domain name (e.g., `www.example.com`).

[↑ Back to Table of Contents](#table-of-contents)
***

*To wrap up, it is vital to understand where S3 fits within the broader AWS storage ecosystem.*

## 5. Comparison: S3 vs. EBS vs. EFS

| Feature | **S3** | **EBS** (Elastic Block Store) | **EFS** (Elastic File System) |
| :--- | :--- | :--- | :--- |
| **Type** | Object Storage | Block Storage | File Storage |
| **Access Pattern** | Web/API (HTTP) | Attached to 1 EC2 instance | Shared across many EC2s |
| **Scalability** | Extremely high/Automatic | Manual resizing | Highly scalable/Automatic |
| **Typical Use** | Data Lakes, Backups, Web Assets | OS Drives, Databases | Shared Configs, Home Directories |

[↑ Back to Table of Contents](#table-of-contents)
