# Day 34 – Docker Compose: Real-World Multi-Container Apps

## Objective

Today's goal is to build a more complex, production-like application using Docker Compose.

The application stack consists of:

* Flask web application
* PostgreSQL database
* Redis cache
* Custom Dockerfile
* Docker Compose
* Healthchecks
* Service dependencies
* Restart policies
* Named networks
* Named volumes
* Service labels
* Scaling experiment

The Flask application has already been created separately and pushed to GitHub.

---

# Step 1: Clone the Existing Application

The Flask application is available in my GitHub repository:

```text
https://github.com/vaishnavipawardottech/simple_flask_app
```

On the EC2 Ubuntu instance, clone the repository:

```bash
git clone git@github.com:vaishnavipawardottech/simple_flask_app.git
```

Move into the project:

```bash
cd simple_flask_app
```

Check the files:

```bash
ls
```

The initial project contains the Flask application and its supporting files.

The Docker-related files will be added as part of this Day 34 task.

---

# Task 1: Build Your Own App Stack

## Objective

Create a Docker Compose configuration for a three-service application stack:

1. Flask web application
2. PostgreSQL database
3. Redis cache

The final architecture is:

```text
                    Docker Compose
                         |
          +--------------+--------------+
          |              |              |
          v              v              v
       Flask App     PostgreSQL       Redis
          web            db            cache
          |              |              |
          +--------------+--------------+
                         |
                   app-network
```

---

# Step 2: Add PostgreSQL and Redis Support to the Flask Application

The existing Flask application needs to communicate with PostgreSQL and Redis.

Update the application's dependencies to include:

```text
Flask
psycopg2-binary
redis
```

The Flask application will use:

```text
db
```

as the PostgreSQL hostname and:

```text
redis
```

as the Redis hostname.

These names correspond to the Docker Compose service names.

The application should provide endpoints to test the services:

```text
/
    → Basic Flask application

/health
    → Application health

/db
    → PostgreSQL connection test

/cache
    → Redis connection test
```

---

# Step 3: Create the Dockerfile

Create:

```text
app/Dockerfile
```

Use:

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

EXPOSE 5000

CMD ["python", "app.py"]
```

The Dockerfile creates a custom image for the Flask web application.

---

# Step 4: Create the `.env` File

Create `.env` in the same directory as `docker-compose.yml`:

```env
POSTGRES_DB=devopsdb
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres123
DB_HOST=db
REDIS_HOST=redis
```

The `.env` file stores configuration values used by Docker Compose.

The `.env` file should **not be committed to Git**.

Make sure `.gitignore` contains:

```gitignore
.env
.env.*
```

---

# Step 5: Create `docker-compose.yml`

Create:

```text
docker-compose.yml
```

Use:

```yaml
services:

  web:
    build: ./app
    ports:
      - "5000:5000"
    environment:
      DB_HOST: ${DB_HOST}
      POSTGRES_DB: ${POSTGRES_DB}
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      REDIS_HOST: ${REDIS_HOST}
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_started
    restart: on-failure
    networks:
      - app-network
    labels:
      com.devops.day: "34"
      com.devops.service: "web"

  db:
    image: postgres:16
    environment:
      POSTGRES_DB: ${POSTGRES_DB}
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
    volumes:
      - postgres-data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER} -d ${POSTGRES_DB}"]
      interval: 5s
      timeout: 5s
      retries: 5
    restart: always
    networks:
      - app-network
    labels:
      com.devops.day: "34"
      com.devops.service: "database"

  redis:
    image: redis:7-alpine
    networks:
      - app-network
    labels:
      com.devops.day: "34"
      com.devops.service: "cache"

networks:
  app-network:
    driver: bridge

volumes:
  postgres-data:
```

---

# Task 2: depends_on & Healthchecks

## Objective

Ensure that the Flask application starts only after PostgreSQL is ready to accept connections.

## PostgreSQL Healthcheck

The database service contains:

```yaml
healthcheck:
  test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER} -d ${POSTGRES_DB}"]
  interval: 5s
  timeout: 5s
  retries: 5
```

The `pg_isready` command checks whether PostgreSQL is ready to accept connections.

### Healthcheck Configuration

| Option     | Purpose                          |
| ---------- | -------------------------------- |
| `test`     | Command used to check PostgreSQL |
| `interval` | Runs the check every 5 seconds   |
| `timeout`  | Allows 5 seconds for a check     |
| `retries`  | Allows 5 failed checks           |

---

## depends_on

The Flask service contains:

```yaml
depends_on:
  db:
    condition: service_healthy
```

This means the web application waits for PostgreSQL to become healthy.

Redis uses:

```yaml
depends_on:
  redis:
    condition: service_started
```

The startup sequence becomes:

```text
PostgreSQL starts
      |
      v
Healthcheck runs
      |
      v
Database becomes healthy
      |
      v
Flask application starts
```

---

## Validate the Compose Configuration

Before starting the services:

```bash
docker compose config
```

If there are no validation errors, start the stack:

```bash
docker compose up --build
```

Or run it in detached mode:

```bash
docker compose up --build -d
```

Check the services:

```bash
docker compose ps
```

The database should eventually show:

```text
Up (healthy)
```

Check the database health directly:

```bash
docker inspect $(docker compose ps -q db) --format='{{.State.Health.Status}}'
```

Expected:

```text
healthy
```

View logs:

```bash
docker compose logs
```

Follow logs:

```bash
docker compose logs -f
```

---

# Test the Application

## Test Flask

Open:

```text
http://localhost:5000
```

Expected:

```text
Hello from DevOps Compose Demo!
```

## Test PostgreSQL

Open:

```text
http://localhost:5000/db
```

Expected:

```text
Successfully connected to PostgreSQL!
```

## Test Redis

Open:

```text
http://localhost:5000/cache
```

Expected:

```text
Redis value: Hello from Redis!
```

---

# Test Dependency Behavior

Bring down the complete stack:

```bash
docker compose down
```

Start it again:

```bash
docker compose up
```

Monitor the logs:

```bash
docker compose logs -f
```

The database starts first and performs its healthcheck.

Once PostgreSQL becomes healthy, the Flask service starts.

This demonstrates the difference between:

```text
Container started
```

and:

```text
Application inside the container is actually ready
```

---

# Task 3: Restart Policies

## Objective

Test Docker's restart policies and understand how they behave when containers stop.

The PostgreSQL service uses:

```yaml
restart: always
```

---

## Test `restart: always`

Start the application:

```bash
docker compose up -d
```

Find the database container:

```bash
docker compose ps -q db
```

Kill the database container:

```bash
docker kill $(docker compose ps -q db)
```

Check the services:

```bash
docker compose ps
```

The database container should restart automatically.

---

## Test `restart: on-failure`

Temporarily change:

```yaml
restart: always
```

to:

```yaml
restart: on-failure
```

Start the stack:

```bash
docker compose up -d
```

Kill the database:

```bash
docker kill $(docker compose ps -q db)
```

Check:

```bash
docker compose ps
```

`on-failure` is designed to restart a container when its process exits with a failure status.

A manually stopped or killed container does not behave exactly like a process that exits with a non-zero status.

---

## Restart Policy Comparison

| Policy           | Behavior                                       | Typical Use                                         |
| ---------------- | ---------------------------------------------- | --------------------------------------------------- |
| `no`             | Never automatically restart                    | Development/testing                                 |
| `always`         | Restart whenever the container stops           | Important long-running services                     |
| `on-failure`     | Restart when the container exits with an error | Applications where failures should trigger recovery |
| `unless-stopped` | Restart unless manually stopped                | Long-running services                               |

For the final Day 34 configuration, PostgreSQL uses:

```yaml
restart: always
```

---

# Task 4: Custom Dockerfiles in Compose

## Objective

Build the Flask application from a custom Dockerfile instead of using a pre-built image.

The Compose file uses:

```yaml
web:
  build: ./app
```

This tells Docker Compose to build the web application image from the Dockerfile located inside the `app` directory.

---

## Make a Code Change

Modify the Flask application's response.

For example:

```python
return "Day 34 - Docker Compose Multi-Container Application!"
```

Then rebuild and restart:

```bash
docker compose up --build -d
```

Check the containers:

```bash
docker compose ps
```

Test the application:

```text
http://localhost:5000
```

The updated application response should be displayed.

This demonstrates that the application can be rebuilt from its source code using Docker Compose.

---

# Task 5: Named Networks & Volumes

## Named Network

The Compose file explicitly defines:

```yaml
networks:
  app-network:
    driver: bridge
```

Each service joins the network using:

```yaml
networks:
  - app-network
```

Check the networks:

```bash
docker network ls
```

Inspect the Compose network:

```bash
docker network inspect simple_flask_app_app-network
```

The exact network name may vary depending on the Compose project name.

The services communicate using service names:

```text
web → db
web → redis
```

The Flask application therefore uses:

```text
DB_HOST=db
REDIS_HOST=redis
```

instead of hard-coded container IP addresses.

---

# Named Volume

PostgreSQL uses:

```yaml
volumes:
  - postgres-data:/var/lib/postgresql/data
```

The named volume is defined as:

```yaml
volumes:
  postgres-data:
```

Check volumes:

```bash
docker volume ls
```

Inspect the volume:

```bash
docker volume inspect simple_flask_app_postgres-data
```

The exact volume name may vary depending on the Compose project name.

---

# Test Database Persistence

Enter PostgreSQL:

```bash
docker compose exec db psql -U postgres -d devopsdb
```

Create a table:

```sql
CREATE TABLE test_data (
    id SERIAL PRIMARY KEY,
    message TEXT
);
```

Insert data:

```sql
INSERT INTO test_data (message)
VALUES ('Docker Compose Day 34');
```

Verify:

```sql
SELECT * FROM test_data;
```

Exit PostgreSQL:

```sql
\q
```

Remove the containers:

```bash
docker compose down
```

Do **not** use `-v`.

Start the application again:

```bash
docker compose up -d
```

Enter PostgreSQL:

```bash
docker compose exec db psql -U postgres -d devopsdb
```

Run:

```sql
SELECT * FROM test_data;
```

The data should still exist because PostgreSQL data is stored in the named volume.

---

## Important

Avoid:

```bash
docker compose down -v
```

when testing persistence.

The `-v` option removes the Compose volumes.

---

# Service Labels

Labels were added to each service for organization.

### Web

```yaml
labels:
  com.devops.day: "34"
  com.devops.service: "web"
```

### PostgreSQL

```yaml
labels:
  com.devops.day: "34"
  com.devops.service: "database"
```

### Redis

```yaml
labels:
  com.devops.day: "34"
  com.devops.service: "cache"
```

Check the labels:

```bash
docker inspect $(docker compose ps -q web) --format='{{json .Config.Labels}}'
```

Labels can help identify and organize containers in larger environments.

---

# Task 6: Scaling – Bonus

## Objective

Scale the Flask web application to three replicas.

Run:

```bash
docker compose up -d --scale web=3
```

Check:

```bash
docker compose ps
```

Docker Compose attempts to create:

```text
web-1
web-2
web-3
```

---

# Why Simple Scaling Breaks With Port Mapping

The web service contains:

```yaml
ports:
  - "5000:5000"
```

This means:

```text
Host port 5000
      |
      v
Container port 5000
```

When three replicas are created, all three containers attempt to bind the same host port:

```text
Host:5000
```

A single host port cannot normally be bound by multiple containers at the same time.

Therefore, scaling the service with a fixed host port creates a port conflict.

---

## Container Port vs Host Port

Each container can independently listen on:

```text
Container:5000
```

because each container has its own network namespace.

The problem is the host-side port:

```text
Host:5000
```

All replicas cannot simultaneously claim the same host port.

---

# Production Scaling Architecture

In a production environment, multiple web application replicas are commonly placed behind a reverse proxy or load balancer.

```text
                    Load Balancer
                         |
          +--------------+--------------+
          |              |              |
          v              v              v
        web-1          web-2          web-3
          |              |              |
          +--------------+--------------+
                         |
              +----------+----------+
              |                     |
              v                     v
         PostgreSQL               Redis
```

The load balancer distributes incoming requests between the web application replicas.

---

# Useful Docker Compose Commands

## Validate configuration

```bash
docker compose config
```

## Build images

```bash
docker compose build
```

## Start services

```bash
docker compose up
```

## Start in detached mode

```bash
docker compose up -d
```

## Build and start

```bash
docker compose up --build
```

## Build and start in detached mode

```bash
docker compose up --build -d
```

## View running services

```bash
docker compose ps
```

## View logs

```bash
docker compose logs
```

## Follow logs

```bash
docker compose logs -f
```

## View logs for web service

```bash
docker compose logs web
```

## Stop and remove containers

```bash
docker compose down
```

## Stop and remove containers and volumes

```bash
docker compose down -v
```

## Scale web service

```bash
docker compose up -d --scale web=3
```

---

# Final Project Structure

After completing Day 34, the project should look like:

```text
simple_flask_app/
│
├── app/
│   ├── app.py
│   ├── requirements.txt
│   └── Dockerfile
│
├── docker-compose.yml
├── .env
├── .gitignore
└── README.md
```

The `.env` file should remain local and should not be pushed to GitHub.

---

# Key Learnings

## 1. Docker Compose manages multi-container applications

Docker Compose allows multiple services to be defined and managed from a single YAML configuration.

---

## 2. Service names provide internal DNS

The Flask application communicates with:

```text
db
```

for PostgreSQL and:

```text
redis
```

for Redis.

Container IP addresses do not need to be hard-coded.

---

## 3. `depends_on` manages service dependencies

Using:

```yaml
condition: service_healthy
```

allows the Flask application to wait until PostgreSQL passes its healthcheck.

---

## 4. Healthchecks verify service readiness

A container being in the running state does not necessarily mean that the application inside the container is ready.

A healthcheck verifies actual service readiness.

---

## 5. Restart policies improve reliability

Restart policies allow Docker to automatically restart containers according to configured conditions.

---

## 6. Named volumes provide data persistence

PostgreSQL data remains available after containers are removed and recreated because the database uses a named volume.

---

## 7. Explicit networks organize service communication

The services communicate through the explicitly defined:

```text
app-network
```

---

## 8. Environment variables separate configuration from Compose configuration

Database configuration is stored in `.env`:

```env
POSTGRES_DB=devopsdb
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres123
```

The Compose file references these values using:

```yaml
${POSTGRES_DB}
${POSTGRES_USER}
${POSTGRES_PASSWORD}
```

The `.env` file is excluded from Git using `.gitignore`.

---

## 9. Custom Dockerfiles allow application images to be built

The Flask service uses:

```yaml
build: ./app
```

which builds the application image from the custom Dockerfile.

---

## 10. Scaling requires traffic distribution

Multiple replicas cannot share the same fixed host port.

A production architecture generally requires a reverse proxy or load balancer to distribute traffic between replicas.

---

# Final Architecture

```text
                         Docker Compose
                              |
             +----------------+----------------+
             |                |                |
             v                v                v
         Flask Web        PostgreSQL         Redis
         Port 5000          Port 5432        Port 6379
             |                |                |
             +----------------+----------------+
                              |
                        app-network
                              |
                     postgres-data volume
```

---

# Conclusion

Day 34 demonstrated how Docker Compose can be used to build and manage a realistic multi-container application.

An existing Flask application was containerized and combined with PostgreSQL and Redis. Docker Compose was used to manage service dependencies, healthchecks, restart policies, networks, volumes, environment variables, and service labels.

The scaling experiment also demonstrated why simply creating multiple application replicas does not work with a fixed host port and why production deployments generally require a reverse proxy or load balancer.
