# Day 59 – Helm: Kubernetes Package Manager

## Overview

On Day 59 of my #90DaysOfDevOps journey, I explored **Helm**, the package manager for Kubernetes.

Until now, I have been creating Kubernetes resources such as Deployments, Services, ConfigMaps, Secrets, and PersistentVolumeClaims using individual YAML files.

Managing multiple YAML files becomes difficult as an application grows. Helm simplifies this by packaging Kubernetes manifests into reusable charts.

Helm allows us to install, configure, upgrade, rollback, and manage Kubernetes applications using a few commands.

---

## 1. What is Helm?

Helm is a package manager for Kubernetes, similar to how `apt` manages packages in Ubuntu.

It uses templates and configuration values to generate Kubernetes manifests and deploy applications.

### Three Core Concepts

| Concept    | Description                                                                       |
| ---------- | --------------------------------------------------------------------------------- |
| Chart      | A package containing Kubernetes manifest templates, default values, and metadata. |
| Release    | A specific installed instance of a Helm chart in a Kubernetes cluster.            |
| Repository | A location where Helm charts are stored and distributed.                          |

### Why Helm?

* Simplifies Kubernetes application deployment.
* Reduces repetitive YAML configuration.
* Supports reusable templates.
* Allows customization through values.
* Provides upgrade and rollback functionality.
* Maintains release revision history.

---

## 2. Install Helm

### Installation on Ubuntu

Download and install Helm using the official installation script:

```bash
curl -fsSL https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
```

Verify the installation:

```bash
helm version
```

Check Helm environment configuration:

```bash
helm env
```

### Verification

```bash
helm version
helm env
```

The version command displays the installed Helm version, while `helm env` displays Helm-related environment variables.

---

## 3. Add Bitnami Repository

Helm repositories contain charts that can be installed into Kubernetes clusters.

Add the Bitnami repository:

```bash
helm repo add bitnami https://charts.bitnami.com/bitnami
```

Update repository information:

```bash
helm repo update
```

List configured repositories:

```bash
helm repo list
```

Search for NGINX charts:

```bash
helm search repo nginx
```

Search for Bitnami charts:

```bash
helm search repo bitnami
```

To count the available charts returned by the repository search:

```bash
helm search repo bitnami | tail -n +2 | wc -l
```

**Note:** The number of available charts can change over time.

---

## 4. Install NGINX Using Helm

Install the Bitnami NGINX chart:

```bash
helm install my-nginx bitnami/nginx
```

Here:

* `my-nginx` is the release name.
* `bitnami/nginx` is the chart being installed.

Check Kubernetes resources:

```bash
kubectl get all
```

Check resources in a specific namespace:

```bash
kubectl get all -n default
```

List Helm releases:

```bash
helm list
```

Inspect the release:

```bash
helm status my-nginx
```

View the generated Kubernetes manifests:

```bash
helm get manifest my-nginx
```

### Verification

```bash
kubectl get pods
kubectl get svc
helm status my-nginx
```

The default replica count and Service type depend on the chart version and its default values.

---

## 5. Customize a Helm Release Using Values

Helm charts provide a `values.yaml` file that defines configurable parameters.

View the default NGINX chart values:

```bash
helm show values bitnami/nginx
```

### Install with --set

Install a customized NGINX release:

```bash
helm install my-nginx-custom bitnami/nginx \
  --set replicaCount=3 \
  --set service.type=NodePort
```

Here:

* `replicaCount=3` requests three replicas.
* `service.type=NodePort` configures the Service as NodePort.

Check the release values:

```bash
helm get values my-nginx-custom
```

View all values, including chart defaults:

```bash
helm get values my-nginx-custom --all
```

### Create custom-values.yaml

Create a file named `custom-values.yaml`:

```yaml
replicaCount: 3

image:
  registry: docker.io
  repository: bitnami/nginx
  tag: latest

service:
  type: NodePort

resources:
  requests:
    cpu: 100m
    memory: 128Mi
  limits:
    cpu: 200m
    memory: 256Mi
```

**Note:** Chart values and image configuration can change between chart versions. Always check `helm show values bitnami/nginx` before using overrides. For reproducible deployments, prefer pinning an image tag instead of using `latest`.

Install using the values file:

```bash
helm install nginx-values bitnami/nginx -f custom-values.yaml
```

Verify:

```bash
helm get values nginx-values
kubectl get pods
kubectl get svc
```

The release should use the configured replica count and Service type, provided those keys are supported by the selected chart version.

---

## 6. Upgrade and Rollback

Helm supports application upgrades while maintaining release history.

### Upgrade the Existing Release

Upgrade `my-nginx` to five replicas:

```bash
helm upgrade my-nginx bitnami/nginx --set replicaCount=5
```

Check the Deployment:

```bash
kubectl get deployments
kubectl get pods
```

### Check Release History

```bash
helm history my-nginx
```

The history shows revision numbers, update timestamps, chart versions, and release status.

### Rollback to Revision 1

```bash
helm rollback my-nginx 1
```

Check the history again:

```bash
helm history my-nginx
```

### Understanding Revisions

| Operation              | Revision |
| ---------------------- | -------- |
| Initial installation   | 1        |
| Upgrade to 5 replicas  | 2        |
| Rollback to revision 1 | 3        |

Rollback creates a new revision rather than deleting or overwriting previous history.

Verify the current release:

```bash
helm status my-nginx
kubectl get deployments
```

---

## 7. Create a Custom Helm Chart

Helm allows us to create our own reusable Kubernetes charts.

### Scaffold a Chart

```bash
helm create my-app
```

Explore the generated structure:

```text
my-app/
├── Chart.yaml
├── values.yaml
├── charts/
├── templates/
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── ingress.yaml
│   ├── hpa.yaml
│   ├── serviceaccount.yaml
│   ├── _helpers.tpl
│   └── NOTES.txt
└── .helmignore
```

### Important Files

| File                      | Purpose                                    |
| ------------------------- | ------------------------------------------ |
| Chart.yaml                | Chart name, version, and metadata.         |
| values.yaml               | Default configuration values.              |
| templates/deployment.yaml | Deployment template.                       |
| templates/service.yaml    | Service template.                          |
| _helpers.tpl              | Reusable template helpers.                 |
| NOTES.txt                 | Instructions displayed after installation. |

### Go Template Syntax

Helm uses Go templating to generate Kubernetes YAML files.

Examples:

```yaml
replicas: {{ .Values.replicaCount }}
```

```yaml
app: {{ .Chart.Name }}
```

```yaml
name: {{ .Release.Name }}
```

These expressions dynamically insert values from the chart configuration and release information.

### Customize values.yaml

Open:

```bash
nano my-app/values.yaml
```

Update the relevant values:

```yaml
replicaCount: 3

image:
  repository: nginx
  pullPolicy: IfNotPresent
  tag: "1.25"

service:
  type: ClusterIP
  port: 80
```

### Validate the Chart

```bash
helm lint my-app
```

### Preview Generated Manifests

```bash
helm template my-release ./my-app
```

This renders the Kubernetes manifests locally without installing anything in the cluster.

### Install the Custom Chart

```bash
helm install my-release ./my-app
```

Verify:

```bash
helm list
kubectl get deployments
kubectl get pods
kubectl get svc
```

The Deployment should initially request three replicas.

### Upgrade the Custom Chart

```bash
helm upgrade my-release ./my-app --set replicaCount=5
```

Verify:

```bash
kubectl get deployment my-release-my-app
kubectl get pods
helm history my-release
```

The replica count should change to five once the Deployment rollout completes.

---

## 8. Cleanup

Uninstall the releases created during this exercise:

```bash
helm uninstall my-nginx
helm uninstall my-nginx-custom
helm uninstall nginx-values
helm uninstall my-release
```

Verify:

```bash
helm list
```

Check Kubernetes resources:

```bash
kubectl get all
```

Remove local chart and values files if no longer required:

```bash
rm -rf my-app
rm -f custom-values.yaml
```

To retain release history after uninstalling:

```bash
helm uninstall my-nginx --keep-history
```

---

## 9. Key Learnings

Through this task, I learned:

* Helm simplifies Kubernetes deployments using reusable charts.
* Charts contain templates and default configuration values.
* Releases represent installed instances of charts.
* Repositories provide charts for installation.
* `--set` and `-f` allow configuration customization.
* `helm upgrade` updates an existing release.
* `helm rollback` restores a previous revision while creating a new revision.
* `helm create` scaffolds a custom chart.
* `helm lint` validates chart structure.
* `helm template` previews Kubernetes manifests before deployment.

### Helm Commands Cheat Sheet

| Command             | Purpose                   |
| ------------------- | ------------------------- |
| `helm version`      | Check Helm version        |
| `helm env`          | Display Helm environment  |
| `helm repo add`     | Add a chart repository    |
| `helm repo update`  | Update repository indexes |
| `helm search repo`  | Search charts             |
| `helm install`      | Install a chart           |
| `helm list`         | List releases             |
| `helm status`       | Inspect a release         |
| `helm get values`   | View release overrides    |
| `helm get manifest` | View generated manifests  |
| `helm upgrade`      | Upgrade a release         |
| `helm history`      | View revision history     |
| `helm rollback`     | Roll back a release       |
| `helm create`       | Create a chart            |
| `helm lint`         | Validate a chart          |
| `helm template`     | Render templates locally  |
| `helm uninstall`    | Remove a release          |

---

## Conclusion

Day 59 helped me understand how Helm makes Kubernetes application management easier, reusable, and more maintainable.

Instead of managing multiple YAML files independently, Helm allows us to package resources into charts, customize deployments through values, and manage application lifecycle through releases.

**Next:** Continue exploring Kubernetes automation and deployment practices as part of my #90DaysOfDevOps journey.

#90DaysOfDevOps #Day59 #Helm #Kubernetes #DevOps #CloudNative
