# Docker Cheat Sheet

Quick reference for commonly used Docker commands.

---

## Container Commands

```bash
docker run nginx                         # Run a container
docker run -it ubuntu bash               # Run interactively
docker run -d nginx                      # Run in detached mode
docker ps                                # List running containers
docker ps -a                             # List all containers
docker stop <container>                  # Stop a container
docker start <container>                 # Start a stopped container
docker restart <container>               # Restart a container
docker rm <container>                    # Remove a container
docker exec -it <container> bash         # Open a shell inside a container
docker logs <container>                  # View container logs
docker inspect <container>               # View container details
```

---

## Image Commands

```bash
docker images                            # List images
docker pull <image>                      # Pull an image
docker build -t <name>:<tag> .           # Build an image
docker build -t <name>:<tag> -f Dockerfile.multistage .  # Build using a specific Dockerfile
docker tag <image> <username>/<repo>:<tag> # Tag an image
docker push <username>/<repo>:<tag>      # Push image to registry
docker rmi <image>                       # Remove an image
```

---

## Volume Commands

```bash
docker volume create <volume>            # Create a named volume
docker volume ls                         # List volumes
docker volume inspect <volume>           # Inspect a volume
docker volume rm <volume>                # Remove a volume
docker run -v <volume>:/data <image>     # Mount named volume
docker run -v ./data:/data <image>       # Bind mount host directory
```

---

## Network Commands

```bash
docker network create <network>          # Create custom network
docker network ls                        # List networks
docker network inspect <network>         # Inspect network
docker network connect <network> <container> # Connect container to network
docker network disconnect <network> <container> # Disconnect container
```

Containers on the same custom network can communicate using **container/service names**.

---

## Docker Compose Commands

```bash
docker compose up -d                     # Create and start services
docker compose down                      # Stop and remove services
docker compose down -v                   # Remove services and volumes
docker compose ps                        # List Compose services
docker compose logs                      # View service logs
docker compose logs -f <service>         # Follow service logs
docker compose build                     # Build service images
docker compose pull                      # Pull service images
docker compose restart                   # Restart services
```

---

## Cleanup Commands

```bash
docker system df                         # Show Docker disk usage
docker container prune                   # Remove stopped containers
docker image prune                       # Remove unused images
docker volume prune                      # Remove unused volumes
docker network prune                     # Remove unused networks
docker system prune                      # Remove unused Docker resources
```

---

## Dockerfile Instructions

```dockerfile
FROM node:20-alpine          # Base image
WORKDIR /app                 # Set working directory
COPY package*.json ./        # Copy files into image
RUN npm install              # Run command during image build
COPY . .                     # Copy application source
EXPOSE 3000                  # Document container port
CMD ["npm", "start"]         # Default command
ENTRYPOINT ["node"]           # Main executable
```

### Quick Difference

| Instruction  | Purpose                       |
| ------------ | ----------------------------- |
| `FROM`       | Select base image             |
| `RUN`        | Execute command during build  |
| `COPY`       | Copy files into image         |
| `WORKDIR`    | Set working directory         |
| `EXPOSE`     | Document the application port |
| `CMD`        | Default startup command       |
| `ENTRYPOINT` | Define the main executable    |

---

## Important Docker Concepts

* **Image** → Read-only template used to create containers.
* **Container** → Running/stopped instance of an image.
* **Volume** → Persistent Docker-managed storage.
* **Bind Mount** → Maps a host path directly into a container.
* **Network** → Allows containers to communicate.
* **Compose** → Defines and manages multi-container applications.
* **Multi-stage build** → Separates build and runtime stages to reduce image size.
* **`.env`** → Stores environment-specific configuration values.
* **Healthcheck** → Checks whether a containerized service is healthy.
