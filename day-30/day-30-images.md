# Day 30 – Docker Images & Container Lifecycle

## Objective

Today's goal is to understand how Docker images and containers work and how a container moves through its complete lifecycle.

### What I will learn

* Relationship between Docker images and containers
* Docker image layers and caching
* Docker image commands
* Complete container lifecycle
* Working with running containers
* Docker cleanup and disk usage

---

# 1. Docker Images

## What is a Docker Image?

A Docker image is a read-only template used to create containers.

An image contains:

* Application code
* Required dependencies
* Libraries
* Configuration
* Filesystem layers
* Metadata

For example, the `nginx` image contains everything required to run an Nginx web server.

## What is a Docker Container?

A container is a running or stopped instance of a Docker image.

The relationship can be understood as:

```text
Docker Image
     |
     | docker create / docker run
     v
Docker Container
```

One image can be used to create multiple containers.

```text
             Docker Image
                  |
       +----------+----------+
       |          |          |
       v          v          v
 Container 1  Container 2  Container 3
```

---

## Task 1: Pull Docker Images

Pull the required images from Docker Hub.

### Pull Nginx

```bash
docker pull nginx
```

### Pull Ubuntu

```bash
docker pull ubuntu
```

### Pull Alpine

```bash
docker pull alpine
```

### Verify the downloaded images

```bash
docker images
```

or:

```bash
docker image ls
```

### Expected Output

The output should contain images similar to:

```text
REPOSITORY   TAG       IMAGE ID       CREATED       SIZE
nginx        latest    ...            ...           ...
ubuntu       latest    ...            ...           ...
alpine       latest    ...            ...           ...
```

---

## Compare Ubuntu vs Alpine

Ubuntu and Alpine are both Linux-based images, but Alpine is much smaller.

### Ubuntu

Ubuntu is a general-purpose Linux distribution with many packages and utilities included.

### Alpine

Alpine Linux is designed to be small, lightweight, and security-focused.

It uses:

* `musl` libc
* BusyBox
* A minimal userspace

Because Alpine contains fewer packages and utilities, its Docker image is much smaller than Ubuntu.

### Check image sizes

```bash
docker images ubuntu
docker images alpine
```

The exact sizes can change depending on the image version.

### Why is Alpine smaller?

```text
Ubuntu
- More packages
- More utilities
- Larger userspace
- Larger image

Alpine
- Minimal packages
- Minimal utilities
- Small userspace
- Much smaller image
```

### Important Point

A smaller image can mean:

* Faster downloads
* Faster deployments
* Less storage usage
* Smaller attack surface

However, smaller does not automatically mean better. The image should contain everything required by the application.

---

# Inspect a Docker Image

Use `docker image inspect` to view detailed information about an image.

```bash
docker image inspect nginx
```

You can see information such as:

* Image ID
* Repository tags
* Image creation information
* Architecture
* Operating system
* Environment variables
* Entrypoint
* Default command
* Exposed ports
* Root filesystem information
* Image layers

For example:

```bash
docker image inspect nginx
```

---

# Remove an Image

First check the available images:

```bash
docker images
```

Remove an image that is no longer required:

```bash
docker rmi alpine
```

You can also use:

```bash
docker image rm alpine
```

Verify:

```bash
docker images
```

### Important

If an image is being used by a container, Docker may not allow it to be removed until the container is removed.

---

# 2. Docker Image Layers

Docker images are built using multiple layers.

Each instruction that changes the filesystem during an image build can create a layer.

For example:

```dockerfile
FROM ubuntu
RUN apt-get update
RUN apt-get install -y nginx
COPY index.html /var/www/html/
```

---

## View Image History

Run:

```bash
docker image history nginx
```

You can also use:

```bash
docker history nginx
```

The output shows the history of the image and information such as:

* Image layers
* Commands used to create layers
* Layer sizes
* Creation information

Example:

```text
IMAGE        CREATED       CREATED BY                         SIZE
...          ...           CMD ["nginx" "-g" "daemon off;"]   0B
...          ...           EXPOSE map[80/tcp:{}]              0B
...          ...           COPY ...                            ...
...          ...           RUN ...                             ...
```

---

## Why do some layers show 0B?

Some Dockerfile instructions create image metadata rather than adding files to the filesystem.

Examples include:

```dockerfile
CMD
EXPOSE
ENTRYPOINT
```

These can appear as `0B` in image history.

A `0B` entry does not necessarily mean the instruction is useless. It can still define important container behavior.

---

## Why Does Docker Use Layers?

Layers provide several advantages.

### 1. Reusability

Common layers can be shared between images.

### 2. Caching

Docker can reuse unchanged layers during image builds.

### 3. Faster Builds

If a layer has not changed, Docker can reuse it instead of rebuilding it.

### 4. Less Storage

Shared layers do not need to be stored multiple times.

### Example

Suppose two images use the same Ubuntu base:

```text
Image A
   |
Application Layer A
   |
Ubuntu Layer
```

```text
Image B
   |
Application Layer B
   |
Ubuntu Layer
```

The same Ubuntu layer can be shared.

---

# 3. Docker Container Lifecycle

A Docker container can move through different states during its lifecycle.

A simplified lifecycle is:

```text
Created
   |
   v
Running
   |
   +----> Paused
   |         |
   |         v
   |      Running
   |
   v
Stopped
   |
   v
Removed
```

A container can also be killed:

```text
Running
   |
   v
Killed
   |
   v
Stopped
```

---

# Task 3: Practice the Full Container Lifecycle

Use one container for the lifecycle practice.

We will create an Nginx container named:

```text
lifecycle-demo
```

---

## Step 1: Create a Container Without Starting It

Run:

```bash
docker create --name lifecycle-demo nginx
```

Check the container:

```bash
docker ps -a
```

The container should show a status similar to:

```text
Created
```

### Important

`docker create` creates the container but does not start it.

---

## Step 2: Start the Container

Run:

```bash
docker start lifecycle-demo
```

Check:

```bash
docker ps -a
```

You can also check only running containers:

```bash
docker ps
```

---

## Step 3: Pause the Container

Run:

```bash
docker pause lifecycle-demo
```

Check:

```bash
docker ps -a
```

A paused container is still running from Docker's perspective, but its processes are temporarily frozen.

---

## Step 4: Unpause the Container

Run:

```bash
docker unpause lifecycle-demo
```

Check:

```bash
docker ps -a
```

---

## Step 5: Stop the Container

Run:

```bash
docker stop lifecycle-demo
```

Check:

```bash
docker ps -a
```

The status should show something similar to:

```text
Exited (0)
```

---

## Step 6: Restart the Container

Run:

```bash
docker start lifecycle-demo
```

Then:

```bash
docker restart lifecycle-demo
```

Check:

```bash
docker ps -a
```

The container should be running again.

---

## Step 7: Kill the Container

First make sure the container is running:

```bash
docker start lifecycle-demo
```

Then:

```bash
docker kill lifecycle-demo
```

Check:

```bash
docker ps -a
```

The container should show an exited state.

### Difference Between Stop and Kill

`docker stop` attempts a graceful shutdown.

```bash
docker stop lifecycle-demo
```

`docker kill` immediately sends a kill signal to the container's main process.

```bash
docker kill lifecycle-demo
```

---

## Step 8: Remove the Container

Run:

```bash
docker rm lifecycle-demo
```

Verify:

```bash
docker ps -a
```

The `lifecycle-demo` container should no longer appear.

---

## Lifecycle Summary

| Command          | Purpose                           |
| ---------------- | --------------------------------- |
| `docker create`  | Create container without starting |
| `docker start`   | Start a stopped container         |
| `docker pause`   | Pause container processes         |
| `docker unpause` | Resume paused processes           |
| `docker stop`    | Gracefully stop container         |
| `docker restart` | Restart container                 |
| `docker kill`    | Immediately terminate container   |
| `docker rm`      | Remove container                  |

---

# 4. Working With Running Containers

## Step 1: Run Nginx in Detached Mode

Run:

```bash
docker run -d --name nginx-demo -p 8080:80 nginx
```

Explanation:

```text
-d
```

Check the running container:

```bash
docker ps
```

---

## Test Nginx

Open the following in your browser:

If Docker is running on a remote Linux/EC2 machine, use that machine's accessible IP and ensure the required port is allowed by the firewall/security group.

```text
lttp://<public IP>:8080
```
or

```text
http://localhost:8080
```

You should see the Nginx welcome page.

---

# Step 2: View Container Logs

Run:

```bash
docker logs nginx-demo
```

This displays logs produced by the container.

---

# Step 3: View Real-Time Logs

Run:

```bash
docker logs -f nginx-demo
```

The `-f` option means follow.

It keeps the command running and displays new log entries as they appear.

Press:

```text
Ctrl + C
```

to stop following the logs. The container itself will continue running.

---

# Step 4: Exec Into the Container

Open a shell inside the running Nginx container:

```bash
docker exec -it nginx-demo /bin/bash
```

If Bash is not available in an image, use:

```bash
docker exec -it nginx-demo /bin/sh
```

Inside the container, try:

```bash
pwd
```

```bash
ls /usr/share/nginx/html
```

Check the Nginx configuration:

```bash
ls /etc/nginx
```

Exit the container:

```bash
exit
```

---

# Step 5: Run a Single Command Inside the Container

You do not always need to enter the container.

For example:

```bash
docker exec nginx-demo ls /usr/share/nginx/html
```

Check the running Nginx process:

```bash
docker exec nginx-demo ps
```

Check the hostname:

```bash
docker exec nginx-demo hostname
```

---

# Step 6: Inspect the Container

Run:

```bash
docker inspect nginx-demo
```

Docker returns detailed JSON information about the container.

Important information includes:

* Container ID
* Container name
* Image
* Container state
* IP address
* Port mappings
* Mounts
* Network configuration
* Environment variables
* Startup configuration

---

## Find the Container IP Address

Use:

```bash
docker inspect nginx-demo
```

There is:

```text
NetworkSettings
```

and:

```text
IPAddress
```

A more direct command is:

```bash
docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' nginx-demo
```

---

## Check Port Mappings

Run:

```bash
docker port nginx-demo
```

Expected output will be similar to:

```text
80/tcp -> 0.0.0.0:8080
```

This means:

```text
Host:8080
     |
     v
Container:80
```

---

## Check Mounts

Run:

```bash
docker inspect nginx-demo
```

Look for:

```text
Mounts
```

For this container, there may be no custom host volume mount because we did not specify one with `-v` or `--mount`.

---

# 5. Docker Cleanup

Cleanup is important because containers, images, volumes, build cache, and other Docker resources can consume disk space.

---

# Step 1: Stop All Running Containers

First check running containers:

```bash
docker ps
```

To stop all currently running containers:

```bash
docker stop $(docker ps -q)
```

Explanation:

```bash
docker ps -q
```

returns only the IDs of running containers.

Those IDs are passed to:

```bash
docker stop
```

Verify:

```bash
docker ps
```

There should be no running containers.

---

# Step 2: Remove All Stopped Containers

Run:

```bash
docker rm $(docker ps -aq)
```

Explanation:

```bash
docker ps -aq
```

returns IDs of all containers, including stopped containers.

Then `docker rm` removes them.

### Alternative

You can remove stopped containers using:

```bash
docker container prune
```

Docker asks for confirmation before removing them.

---

# Step 3: Remove Unused Images

To remove unused/dangling images:

```bash
docker image prune
```

For broader cleanup of unused images:

```bash
docker image prune -a
```

Be careful with:

```bash
docker image prune -a
```

because it can remove images that are not currently associated with containers.

---

# Step 4: Check Docker Disk Usage

Run:

```bash
docker system df
```

This shows Docker disk usage for:

* Images
* Containers
* Local volumes
* Build cache

For more detailed information:

```bash
docker system df -v
```

---

# Docker System Prune

Docker also provides a general cleanup command:

```bash
docker system prune
```

Docker will ask for confirmation.

For a more aggressive cleanup:

```bash
docker system prune -a
```

Be careful because this can remove unused Docker resources, including images that you may want later.

---

# Important Docker Commands Learned Today

## Image Commands

```bash
docker pull nginx
docker images
docker image ls
docker image inspect nginx
docker image history nginx
docker rmi alpine
```

## Container Creation and Execution

```bash
docker create --name lifecycle-demo nginx
docker run -d --name nginx-demo -p 8080:80 nginx
```

## Container Lifecycle

```bash
docker start lifecycle-demo
docker pause lifecycle-demo
docker unpause lifecycle-demo
docker stop lifecycle-demo
docker restart lifecycle-demo
docker kill lifecycle-demo
docker rm lifecycle-demo
```

## Container Monitoring

```bash
docker ps
docker ps -a
docker logs nginx-demo
docker logs -f nginx-demo
docker inspect nginx-demo
docker port nginx-demo
```

## Container Interaction

```bash
docker exec -it nginx-demo /bin/bash
docker exec nginx-demo ls /usr/share/nginx/html
```

## Cleanup

```bash
docker stop $(docker ps -q)
docker rm $(docker ps -aq)
docker image prune
docker system df
docker system prune
```

---


# Image Layers and Containers

A useful way to understand Docker is:

```text
Dockerfile
    |
    v
Docker Image
    |
    +----------------+
    | Multiple Layers|
    +----------------+
    |
    v
Docker Container
    |
    +----------------------+
    | Writable Container   |
    | Layer                 |
    +----------------------+
```

The image layers are generally read-only.

When a container is created, Docker adds a writable layer on top of the image layers.

This allows the container to make runtime filesystem changes without modifying the original image.

---

# Key Learnings

## 1. Image

An image is the template used to create containers.

## 2. Container

A container is an instance of an image.

## 3. Layers

Images are composed of multiple layers that can be reused and cached.

## 4. Caching

Docker can reuse unchanged layers, making image builds faster.

## 5. Container Lifecycle

A container can be:

```text
Created
   ↓
Running
   ↓
Paused
   ↓
Running
   ↓
Stopped
   ↓
Removed
```

It can also be terminated using:

```text
Running
   ↓
Killed
   ↓
Stopped
```

## 6. Logs

`docker logs` helps troubleshoot and monitor containers.

## 7. Exec

`docker exec` allows commands to be executed inside a running container.

## 8. Inspect

`docker inspect` provides detailed information about images and containers.

## 9. Cleanup

Unused containers, images, volumes, and build cache can consume disk space, so Docker cleanup is important.

---

# Final Summary

Today I learned how Docker images and containers work together.

I learned that:

* Images are templates used to create containers.
* Containers are runtime instances of images.
* Docker images are built from layers.
* Layers improve caching, reuse, and storage efficiency.
* Alpine is much smaller than Ubuntu because it contains a much more minimal userspace.
* `docker image history` shows image layer history.
* Containers have a complete lifecycle from creation to removal.
* `docker logs` is useful for checking application output.
* `docker exec` allows commands to be executed inside running containers.
* `docker inspect` provides detailed configuration and runtime information.
* Docker cleanup commands help manage disk usage.

The most important concept from today is:

```text
Image = Template

Container = Instance of the Image

Layers = Building blocks of an Image

Container Lifecycle = Create → Start → Pause/Unpause → Stop/Restart/Kill → Remove
```

# End of Day 30
