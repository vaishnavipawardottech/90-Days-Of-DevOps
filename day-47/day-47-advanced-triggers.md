# Day 47 - Advanced Triggers in GitHub Actions

## What I learned

GitHub Actions workflows can be triggered by different events depending on when we want the automation to run.

In this task, I explored:

- Pull Request events
- PR validation checks
- Scheduled workflows using cron
- Path and branch filters
- `workflow_run`
- `repository_dispatch`
- Event-driven pipelines

---

## Task 1: Pull Request Lifecycle

Created `.github/workflows/pr-lifecycle.yml` to trigger when a Pull Request is:

- Opened
- Updated
- Reopened
- Closed

The workflow prints:

- PR event/action
- PR title
- PR author
- Source branch
- Target branch

It also checks whether the PR was merged.

### Key concept

`pull_request` gives access to useful PR information through:

`github.event.pull_request`

---

## Task 2: Pull Request Checks

Created `.github/workflows/pr-checks.yml` with three checks.

### 1. File size check

Checks whether any file is larger than 1 MB.

If a file exceeds the limit, the workflow fails.

### 2. Branch name check

Allows only these branch naming patterns:

- `feature/*`
- `fix/*`
- `docs/*`

Example:

`feature/login-page`

### 3. PR body check

Checks whether the Pull Request description is present.

If it is empty, the workflow gives a warning without failing the workflow.

### Key concept

GitHub Actions can be used to automatically validate Pull Requests before merging them.

---

## Task 3: Scheduled Workflows

Created `.github/workflows/scheduled-tasks.yml`.

Used cron schedules to run the workflow automatically.

### Schedules used

- Every Monday at 2:30 AM UTC
- Every 6 hours

Also added `workflow_dispatch` so the workflow can be run manually.

The workflow:

1. Prints which schedule triggered it.
2. Performs a health check using `curl`.
3. Checks the HTTP response code.

### Example cron expressions

Every weekday at 9:00 AM IST:

`30 3 * * 1-5`

First day of every month at midnight:

`0 0 1 * *`

### Key concept

Scheduled workflows are useful for:

- Health checks
- Cleanup jobs
- Reports
- Backups
- Monitoring
- Periodic automation

---

## Task 4: Path and Branch Filters

Created workflows to understand when a workflow should run based on the branch and changed files.

### `paths`

The workflow runs only when files inside specific paths are changed.

Example:

`src/**`

`app/**`

### `paths-ignore`

The workflow does not run when only ignored files are changed.

Example:

`*.md`

`docs/**`

### Key concept

Path filters help avoid unnecessary workflow runs.

For example, there is no need to run an application build when only documentation is changed.

---

## Task 5: `workflow_run`

Created two workflows:

- `Run Tests`
- `Deploy After Tests`

The `Run Tests` workflow runs tests on every push.

The `Deploy After Tests` workflow uses:

`workflow_run`

It starts after the `Run Tests` workflow completes.

Deployment happens only when:

`github.event.workflow_run.conclusion == 'success'`

### Pipeline

Push code  
↓  
Run Tests  
↓  
Tests successful  
↓  
Deploy

### Key concept

`workflow_run` is useful when one workflow needs to react to the result of another workflow.

---

## Task 6: `repository_dispatch`

Created `.github/workflows/external-trigger.yml`.

This workflow listens for a custom event:

`repository_dispatch`

with the event type:

`deploy-request`

The workflow also reads data sent with the event:

`github.event.client_payload.environment`

For example:

`production`

### Triggering the workflow

Used GitHub CLI:

    gh api repos/vaishnavipawardottech/github-actions-practice/dispatches \
      -f event_type=deploy-request \
      -f client_payload='{"environment":"production"}'

### What is happening?

An external system sends a request to GitHub's API.

External System  
↓  
GitHub API  
↓  
`repository_dispatch`  
↓  
GitHub Actions workflow  
↓  
Deployment process

The `client_payload` allows the external system to send additional information such as:

`environment = production`

### Why is this useful?

This is useful when something outside GitHub needs to start a GitHub Actions workflow.

Examples:

- Monitoring systems
- Slack bots
- Jenkins
- Deployment platforms
- Internal automation tools

### Important difference

`workflow_call`:

GitHub Actions Workflow A  
↓  
GitHub Actions Workflow B

`repository_dispatch`:

External System  
↓  
GitHub API  
↓  
GitHub Actions Workflow

---

## Key Takeaways

- `pull_request` can trigger workflows for different PR lifecycle events.
- PR checks can automatically validate code before merging.
- `schedule` runs workflows automatically using cron.
- `paths` and `paths-ignore` control workflows based on changed files.
- `workflow_run` allows one workflow to react to another workflow's result.
- `repository_dispatch` allows external systems to trigger GitHub Actions.
- `client_payload` can be used to pass custom data to the workflow.
- Different triggers can be combined to build event-driven CI/CD pipelines.

## Day 47 Summary

Today I explored **advanced GitHub Actions triggers** and understood how workflows can react to Pull Requests, schedules, file changes, other workflows, and external systems.

This helped me understand how GitHub Actions can be used to build more flexible and event-driven CI/CD pipelines.