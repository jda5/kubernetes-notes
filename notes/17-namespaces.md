# 17 - Namespaces

Think of a Kubernetes cluster as a large neighborhood, and **Namespaces** as the individual houses within it.

* Inside a house, family members can just use first names to talk to each other.
* To talk to someone in a _different_ house, you need to use their full name and address.
* Each house can have its own rules and its own budget (Resource Quotas).

Namespaces allow you to logically isolate resources (like Dev vs. Production) within the exact same physical Kubernetes cluster.

## The Built-In Namespaces

When you first spin up a Kubernetes cluster, it automatically creates three namespaces:

1. **`default`**: Where your resources go if you don't specify a namespace. (This is where we have been working so far).
2. **`kube-system`**: Where Kubernetes puts its internal routing, DNS, and networking pods. (Isolated to prevent you from accidentally deleting core cluster components).
3. **`kube-public`**: A namespace for resources that should be accessible to all users across the cluster.

## DNS & Cross-Namespace Communication

Resources *within* the same namespace can talk to each other simply by using their service names (e.g., a web pod can just ping `db-service`).

If a web pod in the `default` namespace needs to talk to a database in the `dev` namespace, it must use the **Fully Qualified Domain Name (FQDN)**. 

When a Service is created, Kubernetes automatically adds a DNS entry in this exact format:

`service-name.namespace.svc.cluster.local`

**Example:**

To reach the `db-service` located in the `dev` namespace, you would connect to:

`db-service.dev.svc.cluster.local`

## Creating and Managing Namespaces

You can create namespaces either imperatively (via CLI) or declaratively (via YAML).

**Imperative Creation:**

```bash
kubectl create namespace dev
```

**Declarative Creation (YAML):**

```yaml
apiVersion: v1
kind: Namespace
metadata:
    name: dev
```

**Assigning a Pod to a Namespace:**

To ensure a Pod is always created in the correct namespace, define it under metadata in your YAML:

```yaml
apiVersion: v1
kind: Pod
metadata:
    name: myapp-pod
    namespace: dev  # <--- Forces the Pod into the 'dev' namespace
    labels:
        app: myapp
```

_(Alternatively, you can apply an existing file to a specific namespace: `kubectl apply -f pod.yml --namespace=dev`)_

## Essential CLI Commands

By default, kubectl only looks in the default namespace. To interact with others, you must use the `--namespace` (or `-n`) flag.

* Get Pods in a specific namespace:

    `kubectl get pods --namespace=kube-system`

* Get Pods across ALL namespaces (Crucial for debugging):

    `kubectl get pods --all-namespaces` (or `kubectl get pods -A`)

### Switching the Default Namespace

If you are working heavily in the `dev` namespace, typing `--namespace=dev` every time gets tedious. You can change your default context so you don't have to type it anymore:

```bash
kubectl config set-context $(kubectl config current-context) --namespace=dev
```

_(Note: This reads your current cluster context, and updates its default namespace permanently until you change it back)._

## Resource Quotas

To prevent a single namespace (like `dev`) from hogging all the physical CPU and Memory of your worker nodes, you can bind a ResourceQuota to it.

```yaml
apiVersion: v1
kind: ResourceQuota
metadata:
    name: compute-quota
    namespace: dev # <--- Applies these limits to the entire 'dev' namespace

spec:
    hard:
        pods: "10"             # Max 10 pods allowed
        requests.cpu: "4"      # Guarantees 4 total CPUs for the namespace
        requests.memory: 5Gi   # Guarantees 5GB of Memory
        limits.cpu: "10"       # Hard cap: Cannot exceed 10 CPUs
        limits.memory: 10Gi    # Hard cap: Cannot exceed 10GB of Memory
```