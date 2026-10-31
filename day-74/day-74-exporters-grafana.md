
# Day 74 — Node Exporter, cAdvisor, and Grafana Dashboards

## Overview

Prometheus collects metrics, but monitoring only Prometheus itself does not provide enough visibility into the complete system.

To monitor the host machine and Docker containers, we can use:

- **Node Exporter:** Collects host-level metrics such as CPU, memory, disk, filesystem, and network usage.
- **cAdvisor:** Collects resource usage and performance metrics for running containers.
- **Grafana:** Visualizes metrics through dashboards, making it easier to monitor system health without repeatedly running PromQL queries manually.

In this task, we extend the Day 73 Prometheus setup by adding Node Exporter, cAdvisor, and Grafana.

## Objectives

- Configure Node Exporter for host metrics.
- Configure cAdvisor for container metrics.
- Add both exporters as Prometheus scrape targets.
- Connect Grafana to Prometheus.
- Build a custom dashboard with CPU, memory, disk, and container metrics.
- Provision the Prometheus data source using YAML.
- Import community dashboards for additional monitoring.

---

## 1. Project Architecture

```text
                 Docker Compose
                       |
       +---------------+----------------+
       |               |                |
  Prometheus      Node Exporter       cAdvisor
       |           Host Metrics    Container Metrics
       |               |                |
       +---------------+----------------+
                       |
                 PromQL Queries
                       |
                    Grafana
                       |
             Observability Dashboard
```

**How it works:**

1. Node Exporter exposes host metrics.
2. cAdvisor exposes container metrics.
3. Prometheus scrapes metrics from both exporters at regular intervals.
4. PromQL queries the collected time-series data.
5. Grafana uses Prometheus as a data source to visualize metrics in dashboards.

---

## 2. Add Node Exporter for Host Metrics

Node Exporter exposes Linux system metrics in a format that Prometheus can scrape.

### Update `docker-compose.yml`

Add the following service to the existing Docker Compose file:

```yaml
  node-exporter:
    image: prom/node-exporter:latest
    container_name: node-exporter
    ports:
      - "9100:9100"
    volumes:
      - /proc:/host/proc:ro
      - /sys:/host/sys:ro
      - /:/rootfs:ro
    command:
      - '--path.procfs=/host/proc'
      - '--path.sysfs=/host/sys'
      - '--path.rootfs=/rootfs'
      - '--collector.filesystem.mount-points-exclude=^/(sys|proc|dev|host|etc)($$|/)'
    restart: unless-stopped
```

### Why are these volume mounts required?

| Mount | Purpose |
|---|---|
| `/proc` | Provides kernel and process information, including CPU and memory statistics. |
| `/sys` | Provides system, hardware, and driver information. |
| `/` | Provides filesystem information used to collect disk and filesystem metrics. |
| `:ro` | Mounts the paths as read-only so the exporter does not modify them. |

**Note:** These mounts are designed for Linux environments. On Windows or macOS with Docker Desktop, Node Exporter may report metrics from the Linux VM rather than the physical host. Some host metrics may therefore be limited.

### Configure Prometheus

Update `prometheus.yml`:

```yaml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: "prometheus"
    static_configs:
      - targets: ["prometheus:9090"]

  - job_name: "node-exporter"
    static_configs:
      - targets: ["node-exporter:9100"]
```

**Important:** The service names are used because the containers communicate through Docker Compose's internal network.

### Restart the stack

```bash
docker compose up -d
```

Verify the exporter endpoint:

```bash
curl http://localhost:9100/metrics
```

On Windows, you can also open `http://localhost:9100/metrics` in your browser.

Open Prometheus at `http://localhost:9090` and navigate to **Status → Targets**.

The `node-exporter` target should show as `UP`.

### Explore host metrics using PromQL

**CPU time per core:**

```promql
node_cpu_seconds_total{mode="idle"}
```

This shows the accumulated CPU time spent in idle mode for each CPU core.

**Total memory:**

```promql
node_memory_MemTotal_bytes
```

**Available memory:**

```promql
node_memory_MemAvailable_bytes
```

**Memory usage percentage:**

```promql
(1 - node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes) * 100
```

**Filesystem usage percentage:**

```promql
(1 - node_filesystem_avail_bytes / node_filesystem_size_bytes) * 100
```

**Network receive rate:**

```promql
rate(node_network_receive_bytes_total[5m])
```

These queries help us understand host resource usage and identify potential resource bottlenecks.

---

## 3. Add cAdvisor for Container Metrics

cAdvisor (Container Advisor) monitors resource usage and performance of running containers.

It exposes metrics such as container CPU usage, memory consumption, and network activity.

### Update `docker-compose.yml`

Add the following service:

```yaml
  cadvisor:
    image: gcr.io/cadvisor/cadvisor:latest
    container_name: cadvisor
    ports:
      - "8080:8080"
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro
      - /sys:/sys:ro
      - /var/lib/docker/:/var/lib/docker:ro
    restart: unless-stopped
```

### Why are these volume mounts required?

| Mount | Purpose |
|---|---|
| `/var/run/docker.sock` | Allows cAdvisor to discover and inspect Docker containers. |
| `/sys` | Provides kernel and control-group information used for resource statistics. |
| `/var/lib/docker/` | Provides access to Docker's container storage information. |
| `:ro` | Mounts the paths as read-only where supported. |

**Security note:** Access to the Docker socket can provide significant control over the Docker environment. Only grant this access to trusted components.

### Configure Prometheus

Add the cAdvisor scrape job to `prometheus.yml`:

```yaml
  - job_name: "cadvisor"
    static_configs:
      - targets: ["cadvisor:8080"]
```

Your complete `scrape_configs` section should now contain all three jobs:

```yaml
scrape_configs:
  - job_name: "prometheus"
    static_configs:
      - targets: ["prometheus:9090"]

  - job_name: "node-exporter"
    static_configs:
      - targets: ["node-exporter:9100"]

  - job_name: "cadvisor"
    static_configs:
      - targets: ["cadvisor:8080"]
```

Restart the stack:

```bash
docker compose up -d
```

Verify cAdvisor at `http://localhost:8080`.

Open Prometheus → **Status → Targets** and confirm that the `cadvisor` target is `UP`.

### Explore container metrics using PromQL

**CPU usage rate per container:**

```promql
rate(container_cpu_usage_seconds_total{name!=""}[5m])
```

This returns CPU usage in CPU-seconds per second for matching containers.

**Memory usage per container:**

```promql
container_memory_usage_bytes{name!=""}
```

**Network receive rate per container:**

```promql
rate(container_network_receive_bytes_total{name!=""}[5m])
```

**Top three containers by memory usage:**

```promql
topk(3, container_memory_usage_bytes{name!=""})
```

The `{name!=""}` filter excludes series with an empty `name` label. The exact labels and available metrics can vary by environment and cAdvisor version.

### Node Exporter vs. cAdvisor

| Feature | Node Exporter | cAdvisor |
|---|---|---|
| Monitoring scope | Host/system level | Container level |
| CPU metrics | Host CPU statistics | Individual container CPU usage |
| Memory metrics | Host memory statistics | Container memory consumption |
| Disk metrics | Host filesystems and disk-related statistics | Container-related storage metrics, depending on the environment |
| Network metrics | Host network interfaces | Container network activity |
| Example use | Investigating high host CPU usage | Identifying a container consuming excessive memory |

**When should we use each?**

Use Node Exporter when you need to understand the health and resource utilization of the host machine.

Use cAdvisor when you need visibility into the resource consumption of individual Docker containers.

Together, they help distinguish host-level problems from container-level resource issues.

---

## 4. Set Up Grafana

Grafana is a visualization and observability platform. It connects to data sources such as Prometheus and allows us to build dashboards, explore metrics, and configure alerts.

### Add Grafana to `docker-compose.yml`

```yaml
  grafana:
    image: grafana/grafana-enterprise:latest
    container_name: grafana
    ports:
      - "3000:3000"
    volumes:
      - grafana_data:/var/lib/grafana
    environment:
      - GF_SECURITY_ADMIN_USER=admin
      - GF_SECURITY_ADMIN_PASSWORD=admin123
    restart: unless-stopped
```

Add the named volume at the bottom of your existing Compose file:

```yaml
volumes:
  prometheus_data:
  grafana_data:
```

**Important:** Keep any other existing named volumes, including those used by your notes application.

Start the stack:

```bash
docker compose up -d
```

Open Grafana at `http://localhost:3000`.

For this local practice setup, log in using:

- Username: `admin`
- Password: `admin123`

Change the default password before using Grafana in a shared or production environment.

### Configure Prometheus as a data source

1. Open **Connections → Data Sources**.
2. Select **Add data source**.
3. Choose **Prometheus**.
4. Set the URL to:

   ```text
   http://prometheus:9090
   ```

5. Click **Save & Test**.

Grafana should successfully connect to the Prometheus API.

**Why use `http://prometheus:9090` instead of `http://localhost:9090`?**

Grafana and Prometheus run in separate containers. Inside the Grafana container, `localhost` refers to Grafana itself. The hostname `prometheus` resolves to the Prometheus service through the shared Docker Compose network.

---

## 5. Build a Custom Grafana Dashboard

Create a dashboard that displays host and container health.

Navigate to **Dashboards → New → New Dashboard → Add Visualization**. Select Prometheus as the data source for each panel.

Create the following five panels.

### Panel 1: CPU Usage %

**PromQL query:**

```promql
100 - (avg(rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)
```

- Visualization: Gauge
- Title: `CPU Usage %`
- Unit: Percent (0–100)
- Suggested thresholds: Green below 60, yellow from 60 to below 80, red at 80 and above.

This query estimates average host CPU utilization across the CPU cores represented by the metric.

### Panel 2: Memory Usage %

**PromQL query:**

```promql
(1 - node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes) * 100
```

- Visualization: Gauge
- Title: `Memory Usage %`
- Unit: Percent (0–100)

This shows the percentage of total host memory that is not currently available.

### Panel 3: Container CPU Usage

**PromQL query:**

```promql
rate(container_cpu_usage_seconds_total{name!=""}[5m]) * 100
```

- Visualization: Time series
- Title: `Container CPU Usage`
- Legend: `{{name}}`
- Unit: Percent

The query shows CPU consumption as a percentage of one CPU core's capacity. Values may exceed 100% when a container uses multiple cores.

### Panel 4: Container Memory Usage

**PromQL query:**

```promql
container_memory_usage_bytes{name!=""} / 1024 / 1024
```

- Visualization: Bar chart
- Title: `Container Memory (MB)`
- Legend: `{{name}}`
- Unit: MiB, if available in the Grafana version.

This converts memory values from bytes to mebibytes (MiB).

### Panel 5: Disk Usage %

**PromQL query:**

```promql
(1 - node_filesystem_avail_bytes{mountpoint="/"} / node_filesystem_size_bytes{mountpoint="/"}) * 100
```

- Visualization: Stat
- Title: `Disk Usage %`
- Unit: Percent (0–100)

This estimates filesystem usage for the root mount point. If the metric is unavailable, inspect the available `node_filesystem_*` series and select the appropriate mount point and filesystem.

### Save the dashboard

Save the dashboard with this name:

**DevOps Observability Overview**

The dashboard now provides a quick view of host CPU and memory usage, container resource consumption, and disk utilization.

---

## 6. Automatically Provision the Prometheus Data Source

Manually configuring a data source through the Grafana UI works for practice, but repeating the process across environments can be time-consuming.

Grafana supports provisioning through YAML configuration files, making data-source configuration repeatable and easier to manage through version control.

### Create the directory structure

From the directory containing `docker-compose.yml`, run:

```bash
mkdir -p grafana/provisioning/datasources
mkdir -p grafana/provisioning/dashboards
```

On Windows, these commands work in Git Bash. You can also create the folders using File Explorer.

### Create `grafana/provisioning/datasources/datasources.yml`

```yaml
apiVersion: 1

datasources:
  - name: Prometheus
    type: prometheus
    access: proxy
    url: http://prometheus:9090
    isDefault: true
    editable: false
```

### Update the Grafana service

Add the provisioning mount to the existing Grafana service:

```yaml
  grafana:
    image: grafana/grafana-enterprise:latest
    container_name: grafana
    ports:
      - "3000:3000"
    volumes:
      - grafana_data:/var/lib/grafana
      - ./grafana/provisioning:/etc/grafana/provisioning
    environment:
      - GF_SECURITY_ADMIN_USER=admin
      - GF_SECURITY_ADMIN_PASSWORD=admin123
    restart: unless-stopped
```

Ensure the top-level volume definitions still include both `prometheus_data` and `grafana_data`, as well as any other volumes already required by your application.

Restart Grafana:

```bash
docker compose up -d grafana
```

Check **Connections → Data Sources**. Prometheus should be configured automatically.

### Why is YAML provisioning better than manual configuration?

- **Repeatability:** The same data-source settings can be reused across environments.
- **Version control:** Configuration changes can be tracked in Git.
- **Automation:** New environments can start with the required data source already configured.
- **Consistency:** Reduces manual configuration errors between development, staging, and production.

Provisioning also makes it easier to maintain observability configuration alongside application infrastructure.

---

## 7. Import Community Dashboards

Grafana provides community dashboards that can be imported instead of building every panel manually.

### Import Node Exporter Full

1. Navigate to **Dashboards → New → Import**.
2. Enter dashboard ID `1860`.
3. Select your Prometheus data source.
4. Click **Import**.

The Node Exporter Full dashboard includes panels for host CPU, memory, filesystem, disk, and network metrics.

### Import a Docker monitoring dashboard

1. Navigate to **Dashboards → New → Import**.
2. Enter dashboard ID `193`.
3. Select your Prometheus data source.
4. Import the dashboard and explore its container monitoring panels.

Dashboard compatibility depends on the dashboard's expected metrics, labels, and exporter versions. If a panel shows no data, check its queries and verify that the required metrics are available in Prometheus.

---

## 8. Verify the Complete Setup

Check the running containers:

```bash
docker compose ps
```

Confirm that the following services are running:

- Prometheus
- Node Exporter
- cAdvisor
- Grafana
- Notes application from Day 73, if retained in the existing Compose setup

### Verification checklist

- [ ] Node Exporter is accessible on port `9100`.
- [ ] cAdvisor is accessible on port `8080`.
- [ ] Prometheus is accessible on port `9090`.
- [ ] Grafana is accessible on port `3000`.
- [ ] Node Exporter target shows `UP` in Prometheus.
- [ ] cAdvisor target shows `UP` in Prometheus.
- [ ] Prometheus data source passes Grafana's connection test.
- [ ] The custom dashboard contains CPU, memory, container, and disk panels.
- [ ] Prometheus data-source provisioning works through YAML.
- [ ] Community dashboards have been explored.

---

## 9. Troubleshooting

### Exporter target is DOWN

Check the running containers:

```bash
docker compose ps
docker compose logs node-exporter
docker compose logs cadvisor
docker compose logs prometheus
```

Verify that the service names in `prometheus.yml` match the Docker Compose service names.

### Grafana shows "No data"

1. Confirm that the Prometheus data source is configured correctly.
2. Run the same PromQL query in the Prometheus UI.
3. Verify that the required metric exists.
4. Check that the target is `UP`.
5. Confirm that the dashboard's time range includes recent data.

### Metrics are missing on Docker Desktop

Docker Desktop runs Linux containers inside a Linux virtual machine on Windows and macOS. Node Exporter may therefore expose VM-level metrics rather than all physical-host metrics. cAdvisor's available container metrics can also vary with the Docker environment.

### Port conflicts

If a port is already in use, change the host side of the port mapping while keeping the container port unchanged. For example:

```yaml
ports:
  - "3001:3000"
```

Grafana would then be accessible at `http://localhost:3001`.

---

## 10. Key Takeaways

- **Node Exporter** provides host-level metrics.
- **cAdvisor** provides container-level resource metrics.
- **Prometheus** scrapes, stores, and queries metrics using PromQL.
- **Grafana** turns collected metrics into dashboards that are easier to understand.
- **YAML provisioning** makes data-source configuration repeatable and suitable for version control.
- **Community dashboards** provide reusable visualizations for common monitoring scenarios.

Observability becomes more useful when we combine metric collection with visualization. Instead of relying only on raw PromQL queries, dashboards help us identify resource trends and investigate system health more efficiently.

## References

- [Observability Project Repository](https://github.com/vaishnavipawardottech/observability)
- [Node Exporter](https://github.com/prometheus/node_exporter)
- [cAdvisor](https://github.com/google/cadvisor)
- [Prometheus Documentation](https://prometheus.io/docs/)
- [Grafana Documentation](https://grafana.com/docs/)
- [Grafana Dashboard 1860 — Node Exporter Full](https://grafana.com/grafana/dashboards/1860-node-exporter-full/)
- [Grafana Dashboard 193 — Docker Monitoring](https://grafana.com/grafana/dashboards/193-docker-monitoring/)
- [Reference Repository — Observability for DevOps](https://github.com/LondheShubham153/observability-for-devops)
