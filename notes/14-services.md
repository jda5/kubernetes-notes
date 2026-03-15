# 14 - Services (NodePort)

Pods are ephemeral and have internal IP addresses (e.g., `10.244.0.2`) that cannot be pinged from outside the cluster. 

**Services** are Kubernetes objects that solve this problem. They enable loose coupling between microservices by providing a stable, virtual interface for communication — whether that is frontend-to-backend communication, or exposing your app to external users on your laptop.

## Types of Services

* **NodePort:** Exposes the Service on each physical Node's IP at a static port. Used for external access.
* **ClusterIP (Default):** Creates a virtual IP inside the cluster to enable internal communication between different Pods/tiers. 
* **LoadBalancer:** Provisions an external load balancer (via supported Cloud Providers like AWS, GCP, Azure) to distribute traffic.

## Deep Dive: The NodePort Service

A NodePort service bridges the gap between the external network and the internal Pod network. To understand it, you must understand the "Three Ports" from the perspective of the Service:

```
             ┌──────────────────────────────────────────────────────┐
             │                                                      │
             │                                                      │
             │          ╭───────────────╮                           │
             ├───┐      │               │                           │
             │   │      │               │ (2) Port                  │
(3) NodePort │   ├ ─ ─ ─     Service    ├ ─ ─ ─ ─ ─                 │
             │   │      │               │          │                │
             ├───┘      │               │                           │
             │          ╰───────────────╯          │(3) TargetPort  │
             │                                ╭──── ──────────╮     │
             │                                │               │     │
             │                                │               │     │
             │                                │      App      │     │
             │                                │               │     │
             │                                │Pod            │     │
             │                                ╰───────────────╯     │
             │ Node                                                 │
             └──────────────────────────────────────────────────────┘
```

1. `nodePort`: The port opened on the physical Worker Node itself. This is what you hit from your external laptop (e.g., `http://192.168.1.2:30008`). _Must be within the valid range of 30000 - 32767_.
2. `port` (Mandatory): The port on the virtual Service object itself.
3. `targetPort`: The port that the actual application container is listening on inside the Pod (e.g., port `80` for a web server). (_If omitted, it defaults to the same value as port_).

## The "Magic" Features of Services

Services do much more than just map ports. They are incredibly dynamic:

* **Connected via Selectors**: Just like ReplicaSets, Services use `labels` and `selectors` to know which Pods to route traffic to.
* **Built-in Load Balancing**: If your Service's selector matches 3 running Pods, the Service automatically acts as a load balancer, distributing external requests across all 3 Pods using a random algorithm.
* **Cluster-Wide Span**: A NodePort service spans _all_ nodes in the cluster. If you have 3 Worker Nodes, the `nodePort` (e.g., `30008`) is opened on all 3. You can access your application using the IP address of _any_ node in the cluster, and the Service will route it to the correct Pod.

## YAML Definition

```yaml
apiVersion: v1
kind: Service
metadata:
    name: myapp-service
spec:
    type: NodePort # Defines the type of service
    
    # The Array of ports to map
    ports:
        - targetPort: 80    # Port on the Pod
          port: 80          # Port on the Service (Mandatory)
          nodePort: 30008   # Port on the physical Node (30000-32767)
          
    # The Glue: Routes traffic to any Pod with these labels
    selector:
        app: myapp
        type: front-end
```

## Commands

* Create the service (or use `apply`).

    `kubectl create -f service-definition.yml`

* List all services to view their assigned Cluster-IPs and port mappings.

    `kubectl get services`