# Day 39 – What is CI/CD?

## Goal

Understand why CI/CD exists, how CI differs from Continuous Delivery and Continuous Deployment, and how a CI/CD pipeline is structured.

Today focused on **concepts and pipeline design**, without creating an actual pipeline.

---

# Task 1 – The Problem

Imagine a team of 5 developers working on the same application and manually deploying code to production.

## 1. What Can Go Wrong?

Manual development and deployment can lead to:

* Merge conflicts between developers.
* Bugs reaching production because testing is inconsistent.
* Human errors during deployment.
* Different developers using different environments.
* Deployments taking too much time.
* Difficulties knowing which code version is deployed.
* No consistent process for build, test, and deployment.
* Rollbacks becoming difficult when something goes wrong.

CI/CD automates repetitive parts of this process and provides a consistent way to build, test, and deploy applications.

---

## 2. What Does "It Works on My Machine" Mean?

"It works on my machine" means an application works in one developer's environment but fails somewhere else.

This can happen because of differences in:

* Operating system
* Runtime or language version
* Dependencies
* Environment variables
* Configuration
* Database versions
* Installed tools

CI helps detect these environment and integration problems earlier by automatically building and testing code in a controlled environment.

---

## 3. How Many Times Can a Team Safely Deploy Manually?

There is no fixed number.

The problem is that **manual deployment does not scale well**. As deployment frequency increases, the chance of human error and inconsistent processes also increases.

Automation allows teams to deploy much more frequently and consistently.

---

# Task 2 – CI vs CD

## 1. Continuous Integration (CI)

Continuous Integration means developers frequently integrate their code into a shared repository.

Whenever code is pushed or a pull request is created, automated processes can build the application and run tests.

**Purpose:** Detect integration problems and bugs early.

### Real-World Example

A developer pushes code to GitHub. A CI pipeline automatically:

```text
Checkout → Install Dependencies → Build → Run Tests
```

If a test fails, the team knows before the code reaches deployment.

---

## 2. Continuous Delivery

Continuous Delivery extends CI by automatically preparing validated code for release.

After the application passes build and testing, it is packaged and kept **ready to deploy**, but production deployment usually requires a manual approval or trigger.

### Real-World Example

```text
Code → Build → Test → Docker Image → Staging → Production Approval
```

The application is always in a deployable state, but the production release is manually approved.

---

## 3. Continuous Deployment

Continuous Deployment goes one step further.

Every change that successfully passes the required automated checks is **automatically deployed to production** without a manual approval step.

### Real-World Example

```text
Code → Build → Test → Docker Image → Production
```

If all automated checks pass, the new version is automatically released.

---

## Quick Difference

| Concept               | Main Idea                               | Production Deployment   |
| --------------------- | --------------------------------------- | ----------------------- |
| CI                    | Build and test code frequently          | Not necessarily         |
| Continuous Delivery   | Keep validated code ready for release   | Usually manual approval |
| Continuous Deployment | Automatically release validated changes | Automatic               |

**Important:** CI/CD is a practice and methodology. Tools such as GitHub Actions, Jenkins, GitLab CI and CircleCI are used to implement it.

---

# Task 3 – Pipeline Anatomy

A CI/CD pipeline is divided into different levels of work.

## Trigger

The event that starts a pipeline.

Examples:

* Push to a branch
* Pull request
* Tag creation
* Manual trigger
* Scheduled execution

---

## Stage

A logical phase of the pipeline.

Examples:

```text
Build
Test
Deploy
```

Stages help organize the pipeline into meaningful phases.

---

## Job

A unit of work executed within a stage.

For example, a `Test` stage could contain:

```text
Test Stage
├── Unit Tests
└── Integration Tests
```

Jobs can sometimes run in parallel.

---

## Step

A single command or action inside a job.

Example:

```text
Job: Build
  Step 1 → Checkout code
  Step 2 → Install dependencies
  Step 3 → Build application
```

---

## Runner

The machine or environment that executes the jobs.

For example, a GitHub Actions job can run on an Ubuntu runner.

---

## Artifact

A file or output produced by a job that can be used later.

Examples:

* Build files
* JAR files
* Test reports
* Docker image metadata
* Application packages

Artifacts allow output from one part of a pipeline to be stored and passed to later stages.

---

# Task 4 – CI/CD Pipeline Diagram

Scenario:

> A developer pushes code to GitHub. The application is tested, built into a Docker image, and deployed to a staging server.

## Pipeline

```text
                Developer
                    |
                    | git push
                    ↓
               ┌─────────┐
               │ GitHub  │
               └────┬────┘
                    |
                 Trigger
                    ↓
        ┌─────────────────────┐
        │     BUILD STAGE     │
        │                     │
        │ Checkout Code       │
        │ Install Dependencies│
        │ Build Application   │
        └──────────┬──────────┘
                   |
                   ↓
        ┌─────────────────────┐
        │      TEST STAGE     │
        │                     │
        │ Unit Tests          │
        │ Integration Tests   │
        └──────────┬──────────┘
                   |
              Tests Pass
                   ↓
        ┌─────────────────────┐
        │   DOCKER BUILD      │
        │                     │
        │ Build Docker Image  │
        │ Tag Image           │
        └──────────┬──────────┘
                   |
                   ↓
        ┌─────────────────────┐
        │   DEPLOY STAGE      │
        │                     │
        │ Deploy to Staging   │
        └─────────────────────┘
```

### Flow

```text
Developer
    ↓
GitHub Push
    ↓
Trigger
    ↓
Build
    ↓
Test
    ↓
Docker Image
    ↓
Staging Server
```

---

# Task 5 – Explore CI/CD in the Wild

For this task, I explored the **FastAPI** open-source repository and inspected its GitHub Actions workflows.

## Repository

**Repository:** FastAPI

**Workflow Directory:**

```text
.github/workflows/
```

The repository contains multiple workflow YAML files such as `test.yml`, `build-docs.yml`, `publish.yml`, `pre-commit.yml`, and others.

## Workflow Selected

**Workflow:** `test.yml`

The workflow can be found inside:

```text
.github/workflows/test.yml
```

## What Triggers It?

The `test.yml` workflow is triggered by:

* Pushes to the `master` branch
* Pull requests
* A scheduled weekly run using cron

```yaml
on:
  push:
    branches:
      - master
  pull_request:
  schedule:
    - cron: "0 0 * * 1"
```

## How Many Jobs Does It Have?

The workflow contains multiple jobs. The first jobs defined include:

```text
changes
test
```

The `test` job depends on the `changes` job and runs when relevant source files have changed or when running against the `master` branch.

## What Does It Do?

The workflow is mainly used to **automatically test the FastAPI project**.

A simplified view is:

```text
Code Push / Pull Request
          ↓
       Trigger
          ↓
    Check Changes
          ↓
      Run Tests
          ↓
 Test Different Environments
```

The `test` job uses a matrix to run tests across different operating systems and Python versions. It also performs different dependency-resolution and test configurations.

## What I Learned

This example shows how a real open-source project uses GitHub Actions for CI:

```text
Developer Change
      ↓
GitHub Event
      ↓
Workflow Trigger
      ↓
Jobs
      ↓
Automated Tests
      ↓
Result
```
This connects directly with the CI/CD concepts learned today: **triggers, jobs, steps, runners, and automated testing**.

---

# Key Takeaways

### 1. CI/CD Reduces Manual Work

Instead of manually repeating build, test, and deployment steps, pipelines automate these processes consistently.

### 2. CI, Delivery and Deployment Are Different

```text
CI                 → Build + Test
Continuous Delivery → Build + Test + Ready to Release
Continuous Deployment → Build + Test + Automatic Production Release
```

### 3. Pipelines Are Made of Smaller Components

```text
Trigger
   ↓
Stage
   ↓
Job
   ↓
Step
   ↓
Runner
   ↓
Artifact
```

Understanding these building blocks makes tools such as GitHub Actions and Jenkins much easier to learn.
