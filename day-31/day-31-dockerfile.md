# Day 31 – Dockerfile: Build Your Own Images

## Objective

Today's goal is to learn how to write Dockerfiles and build custom Docker images.

In this task, I will learn:

* How to create a Dockerfile
* How to build a custom Docker image
* How Dockerfile instructions work
* Difference between `CMD` and `ENTRYPOINT`
* How to build a simple web application image
* How `.dockerignore` works
* How Docker build cache works
* Why Dockerfile layer order matters

---

# What is a Dockerfile?

A Dockerfile is a text file containing instructions that Docker uses to build an image.

Example:

```dockerfile
FROM ubuntu

RUN apt-get update && apt-get install -y curl

CMD ["echo", "Hello from my custom image!"]
```

Docker reads these instructions from top to bottom and creates image layers.

The basic process is:

```text
Dockerfile
    |
    v
docker build
    |
    v
Docker Image
    |
    v
docker run
    |
    v
Container
```

---

# Task 1: Your First Dockerfile

## Step 1: Create the project folder

```bash
mkdir my-first-image
cd my-first-image
```

---

## Step 2: Create the Dockerfile

Create a file named exactly:

```text
Dockerfile
```

Dockerfile contents:

```dockerfile
FROM ubuntu

RUN apt-get update && apt-get install -y curl

CMD ["echo", "Hello from my custom image!"]
```

---

## Understanding the Dockerfile

### FROM

```dockerfile
FROM ubuntu
```

`FROM` specifies the base image.

Here, Ubuntu is used as the base image.

---

### RUN

```dockerfile
RUN apt-get update && apt-get install -y curl
```

`RUN` executes commands while the image is being built.

Here it:

1. Updates Ubuntu package information.
2. Installs `curl`.

---

### CMD

```dockerfile
CMD ["echo", "Hello from my custom image!"]
```

`CMD` specifies the default command that runs when a container starts.

---

## Step 3: Build the image

From inside the `my-first-image` directory:

```bash
docker build -t my-ubuntu:v1 .
```

Explanation:

```text
docker build
```

Builds an image.

```text
-t my-ubuntu:v1
```

Assigns the image name and tag.

```text
.
```

Specifies the current directory as the build context.

---

## Step 4: Verify the image

```bash
docker images
```

Look for:

```text
my-ubuntu
```

with the tag:

```text
v1
```

---

## Step 5: Run the container

```bash
docker run --rm my-ubuntu:v1
```

Expected output:

```text
Hello from my custom image!
```

The `--rm` option automatically removes the container after it exits.

---

## Task 1 Result

The custom Ubuntu image was successfully created with `curl` installed, and the default command printed:

```text
Hello from my custom image!
```

---

# Task 2: Dockerfile Instructions

The main Dockerfile instructions required for this task are:

* `FROM`
* `RUN`
* `COPY`
* `WORKDIR`
* `EXPOSE`
* `CMD`

---

## Step 1: Create a new project

Go back to the parent directory:

```bash
cd ..
```

Create a new directory:

```bash
mkdir dockerfile-instructions
cd dockerfile-instructions
```

---

## Step 2: Create a file to copy

Create:

```text
message.txt
```

Add some text:

```text
Hello from the Docker image!
```

---

## Step 3: Create Dockerfile

Create a file named:

```text
Dockerfile
```

Use:

```dockerfile
FROM ubuntu

RUN apt-get update && apt-get install -y curl

WORKDIR /app

COPY message.txt .

EXPOSE 8080

CMD ["cat", "message.txt"]
```

---

## Understanding Each Instruction

### FROM

```dockerfile
FROM ubuntu
```

Specifies the base image.

---

### RUN

```dockerfile
RUN apt-get update && apt-get install -y curl
```

Runs commands during image build.

This installs `curl` inside the image.

---

### WORKDIR

```dockerfile
WORKDIR /app
```

Sets `/app` as the working directory.

Following instructions operate relative to this directory.

---

### COPY

```dockerfile
COPY message.txt .
```

Copies `message.txt` from the build context on the host into the working directory inside the image.

The final location is:

```text
/app/message.txt
```

---

### EXPOSE

```dockerfile
EXPOSE 8080
```

Documents that the application in the image is intended to use port `8080`.

Important:

`EXPOSE` does not publish the port to the host.

Port publishing is done using `docker run -p`.

---

### CMD

```dockerfile
CMD ["cat", "message.txt"]
```

Defines the default command that runs when the container starts.

---

## Step 4: Build the image

```bash
docker build -t dockerfile-demo:v1 .
```

---

## Step 5: Run the image

```bash
docker run --rm dockerfile-demo:v1
```

Expected output:

```text
Hello from the Docker image!
```

---

# Task 3: CMD vs ENTRYPOINT

## CMD

`CMD` defines a default command.

Create a directory:

```bash
mkdir cmd-demo
cd cmd-demo
```

Create a Dockerfile:

```dockerfile
FROM ubuntu

CMD ["echo", "hello"]
```

Build:

```bash
docker build -t cmd-demo:v1 .
```

Run normally:

```bash
docker run --rm cmd-demo:v1
```

Output:

```text
hello
```

---

## Override CMD

Now run:

```bash
docker run --rm cmd-demo:v1 echo "custom command"
```

Output:

```text
custom command
```

The command supplied during `docker run` replaces the `CMD`.

Therefore:

```text
CMD = Default command
```

It can be overridden.

---

# ENTRYPOINT

Go back:

```bash
cd ..
```

Create:

```bash
mkdir entrypoint-demo
cd entrypoint-demo
```

Create a Dockerfile:

```dockerfile
FROM ubuntu

ENTRYPOINT ["echo"]
```

Build:

```bash
docker build -t entrypoint-demo:v1 .
```

Run without arguments:

```bash
docker run --rm entrypoint-demo:v1
```

Run with an argument:

```bash
docker run --rm entrypoint-demo:v1 "Hello Docker"
```

Expected output:

```text
Hello Docker
```

Another example:

```bash
docker run --rm entrypoint-demo:v1 "This is an argument"
```

Output:

```text
This is an argument
```

With `ENTRYPOINT`, the arguments supplied after the image name are passed to the entrypoint.

---

## CMD vs ENTRYPOINT

### CMD

```dockerfile
CMD ["echo", "hello"]
```

Provides a default command that can be replaced.

Example:

```bash
docker run --rm image-name echo "custom"
```

---

### ENTRYPOINT

```dockerfile
ENTRYPOINT ["echo"]
```

Defines the main executable.

Arguments can be supplied to it:

```bash
docker run --rm image-name "Hello Docker"
```

Conceptually:

```text
CMD

docker run image
        |
        v
default command

docker run image custom-command
        |
        v
custom-command replaces CMD
```

```text
ENTRYPOINT

docker run image argument
        |
        v
ENTRYPOINT + argument
```

---

## When to use CMD vs ENTRYPOINT?

Use `CMD` when you want to provide a default command that users can easily override.

Use `ENTRYPOINT` when the container should behave like a specific executable and additional arguments should be passed to it.

They can also be used together:

```dockerfile
ENTRYPOINT ["echo"]
CMD ["Hello Docker"]
```

Then:

```bash
docker run --rm image-name
```

uses:

```text
echo Hello Docker
```

while:

```bash
docker run --rm image-name "Custom message"
```

uses:

```text
echo Custom message
```

---

# Task 4: Build a Simple Web App Image

## Step 1: Create project directory

Go back:

```bash
cd ..
```

Create:

```bash
mkdir my-website
cd my-website
```

---

## Step 2: Create index.html

Create:

```text
index.html
```

Example content:

```html
<!DOCTYPE html>
<html>
<head>
    <title>My Docker Website</title>
</head>
<body>
    <h1>Hello from my Docker container!</h1>
    <p>This website is running using Nginx and Docker.</p>
</body>
</html>
```

---

## Step 3: Create Dockerfile

Create:

```text
Dockerfile
```

Add:

```dockerfile
FROM nginx:alpine

COPY index.html /usr/share/nginx/html/index.html
```

---

## Understanding the Dockerfile

### FROM

```dockerfile
FROM nginx:alpine
```

Uses the lightweight Alpine-based Nginx image.

### COPY

```dockerfile
COPY index.html /usr/share/nginx/html/index.html
```

Copies the local `index.html` into the directory from which Nginx serves web content.

Nginx serves files from:

```text
/usr/share/nginx/html/
```

---

## Step 4: Build the image

```bash
docker build -t my-website:v1 .
```

---

## Step 5: Verify

```bash
docker images
```

Look for:

```text
my-website
```

with:

```text
v1
```

---

## Step 6: Run the container

```bash
docker run -d --name my-website-container -p 8080:80 my-website:v1
```

Check:

```bash
docker ps
```

---

## Step 7: Open the website

Open in your browser:

```text
http://localhost:8080
```

You should see:

```text
Hello from my Docker container!
```

---

# Task 5: .dockerignore

## What is .dockerignore?

`.dockerignore` tells Docker which files and directories should not be included in the build context sent to the Docker daemon.

This can:

* Reduce build context size
* Improve build performance
* Prevent unnecessary files from being copied
* Help avoid accidentally including sensitive files

---

## Step 1: Create .dockerignore

Inside a project directory, create:

```text
.dockerignore
```

Add:

```text
node_modules
.git
*.md
.env
```

This tells Docker to ignore:

```text
node_modules
.git
all .md files
.env
```

---

## Example

Project:

```text
my-project/
├── Dockerfile
├── index.html
├── README.md
├── notes.md
├── .env
├── .git/
└── node_modules/
```

With:

```text
.dockerignore
```

containing:

```text
node_modules
.git
*.md
.env
```

Docker will exclude those paths from the build context.

---

## Important Note

`.dockerignore` prevents files from being sent as part of the build context.

It does not remove files that are already present in a base image.

It also does not automatically remove a file from an image if the Dockerfile creates or downloads that file during the build.

---

## Verify .dockerignore

A simple way to verify is to use a Dockerfile that copies the build context:

```dockerfile
FROM ubuntu

WORKDIR /app

COPY . .
```

Build:

```bash
docker build -t dockerignore-demo:v1 .
```

Run:

```bash
docker run --rm -it dockerignore-demo:v1 /bin/bash
```

Inside the container:

```bash
ls -la
```

Files/directories listed in `.dockerignore` should not be present if they were only coming from the build context.

Exit:

```bash
exit
```

---

# Task 6: Build Optimization

Docker uses build cache to avoid rebuilding unchanged layers.

---

## Step 1: Create a Dockerfile

Example:

```dockerfile
FROM ubuntu

RUN apt-get update && apt-get install -y curl

WORKDIR /app

COPY message.txt .

CMD ["cat", "message.txt"]
```

Build:

```bash
docker build -t cache-demo:v1 .
```

During the build, Docker may show:

```text
CACHED
```

for steps that can reuse previously built layers.

---

## Step 2: Change a frequently changing file

Change the contents of:

```text
message.txt
```

For example:

```text
Hello from the updated Docker image!
```

Build again:

```bash
docker build -t cache-demo:v2 .
```

Docker can reuse unchanged earlier layers and rebuild the layer affected by the changed file and subsequent layers.

---

## Why Does Layer Order Matter?

Dockerfile instructions create layers.

When a layer changes, Docker may need to rebuild that layer and the layers that come after it.

Therefore, frequently changing instructions should generally be placed later in the Dockerfile.

---

## Bad Example

```dockerfile
FROM ubuntu

COPY . .

RUN apt-get update && apt-get install -y curl

CMD ["echo", "Hello"]
```

If application files change, the `COPY` layer changes, potentially causing later layers to be rebuilt.

---

## Better Example

```dockerfile
FROM ubuntu

RUN apt-get update && apt-get install -y curl

WORKDIR /app

COPY . .

CMD ["echo", "Hello"]
```

The dependency installation layer can remain cached when only application files change.

---

## General Optimization Principle

```text
Less frequently changing instructions
                ↓
More frequently changing instructions
```

For example:

```text
FROM
RUN dependencies
WORKDIR
COPY dependency files
RUN install dependencies
COPY application code
CMD
```

The exact best order depends on the application and its build process.

---

# Useful Docker Build Commands

## Build an image

```bash
docker build -t image-name:tag .
```

## Build without cache

```bash
docker build --no-cache -t image-name:tag .
```

## List images

```bash
docker images
```

## Run an image

```bash
docker run image-name:tag
```

## Run in detached mode

```bash
docker run -d image-name:tag
```

## Build and tag

```bash
docker build -t my-app:v1 .
```

---

# Dockerfile Instructions Summary

| Instruction     | Purpose                                       |
| --------------- | --------------------------------------------- |
| `FROM`          | Specifies the base image                      |
| `RUN`           | Executes commands during image build          |
| `COPY`          | Copies files from build context into image    |
| `ADD`           | Copies files and supports additional features |
| `WORKDIR`       | Sets the working directory                    |
| `EXPOSE`        | Documents the intended container port         |
| `CMD`           | Provides the default command                  |
| `ENTRYPOINT`    | Defines the main executable                   |
| `.dockerignore` | Excludes files from the build context         |

---

# Dockerfile vs Docker Image vs Container

```text
Dockerfile
    |
    | docker build
    v
Docker Image
    |
    | docker run
    v
Docker Container
```

### Dockerfile

Instructions for creating an image.

### Docker Image

Packaged, reusable application environment.

### Docker Container

Running instance of an image.

---

# Important Concepts Learned

## 1. Dockerfile

A Dockerfile contains instructions used to build a Docker image.

## 2. Base Image

`FROM` defines the starting point of an image.

## 3. Build-Time Commands

`RUN` executes commands while building the image.

## 4. Copying Files

`COPY` transfers files from the build context into the image.

## 5. Working Directory

`WORKDIR` defines the directory in which subsequent commands operate.

## 6. Port Documentation

`EXPOSE` documents the port an application listens on.

It does not publish the port.

## 7. Default Command

`CMD` defines the default command executed when the container starts.

## 8. Entry Point

`ENTRYPOINT` defines the main executable for the container.

## 9. .dockerignore

`.dockerignore` prevents unnecessary files from being sent in the build context.

## 10. Build Cache

Docker reuses unchanged build layers whenever possible.

## 11. Layer Ordering

Frequently changing instructions should generally be placed later so that earlier layers can remain cached.

---

# Final Dockerfile Examples

## Custom Ubuntu Image

```dockerfile
FROM ubuntu

RUN apt-get update && apt-get install -y curl

CMD ["echo", "Hello from my custom image!"]
```

---

## Dockerfile Instructions Example

```dockerfile
FROM ubuntu

RUN apt-get update && apt-get install -y curl

WORKDIR /app

COPY message.txt .

EXPOSE 8080

CMD ["cat", "message.txt"]
```

---

## CMD Example

```dockerfile
FROM ubuntu

CMD ["echo", "hello"]
```

---

## ENTRYPOINT Example

```dockerfile
FROM ubuntu

ENTRYPOINT ["echo"]
```

---

## Nginx Website Example

```dockerfile
FROM nginx:alpine

COPY index.html /usr/share/nginx/html/index.html
```

---

# Final Summary

Today I learned how to create custom Docker images using Dockerfiles.

The main workflow is:

```text
Write Dockerfile
       ↓
docker build
       ↓
Docker Image
       ↓
docker run
       ↓
Container
```

I learned:

* How to create a Dockerfile
* How `FROM`, `RUN`, `COPY`, `WORKDIR`, `EXPOSE`, and `CMD` work
* Difference between `CMD` and `ENTRYPOINT`
* How to create an Nginx-based website image
* How `.dockerignore` works
* How Docker build cache works
* Why Dockerfile layer ordering affects build speed

The most important commands from today are:

```bash
docker build -t my-image:v1 .
docker images
docker run --rm my-image:v1
docker run -d --name my-container -p 8080:80 my-image:v1
docker ps
docker logs my-container
docker exec -it my-container /bin/sh
docker stop my-container
docker rm my-container
```

The key concept is:

```text
Dockerfile = Instructions

Image = Built package

Container = Running instance
```

# End of Day 31
