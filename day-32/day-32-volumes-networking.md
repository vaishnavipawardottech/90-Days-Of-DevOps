# Day 32 – Docker Volumes and Networking

## Overview

Today I learned about:

- Docker volumes
- Named volumes
- Bind mounts
- Volume persistence
- Docker bridge networking
- Default bridge network
- Custom bridge networks
- Container-to-container communication

---

# Task 1: Named Volumes

## Goal

Create a named volume, attach it to a container, store data in it, remove the container, and verify that the data is still available.

## Commands

### 1. Create a named volume

```bash
docker volume create mydata
```

### 2. Run an Nginx container with the volume

```bash
docker run -d --name volume-test -v mydata:/usr/share/nginx/html nginx
```

### 3. Create a file inside the volume

```bash
docker exec volume-test sh -c "echo 'Hello from Docker volume' > /usr/share/nginx/html/message.txt"
```

### 4. Check the file

```bash
docker exec volume-test cat /usr/share/nginx/html/message.txt
```

### 5. Remove the container

```bash
docker rm -f volume-test
```

### 6. Create a new container using the same volume

```bash
docker run -d --name volume-test-2 -v mydata:/usr/share/nginx/html nginx
```

### 7. Check the file again

```bash
docker exec volume-test-2 cat /usr/share/nginx/html/message.txt
```

## Result

The file is still available after removing the first container.

This shows that the data is stored in the Docker volume and not only inside the container.

---

# Task 2: Bind Mounts

## Goal

Use a directory from the host machine inside a Docker container.

## Commands

### 1. Create a directory on the host

```bash
mkdir my-app-data
```

### 2. Create a file in the directory

```bash
echo "Hello from host" > my-app-data/message.txt
```

### 3. Run an Nginx container with the directory mounted

```bash
docker run -d --name bind-test -v $(pwd)/my-app-data:/usr/share/nginx/html nginx
```

### 4. Check the file from the container

```bash
docker exec bind-test cat /usr/share/nginx/html/message.txt
```

## Result

The file created on the host is available inside the container.

This is called a bind mount because a host directory is directly mounted into the container.

---

# Task 3: Volume Persistence

## Goal

Verify that data remains available when a container is removed and a new container uses the same volume.

## Commands

### 1. Create a volume

```bash
docker volume create postgres-data
```

### 2. Run a PostgreSQL container with the volume

```bash
docker run -d \
  --name postgres-test \
  -e POSTGRES_PASSWORD=secret \
  -v postgres-data:/var/lib/postgresql/data \
  postgres:16
```

### 3. Check the container

```bash
docker ps
```

### 4. Remove the container

```bash
docker rm -f postgres-test
```

### 5. Run a new PostgreSQL container with the same volume

```bash
docker run -d \
  --name postgres-test-2 \
  -e POSTGRES_PASSWORD=secret \
  -v postgres-data:/var/lib/postgresql/data \
  postgres:16
```

### 6. Check the new container

```bash
docker ps
```

## Result

The PostgreSQL data directory is stored in the named volume.

Removing the container does not remove the volume.

---

# Task 4: Default Bridge Network

## Goal

Run two containers on Docker's default bridge network and test communication using IP address and container name.

## 1. Run two containers

When `--network` is not specified, Docker uses the default `bridge` network.

```bash
docker run -dit --name container1 ubuntu bash
```

```bash
docker run -dit --name container2 ubuntu bash
```

## 2. Check the default bridge network

```bash
docker network inspect bridge
```

Look for `container1` and `container2` in the `Containers` section.

## 3. Get the container IP addresses

Run:

```bash
docker inspect container1
```

and:

```bash
docker inspect container2
```

Search the output for:

```text
"IPAddress"
```

You will find an IP address for each container.

Example:

```text
container1 → 172.17.0.2
container2 → 172.17.0.3
```

The actual IP addresses can be different.

## 4. Install ping

Enter `container1`:

```bash
docker exec -it container1 bash
```

Inside the container:

```bash
apt update
apt install iputils-ping -y
```

## 5. Ping container2 by IP

Use the IP address you found for `container2`:

```bash
ping <container2-IP>
```

For example:

```bash
ping 172.17.0.3
```

The containers can communicate by IP.

## 6. Ping container2 by name

Try:

```bash
ping container2
```

On the default bridge network, name-based communication normally does not work.

## Result

- Communication by IP → Works
- Communication by container name → Does not normally work

---

# Task 5: Custom Networks

## Goal

Create a custom bridge network and verify that containers can communicate using their names.

## 1. Create a custom network

```bash
docker network create --driver bridge my-app-net
```

## 2. Check the network

```bash
docker network ls
```

You should see:

```text
my-app-net
```

## 3. Run two containers on the custom network

```bash
docker run -dit --name app1 --network my-app-net ubuntu bash
```

```bash
docker run -dit --name app2 --network my-app-net ubuntu bash
```

## 4. Check the network

```bash
docker network inspect my-app-net
```

Look for `app1` and `app2` in the `Containers` section.

## 5. Enter app1

```bash
docker exec -it app1 bash
```

## 6. Install ping

Inside the container:

```bash
apt update
apt install iputils-ping -y
```

## 7. Ping app2 by name

```bash
ping app2
```

The ping should work.

## Result

Containers on a custom bridge network can communicate using container names.

---

# Why Does Custom Networking Allow Name-Based Communication?

Docker provides built-in DNS service for user-defined networks.

When containers are connected to a custom bridge network, Docker can resolve a container name to its IP address.

For example:

```text
app1 → app2
      ↓
Docker DNS
      ↓
app2 IP address
```

The default `bridge` network does not provide the same automatic container-name DNS resolution.

Therefore:

```text
Default bridge:
container1 → IP address → container2

Custom bridge:
app1 → container name → app2
```

---

# Task 6: Put It Together

## Goal

Create a custom network, run a PostgreSQL database with a volume, run an app container on the same network, and verify that the app can reach the database by container name.

## 1. Create a custom network

```bash
docker network create --driver bridge my-app-net
```

## 2. Create a volume

```bash
docker volume create postgres-data
```

## 3. Run PostgreSQL on the custom network

```bash
docker run -d \
  --name my-db \
  --network my-app-net \
  -e POSTGRES_PASSWORD=secret \
  -v postgres-data:/var/lib/postgresql/data \
  postgres:16
```

## 4. Check the database container

```bash
docker ps
```

Make sure `my-db` is running.

## 5. Run the app container on the same network

```bash
docker run -dit --name my-app --network my-app-net ubuntu bash
```

Now both containers are connected to:

```text
my-app-net
```

## 6. Enter the app container

```bash
docker exec -it my-app bash
```

## 7. Install PostgreSQL client

Inside the app container:

```bash
apt update
apt install postgresql-client -y
```

## 8. Connect to PostgreSQL using the container name

```bash
psql -h my-db -U postgres -W
```

Enter the PostgreSQL password:

```text
secret
```

If the connection succeeds, you will get:

```text
postgres=#
```

## Result

The app container successfully reached the PostgreSQL database using:

```text
my-db
```

instead of using the database container's IP address.

---

# Important Commands Learned

## Docker Volumes

```bash
docker volume create <volume-name>
```

```bash
docker volume ls
```

```bash
docker volume inspect <volume-name>
```

```bash
docker volume rm <volume-name>
```

## Docker Networks

```bash
docker network ls
```

```bash
docker network create --driver bridge <network-name>
```

```bash
docker network inspect <network-name>
```

```bash
docker network rm <network-name>
```

---

# Key Learnings

1. A Docker volume stores data outside the container's writable layer.

2. Named volumes can be reused by different containers.

3. Removing a container does not automatically remove its named volume.

4. A bind mount uses a directory from the host machine.

5. Containers on the default bridge network can communicate using IP addresses.

6. The default bridge network does not normally provide automatic container-name DNS resolution.

7. User-defined bridge networks provide Docker DNS for container names.

8. Containers on a custom network can communicate using container names.

9. A database container and an app container can communicate through a custom network.

10. Using container names is better than depending on container IP addresses because container IP addresses can change.

---

# Cleanup

After completing the tasks, containers and networks can be removed if they are no longer needed.

```bash
docker rm -f volume-test-2 volume-test-2 bind-test postgres-test-2 container1 container2 app1 app2 my-db my-app
```

Remove the networks:

```bash
docker network rm my-app-net
```

Remove the volumes only if the stored data is no longer needed:

```bash
docker volume rm mydata postgres-data
```
