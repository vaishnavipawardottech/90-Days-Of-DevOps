# Day 52 – Kubernetes Namespaces and Deployments

## Overview

Today I learned about **Kubernetes Namespaces and Deployments**.

Namespaces help organize Kubernetes resources into separate environments such as development and staging. Deployments help manage applications by maintaining the desired number of Pod replicas, providing self-healing, scaling, rolling updates, and rollbacks.

---

# Task 1: Explore Default Namespaces

First, I listed the namespaces available in the Kubernetes cluster:

```bash
kubectl get namespaces
```

Kubernetes provides several built-in namespaces:

* `default` – Used when no namespace is specified.
* `kube-system` – Contains Kubernetes system components.
* `kube-public` – Contains resources that can be publicly accessed.
* `kube-node-lease` – Used for node heartbeat information.

I then checked the Pods running in the `kube-system` namespace:

```bash
kubectl get pods -n kube-system
```

These Pods belong to Kubernetes system components and help keep the cluster running.

### Verify

**How many Pods are running in `kube-system`?**

I checked the output of:

```bash
kubectl get pods -n kube-system
```

The number of running Pods depends on the Kubernetes cluster setup. In my cluster, I counted the Pods shown in the command output.

---

# Task 2: Create and Use Custom Namespaces

I created two namespaces for different environments:

```bash
kubectl create namespace dev
kubectl create namespace staging
```

I verified them using:

```bash
kubectl get namespaces
```

I also created a `production` namespace using a YAML manifest.

### `namespace.yaml`

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: production
```

Applied using:

```bash
kubectl apply -f namespace.yaml
```

### Running Pods in Specific Namespaces

I created an Nginx Pod in the `dev` namespace:

```bash
kubectl run nginx-dev --image=nginx:latest -n dev
```

And another one in the `staging` namespace:

```bash
kubectl run nginx-staging --image=nginx:latest -n staging
```

To view Pods across all namespaces:

```bash
kubectl get pods -A
```

To view Pods in a particular namespace:

```bash
kubectl get pods -n dev
kubectl get pods -n staging
```

### Verify

**Does `kubectl get pods` show these Pods? What about `kubectl get pods -A`?**

No. Running:

```bash
kubectl get pods
```

only displays Pods from the `default` namespace.

The Pods created in `dev` and `staging` are not shown.

Running:

```bash
kubectl get pods -A
```

shows Pods from **all namespaces**, including the Pods in `dev` and `staging`.

---

# Task 3: Create the First Deployment

I created a Deployment with 3 replicas.

### `nginx-deployment.yaml`

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
  namespace: dev
  labels:
    app: nginx

spec:
  replicas: 3

  selector:
    matchLabels:
      app: nginx

  template:
    metadata:
      labels:
        app: nginx

    spec:
      containers:
        - name: nginx
          image: nginx:1.24
          ports:
            - containerPort: 80
```

I applied the Deployment:

```bash
kubectl apply -f nginx-deployment.yaml
```

Then checked the Deployment:

```bash
kubectl get deployments -n dev
```

And the Pods:

```bash
kubectl get pods -n dev
```

The Deployment created 3 Pods because the manifest specifies:

```yaml
replicas: 3
```

---

## Understanding the Deployment Manifest

### `apiVersion`

```yaml
apiVersion: apps/v1
```

Deployments use the `apps/v1` API version.

### `kind`

```yaml
kind: Deployment
```

Specifies that the resource being created is a Deployment.

### `metadata`

```yaml
metadata:
  name: nginx-deployment
  namespace: dev
```

Defines the Deployment name and the namespace in which it will exist.

### `replicas`

```yaml
replicas: 3
```

Specifies that Kubernetes should maintain 3 replicas of the Pod.

### `selector`

```yaml
selector:
  matchLabels:
    app: nginx
```

Defines which Pods belong to the Deployment.

### `template`

```yaml
template:
  metadata:
    labels:
      app: nginx
```

This is the Pod template used by the Deployment to create Pods.

The labels in the template must match the Deployment selector.

### Container

```yaml
containers:
  - name: nginx
    image: nginx:1.24
```

Defines the container and the image that each Pod will run.

---

## Verify

**What do the READY, UP-TO-DATE, and AVAILABLE columns mean?**

For example:

```text
NAME               READY   UP-TO-DATE   AVAILABLE
nginx-deployment   3/3     3            3
```

### READY

Shows how many replicas are currently ready compared to the desired number.

`3/3` means all 3 desired replicas are ready.

### UP-TO-DATE

Shows how many replicas are running the latest version of the Deployment configuration.

### AVAILABLE

Shows how many replicas are currently available to serve the application.

---

# Task 4: Self-Healing

I checked the Pods:

```bash
kubectl get pods -n dev
```

I then deleted one of the Pods:

```bash
kubectl delete pod <pod-name> -n dev
```

Immediately after deletion, I checked the Pods again:

```bash
kubectl get pods -n dev
```

The Deployment detected that the number of running replicas had fallen below the desired count.

The desired state was:

```text
3 replicas
```

After deleting one Pod:

```text
2 replicas
```

Kubernetes automatically created a new Pod to bring the number back to 3.

### Verify

**Is the replacement Pod's name the same as the deleted Pod?**

No.

The replacement Pod receives a **new, different name**.

For example:

```text
Deleted:
nginx-deployment-abc12-xyz34

Created:
nginx-deployment-def56-uvw78
```

The important point is that Kubernetes maintains the desired number of replicas rather than bringing back the exact same Pod.

---

# Task 5: Scale the Deployment

I first scaled the Deployment from 3 replicas to 5:

```bash
kubectl scale deployment nginx-deployment --replicas=5 -n dev
```

Then checked the Pods:

```bash
kubectl get pods -n dev
```

Kubernetes created additional Pods until 5 replicas were running.

I then scaled the Deployment down to 2 replicas:

```bash
kubectl scale deployment nginx-deployment --replicas=2 -n dev
```

Again, I checked the Pods:

```bash
kubectl get pods -n dev
```

Kubernetes terminated the extra Pods until only 2 replicas remained.

### Verify

**When you scaled down from 5 to 2, what happened to the extra Pods?**

Kubernetes terminated **3 Pods** because the desired replica count changed from 5 to 2.

The Deployment then maintained only the required 2 Pods.

```text
5 Pods
  ↓
Scale down to 2
  ↓
3 extra Pods terminated
  ↓
2 Pods remain
```

### Scaling using YAML

Scaling can also be done declaratively by changing the manifest:

```yaml
spec:
  replicas: 4
```

Then applying it:

```bash
kubectl apply -f nginx-deployment.yaml
```

Kubernetes adjusts the number of Pods to match the new desired state.

---

# Task 6: Rolling Update

I updated the Nginx image from:

```text
nginx:1.24
```

to:

```text
nginx:1.25
```

using:

```bash
kubectl set image deployment/nginx-deployment nginx=nginx:1.25 -n dev
```

I monitored the rollout:

```bash
kubectl rollout status deployment/nginx-deployment -n dev
```

Kubernetes gradually replaced the old Pods with Pods running the new image.

This process is called a **rolling update**.

---

## Rollout History

I checked the Deployment's rollout history:

```bash
kubectl rollout history deployment/nginx-deployment -n dev
```

This shows the revisions created when the Deployment configuration changes.

---

## Rollback

I rolled back the Deployment to the previous revision:

```bash
kubectl rollout undo deployment/nginx-deployment -n dev
```

Then checked the rollout status:

```bash
kubectl rollout status deployment/nginx-deployment -n dev
```

Finally, I verified the image:

```bash
kubectl describe deployment nginx-deployment -n dev | grep Image
```

### Verify

**What image version is running after the rollback?**

After the rollback, the Deployment returned to the **previous image version, `nginx:1.24`**.

The update sequence was:

```text
nginx:1.24
     ↓
Rolling update
     ↓
nginx:1.25
     ↓
Rollback
     ↓
nginx:1.24
```

---

# Task 7: Clean Up

After completing the practical tasks, I removed the resources:

```bash
kubectl delete deployment nginx-deployment -n dev

kubectl delete pod nginx-dev -n dev
kubectl delete pod nginx-staging -n staging

kubectl delete namespace dev staging production
```

I verified the resources:

```bash
kubectl get namespaces
kubectl get pods -A
```

Deleting a namespace also removes the resources contained inside that namespace, so namespace deletion should be performed carefully.

---

# Important Commands Practised

```bash
# Namespaces
kubectl get namespaces
kubectl get pods -n kube-system

# Create namespaces
kubectl create namespace dev
kubectl create namespace staging
kubectl apply -f namespace.yaml

# Pods in namespaces
kubectl run nginx-dev --image=nginx:latest -n dev
kubectl run nginx-staging --image=nginx:latest -n staging
kubectl get pods -A

# Deployment
kubectl apply -f nginx-deployment.yaml
kubectl get deployments -n dev
kubectl get pods -n dev

# Self-healing
kubectl delete pod <pod-name> -n dev

# Scaling
kubectl scale deployment nginx-deployment --replicas=5 -n dev
kubectl scale deployment nginx-deployment --replicas=2 -n dev

# Rolling update
kubectl set image deployment/nginx-deployment nginx=nginx:1.25 -n dev
kubectl rollout status deployment/nginx-deployment -n dev

# Rollout history
kubectl rollout history deployment/nginx-deployment -n dev

# Rollback
kubectl rollout undo deployment/nginx-deployment -n dev

# Verify image
kubectl describe deployment nginx-deployment -n dev | grep Image

# ReplicaSets
kubectl get replicasets -n dev

# Cleanup
kubectl delete deployment nginx-deployment -n dev
kubectl delete namespace dev staging production
```

---

# Key Learnings

* **Namespaces** organize Kubernetes resources into separate environments.
* `kubectl get pods` shows Pods from the current/default namespace.
* `kubectl get pods -A` shows Pods across all namespaces.
* A **Deployment** maintains the desired number of Pod replicas.
* If a Deployment-managed Pod is deleted, Kubernetes creates a replacement Pod.
* The replacement Pod gets a **different name**.
* Scaling from 5 to 2 replicas causes Kubernetes to terminate 3 Pods.
* Deployments can be scaled imperatively using `kubectl scale`.
* Deployments can also be scaled declaratively by changing `replicas` in the YAML manifest.
* A **rolling update** gradually replaces old Pods with new ones.
* `kubectl rollout history` displays Deployment revisions.
* `kubectl rollout undo` rolls back to the previous revision.
* Deployments use ReplicaSets to manage their Pods.

---

# Conclusion

Day 52 helped me understand how **Namespaces and Deployments** are used to manage applications in Kubernetes.

Namespaces provide organization and separation between environments, while Deployments allow Kubernetes to maintain the desired number of replicas and handle scaling, updates, and rollbacks.

The main concept I took away from this practice is:

> **Define the desired state, and Kubernetes works continuously to maintain it.**
