# Day 37 – Docker Revision

## Goal

Revise and consolidate the Docker concepts covered from **Day 29–36** through quick notes, self-assessment, and quick-fire questions.

---

## Self-Assessment Revision

### 1. Running Containers

A container can be started interactively using `-it` or in the background using `-d`.

```bash
docker run -it ubuntu bash
docker run -d nginx
```

### 2. Managing Containers and Images

Use `docker ps` to view running containers and `docker ps -a` to view all containers. Containers can be stopped and removed using `docker stop` and `docker rm`. Images can be listed and removed using `docker images` and `docker rmi`.

### 3. Image Layers and Caching

Docker images are built in layers. Each Dockerfile instruction generally creates a layer. Docker reuses unchanged layers from previous builds, which makes subsequent builds faster.

### 4. Dockerfile Basics

A Dockerfile defines how an image is built.

Common instructions:

* `FROM` – defines the base image.
* `RUN` – executes commands while building the image.
* `COPY` – copies files from the build context into the image.
* `WORKDIR` – sets the working directory.
* `CMD` – defines the default command when the container starts.

### 5. CMD vs ENTRYPOINT

`CMD` provides the default command or arguments and can easily be overridden at runtime.

`ENTRYPOINT` defines the main executable of the container and is harder to override.

### 6. Building and Tagging Images

A custom image can be built and tagged using:

```bash
docker build -t myapp:latest .
```

The tag helps identify different versions of an image.

### 7. Named Volumes

Named volumes store persistent container data outside the container's writable layer.

```bash
docker volume create app-data
docker run -v app-data:/data myapp
```

### 8. Bind Mounts

A bind mount maps a specific host directory to a container directory.

```bash
docker run -v ./data:/app/data myapp
```

Useful when the host files need to be directly accessible or modified.

### 9. Docker Networks

Containers connected to the same custom Docker network can communicate using the **container/service name** instead of an IP address.

```bash
docker network create app-network
docker network connect app-network container1
```

### 10. Docker Compose

Docker Compose defines and manages multiple services using a `compose.yaml` or `docker-compose.yml` file.

```bash
docker compose up -d
docker compose down
```

It is useful for multi-container applications such as frontend + backend + database.

### 11. Environment Variables and `.env`

Environment variables can be passed to containers through Compose.

A `.env` file can store configuration values separately from the Compose file.

```yaml
environment:
  MONGO_URL: ${MONGO_URL}
```

### 12. Multi-Stage Docker Builds

Multi-stage builds use multiple stages such as `builder` and `runtime`. Build dependencies and source files can be left behind, while only the required runtime files are copied into the final image.

**Result:** smaller and cleaner production images.

### 13. Pushing Images to Docker Hub

An image is tagged with the Docker Hub repository name and then pushed.

```bash
docker tag myapp:latest username/myapp:latest
docker push username/myapp:latest
```

### 14. Healthchecks and `depends_on`

A healthcheck determines whether a container's service is healthy.

`depends_on` controls service startup order in Compose. With healthcheck conditions, a dependent service can wait for another service to become healthy before starting.

---

## Quick-Fire Questions

### 1. What is the difference between an image and a container?

An **image** is a read-only template used to create containers. A **container** is a running or stopped instance of an image.

---

### 2. What happens to data inside a container when you remove it?

Data stored only in the container's writable layer is removed with the container. Data stored in a **volume or bind mount persists**.

---

### 3. How do two containers on the same custom network communicate?

They communicate using the **container/service name as the hostname**.

Example:

```text
backend → mongodb:27017
```

---

### 4. What does `docker compose down -v` do differently from `docker compose down`?

`docker compose down` stops and removes Compose containers and networks.

`docker compose down -v` also removes the **named and anonymous volumes** created by the Compose project.

---

### 5. Why are multi-stage builds useful?

They separate the build environment from the runtime environment, allowing us to create **smaller, cleaner production images** without unnecessary build dependencies.

---

### 6. What is the difference between `COPY` and `ADD`?

`COPY` simply copies files/directories into the image.

`ADD` has additional features such as extracting local tar archives and handling URLs.

**Prefer `COPY` when those extra features are not required.**

---

### 7. What does `-p 8080:80` mean?

It maps:

```text
Host port 8080 → Container port 80
```

So the application running on port `80` inside the container is accessible through port `8080` on the host.

---

### 8. How do you check how much disk space Docker is using?

```bash
docker system df
```

It shows disk usage by images, containers, local volumes, and build cache.

---
