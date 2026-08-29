# Day 33 – Docker Compose: Multi-Container Basics

## Overview

Today I learned how to use Docker Compose to run multiple containers using a single YAML file.

Topics covered:

- Docker Compose installation and version
- Creating a Compose file
- Running Nginx with Docker Compose
- Running WordPress and MySQL together
- Compose networks
- Named volumes
- Compose commands
- Environment variables
- `.env` files

---

# Task 1: Install & Verify

## Check Docker Compose

```bash
docker compose version
```

If Docker Compose is available, it will show the Compose version.

Example:

```text
Docker Compose version v2.x.x
```

Docker Compose is available as a Docker CLI plugin, so the command is:

```bash
docker compose
```

---

# Task 2: Your First Compose File

## Goal

Create a Compose file that runs one Nginx container and maps a port.

## 1. Create the folder

```bash
mkdir compose-basics
cd compose-basics
```

## 2. Create `docker-compose.yml`

```yaml
services:
  web:
    image: nginx
    ports:
      - "8080:80"
```

## 3. Start the container

```bash
docker compose up
```

The container runs in the foreground and logs are visible in the terminal.

## 4. Access Nginx

Open a browser and visit:

```text
http://localhost:8080
```

The Nginx welcome page should appear.

## 5. Stop and remove the container

Press:

```text
Ctrl + C
```

Then run:

```bash
docker compose down
```

---

# Task 3: Two-Container Setup

## Goal

Run WordPress and MySQL together using Docker Compose.

Compose automatically creates a network for the services.

MySQL also uses a named volume so that its data persists.

## 1. Create a folder

From the parent directory:

```bash
mkdir wordpress-compose
cd wordpress-compose
```

## 2. Create `docker-compose.yml`

```yaml
services:
  db:
    image: mysql:8.0
    environment:
      MYSQL_DATABASE: wordpress
      MYSQL_USER: wordpress
      MYSQL_PASSWORD: wordpress
      MYSQL_ROOT_PASSWORD: rootpassword
    volumes:
      - mysql-data:/var/lib/mysql

  wordpress:
    image: wordpress:latest
    ports:
      - "8080:80"
    environment:
      WORDPRESS_DB_HOST: db:3306
      WORDPRESS_DB_USER: wordpress
      WORDPRESS_DB_PASSWORD: wordpress
      WORDPRESS_DB_NAME: wordpress
    depends_on:
      - db

volumes:
  mysql-data:
```

## Important

The WordPress database host is:

```text
db:3306
```

`db` is the MySQL service name.

Compose provides DNS, so WordPress can find MySQL using the service name.

## 3. Start both services

```bash
docker compose up -d
```

## 4. Check running services

```bash
docker compose ps
```

You should see:

```text
db
wordpress
```

## 5. Open WordPress

Open:

```text
http://localhost:8080
```

Complete the WordPress setup in the browser.

## 6. Check the Compose network

```bash
docker network ls
```

Compose creates a network automatically for the project.

## 7. Check the named volume

```bash
docker volume ls
```

You should see the volume created for MySQL.

## 8. Test persistence

First stop and remove the Compose containers and network:

```bash
docker compose down
```

Then start them again:

```bash
docker compose up -d
```

Open:

```text
http://localhost:8080
```

The MySQL data stored in the named volume remains available.

## Important

`docker compose down` removes the containers and network, but it does not remove the named volume by default.

Therefore, the MySQL data remains.

---

# Task 4: Compose Commands

## 1. Start services in detached mode

```bash
docker compose up -d
```

The `-d` option runs the services in the background.

## 2. View running services

```bash
docker compose ps
```

## 3. View logs of all services

```bash
docker compose logs
```

## 4. Follow logs continuously

```bash
docker compose logs -f
```

Press:

```text
Ctrl + C
```

to stop viewing the logs.

## 5. View logs of a specific service

For MySQL:

```bash
docker compose logs db
```

For WordPress:

```bash
docker compose logs wordpress
```

## 6. Stop services without removing them

```bash
docker compose stop
```

The containers remain but are stopped.

## 7. Start the stopped services again

```bash
docker compose start
```

## 8. Remove containers and network

```bash
docker compose down
```

The named volume is not removed by this command.

## 9. Remove containers, network, and volumes

Only use this when you also want to delete the stored database data:

```bash
docker compose down -v
```

## 10. Rebuild images

If you make changes that require rebuilding an image:

```bash
docker compose build
```

To build and start the services:

```bash
docker compose up -d --build
```

---

# Task 5: Environment Variables

## Part 1: Environment variables directly in Compose

Create a new folder:

```bash
mkdir environment-demo
cd environment-demo
```

Create `docker-compose.yml`:

```yaml
services:
  app:
    image: alpine
    environment:
      APP_NAME: my-app
      APP_ENV: development
    command: sh -c "echo App Name: $$APP_NAME && echo Environment: $$APP_ENV"
```

Start it:

```bash
docker compose up
```

The output should show:

```text
App Name: my-app
Environment: development
```

The variables are defined directly inside `docker-compose.yml`.

---

# Part 2: Use a `.env` File

Create a `.env` file in the same folder as `docker-compose.yml`.

`.env`:

```text
APP_NAME=my-compose-app
APP_ENV=development
```

Update `docker-compose.yml`:

```yaml
services:
  app:
    image: alpine
    environment:
      APP_NAME: ${APP_NAME}
      APP_ENV: ${APP_ENV}
    command: sh -c "echo App Name: $$APP_NAME && echo Environment: $$APP_ENV"
```

## Start the service

```bash
docker compose up
```

You should see:

```text
App Name: my-compose-app
Environment: development
```

This verifies that Docker Compose picked up the values from `.env`.

---

# Compose File Structure

A basic Compose file looks like:

```yaml
services:
  service-name:
    image: image-name
    ports:
      - "host-port:container-port"
    environment:
      VARIABLE: value
```

For multiple services:

```yaml
services:
  service1:
    image: image1

  service2:
    image: image2
```

Compose automatically creates a network for services in the same Compose project.

---

# Important Concepts

## 1. Docker Compose

Docker Compose allows multiple containers to be defined and managed from one YAML file.

Instead of running many `docker run` commands, we can use:

```bash
docker compose up
```

## 2. Services

Each service in `docker-compose.yml` represents a container/application.

Example:

```yaml
services:
  db:
    image: mysql:8.0

  wordpress:
    image: wordpress:latest
```

Here:

- `db` is the MySQL service
- `wordpress` is the WordPress service

## 3. Service Name Communication

Services on the same Compose network can communicate using their service names.

For example:

```text
wordpress → db
```

WordPress uses:

```text
db:3306
```

It does not need the MySQL container IP address.

## 4. Named Volumes

A named volume keeps data even when the container is removed.

Example:

```yaml
volumes:
  mysql-data:
```

And:

```yaml
volumes:
  - mysql-data:/var/lib/mysql
```

## 5. `docker compose down`

```bash
docker compose down
```

Removes the containers and network created by Compose.

Named volumes are kept.

## 6. `docker compose down -v`

```bash
docker compose down -v
```

Removes the containers, network, and named volumes.

This can delete persistent database data.

---

# Useful Docker Compose Commands

```bash
docker compose version
```

```bash
docker compose up
```

```bash
docker compose up -d
```

```bash
docker compose ps
```

```bash
docker compose logs
```

```bash
docker compose logs -f
```

```bash
docker compose logs <service-name>
```

```bash
docker compose stop
```

```bash
docker compose start
```

```bash
docker compose down
```

```bash
docker compose down -v
```

```bash
docker compose build
```

```bash
docker compose up -d --build
```

---

# Key Learnings

1. Docker Compose manages multiple containers from one YAML file.

2. `docker compose up` starts the services.

3. `docker compose up -d` starts services in detached mode.

4. Compose automatically creates a network for services in the same project.

5. Services can communicate using their service names.

6. Named volumes can be used for persistent data.

7. `docker compose down` removes containers and networks but keeps named volumes.

8. `docker compose down -v` also removes named volumes.

9. Environment variables can be written directly in the Compose file.

10. A `.env` file can be used to store environment variable values.

11. `docker compose logs` is used to view service logs.

12. `docker compose stop` stops services without removing containers.

13. `docker compose start` starts stopped services again.

14. `docker compose build` rebuilds images.

