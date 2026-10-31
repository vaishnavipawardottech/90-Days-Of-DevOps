# Day 76 --- OpenTelemetry and Alerting

## Objective

Day 76 adds the third pillar of observability---**traces**---to the
metrics and logs stack built on earlier days. It also introduces
alerting, so the system can flag conditions that need attention instead
of requiring someone to watch dashboards continuously.

By the end of this task, the stack includes: - Metrics: Prometheus, Node
Exporter, cAdvisor, and the OpenTelemetry Collector's Prometheus
exporter. - Logs: Promtail and Loki. - Traces: OTLP data received by the
OpenTelemetry Collector and shown in its debug output. - Alerting:
Prometheus alert rules and a Grafana alert rule with a notification
contact point.

> This is a learning setup. The Collector's debug exporter displays
> traces but does not store or visualize them in a trace backend. A
> production tracing setup would typically export to a backend such as
> Jaeger or Grafana Tempo.

## Task 1 --- Understand OpenTelemetry

### What is OpenTelemetry (OTel)?

OpenTelemetry is a vendor-neutral, open-source framework for generating,
collecting, and exporting telemetry data---metrics, logs, and traces. It
is **not a storage or visualization backend**. It helps applications and
infrastructure send telemetry to backends such as Prometheus, Jaeger,
Loki, Datadog, or Grafana Tempo.

### What is the OpenTelemetry Collector?

The Collector is a standalone service that receives, processes, and
exports telemetry. Its pipeline has three main components:

-   **Receivers:** Accept telemetry, for example through OTLP gRPC or
    OTLP HTTP.
-   **Processors:** Modify or prepare telemetry, such as batching,
    filtering, or sampling.
-   **Exporters:** Send telemetry to a destination, such as a
    Prometheus-compatible endpoint or debug output.

``` text
Telemetry source -> Receiver -> Processor -> Exporter -> Backend
```

### What is OTLP?

OTLP means **OpenTelemetry Protocol**. It is the standard protocol used
to transmit telemetry to a Collector or compatible receiver.

-   OTLP/gRPC commonly uses port `4317`.
-   OTLP/HTTP commonly uses port `4318`.

### What are distributed traces?

A trace follows one request as it moves through multiple services. Each
operation is represented by a **span**. A span can include a trace ID,
span ID, parent span ID, start time, duration, and attributes.

``` text
User request
   |
   v
API Gateway (span 1)
   |
   v
Auth Service (span 2)
   |
   v
Database (span 3)
```

A trace helps show where a request spent time or where an operation
failed. In this day's setup, a sample trace is sent to the Collector and
printed in debug output.

## Task 2 --- Add the OpenTelemetry Collector

Create the directory:

``` bash
mkdir -p otel-collector
```

Create `otel-collector/otel-collector-config.yml`:

``` yaml
receivers:
  otlp:
    protocols:
      grpc:
        endpoint: 0.0.0.0:4317
      http:
        endpoint: 0.0.0.0:4318

processors:
  batch:

exporters:
  prometheus:
    endpoint: "0.0.0.0:8889"
  debug:
    verbosity: detailed

service:
  pipelines:
    metrics:
      receivers: [otlp]
      processors: [batch]
      exporters: [prometheus]
    traces:
      receivers: [otlp]
      processors: [batch]
      exporters: [debug]
    logs:
      receivers: [otlp]
      processors: [batch]
      exporters: [debug]
```

### Configuration explanation

-   **OTLP receiver:** Accepts OTLP gRPC at `4317` and OTLP HTTP at
    `4318`.
-   **Batch processor:** Groups telemetry before exporting to reduce
    overhead.
-   **Prometheus exporter:** Exposes Collector-received metrics on port
    `8889`; Prometheus scrapes this endpoint.
-   **Debug exporter:** Writes received traces and logs to the
    Collector's console output.
-   **Metrics pipeline:** OTLP metrics → batch → Prometheus exporter.
-   **Traces pipeline:** OTLP traces → batch → debug output.
-   **Logs pipeline:** OTLP logs → batch → debug output.

Add this service to your existing `docker-compose.yml`:

``` yaml
otel-collector:
  image: otel/opentelemetry-collector-contrib:latest
  container_name: otel-collector
  ports:
    - "4317:4317"   # OTLP gRPC
    - "4318:4318"   # OTLP HTTP
    - "8889:8889"   # Prometheus exporter endpoint
  volumes:
    - ./otel-collector/otel-collector-config.yml:/etc/otelcol-contrib/config.yaml:ro
  restart: unless-stopped
```

Add the Collector as a Prometheus scrape target in `prometheus.yml`:

``` yaml
- job_name: "otel-collector"
  static_configs:
    - targets: ["otel-collector:8889"]
```

Keep your existing Prometheus scrape jobs. Make sure the Prometheus
container mounts the updated `prometheus.yml`.

Start the stack:

``` bash
docker compose up -d
```

Verify the Collector:

``` bash
docker logs otel-collector 2>&1 | tail -5
```

Then open Prometheus at `http://localhost:9090` → **Status → Targets**.
The `otel-collector` target should be **UP**.

## Task 3 --- Send test telemetry to the Collector

### Send a sample OTLP trace

Run this from your host machine:

``` bash
curl -X POST http://localhost:4318/v1/traces \
  -H "Content-Type: application/json" \
  -d '{
    "resourceSpans": [{
      "resource": {
        "attributes": [{
          "key": "service.name",
          "value": { "stringValue": "my-test-service" }
        }]
      },
      "scopeSpans": [{
        "spans": [{
          "traceId": "5b8efff798038103d269b633813fc60c",
          "spanId": "eee19b7ec3c1b174",
          "name": "test-span",
          "kind": 1,
          "startTimeUnixNano": "1544712660000000000",
          "endTimeUnixNano": "1544712661000000000",
          "attributes": [{
            "key": "http.method",
            "value": { "stringValue": "GET" }
          }, {
            "key": "http.status_code",
            "value": { "intValue": "200" }
          }]
        }]
      }]
    }]
  }'
```

Look for the span in the Collector logs:

``` bash
docker logs otel-collector 2>&1 | grep -A 10 "test-span"
```

The debug exporter should print span information, including the service
and span details. This confirms the OTLP trace reached the Collector. It
is not yet a stored, searchable trace in Grafana.

### Send a sample OTLP metric

``` bash
curl -X POST http://localhost:4318/v1/metrics \
  -H "Content-Type: application/json" \
  -d '{
    "resourceMetrics": [{
      "resource": {
        "attributes": [{
          "key": "service.name",
          "value": { "stringValue": "my-test-service" }
        }]
      },
      "scopeMetrics": [{
        "metrics": [{
          "name": "test_requests_total",
          "sum": {
            "dataPoints": [{
              "asInt": "42",
              "startTimeUnixNano": "1544712660000000000",
              "timeUnixNano": "1544712661000000000"
            }],
            "aggregationTemporality": 2,
            "isMonotonic": true
          }
        }]
      }]
    }]
  }'
```

In Prometheus, query:

``` promql
test_requests_total
```

The metric travels through this pipeline:

``` text
curl -> OTLP receiver -> batch processor -> Collector Prometheus exporter
     -> Prometheus scrapes port 8889 -> PromQL query
```

## Task 4 --- Configure Prometheus alerting rules

Prometheus evaluates alert rules against PromQL expressions. If an
expression remains true for the configured `for` duration, the alert
changes from pending to firing.

Create `alert-rules.yml`:

``` yaml
groups:
  - name: system-alerts
    rules:
      - alert: HighCPUUsage
        expr: 100 - (avg(rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100) > 80
        for: 2m
        labels:
          severity: warning
        annotations:
          summary: "High CPU usage detected"
          description: "CPU usage has been above 80% for more than 2 minutes. Current value: {{ $value }}%"

      - alert: HighMemoryUsage
        expr: (1 - node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes) * 100 > 85
        for: 2m
        labels:
          severity: warning
        annotations:
          summary: "High memory usage detected"
          description: "Memory usage is above 85%. Current value: {{ $value }}%"

      - alert: ContainerDown
        expr: absent(container_last_seen{name="notes-app"})
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "Container is down"
          description: "The notes-app container has not been seen for over 1 minute"

      - alert: TargetDown
        expr: up == 0
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "Scrape target is down"
          description: "{{ $labels.job }} target {{ $labels.instance }} is unreachable"

      - alert: HighDiskUsage
        expr: (1 - node_filesystem_avail_bytes{mountpoint="/"} / node_filesystem_size_bytes{mountpoint="/"}) * 100 > 90
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "Disk space running low"
          description: "Root filesystem usage is above 90%. Current value: {{ $value }}%"
```

### What the alert fields mean

-   `expr`: PromQL condition that determines when the alert is active.
-   `for`: condition must remain true for this duration before firing;
    helps avoid firing on brief spikes.
-   `labels`: metadata such as `severity` that can be used to route
    alerts.
-   `annotations`: human-readable summary and description shown in the
    alert UI and notifications.

### What each alert detects

  -----------------------------------------------------------------------
  Alert                   Condition               Why it matters
  ----------------------- ----------------------- -----------------------
  `HighCPUUsage`          CPU usage above 80% for Signals sustained CPU
                          2 minutes               pressure.

  `HighMemoryUsage`       Memory usage above 85%  Warns of limited
                          for 2 minutes           available memory.

  `ContainerDown`         The `notes-app`         Detects when that
                          `container_last_seen`   container's metric
                          series is absent        series disappears, if
                                                  the expected
                                                  metric/label is
                                                  available.

  `TargetDown`            A Prometheus scrape     Indicates a monitored
                          target reports          target cannot be
                          `up == 0` for 1 minute  scraped.

  `HighDiskUsage`         Root filesystem usage   Warns that disk space
                          above 90% for 5 minutes may run out.
  -----------------------------------------------------------------------

**Note:** These rules depend on the metric names and labels available in
your setup. For example, cAdvisor versions can expose different
container labels, and Node Exporter filesystem metrics may include
multiple devices. Inspect the actual series in Prometheus and adapt
selectors as needed.

Update `prometheus.yml` to load the rules and retain your scrape jobs:

``` yaml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

rule_files:
  - /etc/prometheus/alert-rules.yml

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

  - job_name: "otel-collector"
    static_configs:
      - targets: ["otel-collector:8889"]
```

Mount `alert-rules.yml` in the Prometheus service:

``` yaml
volumes:
  - ./prometheus.yml:/etc/prometheus/prometheus.yml:ro
  - ./alert-rules.yml:/etc/prometheus/alert-rules.yml:ro
  - prometheus_data:/prometheus
```

Keep any other existing Prometheus volumes. Restart Prometheus:

``` bash
docker compose up -d prometheus
```

In Prometheus, open **Status → Rules** to verify the five rules loaded.
Open **Alerts** to inspect their state:

-   **Inactive:** condition is not currently true.
-   **Pending:** condition is true but the `for` duration has not
    elapsed.
-   **Firing:** condition has remained true for the configured duration.

### Test an alert

The task suggests stopping the notes-app container:

``` bash
docker compose stop notes-app
```

Wait 1--2 minutes and inspect Prometheus Alerts. Restart the app
afterward:

``` bash
docker compose start notes-app
```

`TargetDown` fires only for scrape targets. If notes-app itself is not
configured as a Prometheus scrape target, stopping it will not
necessarily trigger `TargetDown`; the `ContainerDown` rule depends on
cAdvisor exposing the matching `container_last_seen` series and labels.

## Task 5 --- Set up Grafana alerts

Grafana-managed alert rules can evaluate queries and send notifications
through configured contact points.

### Create a contact point

1.  Open **Alerting → Contact points → Add contact point**.
2.  Name it `DevOps Team`.
3.  Choose an integration such as email or Slack webhook.
4.  For email, enter your own intended notification address; for Slack,
    configure a valid webhook.
5.  Save the contact point.

A contact point needs valid delivery configuration to actually send
notifications.

### Create a Grafana alert rule

1.  Go to **Alerting → Alert rules → New alert rule**.

2.  Name the rule `High Container Memory`.

3.  Use this query:

    ``` promql
    container_memory_usage_bytes{name="notes-app"} / 1024 / 1024
    ```

4.  Set the condition to **IS ABOVE 100** (more than 100 MiB, using the
    query's conversion).

5.  Evaluate every `1m`, with a pending period of `2m`.

6.  Add the label `severity=warning`.

7.  Link the rule to the `DevOps Team` contact point through the
    notification policy.

8.  Save the rule.

The `name="notes-app"` selector must match the labels emitted by your
cAdvisor setup. If it does not, inspect the metric's labels and update
the selector.

### Configure notification policy

1.  Open **Alerting → Notification policies**.
2.  Set the default contact point to `DevOps Team`.
3.  Optionally add a nested policy matching `severity=critical` and
    route it to a separate contact point or use a different notification
    configuration.
4.  Save and review the policy tree.

Under **Alerting → Alert rules**, inspect whether the rule is
**Normal**, **Pending**, or **Firing**.

### Prometheus alerts vs. Grafana alerts

  -----------------------------------------------------------------------
  Prometheus alerting rules           Grafana alerting
  ----------------------------------- -----------------------------------
  Rules are configured in files and   Rules are managed through Grafana's
  evaluated by Prometheus against     alerting UI or provisioning and can
  PromQL.                             evaluate data sources Grafana
                                      supports.

  Convenient for alerts close to      Convenient for a unified alerting
  Prometheus metrics and              UI, multiple data sources, and
  version-controlled rule files.      contact-point/policy setup.

  Prometheus shows alert states.      Grafana includes contact points and
  Notifications typically require     notification policies for
  Alertmanager and its                delivering alerts.
  routing/receiver configuration.     

  Good for infrastructure and         Good when teams want to manage
  Prometheus-centric alert            alerts and notifications centrally
  conditions.                         in Grafana.
  -----------------------------------------------------------------------

Prometheus rule evaluation and notification delivery are separate
concerns. Without Alertmanager configured, Prometheus alert states can
appear in the UI but Prometheus itself will not deliver notifications.
Grafana alerting can be a simpler starting point for notifications in
this learning stack.

## Task 6 --- Full observability architecture

``` text
                         METRICS
[Node Exporter] --------------------\
[cAdvisor] -------------------------+--> [Prometheus] --> [Grafana dashboards]
[OTel Collector :8889] ------------/          |
                                               +--> [Prometheus alert rules]
                                                        |
                                                        +--> Alertmanager
                                                             (if configured)

                          LOGS
[Docker containers] --> [Promtail] --> [Loki] --> [Grafana Explore / dashboards]

                          TRACES
[OTLP curl / instrumented app] --> [OTel Collector] --> [Debug output]
                                                        |
                                                        +--> Future backend:
                                                             Jaeger / Tempo
```

### Services and ports

  ------------------------------------------------------------------------
  Service                                    Port(s) Purpose
  --------------------- ---------------------------- ---------------------
  Prometheus                                    9090 Metrics storage,
                                                     querying, and rule
                                                     evaluation

  Node Exporter                                 9100 Host system metrics

  cAdvisor                                      8080 Container metrics

  Grafana                                       3000 Dashboards, Explore,
                                                     and alerting

  Loki                                          3100 Log storage and
                                                     querying

  Promtail                                      9080 Log collection agent
                                                     and targets endpoint

  OpenTelemetry                   4317 / 4318 / 8889 OTLP gRPC, OTLP HTTP,
  Collector                                          and Prometheus
                                                     exporter

  Notes app                                     8000 Sample application,
                                                     if present in your
                                                     Compose setup
  ------------------------------------------------------------------------

Verify the containers:

``` bash
docker compose ps
```

Compose may show a service as running without a health check being
defined; inspect logs and endpoints as well.

## Screenshots to add

Capture these from your own environment and place them in your
repository:

1.  **Collector trace debug output:** show `test-span` in the Collector
    logs.
2.  **Prometheus Alerts page:** show the configured rules and their
    current states.
3.  **Grafana Alerting:** show the custom `High Container Memory` rule.
4.  **Full architecture diagram:** include the three telemetry
    pipelines.

Example image references after you save the screenshots:

``` markdown
### OTLP trace in Collector debug output
![Trace output from the OpenTelemetry Collector](screenshots/day-76-otel-trace.png)

### Prometheus alert rules
![Prometheus alert rules and states](screenshots/day-76-prometheus-alerts.png)

### Grafana alert rule
![Grafana High Container Memory alert rule](screenshots/day-76-grafana-alert.png)
```

Replace these sample paths with the real screenshot names you commit.

## Day 76 checklist

-   [ ] OpenTelemetry Collector is running.
-   [ ] Prometheus scrapes the Collector's port `8889`.
-   [ ] A sample OTLP trace appears in Collector debug logs.
-   [ ] A sample OTLP metric can be queried in Prometheus.
-   [ ] Five Prometheus alert rules are loaded.
-   [ ] A Grafana alert rule and contact point are configured.
-   [ ] Alert states have been checked.
-   [ ] Screenshots are added to the repository.
-   [ ] The three-pillar architecture and Prometheus-vs-Grafana alerting
    comparison are documented.

## References

-   [OpenTelemetry documentation](https://opentelemetry.io/docs/)
-   [OpenTelemetry Collector
    documentation](https://opentelemetry.io/docs/collector/)
-   [OTLP specification](https://opentelemetry.io/docs/specs/otlp/)
-   [Prometheus alerting
    rules](https://prometheus.io/docs/prometheus/latest/configuration/alerting_rules/)
-   [Grafana alerting
    documentation](https://grafana.com/docs/grafana/latest/alerting/)
-   [TrainWithShubham observability-for-devops reference
    repository](https://github.com/LondheShubham153/observability-for-devops)
