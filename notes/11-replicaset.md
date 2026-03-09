# 11 - Replication Controllers and ReplicaSets

In the previous section, we learned how to run a single instance of an application using a Pod. But what happens if that Pod crashes or the node it runs on fails? Your application goes offline.

To prevent downtime and ensure **High Availability**, we need a process that constantly monitors our Pods and automatically spins up replacements if they fail. We also need a way to easily scale our application horizontally (run multiple identical Pods) to handle increased user load.

This is the job of the **Replication Controller** and its modern successor, the **ReplicaSet**.

## Core Concepts & The "Why"

* **High Availability:** Even if you only want 1 instance of your application running, you should still use a ReplicaSet. If that single Pod dies, the ReplicaSet will instantly deploy a new one to replace it.
* **Load Balancing & Scaling:** A ReplicaSet allows you to easily specify a "desired state" (e.g., "I want 3 instances running"). It will deploy these Pods across multiple worker nodes to balance the load and expand capacity.
* **The Controller Loop:** The ReplicaSet is a background process (living inside the `kube-controller-manager`) that constantly runs a simple loop: *Are there currently exactly X number of Pods with this specific label? If no, create or delete Pods until there are.*

### Replication Controller vs. ReplicaSet
* **Replication Controller:** The older, original technology. It is largely deprecated in modern Kubernetes.
* **ReplicaSet:** The new, recommended way to set up replication. 
* **The Key Difference:** While they serve the exact same purpose, the ReplicaSet requires a `selector` block (specifically `matchLabels`) in its YAML definition, which allows for much more advanced filtering and grouping of Pods. 

> **CKA Note:** In the real world, you rarely create a ReplicaSet directly. Instead, you create a **Deployment** (covered next in the course), which automatically creates and manages ReplicaSets for you. However, you *must* understand how ReplicaSets work because they are the engine under the hood!

## YAML Definitions & Annotations

Notice how these definition files are essentially "nested" objects. You have the ReplicaSet definition at the top, and a complete Pod definition injected directly into the `template` section.

### Replication Controller (Legacy)

*Note: You will rarely write these, but you may see them on older systems.*

```yaml
# 1. ROOT FIELDS (For the Replication Controller)
apiVersion: v1
kind: ReplicationController
metadata:
  name: myapp-rc
  labels:
    app: myapp

# 2. SPECIFICATION (For the Replication Controller)
spec:
  replicas: 3 # The desired state: We want 3 identical Pods
  
  # 3. THE POD TEMPLATE (The blueprint used to stamp out the replicas)
  # Notice how everything under 'template' is exactly what you'd find in a standard Pod.yaml!
  template: 
    metadata:
      name: myapp-pod
      labels:
        app: myapp
        type: front-end
    spec:
      containers:
        - name: nginx-container
          image: nginx
```

### ReplicaSet (Modern Standard)

```yaml
# 1. ROOT FIELDS (For the ReplicaSet)
# Note the different apiVersion compared to the legacy ReplicationController!
apiVersion: apps/v1 
kind: ReplicaSet
metadata:
  name: myapp-replicaset
  labels:
    app: myapp
    type: front-end

# 2. SPECIFICATION (For the ReplicaSet)
spec:
  replicas: 3
  
  # THE MAJOR DIFFERENCE: The Selector
  # This tells the ReplicaSet *which* Pods it is responsible for managing.
  # It says: "I own any Pod that has the label 'type: front-end'."
  selector: 
    matchLabels:
      type: front-end # <--- This MUST match the labels in the template below!
  
  # 3. THE POD TEMPLATE
  template:
    metadata:
      name: myapp-pod
      labels:
        app: myapp
        type: front-end # <--- Matches the selector above!
    spec:
      containers:
        - name: nginx-container
          image: nginx
```

### Why do we need both a `template` and a `selector` in a ReplicaSet?

A ReplicaSet can actually "adopt" Pods that were already running before the ReplicaSet was even created, simply by matching their labels.

However, it still requires the `template` section. Why? Because if one of those adopted Pods dies in the future, the ReplicaSet needs the blueprint (the template) to know exactly how to build a fresh replacement!

## Managing and Scaling (Commands Cheat Sheet)

### Creating and Viewing

Create the object:

`kubectl create -f replicaset-definition.yml` (or `kubectl apply -f ...`)

List legacy Replication Controllers:

`kubectl get rc`

List modern ReplicaSets:

`kubectl get rs`

(The output shows _DESIRED_ vs _CURRENT_ vs _READY_ states).

### Scaling a ReplicaSet

If your user base suddenly spikes, you need to scale up quickly. There are three ways to do this:

The Declarative Way (Recommended):

Open your YAML file, change replicas: 3 to replicas: 6, save the file, and run:

`kubectl replace -f replicaset-definition.yml (or kubectl apply -f ...)`

The Imperative Scale Command (By File):

`kubectl scale --replicas=6 -f replicaset-definition.yml`

(Warning: This scales the live cluster, but does NOT update the text in your YAML file!)

The Imperative Scale Command (By Name):

`kubectl scale replicaset myapp-replicaset --replicas=6`

### Deleting

Delete the ReplicaSet:

`kubectl delete replicaset myapp-replicaset`

(Note: By default, deleting a ReplicaSet will automatically terminate all the underlying Pods it was managing).