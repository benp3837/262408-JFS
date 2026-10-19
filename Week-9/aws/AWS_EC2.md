# AWS EC2 (Elastic Compute Cloud)

## Table of Contents

* [1. High-Level Overview](#1-high-level-overview)
* [2. Amazon EC2 Fundamentals](#2-amazon-ec2-fundamentals)
    * [2.1 Amazon Machine Image (AMI)](#21-amazon-machine-image-ami)
    * [2.2 Elastic Block Store (EBS)](#22-elastic-block-store-ebs)
* [3. Security & Access](#3-security--access)
    * [3.1 Security Groups](#31-security-groups)
    * [3.2 Accessing Instances via SSH](#32-accessing-instances-via-ssh)
* [4. Scalability & High Availability](#4-scalability--high-availability)
    * [4.1 EC2 Auto Scaling](#41-ec2-auto-scaling)

***

## 1. High-Level Overview

**Amazon EC2 (Elastic Compute Cloud)** is a web service that provides secure, resizable compute capacity in the AWS cloud. It is the fundamental building block of AWS infrastructure, allowing users to rent virtual servers (called **Instances**) to run any application, from a simple web server to complex high-performance computing workloads.

Instead of purchasing and maintaining physical hardware, EC2 allows you to provision virtual machines in minutes, scaling your resources up or down based on demand.

[↑ Back to Table of Contents](#table-of-contents)
***

*Now that we understand what EC2 provides at a high level, let's dive into the core components that define an instance's identity and storage.*

## 2. Amazon EC2 Fundamentals

An EC2 instance is not just a "running computer"; it is a combination of several specific AWS resources that define its operating system, hardware profile, and storage.

### 2.1 Amazon Machine Image (AMI)

An **AMI (Amazon Machine Image)** is a template that contains the software configuration (operating system, application server, and applications) required to launch your instance.

| Component | Description |
| :--- | :--- |
| **Root Volume Template** | Contains the OS and software required to launch the instance. |
| **Launch Permissions** | Controls which AWS accounts can use the AMI. |
| **Block Device Mapping** | Defines which storage volumes (EBS) are attached to the instance on launch. |

**Types of AMIs:**
* **AWS Marketplace AMIs:** Pre-configured software from third-party vendors.
* **Community AMIs:** Shared by other AWS users (use with caution).
* **My AMIs:** Custom images you create from your own existing instances.

[↑ Back to Table of Contents](#table-of-contents)
***

*While the AMI provides the software, the instance needs a way to store data permanently. This is handled by EBS.*

### 2.2 Elastic Block Store (EBS)

**Amazon EBS** provides block-level storage volumes for use with EC2 instances. Think of EBS as a virtual hard drive that you can plug into your virtual server.

**Key Characteristics:**
* **Persistence:** Unlike "Instance Store" (which is ephemeral/temporary), EBS volumes persist independently of the instance life cycle.
* **Snapshots:** You can take point-in-time backups of your EBS volumes using snapshots, which are stored in Amazon S3.
* **High Availability:** EBS volumes are automatically replicated within their Availability Zone to prevent data loss from single component failures.

**EBS vs. Instance Store**

| Feature | EBS (Elastic Block Store) | Instance Store |
| :--- | :--- | :--- |
| **Persistence** | **Persistent:** Data survives instance stop/start. | **Ephemeral:** Data is lost if instance is stopped or terminated. |
| **Use Case** | Databases, file systems, long-term storage. | Temporary caches, buffers, scratch data. |
| **Reliability** | High (replicated within AZ). | Lower (tied to the physical host). |

[↑ Back to Table of Contents](#table-of-contents)
***

*Having the server and storage ready is useless if you cannot secure it or access it. Let's look at the security layer.*

## 3. Security & Access

Security in EC2 is managed through multiple layers, primarily focusing on network traffic control and identity management.

### 3.1 Security Groups

A **Security Group** acts as a **virtual firewall** for your EC2 instance to control incoming and outgoing traffic.

**Core Rules of Security Groups:**
1. **Stateful:** If you send a request from your instance, the response traffic is allowed back in automatically, regardless of inbound rules.
2. **Allow-only:** You can only specify "Allow" rules. You cannot explicitly "Deny" a specific IP; you simply don't include it in the allow list.
3. **Rule-based:** Traffic is permitted only if it matches a specific protocol (TCP/UDP/ICMP), port range, or source (IP/CIDR or another Security Group).

> [!IMPORTANT]
> **Default Behavior:** By default, all inbound traffic is blocked, and all outbound traffic is allowed. You must explicitly add rules to allow traffic (e.g., allow port 22 for SSH).

[↑ Back to Table of Contents](#table-of-contents)
***

*Once the firewall is configured, you need a way to actually log in and manage your instance.*

### 3.2 Accessing Instances via SSH

The standard method for managing Linux-based EC2 instances is through **SSH (Secure Shell)**.

**The SSH Workflow:**
1. **Key Pair:** During instance creation, AWS generates a **Key Pair** (a `.pem` or `.ppk` file). This is your private key.
2. **Public Key:** The public key is injected into the instance's `~/.ssh/authorized_keys` file.
3. **Connection:** You use your private key to authenticate your connection.

**Standard SSH Command:**
```bash
# Ensure your key has the correct permissions (Linux/macOS)
chmod 400 my-key-pair.pem

# Connect to the instance
ssh -i "my-key-pair.pem" ec2-user@<INSTANCE_PUBLIC_IP>
```

> [!TIP]
> Different OS images use different default usernames:
> * **Amazon Linux/RHEL:** `ec2-user`
> * **Ubuntu:** `ubuntu`
> * **Debian:** `admin`

[↑ Back to Table of Contents](#table-of-contents)
***

*Manual management is fine for one server, but for production, you need systems that handle changes in traffic automatically.*

## 4. Scalability & High Availability

To handle fluctuating application loads, AWS provides automated mechanisms to scale your compute resources.

### 4.1 EC2 Auto Scaling

**EC2 Auto Scaling** automatically adds or removes EC2 instances according to conditions you define. This ensures you have the right amount of compute capacity to handle the load of your application without manual intervention.

**The Three Pillars of Auto Scaling:**

1. **Launch Template / Configuration:** Defines *what* to launch (which AMI, instance type, security groups, etc.).
2. **Auto Scaling Group (ASG):** Defines *where* and *how many* to launch (which subnets/AZs, minimum/maximum/desired capacity).
3. **Scaling Policies:** Defines *when* to scale (e.g., "Add 1 instance if CPU utilization > 70%").

**Scaling Types:**
* **Target Tracking Scaling:** Maintains a specific metric (e.g., "Keep average CPU at 50%").
* **Step Scaling:** Increases or decreases capacity in "steps" based on the size of a breach in a threshold.
* **Scheduled Scaling:** Scales based on known time patterns (e.g., "Scale up every Monday at 9 AM").

[↑ Back to Table of Contents](#table-of-contents)
