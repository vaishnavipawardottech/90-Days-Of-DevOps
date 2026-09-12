# Day 45 — Docker Build & Push in GitHub Actions

## Goal

Automate Docker image building and publishing using GitHub Actions.

### Expected Outcome

- Build Docker image automatically through GitHub Actions
- Push Docker image to Docker Hub
- Use `latest` and commit SHA based tags
- Push images only from the `main` branch
- Add GitHub Actions status badge to README
- Pull and run the published image locally

---

# Task 1 — Prepare Dockerized Application

For this task, I used the simple Python application from the previous GitHub Actions practice.

### Project Files

- `app.py`
- `requirements.txt`
- `Dockerfile`
- `test.py`

### Dockerfile

    FROM python:3.13-slim

    WORKDIR /app

    COPY . .

    RUN pip install --no-cache-dir -r requirements.txt

    EXPOSE 80

    CMD ["gunicorn", "--bind", "0.0.0.0:80", "app:app"]

The Dockerfile:

- Uses Python 3.13 slim image
- Creates `/app` as the working directory
- Copies application files
- Installs Python dependencies
- Exposes port `80`
- Runs the Flask application using Gunicorn

---

# Task 2 — Build Docker Image in GitHub Actions

Created:

    .github/workflows/docker-publish.yml

The workflow uses:

- `actions/checkout@v4`
- `docker/setup-docker-action@v5`
- `docker/login-action@v4`
- `docker/build-push-action@v7`

The workflow checks out the repository and builds the Docker image automatically when changes are pushed.

### Main Concepts

- GitHub Actions workflow
- Docker image build
- Docker Hub authentication
- GitHub Actions runners
- Docker build automation

---

# Task 3 — Push Docker Image to Docker Hub

Configured Docker Hub credentials using GitHub:

- Repository Variable: `DOCKER_USERNAME`
- Repository Secret: `DOCKER_TOKEN`

The Docker login step uses:

    username: ${{ vars.DOCKER_USERNAME }}
    password: ${{ secrets.DOCKER_TOKEN }}

The image is tagged as:

    pawarvaishnavi/github-actions-practice-ecommerce:latest

and also with a commit-based tag:

    pawarvaishnavi/github-actions-practice-ecommerce:sha-<commit-sha>

### Why use a SHA tag?

The `latest` tag always points to the most recent image.

The SHA tag identifies the image created from a specific Git commit.

Example:

    latest
    sha-a8f42c9

This makes it possible to identify and pull a specific version of the application.

For example:

    docker pull pawarvaishnavi/github-actions-practice-ecommerce:sha-a8f42c9

---

# Docker Image Naming Issue

Initially, I used:

    github-actions-practice(e-commerce)

This caused:

    invalid reference format

because parentheses are not valid characters in Docker image repository names.

Changed the repository name to:

    github-actions-practice-ecommerce

Docker image repository names should use valid lowercase characters and supported separators such as `-`.

---

# Task 4 — Push Only from Main Branch

The requirement was:

- Feature branch → Build Docker image but do not push
- Main branch → Build and push Docker image

the workflow was configured as:

    on:
      push:
        branches:
          - main

This meant workflows would not run at all for feature branches.

we can do like:
To test the build on feature branches, the trigger was changed to:

    on:
      push:
      workflow_dispatch:

Then the Docker push step was restricted using:

    if: github.ref == 'refs/heads/main'

### Workflow Logic

    Feature branch
          |
          v
    Build Docker image
          |
          v
    Push step skipped

    Main branch
          |
          v
    Build Docker image
          |
          v
    Push Docker image

This demonstrated how GitHub Actions conditions can control individual workflow steps.

### Feature Branch Test

Created a feature branch:

    git checkout -b feature-test

Pushed the changes:

    git add .
    git commit -m "test docker feature branch"
    git push -u origin feature-test

The workflow ran and built the Docker image, but the Docker push step was skipped.

### Main Branch Test

After switching back to main:

    git checkout main
    git push origin main

The workflow built and pushed the Docker images.

---

# Task 5 — GitHub Actions Status Badge

Added a GitHub Actions status badge to `README.md`.

The badge shows whether the Docker Publish workflow is passing or failing.

The badge can also be clicked to open the Docker Publish workflow.

### Purpose

The badge provides a quick visual indication of the CI/CD workflow status directly in the repository README.

---

# Task 6 — Pull and Run Docker Image Locally

After successfully publishing the image to Docker Hub, I tested the published image locally.

### Pull Image

    docker pull pawarvaishnavi/github-actions-practice-ecommerce:latest

### Run Container

    docker run -d -p 8080:80 pawarvaishnavi/github-actions-practice-ecommerce:latest

The application can then be accessed at:

    http://localhost:8080

### Check Running Container

    docker ps

### Enter Running Container

    docker exec -it <container-id> sh

Inside the container:

    ls
    ls /app

Since the application files are copied into `/app`, the application code and related files can be inspected from there.

---

# Docker Image Tags

The final image can have multiple tags pointing to the same build.

Example:

    pawarvaishnavi/github-actions-practice-ecommerce:latest

    pawarvaishnavi/github-actions-practice-ecommerce:sha-a8f42c9

### `latest`

Points to the latest successfully published image.

### `sha-<commit>`

Identifies the image created from a specific Git commit.

This is useful for version tracking and rollback.

---

# Complete CI/CD Flow

The complete workflow now looks like:

    Developer pushes code
            |
            v
    GitHub Actions starts
            |
            v
    Checkout repository
            |
            v
    Build Docker image
            |
            v
    Tag Docker image
            |
            +----------------------+
            |                      |
            v                      v
       Feature branch           Main branch
            |                      |
            v                      v
       Build only           Build + Push
                                   |
                                   v
                              Docker Hub
                                   |
                                   v
                         Pull image locally
                                   |
                                   v
                            Run container
                                   |
                                   v
                           Access application

---

# Important Concepts Learned

## 1. Docker Image Build in CI

GitHub Actions can automatically build Docker images whenever code changes are pushed.

## 2. Docker Hub Authentication

Sensitive Docker Hub credentials should be stored using GitHub Secrets/Variables instead of writing them directly in the workflow.

## 3. Docker Image Tags

Multiple tags can be used for the same Docker image.

    latest
    sha-<commit>

## 4. Commit SHA Tagging

A commit-based tag helps identify exactly which Git version produced a Docker image.

## 5. Conditional Steps

GitHub Actions supports conditions such as:

    if: github.ref == 'refs/heads/main'

This allows specific steps to run only under certain conditions.

## 6. CI/CD Automation

The complete process can be automated:

    Git Push
       ↓
    GitHub Actions
       ↓
    Docker Build
       ↓
    Docker Push
       ↓
    Docker Hub
       ↓
    Docker Pull
       ↓
    Running Container

## 7. Status Badges

GitHub Actions badges provide a quick view of workflow status directly from the repository README.

---

# Files Created / Updated

    .github/
    └── workflows/
        └── docker-publish.yml

    Dockerfile
    README.md
    app.py
    requirements.txt
    test.py

---


# Key Takeaways

- GitHub Actions can automate Docker image builds and publishing.
- Docker Hub credentials should be stored securely using GitHub Secrets and Variables.
- `latest` is useful for the newest image, while SHA tags provide version-specific images.
- Docker image names must follow Docker's image reference format.
- GitHub Actions `if` conditions can control when individual steps execute.
- A workflow can build images on feature branches while allowing publishing only from `main`.
- Docker images published through CI/CD can be pulled and run on local machines or servers.

---

# Repository

GitHub Repository:

https://github.com/vaishnavipawardottech/github-actions-practice

Docker workflow:

.github/workflows/docker-publish.yml

---

# Day 45 Summary

Today I automated the Docker image build and publishing process using GitHub Actions.

I learned how to authenticate with Docker Hub, build Docker images in CI, create `latest` and commit-based tags, restrict Docker pushes to the `main` branch, add a workflow status badge, and finally pull and run the published image locally.

This completed the flow from:

    Git Push → GitHub Actions → Docker Build → Docker Hub → Docker Pull → Running Container