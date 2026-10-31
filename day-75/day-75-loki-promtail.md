# Day 75 --- Log Management with Loki and Promtail

## Objective

Metrics help us identify what changed; logs can provide clues about why
it changed. This task adds Loki and Promtail to the Prometheus, Node
Exporter, cAdvisor, and Grafana stack.

## Task 1 --- Understand the logging pipeline

``` text
Docker containers -> Promtail -> Loki -> Grafana Explore -> Engineer
     write logs      collect      store     query with LogQL
```

-   **Docker containers:** Applications commonly write logs to stdout
    and stderr. With Docker's `json-file` logging driver, Docker writes
    JSON log files.
-   **Promtail:** Reads configured log files, tracks its reading
    position, attaches labels, and pushes entries to Loki.
-   **Loki:** Stores log chunks and indexes labels such as `job` and
    `container_name`.
-   **Grafana:** Uses LogQL to search logs and can display logs
    alongside Prometheus metrics.

### Why does Loki index labels instead of the full log text?

Loki indexes labels rather than creating a full-text index for every
word in every log line. After labels select relevant log streams, Loki
filters the stored log content.

**Benefits:** less indexing overhead, often lower resource/storage cost,
and a label model familiar to Prometheus users.

**Trade-off:** broad searches for arbitrary words may need to scan many
log lines and can be slower than full-text search. Label design matters:
high-cardinality labels such as request IDs or user IDs can create too
many streams and hurt performance.

Loki is useful for cost-conscious, label-oriented log aggregation.
Elasticsearch-based solutions may be preferable when powerful full-text
search is a primary requirement.

## Task 2 --- Add Loki to the stack

Create `loki/loki-config.yml`:

``` yaml
auth_enabled: false

server:
  http_listen_port: 3100

common:
  ring:
    instance_addr: 127.0.0.1
    kvstore:
      store: inmemory
  replication_factor: 1
  path_prefix: /loki

schema_config:
  configs:
    - from: 2020-10-24
      store: tsdb
      object_store: filesystem
      schema: v13
      index:
        prefix: index_
        period: 24h

storage_config:
  filesystem:
    directory: /loki/chunks
```

### What the settings mean

-   `auth_enabled: false`: disables tenant authentication for this local
    learning setup; do not expose it publicly.
-   `http_listen_port: 3100`: Loki HTTP API port.
-   `kvstore.store: inmemory`: keeps ring information in memory for a
    single instance.
-   `replication_factor: 1`: no replication; suitable only for a
    learning setup.
-   `path_prefix: /loki`: base path for Loki storage.
-   `store: tsdb` and `schema: v13`: configure the index schema.
-   `object_store: filesystem`: stores chunks on local disk.
-   `period: 24h`: sets the index period.

Compose service:

``` yaml
loki:
  image: grafana/loki:latest
  container_name: loki
  ports:
    - "3100:3100"
  volumes:
    - ./loki/loki-config.yml:/etc/loki/loki-config.yml:ro
    - loki_data:/loki
  command:
    - -config.file=/etc/loki/loki-config.yml
  restart: unless-stopped
```

Add `loki_data:` under the top-level `volumes:` section alongside
existing volumes. Start and verify:

``` bash
docker compose up -d loki
docker compose logs loki
curl http://localhost:3100/ready
```

When Loki is ready, the endpoint should return `ready`.

## Task 3 --- Add Promtail to collect container logs

Create `promtail/promtail-config.yml`:

``` yaml
server:
  http_listen_port: 9080
  grpc_listen_port: 0

positions:
  filename: /tmp/positions.yaml

clients:
  - url: http://loki:3100/loki/api/v1/push

scrape_configs:
  - job_name: docker
    static_configs:
      - targets:
          - localhost
        labels:
          job: docker
          __path__: /var/lib/docker/containers/*/*-json.log
    pipeline_stages:
      - docker: {}
```

### What the settings mean

-   `server`: exposes Promtail's HTTP endpoint on port 9080.
-   `positions.filename`: tracks how far each file has been read, like a
    bookmark. If deleted, Promtail may re-read logs and send duplicates.
-   `clients.url`: Loki push endpoint. `loki` is the Compose service
    name.
-   `job_name` / `job`: identifies this collection job.
-   `__path__`: glob pattern for Docker JSON log files.
-   `docker` pipeline stage: parses the Docker JSON log envelope to
    extract the timestamp, stream, and message.

Compose service:

``` yaml
promtail:
  image: grafana/promtail:latest
  container_name: promtail
  volumes:
    - ./promtail/promtail-config.yml:/etc/promtail/promtail-config.yml:ro
    - /var/lib/docker/containers:/var/lib/docker/containers:ro
  command:
    - -config.file=/etc/promtail/promtail-config.yml
  depends_on:
    - loki
  ports:
    - "9080:9080"
  restart: unless-stopped
```

The Docker socket is not required by this static file-scraping
configuration. It is commonly mounted when using Docker service
discovery to obtain container metadata.

**Platform note:** The `/var/lib/docker/containers` path is typical on
Linux with Docker's `json-file` driver. On Docker Desktop for
Windows/macOS, logs live inside Docker's Linux VM and may not be
accessible via that host path. If no logs arrive, verify the logging
driver and the path available inside the Promtail container.

Start the stack and check targets:

``` bash
docker compose up -d
docker compose logs promtail
```

Open `http://localhost:9080/targets`. To generate logs, use your
application's real endpoint. The task's example is:

``` bash
for i in $(seq 1 20); do curl -s http://localhost:8000 > /dev/null; done
```

Replace port 8000 if your application uses another port. Check
`docker logs <container-name>` to verify the application actually writes
logs to stdout/stderr.

## Task 4 --- Add Loki as a Grafana data source

Update `grafana/provisioning/datasources/datasources.yml`:

``` yaml
apiVersion: 1

datasources:
  - name: Prometheus
    type: prometheus
    access: proxy
    url: http://prometheus:9090
    isDefault: true
    editable: false

  - name: Loki
    type: loki
    access: proxy
    url: http://loki:3100
    editable: false
```

Keep any existing data sources you need. Restart Grafana:

``` bash
docker compose restart grafana
```

In **Connections → Data sources**, confirm Prometheus and Loki are
listed. Alternatively, add Loki manually and set its URL to
`http://loki:3100` from inside the Compose network, then select **Save &
test**.

## Full Compose stack example

Merge the following services with your existing `docker-compose.yml`;
preserve project-specific ports, volumes, and configuration. This
example assumes you already have `prometheus.yml` and the two Grafana
provisioning files.

``` yaml
services:
  prometheus:
    image: prom/prometheus:latest
    container_name: prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml:ro
      - prometheus_data:/prometheus
    command: ["--config.file=/etc/prometheus/prometheus.yml"]
    restart: unless-stopped

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
      - --path.procfs=/host/proc
      - --path.sysfs=/host/sys
      - --path.rootfs=/rootfs
    restart: unless-stopped

  cadvisor:
    image: gcr.io/cadvisor/cadvisor:latest
    container_name: cadvisor
    ports:
      - "8080:8080"
    volumes:
      - /:/rootfs:ro
      - /var/run:/var/run:ro
      - /sys:/sys:ro
      - /var/lib/docker/:/var/lib/docker:ro
      - /dev/disk/:/dev/disk:ro
    restart: unless-stopped

  grafana:
    image: grafana/grafana:latest
    container_name: grafana
    ports:
      - "3000:3000"
    volumes:
      - grafana_data:/var/lib/grafana
      - ./grafana/provisioning/datasources:/etc/grafana/provisioning/datasources:ro
    depends_on:
      - prometheus
      - loki
    restart: unless-stopped

  loki:
    image: grafana/loki:latest
    container_name: loki
    ports:
      - "3100:3100"
    volumes:
      - ./loki/loki-config.yml:/etc/loki/loki-config.yml:ro
      - loki_data:/loki
    command: ["-config.file=/etc/loki/loki-config.yml"]
    restart: unless-stopped

  promtail:
    image: grafana/promtail:latest
    container_name: promtail
    volumes:
      - ./promtail/promtail-config.yml:/etc/promtail/promtail-config.yml:ro
      - /var/lib/docker/containers:/var/lib/docker/containers:ro
    command: ["-config.file=/etc/promtail/promtail-config.yml"]
    depends_on:
      - loki
    ports:
      - "9080:9080"
    restart: unless-stopped

volumes:
  prometheus_data:
  grafana_data:
  loki_data:
```

Example `prometheus.yml` scrape targets (retain any existing targets
too):

``` yaml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: prometheus
    static_configs:
      - targets: ["prometheus:9090"]
  - job_name: node-exporter
    static_configs:
      - targets: ["node-exporter:9100"]
  - job_name: cadvisor
    static_configs:
      - targets: ["cadvisor:8080"]
```

Validate and start:

``` bash
docker compose config
docker compose up -d
docker compose ps
```

## Task 5 --- Query logs with LogQL

In Grafana, open **Explore**, select **Loki**, and try these queries.
The labels available depend on your Promtail configuration.

### Query 1: all collected Docker logs

``` logql
{job="docker"}
```

Returns log entries from streams labeled `job="docker"`.

### Query 2: logs for a named container

``` logql
{container_name="prometheus"}
```

Returns logs labeled with `container_name="prometheus"`. **Important:**
the static Promtail config above only adds `job="docker"`; it does not
automatically create `container_name`. If this returns no results,
inspect available labels and configure Docker discovery/relabeling or
another collection method to add the container label.

### Query 3: lines containing `error`

``` logql
{job="docker"} |= "error"
```

Returns lines containing the case-sensitive text `error`.
Case-insensitive version:

``` logql
{job="docker"} |~ "(?i)error"
```

### Query 4: exclude health-check noise

``` logql
{job="docker"} != "health"
```

Excludes lines containing the case-sensitive text `health`.

### Query 5: HTTP 4xx or 5xx status patterns

``` logql
{job="docker"} |~ "status=[45]\\d{2}"
```

Matches lines such as `status=404` or `status=500`, if logs use this
format.

### Additional useful queries

Count entries over five-minute windows:

``` logql
count_over_time({job="docker"}[5m])
```

Log-entry rate per second over five minutes:

``` logql
rate({job="docker"}[5m])
```

Top five containers by log rate, if `container_name` is available:

``` logql
topk(5, sum by (container_name) (rate({job="docker"}[5m])))
```

### Exercise: notes-app errors in the last hour

``` logql
{container_name="notes-app"} |= "error"
```

Set Grafana's time picker to **Last 1 hour**. For case-insensitive
search, use:

``` logql
{container_name="notes-app"} |~ "(?i)error"
```

This assumes the stream has the `container_name="notes-app"` label.

### Exercise: count error lines per minute

Count matching lines in one-minute windows:

``` logql
sum by (container_name) (
  count_over_time({container_name="notes-app"} |~ "(?i)error" [1m])
)
```

Or calculate the per-second rate of error lines over one-minute windows:

``` logql
sum by (container_name) (
  rate({container_name="notes-app"} |~ "(?i)error" [1m])
)
```

The first query counts matching lines per one-minute range; the second
reports a rate. Both require the container label.

## Task 6 --- Correlate metrics and logs

### Add a logs panel to the Day 74 dashboard

1.  Open the existing dashboard and add a panel.
2.  Select Loki as the data source.
3.  Query `{job="docker"}`.
4.  Select the **Logs** visualization.
5.  Set the title to **Container Logs**, then apply and save.

### Compare CPU metrics and logs in Explore split view

Prometheus query for the left panel:

``` promql
rate(container_cpu_usage_seconds_total{name="notes-app"}[5m])
```

Loki query for the right panel:

``` logql
{container_name="notes-app"}
```

Use the same time range in both panels. These example labels must exist
in your environment; cAdvisor metric labels vary, and the static
Promtail configuration above does not add `container_name` by itself.
Inspect available labels and adjust your configuration/query if
necessary.

### How does Grafana help incident response?

Having metrics and logs in the same interface reduces context switching.
An engineer can spot a CPU or memory anomaly, focus on that time range,
and inspect log messages from the same period for errors, retries, or
unusual activity. Metrics indicate **what changed**; logs can provide
evidence about **why it changed**. Logs are clues, not automatic proof
of root cause.

## Loki vs. ELK

  -----------------------------------------------------------------------
  Area                    Loki + Grafana          ELK (Elasticsearch,
                                                  Logstash, Kibana)
  ----------------------- ----------------------- -----------------------
  Indexing                Indexes labels; log     Elasticsearch commonly
                          content is filtered     indexes searchable text
                          after selecting         and fields for richer
                          streams.                full-text search.

  Cost and resources      Often lighter for       Indexing more text can
                          label-based log         need more storage and
                          exploration; depends on compute.
                          volume and retention.   

  Querying                LogQL selectors,        Elasticsearch Query DSL
                          filters, and            and Kibana
                          aggregations.           search/analysis.

  Good fit                Teams using             Search-heavy workflows,
                          Prometheus/Grafana that advanced full-text
                          need straightforward    search, and detailed
                          service/container log   indexed-field analysis.
                          exploration.            

  Trade-off               Broad text searches may Rich search can come
                          scan lots of log lines; with greater
                          label design matters.   operational and
                                                  resource overhead.
  -----------------------------------------------------------------------

**When to use which:** Choose Loki when label-based log exploration
alongside Prometheus metrics is sufficient and simplicity matters.
Consider ELK when advanced full-text search and indexed-field analysis
are central requirements. The best choice depends on query patterns,
scale, budget, and team expertise.

## Screenshots to add

Screenshots must be captured from your own running environment. Add
these two images to your repository:

1.  **Grafana Explore with Loki logs:** show `{job="docker"}` and
    visible log entries.
2.  **Metrics and logs side by side:** show the Prometheus CPU query and
    Loki logs query with the same time range.

Suggested Markdown once the screenshots are saved:

``` markdown
### Grafana Explore — Loki logs
![Grafana Explore showing Loki logs](screenshots/day-75-loki-explore.png)

### Metrics and logs side by side
![Prometheus metrics and Loki logs in Grafana Explore](screenshots/day-75-metrics-logs-split.png)
```

## Troubleshooting

-   **Loki not ready:** check `docker compose ps`,
    `docker compose logs loki`, and `curl http://localhost:3100/ready`.
-   **No logs:** inspect `docker compose logs promtail`, open
    `http://localhost:9080/targets`, verify the mounted path, Docker
    logging driver, file permissions, and Loki reachability.
-   **No `container_name` results:** the basic static scrape config does
    not add that label. Inspect labels and configure
    discovery/relabeling if container-specific queries are needed.
-   **Duplicate logs after restart:** deleting the positions file may
    cause Promtail to re-read existing log files.
-   **Docker Desktop path issues:** Docker's internal log files may not
    be exposed at `/var/lib/docker/containers` on the host. Confirm the
    path from inside the Promtail container.

## Day 75 checklist

-   [ ] Loki responds at `/ready`.
-   [ ] Promtail is running and can read the expected logs.
-   [ ] Loki is configured as a Grafana data source.
-   [ ] At least five LogQL queries have been tested.
-   [ ] Metrics and logs can be inspected over the same time range.
-   [ ] Both screenshots have been added.
-   [ ] Loki's label-indexing trade-off, incident-response benefit, and
    Loki-vs-ELK comparison are documented.

## References

-   [Grafana Loki documentation](https://grafana.com/docs/loki/latest/)
-   [Promtail
    documentation](https://grafana.com/docs/loki/latest/send-data/promtail/)
-   [LogQL documentation](https://grafana.com/docs/loki/latest/query/)
-   [TrainWithShubham observability-for-devops reference
    repository](https://github.com/LondheShubham153/observability-for-devops)
