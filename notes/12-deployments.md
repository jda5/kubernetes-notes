# 12 - Deployments

While a ReplicaSet is great for ensuring a specific number of Pods are running, it lacks the advanced features required for managing a live application in a true production environment. 

A **Deployment** is a higher-level Kubernetes object that sits on top of a ReplicaSet. It provides crucial capabilities for upgrading and modifying your application without causing downtime for your users.

## Production Use Cases (Why we use Deployments)

Deployments give us several "superpowers" over basic ReplicaSets:

* **Rolling Updates:** When you release a new version of your app (a new Docker image), you don't want to destroy all the old Pods at once—that causes downtime. A Deployment seamlessly upgrades instances one by one (or in small batches).

* **Rollbacks:** If a new update contains a critical bug, a Deployment allows you to instantly undo the change and roll back to the previous, stable ReplicaSet.
* **Pause and Resume:** If you need to make multiple changes to your environment (like changing resource limits, updating environment variables, and changing the image), you can "pause" the Deployment rollout, apply all changes, and then "resume" it so they roll out together.

## The Kubernetes Object Hierarchy

It is crucial to understand the chain of command here. When you create a Deployment, it triggers a domino effect:

1.  **Deployment:** You create a Deployment with your desired state (e.g., 3 replicas of the `nginx` image).
2.  **ReplicaSet:** The Deployment automatically creates a ReplicaSet to handle the actual scaling.
3.  **Pods:** The ReplicaSet automatically creates the 3 individual Pods.

## The YAML Definition

The YAML definition is **exactly the same** as a ReplicaSet, except for the `kind` field.

```yaml
# 1. ROOT FIELDS
apiVersion: apps/v1
kind: Deployment    # <--- The ONLY difference from a ReplicaSet!
metadata: 
    name: myapp-deployment
    labels:
        app: myapp
        type: front-end

# 2. SPECIFICATION (For the Deployment)
spec:
    replicas: 3
    
    # 3. SELECTOR (Tells the Deployment which Pods it owns)
    selector:
        matchLabels:
            type: front-end
            
    # 4. THE POD TEMPLATE (The blueprint for the Pods)
    template:
        metadata:
            name: myapp-pod
            labels:
                app: myapp
                type: front-end # <--- Must match the selector above
        spec:
            containers:
                - name: nginx-container
                  image: nginx
```

## Essential Commands

Because Deployments create other objects automatically, you have a few ways to check your work.

* **Create or Update the Deployment**
    
    `kubectl apply -f deployment-definition.yml`

* **View the Deployment**
    
    `kubectl get deployments`

* **View the automatically created ReplicaSet**
    
    `kubectl get replicaset` (or `kubectl get rs`)

* **View the automatically created Pods**
    
    `kubectl get pods`

* **The "See Everything" Command**

    `kubectl get all`