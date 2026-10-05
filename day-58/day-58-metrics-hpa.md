# Day 58 – Metrics Server and Horizontal Pod Autoscaler (HPA)

## Overview

On Day 58 of my #90DaysOfDevOps journey, I explored **Kubernetes Metrics Server** and the **Horizontal Pod Autoscaler (HPA)**.

Until now, I had configured CPU and memory requests and limits for Kubernetes workloads. Today, I used those resource requests with the Metrics Server and HPA to monitor actual resource usage and automatically adjust the number of application Pods based on CPU utilization.

This is an important Kubernetes capability because applications do not always receive the same amount of traffic. HPA allows Kubernetes to increase or decrease the number of Pods based on workload demand.

---

# 1. What is Metrics Server?

**Metrics Server** is a Kubernetes component that collects resource usage metrics such as:

* CPU usage
* Memory usage

It collects these metrics from the kubelets running on Kubernetes nodes and makes them available through the Kubernetes Metrics API.

The metrics can then be viewed using:

```bash
kubectl top nodes
```

and:

```bash
kubectl top pods -A
```

Metrics Server is especially important for autoscaling because HPA needs current resource usage to determine whether additional Pods are required.

---

# 2. Why Does HPA Need Metrics Server?

The Horizontal Pod Autoscaler needs two important pieces of information:

1. The configured resource request.
2. The current resource utilization.

For example, if a Pod has:

```yaml
resources:
  requests:
    cpu: 200m
```

and Kubernetes observes that the Pod is using approximately:

```text
100m CPU
```

then the CPU utilization is approximately:

```text
100m / 200m × 100 = 50%
```

If the HPA target is 50%, Kubernetes can use this information to determine whether the number of replicas needs to change.

Without CPU requests, CPU utilization percentage cannot be calculated correctly for the HPA.

---

# 3. Installing Metrics Server

First, I checked whether Metrics Server was already running:

```bash
kubectl get pods -n kube-system | grep metrics-server
```

For a Kind or kubeadm cluster, Metrics Server can be installed using the official release manifest.

After installation, I verified the Metrics Server Pod:

```bash
kubectl get pods -n kube-system | grep metrics-server
```

The Pod should eventually reach:

```text
Running
```

Metrics Server may take some time before metrics become available.

I then checked node metrics:

```bash
kubectl top nodes
```

and all Pod metrics:

```bash
kubectl top pods -A
```

---

# 4. kubectl top

The `kubectl top` command displays the **current resource usage** of Kubernetes nodes and Pods.

### Node Usage

```bash
kubectl top nodes
```

Example:

```text
NAME                  CPU(cores)   CPU%   MEMORY(bytes)   MEMORY%
ip-172-31-41-43       120m         6%     950Mi           25%
ip-172-31-43-185      180m         9%     1100Mi          29%
```

The actual values depend on the current workload in the cluster.

### Pod Usage

```bash
kubectl top pods -A
```

To sort Pods by CPU usage:

```bash
kubectl top pods -A --sort-by=cpu
```

This helps identify which Pods are currently consuming the most CPU.

---

# 5. Actual Usage vs Requests and Limits

One important concept I learned is that `kubectl top` does **not** show CPU requests or limits.

For example:

```yaml
resources:
  requests:
    cpu: 200m
    memory: 128Mi

  limits:
    cpu: 500m
    memory: 256Mi
```

These values define the resources configured for the container.

However:

```bash
kubectl top pods
```

shows the **actual resource usage**.

| Configuration  | Meaning                                                              |
| -------------- | -------------------------------------------------------------------- |
| CPU Request    | CPU guaranteed/requested for scheduling and utilization calculations |
| CPU Limit      | Maximum CPU the container can use                                    |
| Memory Request | Memory requested for scheduling                                      |
| Memory Limit   | Maximum memory the container can use                                 |
| `kubectl top`  | Current resource usage                                               |

---

# 6. Create a CPU-Based Deployment

For the HPA experiment, I created a Deployment using the Kubernetes HPA example image.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: php-apache
spec:
  selector:
    matchLabels:
      run: php-apache
  replicas: 1
  template:
    metadata:
      labels:
        run: php-apache
    spec:
      containers:
        - name: php-apache
          image: registry.k8s.io/hpa-example
          ports:
            - containerPort: 80
          resources:
            requests:
              cpu: 200m
```

Apply the Deployment:

```bash
kubectl apply -f php-apache.yaml
```

Verify:

```bash
kubectl get deployment php-apache
kubectl get pods
```

---

# 7. Expose the Deployment

I exposed the Deployment through a Kubernetes Service:

```bash
kubectl expose deployment php-apache --port=80
```

Verify the Service:

```bash
kubectl get svc php-apache
```

The Service allows other Pods in the cluster to access the application using:

```text
http://php-apache
```

---

# 8. Check CPU Usage

After the Pod started, I checked its current CPU usage:

```bash
kubectl top pod
```

For the specific Pod:

```bash
kubectl top pod <pod-name>
```

The CPU usage changes depending on the workload.

---

# 9. Create HPA Using Imperative Command

I created an HPA that targets an average CPU utilization of 50%:

```bash
kubectl autoscale deployment php-apache \
  --cpu-percent=50 \
  --min=1 \
  --max=10
```

This configuration means:

```text
Minimum replicas = 1
Maximum replicas = 10
CPU target       = 50%
```

Check the HPA:

```bash
kubectl get hpa
```

For more information:

```bash
kubectl describe hpa php-apache
```

Initially, the `TARGETS` column may show:

```text
<unknown>
```

This can happen while Metrics Server is collecting metrics.

After metrics become available, it should show a value similar to:

```text
20%/50%
```

The exact value depends on current CPU usage.

---

# 10. How HPA Calculates Desired Replicas

HPA uses the current resource utilization and target utilization to determine the desired number of replicas.

A simplified formula is:

```text
desiredReplicas =
ceil(currentReplicas × currentUsage / targetUsage)
```

For example:

```text
Current replicas = 2
Current CPU      = 80%
Target CPU       = 50%
```

Then:

```text
desiredReplicas =
ceil(2 × 80 / 50)

= ceil(3.2)

= 4
```

Therefore, HPA may increase the Deployment to approximately four replicas, subject to Kubernetes HPA behavior and other constraints.

---

# 11. Generate Load

To generate CPU load, I created a temporary load-generator Pod:

```bash
kubectl run load-generator \
  --image=busybox:1.36 \
  --restart=Never \
  -- /bin/sh -c "while true; do wget -q -O- http://php-apache; done"
```

Check the load generator:

```bash
kubectl get pods
```

Check CPU usage:

```bash
kubectl top pods
```

Check HPA:

```bash
kubectl get hpa php-apache
```

Watch the HPA continuously:

```bash
kubectl get hpa php-apache --watch
```

The increased CPU usage can cause HPA to increase the number of replicas.

---

# 12. Observe Pod Scaling

I monitored the Deployment:

```bash
kubectl get deployment php-apache --watch
```

I also monitored Pods:

```bash
kubectl get pods --watch
```

Under increased CPU load, the HPA can increase the number of replicas.

The general flow is:

```text
Increased Traffic
       ↓
Higher CPU Usage
       ↓
Metrics Server collects metrics
       ↓
HPA evaluates CPU utilization
       ↓
Desired replicas increase
       ↓
Deployment creates additional Pods
```

When the workload decreases:

```text
Traffic decreases
       ↓
CPU usage decreases
       ↓
Metrics Server reports lower usage
       ↓
HPA evaluates utilization
       ↓
Replica count can decrease
```

---

# 13. Stop the Load

After testing autoscaling, I removed the load generator:

```bash
kubectl delete pod load-generator
```

Check the HPA:

```bash
kubectl get hpa
```

Check the Deployment:

```bash
kubectl get deployment php-apache
```

HPA scale-down can take longer because Kubernetes uses a stabilization period to prevent rapid scaling up and down.

---

# 14. HPA Using YAML

After testing the imperative HPA command, I created an HPA declaratively using the `autoscaling/v2` API.

Example:

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: php-apache
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: php-apache

  minReplicas: 1
  maxReplicas: 10

  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 50

  behavior:
    scaleUp:
      stabilizationWindowSeconds: 0
      policies:
        - type: Percent
          value: 100
          periodSeconds: 15

    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
        - type: Percent
          value: 50
          periodSeconds: 60
```

Apply the HPA:

```bash
kubectl apply -f php-apache-hpa.yaml
```

Verify:

```bash
kubectl get hpa
```

Detailed information:

```bash
kubectl describe hpa php-apache
```

---

# 15. What Does the `behavior` Section Do?

The `behavior` section controls how quickly HPA is allowed to scale the application.

### Scale Up

```yaml
scaleUp:
  stabilizationWindowSeconds: 0
```

This allows scaling up without waiting for a stabilization period.

### Scale Down

```yaml
scaleDown:
  stabilizationWindowSeconds: 300
```

This provides a five-minute stabilization window before scaling down.

This helps prevent unnecessary scaling caused by short-lived traffic spikes.

In simple terms:

```text
Scale Up   → Fast
Scale Down → More gradual
```

---

# 16. autoscaling/v1 vs autoscaling/v2

Kubernetes provides multiple HPA API versions.

### autoscaling/v1

The older HPA API supports basic CPU-based autoscaling.

Example:

```yaml
apiVersion: autoscaling/v1
```

It is useful for simple CPU-based scaling but provides fewer configuration options.

### autoscaling/v2

The `autoscaling/v2` API provides more advanced autoscaling capabilities.

Example:

```yaml
apiVersion: autoscaling/v2
```

It supports:

* CPU metrics
* Memory metrics
* Multiple metrics
* Custom metrics
* External metrics
* Scaling behavior configuration
* Scale-up policies
* Scale-down policies
* Stabilization windows

For modern Kubernetes workloads, `autoscaling/v2` provides much more flexibility.

---

# 17. HPA with CPU and Memory

With `autoscaling/v2`, multiple resource metrics can be configured.

For example:

```yaml
metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 50

  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 70
```

This allows HPA to consider both CPU and memory utilization.

---

# 18. HPA Troubleshooting

If HPA shows:

```text
TARGETS: <unknown>
```

check Metrics Server:

```bash
kubectl get pods -n kube-system | grep metrics-server
```

Check node metrics:

```bash
kubectl top nodes
```

Check Pod metrics:

```bash
kubectl top pods
```

Check HPA details:

```bash
kubectl describe hpa php-apache
```

One of the most common causes of HPA not working is missing CPU requests.

For example, this is required for CPU utilization-based HPA:

```yaml
resources:
  requests:
    cpu: 200m
```

Without a CPU request, Kubernetes cannot calculate CPU utilization as a percentage of the requested CPU.

---

# 19. Cleanup

After completing the experiment, I removed the resources created for the HPA test.

Delete the HPA:

```bash
kubectl delete hpa php-apache
```

Delete the Service:

```bash
kubectl delete service php-apache
```

Delete the Deployment:

```bash
kubectl delete deployment php-apache
```

Delete the load-generator if it still exists:

```bash
kubectl delete pod load-generator --ignore-not-found
```

Metrics Server can remain installed because it is useful for future Kubernetes monitoring and autoscaling experiments.

---

# 20. Key Learnings

Through Day 58, I learned:

* Metrics Server provides resource usage metrics to Kubernetes.
* `kubectl top` shows current CPU and memory usage.
* Resource requests are important for HPA calculations.
* HPA automatically adjusts the number of replicas.
* HPA can scale workloads up when resource utilization increases.
* HPA can scale workloads down when utilization decreases.
* `autoscaling/v2` provides more functionality than `autoscaling/v1`.
* HPA `behavior` controls scaling speed and stabilization.
* Scale-up is generally designed to react quickly.
* Scale-down is intentionally more conservative.
* HPA works with Kubernetes workloads such as Deployments, StatefulSets, and ReplicaSets.

---

# 21. Important Commands

| Command                             | Purpose                        |
| ----------------------------------- | ------------------------------ |
| `kubectl top nodes`                 | View node CPU and memory usage |
| `kubectl top pods -A`               | View Pod resource usage        |
| `kubectl top pods -A --sort-by=cpu` | Sort Pods by CPU usage         |
| `kubectl get hpa`                   | List HPAs                      |
| `kubectl describe hpa`              | Inspect HPA details and events |
| `kubectl autoscale deployment`      | Create an HPA imperatively     |
| `kubectl apply -f hpa.yaml`         | Create HPA declaratively       |
| `kubectl get deployment --watch`    | Watch replica changes          |
| `kubectl get pods --watch`          | Watch Pod scaling              |
| `kubectl delete hpa`                | Remove an HPA                  |

---

# 22. Overall Autoscaling Architecture

The overall flow can be summarized as:

```text
                    Kubernetes Cluster
                           │
                           ▼
                    Metrics Server
                           │
                 CPU / Memory Metrics
                           │
                           ▼
                         HPA
                           │
                    Target Utilization
                           │
                           ▼
                     Deployment
                           │
              ┌────────────┼────────────┐
              ▼            ▼            ▼
            Pod 1        Pod 2        Pod 3
```

Under high traffic:

```text
High Traffic
     ↓
High CPU
     ↓
Metrics Server
     ↓
HPA detects utilization > target
     ↓
More replicas
```

Under low traffic:

```text
Low Traffic
     ↓
Low CPU
     ↓
Metrics Server
     ↓
HPA detects utilization < target
     ↓
Fewer replicas
```

---

# Conclusion

Day 58 helped me understand how Kubernetes can automatically respond to changing workloads.

Metrics Server provides the resource usage data, while HPA uses that data along with configured resource requests and target utilization to make scaling decisions.

This gives Kubernetes applications the ability to handle variable workloads without manually changing the replica count.

The combination of:

```text
Metrics Server
      +
Resource Requests
      +
Horizontal Pod Autoscaler
      =
Automatic Kubernetes Scaling
```

is an important building block for running scalable applications in Kubernetes.

#90DaysOfDevOps #Day58 #Kubernetes #HPA #MetricsServer #DevOps #DevOpsKaJosh #TrainWithShubham
