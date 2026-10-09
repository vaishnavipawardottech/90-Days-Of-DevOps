# Day 61 — Introduction to Terraform and Your First AWS Infrastructure

## 🚀 Introduction

After working with Docker, CI/CD pipelines, and Kubernetes, the next step in the DevOps journey is learning how the infrastructure itself can be created and managed through code.

Today I started with **Terraform**, an Infrastructure as Code (IaC) tool that allows infrastructure to be defined in configuration files instead of creating resources manually through the AWS Console.

For this hands-on task, I used Terraform with AWS to understand the complete workflow of creating infrastructure, checking planned changes, managing Terraform state, modifying resources, and destroying the infrastructure.

---

## 📌 What is Infrastructure as Code?

**Infrastructure as Code (IaC)** means managing infrastructure using configuration files instead of manually creating and configuring resources through a cloud provider's console.

With IaC, infrastructure can be version-controlled, reviewed, reused, and recreated consistently. This makes infrastructure provisioning more predictable and reduces mistakes caused by manual configuration.

Terraform follows this approach by allowing infrastructure to be defined using **HashiCorp Configuration Language (HCL)** and then creating or modifying the required resources based on that configuration.

---

## 💡 Why IaC Matters in DevOps

Without IaC, infrastructure is often created manually:

- Open AWS Console
- Create an EC2 instance
- Configure networking
- Create storage
- Configure security settings
- Repeat the same process for another environment

This becomes difficult to maintain as infrastructure grows.

With IaC:

- Infrastructure configuration is stored as code
- Changes can be tracked through Git
- Environments can be recreated consistently
- Infrastructure changes can be reviewed before applying them
- Manual configuration errors are reduced
- Infrastructure provisioning becomes easier to automate through CI/CD

This makes infrastructure management part of the same development and DevOps workflow as application code.

---

## 🔄 Terraform vs Other Tools

| Tool | Main Purpose | Approach |
|---|---|---|
| **Terraform** | Provision and manage infrastructure | Declarative |
| **AWS CloudFormation** | Provision AWS infrastructure | Declarative |
| **Ansible** | Configure servers and automate tasks | Procedural / configuration management |
| **Pulumi** | Infrastructure as Code | Uses general-purpose programming languages |

### Terraform vs CloudFormation

CloudFormation is designed specifically for AWS, while Terraform can work with multiple cloud providers and services through providers.

### Terraform vs Ansible

Terraform is mainly used to **create and manage infrastructure**, while Ansible is commonly used to **configure and manage systems after they are created**.

For example:

```text
Terraform
   ↓
Create EC2 instance
   ↓
Ansible
   ↓
Configure the server
```

### Terraform vs Pulumi

Both can be used for Infrastructure as Code. Terraform uses HCL as its primary configuration language, while Pulumi allows infrastructure to be defined using programming languages such as Python, TypeScript, Go, and C#.

---

# 🛠️ Day 61 Hands-On

## 1. Terraform Installation

Terraform was installed and verified using:

```bash
terraform -version
```

This confirmed that Terraform was correctly installed and available from the terminal.

---

## 2. AWS CLI Configuration

AWS CLI was configured so Terraform could interact with AWS resources.

```bash
aws configure
```

The configuration included:

- AWS Access Key ID
- AWS Secret Access Key
- Default AWS Region
- Output format

AWS access was then verified using:

```bash
aws sts get-caller-identity
```

This confirmed that the AWS CLI was successfully authenticated with the configured AWS account.

> 🔐 AWS credentials should never be committed to GitHub or hardcoded inside Terraform files.

---

# 📁 Terraform Project Structure

For this hands-on task, I created a Terraform project and separated the configuration into multiple `.tf` files.

```text
Terraform-Guide/
│
├── ec2.tf
├── providers.tf
└── terraform.tf
```

### `terraform.tf`

Contains the Terraform configuration and required AWS provider information.

### `providers.tf`

Contains the AWS provider configuration and region.

### `ec2.tf`

Contains the EC2 infrastructure configuration.

Terraform automatically loads all `.tf` files in the working directory, so the configuration does not have to be placed in a single `main.tf` file.

---

# 🔧 Terraform Configuration

The configuration defines the AWS provider and infrastructure resources using Terraform configuration files.

Terraform configuration follows the desired-state approach: instead of describing every individual CLI action, I describe **what infrastructure should exist**, and Terraform determines the operations required to reach that state.

---

# ⚙️ Terraform Workflow

Terraform follows a simple workflow:

```text
Write
  ↓
terraform init
  ↓
terraform validate
  ↓
terraform plan
  ↓
terraform apply
  ↓
Infrastructure
```

The same configuration can later be modified and Terraform can calculate the required changes.

---

## 3. `terraform init`

The first command executed inside the Terraform project was:

```bash
terraform init
```

### What does `terraform init` do?

`terraform init` initializes the Terraform working directory.

It downloads the required provider plugins and prepares the directory for Terraform operations.

For this project, Terraform downloaded the **AWS provider**.

It also created the `.terraform/` directory.

```text
.terraform/
```

The `.terraform/` directory contains Terraform's local working data, including downloaded provider plugins and other initialization-related files.

The provider allows Terraform to communicate with AWS and manage AWS resources.

---

## 4. `terraform validate`

The configuration was checked using:

```bash
terraform validate
```

This verifies that the Terraform configuration is syntactically valid and structurally correct.

It helps catch configuration errors before attempting to create infrastructure.

---

## 5. `terraform plan`

Before creating or modifying infrastructure, I used:

```bash
terraform plan
```

`terraform plan` shows the changes Terraform intends to make without actually applying them.

The plan makes it possible to review infrastructure changes before they happen.

Terraform uses symbols to represent planned actions:

```text
+  Create
~  Update in-place
-  Destroy
-/+  Destroy and recreate
```

For example:

```text
+ aws_instance.example
```

means Terraform plans to create the EC2 instance.

---

# 🚀 6. `terraform apply`

After reviewing the plan, the infrastructure was created using:

```bash
terraform apply
```

Terraform displayed the execution plan and asked for confirmation.

After confirming with:

```text
yes
```

Terraform created the defined AWS resources.

The infrastructure could then be verified from the AWS Console.

---

# 🧠 Terraform State

One of the most important concepts introduced today was the **Terraform state file**.

Terraform stores information about the infrastructure it manages in:

```text
terraform.tfstate
```

The state allows Terraform to understand the relationship between the configuration and the real infrastructure running in AWS.

For example, after creating resources, Terraform records information such as:

- Resource type
- Resource name
- Resource ID
- Provider information
- Resource attributes
- Current infrastructure details
- Dependencies and relationships

---

## 🔍 Why is Terraform State Important?

Suppose the configuration contains an EC2 instance.

Terraform needs to know whether that instance already exists or whether it needs to create a new one.

The state file helps Terraform keep track of the resources it previously created.

Therefore, when running:

```bash
terraform plan
```

Terraform can compare:

```text
Terraform Configuration
        +
Terraform State
        +
Real Infrastructure
        ↓
Required Changes
```

This is how Terraform can determine that an existing S3 bucket does not need to be created again and that only a new EC2 instance needs to be added.

---

# 🔎 Terraform State Commands

### `terraform show`

```bash
terraform show
```

Displays a human-readable representation of the current Terraform state.

---

### `terraform state list`

```bash
terraform state list
```

Lists all resources currently managed by Terraform.

For example:

```text
aws_s3_bucket.example
aws_instance.example
```

---

### `terraform state show`

To inspect a particular resource:

```bash
terraform state show aws_instance.example
```

This displays detailed information about that resource stored in Terraform state.

The exact resource address depends on the resource names used in the Terraform configuration.

---

# ⚠️ Why Should the State File Not Be Manually Edited?

The state file is managed by Terraform.

Manually changing its contents can make Terraform's understanding of the infrastructure inconsistent with the actual AWS resources.

This can lead to:

- Incorrect plans
- Resource management problems
- Unexpected infrastructure changes
- State corruption

Therefore, Terraform commands should be used to manage state rather than manually editing the JSON file.

---

# 🔐 Why Should `terraform.tfstate` Not Be Committed to Git?

Terraform state can contain sensitive information depending on the resources being managed.

It also represents the current state of a specific infrastructure environment.

For these reasons, local state files should generally be excluded from Git.

The project `.gitignore` should contain entries such as:

```gitignore
.terraform/
*.tfstate
*.tfstate.backup
```

For team environments, Terraform state is normally stored using a remote backend with appropriate access control and locking.

---

# ✏️ 7. Modifying Infrastructure

After creating the infrastructure, I modified the EC2 instance configuration.

The instance tag was changed from:

```text
TerraWeek-Day1
```

to:

```text
TerraWeek-Modified
```

Then I ran:

```bash
terraform plan
```

Terraform detected that only the tag needed to change.

The `~` symbol in the plan represents an **in-place update**.

```text
~ update in-place
```

Terraform did not need to destroy and recreate the EC2 instance because changing the Name tag does not require a new instance.

The change was then applied using:

```bash
terraform apply
```

---

# 🗑️ 8. Destroying Infrastructure

After completing the experiment, I removed the resources using:

```bash
terraform destroy
```

Terraform displayed the resources that would be deleted and asked for confirmation.

After confirming:

```text
yes
```

Terraform removed the infrastructure it was managing.

The AWS Console was then checked to verify that the resources had been removed.

---

# 📋 Important Terraform Commands

| Command | Purpose |
|---|---|
| `terraform init` | Initializes the Terraform project and downloads providers |
| `terraform validate` | Checks Terraform configuration for errors |
| `terraform fmt` | Formats Terraform configuration files |
| `terraform plan` | Shows proposed infrastructure changes |
| `terraform apply` | Creates or modifies infrastructure |
| `terraform show` | Displays the current state in a readable format |
| `terraform state list` | Lists resources managed by Terraform |
| `terraform state show` | Displays details of a specific resource |
| `terraform destroy` | Removes resources managed by Terraform |

---

# 🔄 Complete Terraform Lifecycle

The complete workflow I followed can be summarized as:

```text
Write Terraform Configuration
            ↓
       terraform init
            ↓
      terraform validate
            ↓
       terraform plan
            ↓
      terraform apply
            ↓
     AWS Infrastructure
            ↓
      Modify Configuration
            ↓
       terraform plan
            ↓
      terraform apply
            ↓
      terraform destroy
            ↓
     Infrastructure Removed
```

---

# 🎯 What I Practiced Today

- Infrastructure as Code
- Terraform fundamentals
- Terraform configuration using HCL
- AWS provider configuration
- Terraform project structure
- `terraform init`
- `terraform validate`
- `terraform plan`
- `terraform apply`
- `terraform show`
- `terraform state list`
- `terraform state show`
- `terraform destroy`
- Terraform state management
- AWS infrastructure provisioning
- Infrastructure modification through code

---

# 📸 Evidence

### Terraform Apply

_Add screenshot of `terraform apply` showing the AWS resources being created._

### AWS Console

_Add screenshot showing the created AWS resources._

### Terraform Plan

_Add screenshot showing the EC2 tag modification and the `~` in-place update._

### Terraform Destroy

_Add screenshot showing Terraform destroying the resources._

---

# 💭 Key Takeaway

Day 61 introduced me to **Infrastructure as Code with Terraform**.

Instead of manually creating AWS infrastructure through the console, I was able to define the desired infrastructure using code and let Terraform create, modify, track, and destroy those resources.

The biggest takeaway was understanding the Terraform workflow:

```text
Configuration → Plan → Apply → State → Modify → Destroy
```

This is an important step toward managing cloud infrastructure in a **repeatable, version-controlled, and automated DevOps workflow**.

---

## 🔗 Repository

**Terraform Guide:**  
https://github.com/vaishnavipawardottech/Terraform-Guide

---

## 🚀 Next Step

Day 61 was my first step into **Terraform and Infrastructure as Code**.

The next step is to move beyond basic resources and start working with concepts such as **variables, outputs, data sources, VPCs, modules, and reusable Terraform configurations**.