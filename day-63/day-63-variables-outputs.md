# Day 63 — Variables, Outputs, Data Sources and Expressions

## 🚀 Introduction

Writing Terraform configuration is only the first step. To make infrastructure reusable across different projects and environments, we need to avoid hardcoding values such as AWS regions, CIDR blocks, AMI IDs, and instance types.

Today, I explored how Terraform variables, variable files, outputs, data sources, locals, and built-in functions help make infrastructure configurations more flexible, dynamic, and maintainable.

The goal is to create a configuration that can be reused across development and production environments without rewriting the entire infrastructure code.

---

## 📌 1. Terraform Input Variables

Input variables allow us to pass values into Terraform configurations instead of hardcoding them directly into resource blocks.

For example, instead of writing:

```hcl
instance_type = "t2.micro"
```

we can write:

```hcl
instance_type = var.instance_type
```

The value is then defined in `variables.tf` or supplied through a variable file or command line.

### `variables.tf`

```hcl
variable "region" {
  description = "AWS region for infrastructure"
  type        = string
  default     = "ap-south-1"
}

variable "vpc_cidr" {
  description = "CIDR block for the VPC"
  type        = string
  default     = "10.0.0.0/16"
}

variable "subnet_cidr" {
  description = "CIDR block for the public subnet"
  type        = string
  default     = "10.0.1.0/24"
}

variable "instance_type" {
  description = "EC2 instance type"
  type        = string
  default     = "t2.micro"
}

variable "project_name" {
  description = "Name of the project"
  type        = string
}

variable "environment" {
  description = "Deployment environment"
  type        = string
  default     = "dev"
}

variable "allowed_ports" {
  description = "Ports allowed for inbound traffic"
  type        = list(number)
  default     = [22, 80, 443]
}

variable "extra_tags" {
  description = "Additional resource tags"
  type        = map(string)
  default     = {}
}
```

### Five Common Terraform Variable Types

| Type | Purpose | Example |
|---|---|---|
| `string` | Stores text | `"ap-south-1"` |
| `number` | Stores numeric values | `8080` |
| `bool` | Stores true or false | `true` |
| `list` | Stores an ordered collection | `["dev", "prod"]` |
| `map` | Stores key-value pairs | `{ Environment = "dev" }` |

**Key takeaway:** Variables make Terraform configurations reusable by separating configuration values from infrastructure definitions.

---

## 📂 2. Variable Files and Environments

Terraform supports `.tfvars` files for supplying values to input variables.

This allows us to use the same infrastructure configuration for multiple environments.

### `terraform.tfvars` — Development

```hcl
project_name = "terraweek"
environment  = "dev"
instance_type = "t2.micro"
```

Terraform automatically loads `terraform.tfvars`.

### `prod.tfvars` — Production

```hcl
project_name = "terraweek"
environment  = "prod"
instance_type = "t3.small"

vpc_cidr    = "10.1.0.0/16"
subnet_cidr = "10.1.1.0/24"
```

To preview the development configuration:

```bash
terraform plan
```

To preview the production configuration:

```bash
terraform plan -var-file="prod.tfvars"
```

We can also override a variable from the command line:

```bash
terraform plan -var="instance_type=t2.nano"
```

Environment variables can supply values using the `TF_VAR_` prefix:

```bash
export TF_VAR_environment="staging"
terraform plan
```

### Variable Precedence

When multiple sources provide a value for the same variable, Terraform follows a precedence order. From lowest to highest priority:

1. Variable default values
2. Environment variables (`TF_VAR_*`)
3. `terraform.tfvars` and `terraform.tfvars.json`
4. Automatically loaded `*.auto.tfvars` and `*.auto.tfvars.json` files
5. Command-line `-var` and `-var-file` arguments

When multiple command-line arguments assign the same variable, the later assignment takes precedence.

**Note:** A custom file such as `prod.tfvars` is not automatically loaded. Pass it explicitly with `-var-file`.

---

## 📤 3. Terraform Outputs

Output values display useful information about infrastructure after Terraform applies the configuration.

For example, we may need an EC2 instance's public IP address or the ID of the VPC that was created.

### `outputs.tf`

```hcl
output "vpc_id" {
  description = "ID of the VPC"
  value       = aws_vpc.main.id
}

output "subnet_id" {
  description = "ID of the public subnet"
  value       = aws_subnet.public.id
}

output "instance_id" {
  description = "ID of the EC2 instance"
  value       = aws_instance.server.id
}

output "instance_public_ip" {
  description = "Public IP of the EC2 instance"
  value       = aws_instance.server.public_ip
}

output "instance_public_dns" {
  description = "Public DNS name of the EC2 instance"
  value       = aws_instance.server.public_dns
}

output "security_group_id" {
  description = "ID of the security group"
  value       = aws_security_group.web.id
}
```

The resource addresses must match the resource names used in the configuration.

After applying the configuration:

```bash
terraform apply
```

Terraform displays the declared outputs at the end of a successful apply.

We can also retrieve them separately:

```bash
terraform output
```

To display a specific output:

```bash
terraform output instance_public_ip
```

To retrieve outputs in JSON format:

```bash
terraform output -json
```

### Why Are Outputs Useful?

- Retrieve resource IDs and IP addresses.
- Share information between Terraform modules.
- Make infrastructure information available to scripts and automation.
- Avoid manually searching the AWS Console for resource details.

**Verification:** Compare `terraform output instance_public_ip` with the public IP displayed for the EC2 instance in the AWS Console.

---

## 🔍 4. Terraform Data Sources

A data source retrieves information about existing resources or external infrastructure information without creating that resource itself.

For example, hardcoding an AMI ID can cause problems when the image differs between AWS regions.

Instead, Terraform can query AWS for a suitable image.

### Fetch the Latest Matching Amazon Linux 2 AMI

```hcl
data "aws_ami" "amazon_linux" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["amzn2-ami-hvm-*-x86_64-gp2"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }

  filter {
    name   = "root-device-type"
    values = ["ebs"]
  }
}
```

The filters select Amazon-owned images matching the specified name, virtualization type, and root-device type.

The EC2 instance can reference the selected AMI dynamically:

```hcl
resource "aws_instance" "server" {
  ami           = data.aws_ami.amazon_linux.id
  instance_type = var.instance_type

  # Other configuration
}
```

### Fetch Available Availability Zones

```hcl
data "aws_availability_zones" "available" {
  state = "available"
}
```

To use the first available zone:

```hcl
availability_zone = data.aws_availability_zones.available.names[0]
```

The selected zone is determined by the availability-zone data source.

### Resource vs Data Source

| Resource | Data Source |
|---|---|
| Creates and manages infrastructure | Reads information |
| Can modify or destroy managed resources | Does not create or manage the queried resource |
| Example: `aws_instance` | Example: `aws_ami` |

**Key takeaway:** Data sources allow Terraform to discover infrastructure information dynamically rather than relying on hardcoded IDs.

---

## 🏷️ 5. Locals and Dynamic Tags

Locals allow us to define reusable expressions and computed values inside a Terraform configuration.

They are useful when the same value needs to be reused in multiple resources.

### Locals Block

```hcl
locals {
  name_prefix = "${var.project_name}-${var.environment}"

  common_tags = {
    Project     = var.project_name
    Environment = var.environment
    ManagedBy   = "Terraform"
  }
}
```

Here, `name_prefix` combines the project name and environment.

For example:

```text
terraweek-dev
```

### Applying Consistent Tags

```hcl
tags = merge(local.common_tags, {
  Name = "${local.name_prefix}-server"
})
```

The `merge()` function combines the common tags with resource-specific tags.

The same approach can be used for the VPC, subnet, security group, and EC2 instance.

Example resource names:

```text
terraweek-dev-vpc
terraweek-dev-subnet
terraweek-dev-server
```

This makes resources easier to identify and filter in the AWS Console.

---

## 🧮 6. Built-in Functions and Conditional Expressions

Terraform provides built-in functions for manipulating strings, collections, maps, and network addresses.

We can test expressions interactively using:

```bash
terraform console
```

### Five Useful Built-in Functions

**1. `upper()` — Convert text to uppercase**

```hcl
upper("terraweek")
```

Output:

```text
"TERRAWEEK"
```

**2. `join()` — Combine strings using a separator**

```hcl
join("-", ["terra", "week", "2026"])
```

Output:

```text
"terra-week-2026"
```

**3. `length()` — Count elements**

```hcl
length(["a", "b", "c"])
```

Output:

```text
3
```

**4. `lookup()` — Retrieve a value from a map**

```hcl
lookup(
  { dev = "t2.micro", prod = "t3.small" },
  "dev"
)
```

Output:

```text
"t2.micro"
```

**5. `cidrsubnet()` — Calculate a subnet CIDR block**

```hcl
cidrsubnet("10.0.0.0/16", 8, 1)
```

Output:

```text
"10.0.1.0/24"
```

This is useful when planning network ranges and generating subnet CIDR blocks.

Other useful functions include `format()`, `toset()`, and `merge()`.

### Conditional Expressions

Conditional expressions select a value based on whether a condition is true or false.

The general syntax is:

```hcl
condition ? true_value : false_value
```

For example:

```hcl
instance_type = var.environment == "prod" ? "t3.small" : "t2.micro"
```

This expression selects `t3.small` for production and `t2.micro` for other environments.

To use this expression, place it in the appropriate configuration or local value and reference that value from the EC2 resource. Avoid declaring the same argument twice in a resource block.

**Important:** If the selected instance type differs from the existing one, Terraform's plan will show the required change. Depending on the AWS provider's replacement rules, changing an EC2 instance type may require a stop/start or replacement operation. Always review the plan before applying it.

---

## 🔄 7. Putting Everything Together

The configuration can be organized into separate files:

```text
terraform-basics/
│
├── terraform.tf
├── providers.tf
├── variables.tf
├── main.tf
├── outputs.tf
├── terraform.tfvars
├── prod.tfvars
└── .gitignore
```

### File Responsibilities

| File | Purpose |
|---|---|
| `terraform.tf` | Terraform settings and required providers |
| `providers.tf` | AWS provider configuration |
| `variables.tf` | Input variables and types |
| `main.tf` | VPC, subnet, security group, data sources, and EC2 configuration |
| `outputs.tf` | Infrastructure outputs |
| `terraform.tfvars` | Default development values |
| `prod.tfvars` | Production-specific values |

Terraform automatically loads all `.tf` files in the working directory. The filenames are used to organize the configuration, not to define a mandatory execution order.

### Workflow

```text
Define Variables
       ↓
Configure Environments
       ↓
Retrieve Dynamic Data
       ↓
Create Infrastructure
       ↓
Display Outputs
       ↓
Verify AWS Resources
```

### Useful Commands

```bash
terraform fmt
terraform validate
terraform plan
terraform plan -var-file="prod.tfvars"
terraform apply
terraform output
terraform output instance_public_ip
terraform output -json
terraform console
```

These commands help format, validate, plan, apply, inspect, and test the Terraform configuration.

---

## 📸 Evidence

### 1. Terraform Plan

_Add a screenshot showing the plan for your parameterized infrastructure._

### 2. Terraform Apply and Outputs

_Add a screenshot showing successful resource creation and the generated output values._

### 3. AWS Console

_Add a screenshot showing the VPC, subnet, security group, and EC2 instance._

### 4. Environment Comparison

_Add screenshots or terminal output showing the different configurations selected by `terraform.tfvars` and `prod.tfvars`._

### 5. Terraform Console

_Add a screenshot showing the built-in functions and their results._

---

## 🎯 What I Practiced Today

- Terraform input variables and variable types
- Environment-specific `.tfvars` files
- Variable precedence
- Terraform outputs
- AWS AMI and availability-zone data sources
- Locals and reusable expressions
- Consistent resource tagging using `merge()`
- String, collection, and networking functions
- Conditional expressions
- Reusable Terraform configurations

---

## 💡 Key Takeaway

Day 63 focused on making Terraform configurations dynamic and reusable.

Variables help customize infrastructure, data sources retrieve information dynamically, locals simplify repeated expressions, and outputs expose useful resource details.

Together, these features make it easier to manage infrastructure across different environments without duplicating configuration code.

---

## 🔗 Repository

**Terraform Guide:**  
https://github.com/vaishnavipawardottech/Terraform-Guide

---

## 🚀 Next Step

The next step is to build on these fundamentals by exploring reusable Terraform modules, remote state management, and more structured infrastructure deployments.
