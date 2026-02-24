# 10 - YAML in Kubernetes (Pod Definition)

Kubernetes uses YAML files as the standard input for creating and managing all cluster objects (Pods, ReplicaSets, Deployments, Services, etc.). 

Every single Kubernetes definition file *must* contain four top-level (root) fields. If you are missing any of these, Kubernetes will reject your file.

## The Four Required Root Fields

* **`apiVersion`**: The version of the Kubernetes API you are using to create the object. This changes depending on what you are trying to create. For a Pod, this is always `v1`. *(Other examples include: `apps/v1` for Deployments).*
* **`kind`**: The type of object you are trying to create (e.g., `Pod`, `Service`, `ReplicaSet`, `Deployment`). Note that this is usually capitalized.
* **`metadata`**: Data *about* the object. This is a dictionary that strictly accepts specific keys defined by Kubernetes (like `name` and `labels`).
    * **`labels`**: A sub-dictionary under metadata. Unlike the strict `metadata` keys, you can put *any* custom key-value pairs you want under `labels` (e.g., `app: frontend`, `tier: database`). This is crucial for filtering and grouping objects later!
* **`spec`**: The specification of the object. This section varies wildly depending on the `kind` of object you are creating. It tells Kubernetes exactly what you want inside the object.

## Annotated Pod Example

Here is a standard Pod definition file (`pod-definition.yaml`), annotated to explain exactly what each line does:

```yaml
# API VERSION: For a Pod, this is always v1.
apiVersion: v1

# KIND: We are telling Kubernetes to create a Pod object.
kind: Pod

# METADATA: Data identifying the object.
metadata:
    # The actual name of the Pod in the cluster.
    name: myapp-pod
    # Custom tags to help us identify and filter this Pod later.
    labels:
        app: myapp
        type: front-end

# SPEC: The exact configuration of the Pod's contents.
spec:
    # 'containers' is an array, indicated by the dash below.
    containers:
        # The dash indicates the first item in the 'containers' list.
        - name: nginx-container
          # The image to pull from the container registry (e.g., Docker Hub).
          image: nginx
```