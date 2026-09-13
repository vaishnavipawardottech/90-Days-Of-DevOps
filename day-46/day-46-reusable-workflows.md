# Day 46 — Reusable Workflows & Composite Actions

## Goal

Learn how to reuse GitHub Actions workflows and steps using:

- Reusable Workflows
- `workflow_call`
- Workflow inputs, secrets and outputs
- Composite Actions
- Difference between Reusable Workflows and Composite Actions

---

# Task 1: Understand Reusable Workflows

### Q1. What is a Reusable Workflow?

A reusable workflow is a GitHub Actions workflow that can be called and reused by another workflow instead of writing the same jobs and steps again.

---

### Q2. How do we make a workflow reusable?

We use:

    on:
      workflow_call:

This tells GitHub that the workflow can be called by another workflow.

---

### Q3. Where is a reusable workflow stored?

Reusable workflows are stored inside:

    .github/workflows/

---

### Q4. How do we call a reusable workflow from another workflow?

For a workflow in the same repository:

    jobs:
      build:
        uses: ./.github/workflows/reusable-build.yml

The calling workflow uses the reusable workflow as a job.

---

### Q5. What is the difference between a reusable workflow and a normal action?

A reusable workflow can contain complete jobs and multiple steps.

An action is normally used inside a job's step.

Reusable workflow:

    jobs:
      build:
        uses: ./.github/workflows/reusable-build.yml

Action:

    steps:
      - uses: actions/checkout@v4

---

# Task 2: Create a Reusable Build Workflow

Create:

    .github/workflows/reusable-build.yml

Add:

    name: Reusable Build

    on:
      workflow_call:
        inputs:
          app_name:
            description: "Application name"
            required: true
            type: string

          environment:
            description: "Deployment environment"
            required: true
            type: string
            default: staging

        secrets:
          docker_token:
            required: true

    jobs:
      build:
        runs-on: ubuntu-latest

        steps:
          - name: Checkout code
            uses: actions/checkout@v4

          - name: Print build information
            run: |
              echo "Building ${{ inputs.app_name }} for ${{ inputs.environment }}"

          - name: Check Docker token
            run: |
              if [ -n "${{ secrets.docker_token }}" ]; then
                echo "Docker token is set: true"
              else
                echo "Docker token is set: false"
              fi

### What we did

We created a reusable workflow that accepts:

- `app_name` — application name
- `environment` — target environment
- `docker_token` — Docker token passed by the calling workflow

The workflow checks whether the Docker token was received and reports `true` or `false`.

---

# Task 3: Create a Caller Workflow

Create:

    .github/workflows/call-build.yml

Add:

    name: Call Reusable Build

    on:
      push:
        branches:
          - main
      workflow_dispatch:

    jobs:
      build:
        uses: ./.github/workflows/reusable-build.yml

        with:
          app_name: "my-web-app"
          environment: "production"

        secrets:
          docker_token: ${{ secrets.DOCKER_TOKEN }}

### Flow

    call-build.yml
          |
          | uses
          v
    reusable-build.yml
          |
          +--> Checkout code
          |
          +--> Print build information
          |
          +--> Check Docker token

The caller provides the input values and secret to the reusable workflow.

---

# Task 4: Add Workflow Output

Now generate a build version inside the reusable workflow and pass it back to the caller.

Update:

    .github/workflows/reusable-build.yml

Use:

    name: Reusable Build

    on:
      workflow_call:
        inputs:
          app_name:
            description: "Application name"
            required: true
            type: string

          environment:
            description: "Deployment environment"
            required: true
            type: string
            default: staging

        secrets:
          docker_token:
            required: true

        outputs:
          build_version:
            description: "Generated build version"
            value: ${{ jobs.build.outputs.build_version }}

    jobs:
      build:
        runs-on: ubuntu-latest

        outputs:
          build_version: ${{ steps.version.outputs.build_version }}

        steps:
          - name: Checkout code
            uses: actions/checkout@v4

          - name: Print build information
            run: |
              echo "Building ${{ inputs.app_name }} for ${{ inputs.environment }}"

          - name: Check Docker token
            run: |
              if [ -n "${{ secrets.docker_token }}" ]; then
                echo "Docker token is set: true"
              else
                echo "Docker token is set: false"
              fi

          - name: Generate build version
            id: version
            run: |
              SHORT_SHA=${GITHUB_SHA::7}
              VERSION="v1.0-${SHORT_SHA}"

              echo "Build version: $VERSION"

              echo "build_version=$VERSION" >> "$GITHUB_OUTPUT"

## Understanding the Output Flow

The version is generated inside the `version` step:

    VERSION="v1.0-${SHORT_SHA}"

The step writes it to `$GITHUB_OUTPUT`:

    echo "build_version=$VERSION" >> "$GITHUB_OUTPUT"

Because the step has:

    id: version

we can access the value as:

    steps.version.outputs.build_version

The job then exposes that value:

    jobs.build.outputs.build_version

The reusable workflow exposes the job output:

    workflow_call.outputs.build_version

Finally, the caller can access it using:

    needs.build.outputs.build_version

because:

    show-version:
      needs: build

### Complete flow

    version step
         ↓
    steps.version.outputs.build_version
         ↓
    jobs.build.outputs.build_version
         ↓
    workflow_call.outputs.build_version
         ↓
    needs.build.outputs.build_version
         ↓
    show-version job

For example:

    Build version is: v1.0-abc1234

---

# Task 5: Create a Composite Action

A composite action allows us to combine multiple steps into one reusable custom action.

Create:

    .github/actions/setup-and-greet/action.yml

Add:

    name: Setup and Greet

    description: "Print a greeting, date and runner information"

    inputs:
      name:
        description: "Name to greet"
        required: true

      language:
        description: "Greeting language"
        required: false
        default: "en"

    outputs:
      greeted:
        description: "Whether the greeting was completed"
        value: ${{ steps.greet.outputs.greeted }}

    runs:
      using: "composite"

      steps:
        - name: Print greeting
          id: greet
          shell: bash
          run: |
            if [ "${{ inputs.language }}" = "en" ]; then
              echo "Hello, ${{ inputs.name }}!"
            elif [ "${{ inputs.language }}" = "hi" ]; then
              echo "Namaste, ${{ inputs.name }}!"
            elif [ "${{ inputs.language }}" = "fr" ]; then
              echo "Bonjour, ${{ inputs.name }}!"
            else
              echo "Hello, ${{ inputs.name }}!"
            fi

            echo "greeted=true" >> "$GITHUB_OUTPUT"

        - name: Print date and runner OS
          shell: bash
          run: |
            echo "Current date: $(date)"
            echo "Runner OS: $RUNNER_OS"

---

## Use the Composite Action

Create:

    .github/workflows/composite-action-test.yml

Add:

    name: Composite Action Test

    on:
      push:
        branches:
          - main
      workflow_dispatch:

    jobs:
      greet:
        runs-on: ubuntu-latest

        steps:
          - name: Checkout code
            uses: actions/checkout@v4

          - name: Run custom greeting action
            id: greeting
            uses: ./.github/actions/setup-and-greet
            with:
              name: "Vaishnavi"
              language: "en"

          - name: Check greeting output
            run: |
              echo "Greeting completed: ${{ steps.greeting.outputs.greeted }}"

The custom action runs multiple steps and returns the `greeted` output.

---

# Task 6: Reusable Workflow vs Composite Action

| Feature | Reusable Workflow | Composite Action |
|---|---|---|
| Trigger | `workflow_call` | Called using `uses:` |
| Location | `.github/workflows/` | `.github/actions/` |
| Contains jobs | Yes | No |
| Contains multiple steps | Yes | Yes |
| Can accept inputs | Yes | Yes |
| Main purpose | Reuse complete jobs/workflows | Reuse multiple steps |

### Simple way to remember

Reusable Workflow:

    Reuse complete jobs/workflows.

Composite Action:

    Reuse a group of steps.

---

# Files Created

    .github/
    ├── workflows/
    │   ├── reusable-build.yml
    │   ├── call-build.yml
    │   └── composite-action-test.yml
    │
    └── actions/
        └── setup-and-greet/
            └── action.yml

---

# Key Takeaway

Reusable Workflows help us reuse **complete jobs or workflows**, while Composite Actions help us reuse **multiple steps**.

This makes GitHub Actions workflows more modular, cleaner and easier to maintain.

---

# Repository

GitHub Actions Practice:

https://github.com/vaishnavipawardottech/github-actions-practice