# Day 35 – Multi-Stage Builds & Docker Hub

## Objective

Learn how to build smaller and more secure Docker images using multi-stage builds and distribute images using Docker Hub.

The practice uses a simple Node.js application cloned from the GitHub repository.

---

## Task 1: Single-Stage Build

A single-stage Dockerfile contains both the application build process and runtime environment in the same image.

### Key points

* Uses a full Node.js base image.
* Installs application dependencies.
* Copies the application into the image.
* Runs the application directly.

### Image

**Image name:** `simple-nodejs-app`

**Image size:** `410 MB`

### Observation

The image contains everything included during the build process, even if some of those files or tools are not required when the application is running.

---

## Task 2: Multi-Stage Build

A multi-stage Dockerfile separates the build environment from the final runtime image.

### Stages

**Builder stage**

Used for:

* Installing dependencies
* Preparing application files

**Runtime stage**

Contains only the files required to run the application.

### Image

**Image name:** `simple-nodejs-multistage`

**Image size:** `58.4 MB`

### Why Multi-Stage Builds?

Multi-stage builds can reduce image size because build-time files, tools, caches, and unnecessary dependencies do not need to be included in the final runtime image.

They also provide a cleaner separation between the build environment and the production runtime.

> For a very small Node.js application, the size difference may be limited. The benefit becomes much larger for applications that require compilers, SDKs, development tools, or large build dependencies.

---

## Image Size Comparison

| Image        | Base Image     |     Size |
| ------------ | -------------- | -------: |
| Single-stage | Node.js        | `410 MB` |
| Multi-stage  | Node.js Alpine | `58.4 MB` |
| Optimized    | Node.js Alpine | `58.4 MB` |

---

## Task 3: Docker Hub

The multi-stage image was tagged and pushed to Docker Hub.

### Repository

`pawarvaishnavi/simple-nodejs-app`

### Tags

* `1.0`
* `latest`

### Verification

The image was pulled again from Docker Hub and started successfully.

The application endpoint was tested after pulling the image to verify that the published image works independently of the original local image.

---

## Task 4: Docker Hub Tags

Docker image tags allow different versions of an image to be identified.

For example:

```text
simple-nodejs-app:1.0
simple-nodejs-app:latest
```

A specific version tag such as `1.0` identifies a particular release.

The `latest` tag is another tag that can point to an image. It does not automatically guarantee that the image is the newest version.

Using explicit version tags is useful for reproducible deployments.

---

## Task 5: Image Best Practices

The final image applies the following practices:

### 1. Minimal Base Image

Used:

```text
node:22-alpine
```

Alpine provides a smaller base image than a general-purpose Ubuntu image.

### 2. Non-Root User

The final image uses:

```dockerfile
USER node
```

Running the application as a non-root user reduces the privileges available to the application inside the container.

### 3. Multi-Stage Build

The build and runtime environments are separated so that unnecessary build-time content does not become part of the final image.

### 4. Specific Base Image Tag

Used:

```text
node:22-alpine
```

instead of:

```text
node:latest
```

Specific tags make the base image version explicit and provide more predictable builds.

### 5. Production Dependencies

The final build installs only the dependencies required to run the application.

---

## Final Observations

* Single-stage images can contain unnecessary build-time content.
* Multi-stage builds separate build requirements from runtime requirements.
* Minimal base images reduce the amount of software included in the final image.
* Running containers as non-root improves security.
* Specific image tags make builds more predictable.
* Docker Hub provides a registry for sharing and distributing container images.
* Version tags make it possible to publish and pull specific image versions.
* `latest` is a tag, not a guarantee that an image represents the newest release.