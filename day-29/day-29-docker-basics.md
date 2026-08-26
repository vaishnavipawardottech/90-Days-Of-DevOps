# Day 29 – Introduction to Docker

## Objective

The goal of Day 29 was to understand the basics of Docker, learn why containers are used, understand containers vs virtual machines, install Docker, and run different containers from Docker Hub.

### Topics Covered

* Containers
* Containers vs Virtual Machines
* Docker architecture
* Docker images
* Docker containers
* Docker Hub
* Running containers
* Interactive mode
* Detached mode
* Port mapping
* Container names
* Container logs
* Executing commands inside containers

---

# Task 1: What is Docker?

## What is a Container?

A container is a lightweight and isolated environment used to run an application along with the dependencies required by that application.

A container packages the application, libraries, configuration, and other required components together so that the application can run consistently across different environments.

For example, instead of manually installing Nginx and configuring it on a server, we can run an Nginx container using:

```bash
docker run nginx
```

### Why Do We Need Containers?

Containers help solve the problem of:

> "It works on my machine, but it doesn't work on the server."

Containers provide:

* Consistent application environments
* Application isolation
* Fast startup
* Easy deployment
* Better resource utilization
* Easier scaling
* Reproducible environments
* Simplified dependency management

---

# Containers vs Virtual Machines

Both containers and virtual machines provide isolation, but they work differently.

| Feature          | Containers                         | Virtual Machines               |
| ---------------- | ---------------------------------- | ------------------------------ |
| Virtualization   | OS-level virtualization            | Hardware-level virtualization  |
| Operating System | Share host kernel                  | Each VM has its own OS         |
| Size             | Lightweight                        | Usually larger                 |
| Startup          | Very fast                          | Slower                         |
| Resource Usage   | Lower                              | Higher                         |
| Isolation        | Process-level isolation            | Stronger hardware/OS isolation |
| Use Case         | Microservices, CI/CD, applications | Full OS environments           |
| Portability      | High                               | High                           |

### Main Difference

A virtual machine contains:

```text
Application
Libraries
Guest Operating System
Virtual Hardware
Host Operating System
Physical Hardware
```

A container contains:

```text
Application
Libraries
Container
Docker Engine
Host Operating System
Physical Hardware
```

Containers share the host operating system kernel, while virtual machines have their own guest operating system.

---

# Docker Architecture

Docker follows a client-server architecture.

The main components are:

1. Docker Client
2. Docker Daemon
3. Docker Images
4. Docker Containers
5. Docker Registry

## Docker Client

The Docker Client is the command-line interface used to interact with Docker.

Examples:

```bash
docker run
docker ps
docker stop
docker rm
docker logs
docker exec
```

When we execute a Docker command, the Docker client communicates with the Docker daemon.

---

## Docker Daemon

The Docker daemon is the background service responsible for managing Docker objects.

It handles:

* Images
* Containers
* Networks
* Volumes

On Linux, the Docker service can be checked using:

```bash
sudo systemctl status docker
```

---

## Docker Image

A Docker image is a read-only template used to create containers.

Examples:

```text
nginx
ubuntu
hello-world
```

For example:

```bash
docker run nginx
```

uses the Nginx image to create a container.

---

## Docker Container

A container is a running or stopped instance created from a Docker image.

For example:

```text
Nginx Image
     |
     v
Nginx Container
```

Multiple containers can be created from the same image.

---

## Docker Registry

A registry stores and distributes Docker images.

Docker Hub is a popular public Docker registry.

When we run:

```bash
docker run nginx
```

Docker can pull the Nginx image from Docker Hub if the image is not already available locally.

---

# Docker Architecture in My Own Words

My understanding of the Docker workflow is:

```text
                 Docker Hub
                     |
                     | Pull Image
                     v
+--------------------+--------------------+
|              Docker Daemon              |
|                                          |
|       Images  --->  Containers           |
|                                          |
+--------------------+--------------------+
                     ^
                     |
              Docker Client
              (docker CLI)
                     |
                     |
             docker commands
```

For example:

```text
docker run nginx
       |
       v
Docker Client
       |
       v
Docker Daemon
       |
       v
Check Nginx Image
       |
       +---- Image exists locally
       |
       +---- Image does not exist
                    |
                    v
                Docker Hub
                    |
                    v
                Pull Image
                    |
                    v
              Create Container
                    |
                    v
              Start Container
```

---

# Task 2: Install Docker

## Step 1 – Update Packages

```bash
sudo apt update
```

## Step 2 – Install Docker

```bash
sudo apt install docker.io -y
```

## Step 3 – Start Docker

```bash
sudo systemctl start docker
```

## Step 5 – Verify Docker Installation

```bash
docker --version
```

---

## Check Docker Service

```bash
sudo systemctl status docker
```

Expected status:

```text
Active: active (running)
```
---

# Run the Hello World Container

Command:

```bash
sudo docker run hello-world
```

Docker downloads the `hello-world` image if it is not already available locally, creates a container from the image, runs it, prints the message, and then the container exits.

---

# Task 3: Run Real Containers

# 1. Run an Nginx Container

Command:

```bash
sudo docker run -d --name my-nginx -p 8080:80 nginx
```

### Explanation

```text
-d
```

Runs the container in detached mode.

```text
--name my-nginx
```

Assigns the custom name `my-nginx`.

```text
-p 8080:80
```

Maps host port 8080 to container port 80.

```text
nginx
```

Specifies the Nginx image.

---

### Access Nginx

If running Docker on an EC2 instance, open:

```text
http://<EC2-PUBLIC-IP>:8080
```

The Nginx welcome page should be displayed.

# 2. Run an Ubuntu Container

Run:

```bash
sudo docker run -it --name my-ubuntu ubuntu
```

The `-it` option allows interactive access to the container.

After entering the container, I explored it using:

```bash
ls
```

```bash
pwd
```

```bash
whoami
```

```bash
cat /etc/os-release
```

To exit the container:

```bash
exit
```
---

# 3. List Running Containers

Command:

```bash
sudo docker ps
```

This displays only currently running containers.

---

# 4. List All Containers

Command:

```bash
sudo docker ps -a
```

This displays both running and stopped containers.

---

# 5. Stop and Remove a Container

Stop the Nginx container:

```bash
sudo docker stop my-nginx
```

Remove the container:

```bash
sudo docker rm my-nginx
```

---

# Task 4: Explore Docker

## 1. Detached Mode
### What is Detached Mode?

Detached mode allows a container to run in the background without keeping the terminal attached to the container.

The `-d` option is commonly used for services such as:

* Nginx
* Web applications
* Databases
* APIs

Run:

```bash
sudo docker run -d --name nginx-detached -p 8081:80 nginx
```

The terminal returns immediately because the container runs in the background.

---

# 2. Custom Container Name

The container was given a custom name using:

```bash
--name nginx-detached
```

This makes it easier to manage the container. Instead of using a randomly generated container name.

---

# 3. Port Mapping

Run:

```bash
sudo docker run -d --name nginx-port -p 8082:80 nginx
```

Port mapping follows:

```text
-p HOST_PORT:CONTAINER_PORT
```

Therefore:

```text
8082:80
```

means:

```text
Host Port 8082
       |
       v
Container Port 80
```

Nginx can then be accessed using:

```text
http://<EC2-PUBLIC-IP>:8082
```

---

# 4. Check Container Logs

Run:

```bash
sudo docker logs nginx-port
```

To continuously follow the logs:

```bash
sudo docker logs -f nginx-port
```

Press:

```text
Ctrl + C
```

to stop following the logs.

---

# 5. Run a Command Inside a Running Container

Execute a command:

```bash
sudo docker exec nginx-port ls
```

To open a shell inside the container:

```bash
sudo docker exec -it nginx-port /bin/bash
```

Inside the container:

```bash
pwd
```
Exit:

```bash
exit
```

---

# Useful Docker Commands Learned

| Command             | Purpose                                      |
| ------------------- | -------------------------------------------- |
| `docker --version`  | Check Docker version                         |
| `docker run`        | Create and start a container                 |
| `docker ps`         | List running containers                      |
| `docker ps -a`      | List all containers                          |
| `docker stop`       | Stop a container                             |
| `docker start`      | Start a stopped container                    |
| `docker rm`         | Remove a container                           |
| `docker images`     | List local images                            |
| `docker pull`       | Download an image                            |
| `docker logs`       | View container logs                          |
| `docker exec`       | Execute a command inside a running container |
| `docker run -it`    | Run container interactively                  |
| `docker run -d`     | Run container in detached mode               |
| `docker run -p`     | Map host and container ports                 |
| `docker run --name` | Give a custom name to a container            |

---

# Why Docker Matters for DevOps

Docker is an important part of modern DevOps because applications can be packaged and deployed consistently across different environments.

Docker containers are commonly used in:

* CI/CD pipelines
* Microservices
* Cloud deployments
* Application testing
* Development environments
* Kubernetes
* Scalable application deployments

Today's exercise was my first hands-on experience with Docker containers, from pulling images to creating, running, exploring, stopping, and removing containers.

---

# Conclusion

Day 29 introduced me to Docker and containerization.

I learned the difference between containers and virtual machines, understood the basic Docker architecture, installed Docker, and worked with containers from Docker Hub.

I also practiced running Nginx and Ubuntu containers, interactive and detached modes, port mapping, custom container names, container logs, and executing commands inside running containers.

This gave me the foundation required for the upcoming Docker topics such as images, Dockerfiles, volumes, networks, Docker Compose, and containerized application deployment.
