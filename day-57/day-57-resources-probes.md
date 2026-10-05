# Day 57 – Resource Requests, Limits, and Probes

## Overview

On Day 57 of my #90DaysOfDevOps journey, I explored Kubernetes resource management and container health monitoring.

I learned how to define CPU and memory requests and limits, observe `OOMKilled` when a container exceeds its memory limit, understand why Pods remain Pending due to insufficient cluster resources, and configure liveness, readiness, and startup probes.

These configurations help Kubernetes schedule workloads efficiently, maintain application health, and manage traffic reliably.

---

## 1. Resource Requests and Limits

Kubernetes uses resource requests and limits to manage CPU and memory allocation for containers.

### Requests vs Limits

| Resource | Requests                               | Limits                       |
| -------- | -------------------------------------- | ---------------------------- |
| CPU      | Minimum amount used for scheduling     | Maximum CPU usage allowed    |
| Memory   | Amount considered during scheduling    | Maximum memory allowed       |
| Purpose  | Helps scheduler select a suitable node | Enforces resource boundaries |

### Pod Manifest

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: resource-pod
spec:
  containers:
    - name: nginx
      image: nginx:latest
      resources:
        requests:
          cpu: "100m"
          memory: "128Mi"
        limits:
          cpu: "250m"
          memory: "256Mi"
```

### Apply and Verify

```bash
kubectl apply -f resource-pod.yml

kubectl get pod resource-pod

kubectl describe pod resource-pod
```

### Expected Observations

* CPU Request: 100m (0.1 CPU)
* Memory Request: 128Mi
* CPU Limit: 250m
* Memory Limit: 256Mi
* QoS Class: Burstable

### Kubernetes QoS Classes

| QoS Class  | Condition                                                                                          |
| ---------- | -------------------------------------------------------------------------------------------------- |
| Guaranteed | CPU and memory requests equal limits for every container                                           |
| Burstable  | At least one resource request or limit is specified, but the Pod does not meet Guaranteed criteria |
| BestEffort | No CPU or memory requests or limits are specified                                                  |

**Verification:** The Pod belongs to the `Burstable` QoS class because its resource requests are lower than its limits.

---

## 2. OOMKilled – Exceeding Memory Limits

OOMKilled occurs when a container exceeds its available memory limit and the Linux kernel terminates the process.

Unlike CPU, memory cannot be throttled. Exceeding the memory limit can result in termination.

### Pod Manifest

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: oom-pod
spec:
  containers:
    - name: memory-stress
      image: polinux/stress
      command: ["stress"]
      args:
        - "--vm"
        - "1"
        - "--vm-bytes"
        - "200M"
        - "--vm-hang"
        - "1"
      resources:
        requests:
          memory: "50Mi"
        limits:
          memory: "100Mi"
```

### Apply and Monitor

```bash
kubectl apply -f oom-pod.yml

kubectl get pod oom-pod -w

kubectl describe pod oom-pod
```

### Expected Observation

```text
Reason: OOMKilled
Exit Code: 137
```

The container attempts to allocate approximately 200 MB while its memory limit is 100Mi. The container may be restarted depending on its restart policy.

**Verification:**

* Reason: `OOMKilled`
* Exit Code: `137`
* Exit code 137 indicates termination by SIGKILL (128 + 9).

---

## 3. Pending Pod – Requesting Too Much

Kubernetes schedules Pods based on resource requests.

If a Pod requests more CPU or memory than any available node can provide, it remains in the Pending state.

### Pod Manifest

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: resource-pending-pod
spec:
  containers:
    - name: nginx
      image: nginx:latest
      resources:
        requests:
          cpu: "100"
          memory: "128Gi"
```

### Apply and Inspect

```bash
kubectl apply -f pending-pod.yml

kubectl get pod resource-pending-pod

kubectl describe pod resource-pending-pod
```

### Expected Event

```text
Warning  FailedScheduling

0/3 nodes are available:
Insufficient cpu,
Insufficient memory.
```

The exact node count and event message depend on cluster capacity.

**Verification:** The scheduler reports `Insufficient cpu` and/or `Insufficient memory`, and the Pod remains Pending.

---

## 4. Liveness Probe

A liveness probe checks whether a container is functioning correctly.

If the probe fails continuously beyond the configured failure threshold, Kubernetes restarts the container.

### Pod Manifest

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: liveness-pod
spec:
  containers:
    - name: busybox
      image: busybox:latest
      command:
        - sh
        - -c
        - "touch /tmp/healthy; sleep 30; rm -f /tmp/healthy; sleep 3600"
      livenessProbe:
        exec:
          command:
            - cat
            - /tmp/healthy
        periodSeconds: 5
        failureThreshold: 3
```

### Apply and Monitor

```bash
kubectl apply -f liveness-pod.yml

kubectl get pod liveness-pod -w

kubectl describe pod liveness-pod
```

### Expected Observation

Initially, the probe succeeds because `/tmp/healthy` exists.

After 30 seconds, the file is deleted. The probe fails three consecutive times, and Kubernetes restarts the container.

Expected events include:

```text
Warning  Unhealthy
Liveness probe failed
```

**Verification:** The restart count increases after liveness probe failures.

---

## 5. Readiness Probe

A readiness probe determines whether a container is ready to receive traffic.

When readiness fails:

* The Pod becomes NotReady.
* The Pod is removed from the Service's ready endpoints.
* The container is not restarted solely because of readiness failure.

### Pod Manifest

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: readiness-pod
  labels:
    app: readiness-demo
spec:
  containers:
    - name: nginx
      image: nginx:latest
      readinessProbe:
        httpGet:
          path: /
          port: 80
        periodSeconds: 5
        failureThreshold: 3
```

### Apply and Expose

```bash
kubectl apply -f readiness-pod.yml

kubectl expose pod readiness-pod \
  --port=80 \
  --name=readiness-svc

kubectl get endpoints readiness-svc
```

Initially, the Pod IP appears in the Service endpoints.

### Break the Readiness Probe

```bash
kubectl exec readiness-pod -- rm /usr/share/nginx/html/index.html
```

Wait for the readiness probe to fail.

```bash
kubectl get pods

kubectl get endpoints readiness-svc

kubectl describe pod readiness-pod
```

### Expected Observation

```text
READY: 0/1
```

The Service endpoints become empty because the Pod is no longer ready.

**Verification:** The container is not restarted. Its restart count remains unchanged because readiness probes control traffic, not container restarts.

---

## 6. Startup Probe

A startup probe gives slow-starting applications additional time to initialize.

Until the startup probe succeeds, Kubernetes does not execute the configured liveness and readiness probes.

### Pod Manifest

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: startup-pod
spec:
  containers:
    - name: startup-container
      image: busybox:latest
      command:
        - sh
        - -c
        - "sleep 20 && touch /tmp/started && sleep 3600"

      startupProbe:
        exec:
          command:
            - cat
            - /tmp/started
        periodSeconds: 5
        failureThreshold: 12

      livenessProbe:
        exec:
          command:
            - cat
            - /tmp/started
        periodSeconds: 5
        failureThreshold: 3
```

### Apply and Verify

```bash
kubectl apply -f startup-pod.yml

kubectl get pod startup-pod -w

kubectl describe pod startup-pod
```

### Expected Observation

* The container takes approximately 20 seconds to initialize.
* The startup probe initially fails.
* Once `/tmp/started` is created, the startup probe succeeds.
* The liveness probe then becomes active.

### What if failureThreshold is 2?

With `periodSeconds: 5` and `failureThreshold: 2`, the startup probe has a much smaller startup window.

If the probe fails twice before initialization completes, Kubernetes restarts the container.

**Verification:** Startup probes prevent premature restarts of applications that need additional initialization time.

---

## 7. Liveness vs Readiness vs Startup Probes

| Probe     | Purpose                                               | On Failure                                 |
| --------- | ----------------------------------------------------- | ------------------------------------------ |
| Liveness  | Checks whether the container is alive                 | Restarts the container                     |
| Readiness | Checks whether the application can receive traffic    | Removes Pod from ready Service endpoints   |
| Startup   | Checks whether application initialization is complete | Restarts container after failure threshold |

### Probe Types

* `httpGet` – Sends an HTTP request to an endpoint.
* `exec` – Executes a command inside the container.
* `tcpSocket` – Checks whether a TCP port is accepting connections.

---

## 8. CPU vs Memory Limit Behavior

| Resource | When Limit Is Exceeded                     |
| -------- | ------------------------------------------ |
| CPU      | Container is throttled                     |
| Memory   | Container can be terminated with OOMKilled |

CPU is a compressible resource, whereas memory is incompressible.

---

## 9. Cleanup

After completing the experiments, remove the created resources.

```bash
kubectl delete pod resource-pod
kubectl delete pod oom-pod
kubectl delete pod resource-pending-pod
kubectl delete pod liveness-pod
kubectl delete pod readiness-pod
kubectl delete pod startup-pod

kubectl delete service readiness-svc
```

Verify cleanup:

```bash
kubectl get pods
kubectl get services
```

---

## 10. Screenshots

Add terminal screenshots of your practical implementation below.

### 1. Resource Requests, Limits and QoS Class

![Resource Requests and Limits](screenshots/day-57/resource-requests-limits.png)

### 2. OOMKilled – Exit Code 137

![OOMKilled](screenshots/day-57/oomkilled.png)

### 3. Pending Pod – Insufficient Resources

![Pending Pod](screenshots/day-57/pending-pod.png)

### 4. Liveness Probe – Container Restart

![Liveness Probe](screenshots/day-57/liveness-probe.png)

### 5. Readiness Probe – Empty Endpoints

![Readiness Probe](screenshots/day-57/readiness-probe.png)

### 6. Startup Probe

![Startup Probe](screenshots/day-57/startup-probe.png)

---

## Key Learnings

* Understood the difference between resource requests and limits.
* Learned how Kubernetes uses requests for scheduling.
* Observed memory-related container termination through OOMKilled.
* Understood why excessive resource requests cause Pods to remain Pending.
* Implemented liveness probes for automatic container recovery.
* Used readiness probes to control traffic routing.
* Configured startup probes for slow-starting applications.
* Learned how Kubernetes maintains application health and resource efficiency.

---

**Day 57 Completed!**

Continuing my #90DaysOfDevOps journey, one concept and one hands-on implementation at a time.

#90DaysOfDevOps #Kubernetes #K8s #DevOps #CloudComputing #ContainerOrchestration
