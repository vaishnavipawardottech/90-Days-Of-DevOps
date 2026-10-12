# Day 64: Terraform State Management and Remote Backends

## Overview

Terraform state is the link between our Terraform configuration and the actual infrastructure running in the cloud. It tracks the resources managed by Terraform and stores information about their attributes.

Effective state management is essential to prevent resource conflicts, recover from mistakes, import existing infrastructure, and detect configuration drift.

In this practical session, I explored Terraform state inspection, S3 remote backends, state locking, resource importing, state manipulation, and drift reconciliation.

## Objectives

- Inspect and understand Terraform state.
- Migrate local state to an Amazon S3 remote backend.
- Configure state locking using Amazon DynamoDB.
- Import an existing AWS resource into Terraform.
- Rename and remove resources from state safely.
- Simulate and reconcile infrastructure drift.

## 1. Inspecting Terraform State

Before configuring a remote backend, I used my existing Terraform configuration from Day 63 to provision infrastructure and inspect its state.

### Commands used

```bash
terraform show
terraform state list
terraform state show aws_instance.<resource_name>
terraform state show aws_vpc.<resource_name>
```

**What these commands do:**

- `terraform show` displays the current state in a readable format.
- `terraform state list` lists resource addresses tracked in the state.
- `terraform state show` displays the stored attributes of a specific resource.

The state file contains more information than the arguments explicitly written in `.tf` files. For example, an EC2 instance's state may include its instance ID, AMI, instance type, subnet, private IP, public IP, tags, and other provider-computed attributes.

### Understanding the serial number

The `serial` field in `terraform.tfstate` is a monotonically increasing state revision number. It increases as Terraform writes updated state, helping Terraform identify newer state snapshots and protect against certain accidental overwrites.

**Key takeaway:** Terraform state is not simply a copy of the configuration. It records the relationship between declared resources and the infrastructure Terraform manages.

## 2. Configuring an S3 Remote Backend

Local state files can be lost with a damaged computer, accidental deletion, or other local failures. A remote backend allows a team to store and access shared state centrally.

### Architecture: Local vs. Remote State

**Local state**

```text
Terraform Configuration (.tf)
            |
            v
     Terraform CLI
            |
            v
   Local terraform.tfstate
            |
            v
   AWS Infrastructure
```

**Remote state with locking**

```text
Developer / Terraform CLI
            |
            v
 Terraform Configuration
            |
            v
      S3 Backend
            |
            +------> State file
            |        dev/terraform.tfstate
            |
            +------> DynamoDB
                     State locking
            |
            v
      AWS Infrastructure
```

S3 stores the remote state, while DynamoDB coordinates access by managing state locks. S3 bucket versioning provides recovery options for previous state versions.

### Step 1: Create the S3 bucket

I created a dedicated bucket for Terraform state in the `ap-south-1` region.

Replace `<yourname>` with a suitable unique name before running these commands.

```bash
aws s3api create-bucket \
  --bucket terraweek-state-<yourname> \
  --region ap-south-1 \
  --create-bucket-configuration LocationConstraint=ap-south-1
```

Enable versioning:

```bash
aws s3api put-bucket-versioning \
  --bucket terraweek-state-<yourname> \
  --versioning-configuration Status=Enabled
```

### Step 2: Create the DynamoDB lock table

```bash
aws dynamodb create-table \
  --table-name terraweek-state-lock \
  --attribute-definitions AttributeName=LockID,AttributeType=S \
  --key-schema AttributeName=LockID,KeyType=HASH \
  --billing-mode PAY_PER_REQUEST \
  --region ap-south-1
```

The table uses `LockID` as its string partition key, as required by the DynamoDB-based locking mechanism.

### Step 3: Configure the backend

I added the backend configuration to the existing `terraform` block in my Terraform configuration. Terraform permits only one backend block per configuration.

```hcl
terraform {
  backend "s3" {
    bucket         = "terraweek-state-<yourname>"
    key            = "dev/terraform.tfstate"
    region         = "ap-south-1"
    dynamodb_table = "terraweek-state-lock"
    encrypt        = true
  }
}
```

Replace the placeholder with the actual bucket name. The bucket and DynamoDB table must exist before Terraform initializes this backend.

### Step 4: Migrate the existing state

```bash
terraform init -migrate-state
```

Terraform prompts to copy the existing local state to the remote backend. I confirmed the migration when prompted.

### Step 5: Verify the migration

```bash
terraform state list
terraform plan
```

I also checked the S3 bucket to verify that `dev/terraform.tfstate` was present.

After a successful migration, Terraform should continue tracking the same resources, and the plan should report no changes if the configuration and infrastructure are already synchronized.

The original local state file may be removed during migration, while a backup may remain. I verified the remote state rather than relying only on the local file's presence.

**Important:** State files can contain sensitive information. They should never be committed to a public GitHub repository.

### Screenshot evidence

- [ ] S3 bucket showing `dev/terraform.tfstate`
- [ ] Bucket versioning enabled
- [ ] Successful backend initialization and state migration
- [ ] `terraform plan` showing no changes

## 3. Testing State Locking

State locking prevents multiple Terraform operations from modifying the same state simultaneously when the backend supports locking.

### Testing procedure

1. Open two terminals in the same Terraform project.
2. In Terminal 1, run `terraform apply` and wait at the approval prompt.
3. In Terminal 2, run `terraform plan`.
4. Observe whether the second operation is blocked by the lock held by the first operation.

The second terminal should report that Terraform cannot acquire the state lock while the first operation holds it.

The error commonly includes details such as the lock ID, operation, and information about the process holding the lock. The exact message depends on the Terraform version and backend.

### Why is locking important?

Without locking, concurrent operations could read different state versions and attempt conflicting infrastructure changes. Locking helps protect state consistency in team environments and CI/CD pipelines.

### Handling a stale lock

If an operation fails unexpectedly and leaves a stale lock, first verify that no Terraform operation is still running. Only then, if appropriate, use:

```bash
terraform force-unlock <LOCK_ID>
```

**Caution:** Never force-unlock a state that another active operation is using. Doing so can allow concurrent writers and cause state corruption.

### Screenshot evidence

- [ ] Terminal showing the state lock error
- [ ] Lock ID and relevant error details

## 4. Importing an Existing AWS Resource

Terraform can take over management of infrastructure that already exists in AWS. Importing connects an existing resource to a Terraform resource address in state; it does not create the AWS resource from scratch.

### Step 1: Create an S3 bucket

I created a separate test bucket manually in AWS, using a globally unique name such as `terraweek-import-test-<yourname>`.

### Step 2: Define the resource

I added an `aws_s3_bucket` resource block to the Terraform configuration with the actual bucket name.

```hcl
resource "aws_s3_bucket" "imported" {
  bucket = "terraweek-import-test-<yourname>"
}
```

Replace the placeholder with the real bucket name.

### Step 3: Import the bucket

```bash
terraform import \
  aws_s3_bucket.imported \
  terraweek-import-test-<yourname>
```

Terraform reads the existing bucket and records its association with `aws_s3_bucket.imported` in state.

### Step 4: Verify the import

```bash
terraform state list
terraform state show aws_s3_bucket.imported
terraform plan
```

I checked that the resource appeared in the state and compared the configuration against the real bucket.

If the plan shows changes, I inspect the proposed differences and update the configuration as needed. A successful import does not automatically generate a complete Terraform configuration or guarantee that the plan will show no changes.

### Import vs. creating a resource

- **Creating a resource:** Terraform provisions new infrastructure based on its configuration.
- **Importing a resource:** Terraform associates an existing infrastructure resource with a Terraform resource address so it can be managed through configuration.

**Important:** Importing does not automatically import every related resource or configure all of the resource's settings.

## 5. State Surgery: `state mv` and `state rm`

Terraform provides state commands for changing resource addresses or removing resource tracking without immediately destroying the underlying infrastructure.

### Renaming a resource in state

First, I listed the tracked resources:

```bash
terraform state list
```

Then I renamed the resource address:

```bash
terraform state mv \
  aws_s3_bucket.imported \
  aws_s3_bucket.logs_bucket
```

I also updated the resource label in the `.tf` configuration to `logs_bucket`.

Finally, I ran:

```bash
terraform plan
```

If the configuration and state address are aligned, the rename should not require the bucket to be recreated.

### Removing a resource from state

```bash
terraform state rm aws_s3_bucket.logs_bucket
```

This removes the resource's association from Terraform state but does **not** delete the bucket in AWS.

If the resource remains in the configuration, a subsequent plan will generally propose creating it again because Terraform no longer tracks the existing bucket. Do not apply that plan without understanding the consequences.

### Re-importing the resource

```bash
terraform import \
  aws_s3_bucket.logs_bucket \
  terraweek-import-test-<yourname>
```

I then verified the state and reviewed the plan.

### When would these commands be useful?

- **`terraform state mv`:** Renaming a resource, reorganizing modules, or moving a resource address while preserving its existing state association.
- **`terraform state rm`:** Removing Terraform's tracking of a resource when transferring management elsewhere or intentionally stopping Terraform from managing it. The real resource remains unless separately deleted.
- **`terraform import`:** Bringing existing infrastructure under Terraform management.

These operations should be performed carefully, ideally with a state backup and a reviewed plan.

## 6. Simulating and Reconciling State Drift

State drift occurs when the real infrastructure changes outside the expected Terraform workflow, causing it to differ from the declared configuration.

### Step 1: Start with synchronized infrastructure

```bash
terraform plan
terraform apply
```

I first ensured that the configuration and deployed infrastructure were synchronized.

### Step 2: Introduce a manual change

In the AWS Console, I changed the Name tag of my EC2 instance to `ManuallyChanged`, without updating the corresponding Terraform configuration.

Adding a tag is a straightforward way to demonstrate drift without needing to change the instance type or stop the instance.

### Step 3: Detect the drift

```bash
terraform plan
```

Terraform refreshed its view of the remote resource and compared it with the desired configuration. The plan should identify the tag difference and show the proposed correction.

### Step 4: Reconcile the drift

I chose to restore the configuration-defined tag by running:

```bash
terraform apply
```

After reviewing and approving the proposed change, I ran:

```bash
terraform plan
```

The expected result was **no changes**, confirming that the manual tag change had been reconciled.

### How can teams prevent drift in production?

- Restrict direct console changes through IAM permissions and access controls.
- Use reviewed Terraform changes and CI/CD pipelines for infrastructure updates.
- Run regular plans to identify unexpected changes.
- Keep configurations, state, and team workflows consistent.
- Investigate drift before applying a reconciliation plan, especially in production.

**Key takeaway:** Terraform plans help identify differences between desired configuration and real infrastructure, but every proposed change should be reviewed before applying it.

## 7. Additional State Management Commands

| Command | Purpose |
|---|---|
| `terraform show` | Display current state or a saved plan in readable form. |
| `terraform state list` | List resource addresses in state. |
| `terraform state show <address>` | Inspect one tracked resource. |
| `terraform state mv <source> <destination>` | Change a resource's address in state. |
| `terraform state rm <address>` | Remove a resource association without deleting the real resource. |
| `terraform import <address> <id>` | Associate an existing resource with a Terraform address. |
| `terraform force-unlock <LOCK_ID>` | Remove a stale lock when it is safe to do so. |
| `terraform apply -refresh-only` | Review and record observed infrastructure changes in state without applying normal configuration changes. |
| `terraform refresh` | Legacy command for refreshing state; prefer `terraform plan -refresh-only` or `terraform apply -refresh-only` for an explicit, reviewable workflow. |

## 8. Key Learnings

- Terraform state connects configuration to managed infrastructure.
- S3 remote state provides centralized storage, while bucket versioning supports recovery.
- State locking helps prevent conflicting concurrent operations.
- Importing lets Terraform manage existing resources.
- State commands can change resource tracking without directly changing the real infrastructure.
- Drift detection and reconciliation help maintain consistency between configuration and deployed resources.
- State files must be protected because they may contain sensitive values.

## 9. Practical Evidence Checklist

- [ ] State inspection using `terraform show` and `terraform state list`
- [ ] State file visible in the S3 bucket
- [ ] Successful local-to-remote migration
- [ ] State locking error captured from the second terminal
- [ ] Existing S3 bucket imported and visible in state
- [ ] Resource address renamed using `terraform state mv`
- [ ] Resource removed and re-imported using `terraform state rm` and `terraform import`
- [ ] Manual tag change detected by `terraform plan`
- [ ] Drift reconciled and final plan showing no changes

*Add your own screenshots and actual command outputs to this section after completing each task.*

## Conclusion

Day 64 focused on managing Terraform state safely and understanding how state, configuration, and real infrastructure work together. Remote backends, locking, importing, state manipulation, and drift reconciliation are important practices for maintaining reliable infrastructure as code.

🔗 **GitHub Repository:** https://github.com/vaishnavipawardottech/Terraform-Guide

#90DaysOfDevOps | Terraform | AWS | Infrastructure as Code