# Day 41 – Triggers & Matrix Builds

## 🎯 Goal

Today I learned how to trigger GitHub Actions workflows using different events and how to use **matrix builds** to run the same job across multiple environments.

I worked with:

* Pull Request triggers
* Scheduled triggers
* Manual triggers
* Matrix builds
* Matrix exclusions
* `fail-fast`

---

#  Task 1: Trigger on Pull Request

Created:

```text
.github/workflows/pr-check.yml
```

### Workflow

```yaml
name: PR Check

on:
  pull_request:
    branches:
      - main
    types:
      - opened
      - synchronize

jobs:
  pr-check:
    runs-on: ubuntu-latest

    steps:
      - name: Print PR branch
        run: echo "PR check running for branch: ${{ github.head_ref }}"
```

### What it does

This workflow runs when:

* A pull request is opened against `main`
* New commits are pushed to the pull request branch

`github.head_ref` gives the name of the source branch of the pull request.

### Flow

```text
Create / Update PR
       ↓
Pull Request Event
       ↓
GitHub Actions
       ↓
pr-check Job
       ↓
Print Branch Name
```

### Result

Created a new branch, pushed a commit, and opened a pull request against `main`.

The workflow appeared and ran automatically on the pull request page.


---

#  Task 2: Scheduled Trigger

Created:

```text
.github/workflows/schedule.yml
```

### Workflow

```yaml
name: Scheduled Workflow

on:
  schedule:
    - cron: '0 0 * * *'

jobs:
  scheduled-job:
    runs-on: ubuntu-latest

    steps:
      - name: Print scheduled message
        run: echo "This workflow was triggered by a schedule."
```

The cron expression:

```text
0 0 * * *
```

means the workflow runs **every day at midnight UTC**.

### Cron Question

**What is the cron expression for every Monday at 9 AM?**

```text
0 9 * * 1
```

Explanation:

```text
┌─ Minute: 0
│ ┌─ Hour: 9
│ │ ┌─ Day of month: *
│ │ │ ┌─ Month: *
│ │ │ │ ┌─ Day of week: 1 (Monday)
│ │ │ │ │
0 9 * * 1
```

> Note: GitHub Actions schedules use UTC.


---

# ▶️ Task 3: Manual Trigger

Created:

```text
.github/workflows/manual.yml
```

### Workflow

```yaml
name: Manual Workflow

on:
  workflow_dispatch:
    inputs:
      environment:
        description: "Enter environment name"
        required: true
        default: "staging"

jobs:
  manual-job:
    runs-on: ubuntu-latest

    steps:
      - name: Print environment
        run: echo "Selected environment: ${{ inputs.environment }}"
```

### What it does

The `workflow_dispatch` trigger allows the workflow to be started manually from the GitHub Actions interface.

The workflow accepts an input:

```text
environment
```

For example:

```text
staging
```

or:

```text
production
```

The selected value is then printed by the workflow.


### Result

The workflow was manually triggered and printed the selected environment.


---

#  Task 4: Matrix Builds

Created:

```text
.github/workflows/matrix.yml
```

### Initial Matrix Workflow

```yaml
name: Matrix Build

on:
  push:

jobs:
  test:
    runs-on: ubuntu-latest

    strategy:
      matrix:
        python-version:
          - "3.10"
          - "3.11"
          - "3.12"

    steps:
      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}

      - name: Print Python version
        run: python --version
```

### What is a Matrix?

A matrix allows the same job to run with different combinations of configuration values.

Here we have:

```text
Python 3.10
Python 3.11
Python 3.12
```

So GitHub Actions creates **3 jobs**.

```text
              test
                │
       ┌────────┼────────┐
       ↓        ↓        ↓
    Python    Python    Python
      3.10      3.11      3.12
```

The jobs can run in parallel depending on runner availability.

---

#  Matrix with Multiple Operating Systems

Extended the matrix to include:

```text
ubuntu-latest
windows-latest
```

### Workflow

```yaml
name: Matrix Build

on:
  push:

jobs:
  test:
    strategy:
      fail-fast: false

      matrix:
        os:
          - ubuntu-latest
          - windows-latest

        python-version:
          - "3.10"
          - "3.11"
          - "3.12"

    runs-on: ${{ matrix.os }}

    steps:
      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}

      - name: Print Python version
        run: python --version

      - name: Print operating system
        run: echo "Running on ${{ matrix.os }}"
```

### How many jobs?

We have:

```text
2 operating systems × 3 Python versions
= 6 jobs
```

So GitHub Actions creates **6 jobs**.

```text
Ubuntu
 ├── Python 3.10
 ├── Python 3.11
 └── Python 3.12

Windows
 ├── Python 3.10
 ├── Python 3.11
 └── Python 3.12
```

---

#  Task 5: Exclude & Fail-Fast

## Exclude

Excluded this combination:

```text
Windows + Python 3.10
```

Updated the matrix:

```yaml
strategy:
  fail-fast: false

  matrix:
    os:
      - ubuntu-latest
      - windows-latest

    python-version:
      - "3.10"
      - "3.11"
      - "3.12"

    exclude:
      - os: windows-latest
        python-version: "3.10"
```

### Number of jobs

Originally:

```text
2 OS × 3 Python versions = 6 jobs
```

After excluding one combination:

```text
6 - 1 = 5 jobs
```

So the workflow now runs **5 jobs**.

---

##  Testing `fail-fast: false`

I intentionally added a failing step for one specific matrix combination:

```yaml
- name: Intentional failure
  if: matrix.os == 'ubuntu-latest' && matrix.python-version == '3.11'
  run: exit 1
```

The complete matrix section becomes:

```yaml
strategy:
  fail-fast: false

  matrix:
    os:
      - ubuntu-latest
      - windows-latest

    python-version:
      - "3.10"
      - "3.11"
      - "3.12"

    exclude:
      - os: windows-latest
        python-version: "3.10"
```

Only the Ubuntu + Python 3.11 combination is intentionally failed.

### What I observed

Even though one matrix job failed, the other matrix jobs continued running.

This is because:

```yaml
fail-fast: false
```

allows the remaining matrix jobs to continue.

---

## ⚡ `fail-fast: true` vs `false`

### `fail-fast: true`

This is the default.

If one matrix job fails, GitHub Actions cancels other **in-progress and queued** matrix jobs.

```text
Job 1 → ✅
Job 2 → ❌
Job 3 → Cancelled
Job 4 → Cancelled
```

### `fail-fast: false`

If one matrix job fails, the other matrix jobs continue running.

```text
Job 1 → ✅
Job 2 → ❌
Job 3 → ✅
Job 4 → ✅
```

GitHub documents `fail-fast` as applying to the entire matrix, with the default value being `true`.


---

#  What I Learned

* `pull_request` can trigger workflows when a PR is opened or updated.
* `schedule` allows workflows to run automatically using cron expressions.
* `workflow_dispatch` allows workflows to be triggered manually.
* Inputs can be passed to manually triggered workflows.
* Matrix builds allow the same job to run across multiple environments.
* `2 OS × 3 Python versions = 6 matrix jobs`.
* Using `exclude` removes unwanted combinations.
* `fail-fast: false` allows other matrix jobs to continue even when one fails.
* `fail-fast: true` cancels in-progress and queued matrix jobs when a matrix job fails.


---

#  Key Takeaway

Day 40 taught me how to create my first GitHub Actions workflow.

Day 41 took it further by learning **when workflows should run and how to test across multiple environments at the same time.**

With triggers and matrix builds, a single workflow can automatically respond to different events and validate an application across multiple configurations.
