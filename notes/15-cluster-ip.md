# 15 - Services (ClusterIP)

A typical full-stack application is broken down into multiple tiers (e.g., Frontend, Backend, Database, Redis Cache). These tiers need to communicate with one another to function.

**The Problem:** Pods are ephemeral. They die, they scale up, and they get recreated constantly. Because of this, their internal IP addresses are always changing. If your Frontend is hardcoded to talk to the Backend at `10.244.0.3`, the application will break the moment that Pod dies and gets a new IP.

**The Solution:** The `ClusterIP` Service.

## What is a ClusterIP?

A `ClusterIP` Service groups a specific set of Pods together and provides a **single, stable virtual IP address and DNS name** inside the cluster. 

* **Internal Only:** Unlike a `NodePort`, a `ClusterIP` Service is strictly for internal communication. It cannot be accessed from outside the cluster.
* **Stable Interface:** The Backend Pods can simply send requests to the DNS name `back-end`, and Kubernetes will resolve it to the Service's stable IP.
* **Built-in Load Balancing:** The Service acts as an internal load balancer, randomly forwarding incoming requests to one of the healthy Pods running underneath it.
* **The Default Type:** If you create a Service and do not specify a `type` in the YAML, Kubernetes automatically defaults to `ClusterIP`.

By using `ClusterIP` Services, each layer of your application can scale, crash, or move completely independently without ever breaking the communication links between the tiers.

## YAML Definition

Notice how similar this is to the `NodePort` definition. The only differences are the `type` and the omission of the `nodePort` field.

```yaml
apiVersion: v1
kind: Service
metadata:
    # CRUCIAL: This name becomes the internal DNS name. 
    # Other pods will connect to this service using the hostname "back-end".
    name: back-end

spec:
    type: ClusterIP # (Optional) This is the default type if omitted.
    
    # The Array of ports to map
    ports:
        - targetPort: 80    # The port the backend application is listening on inside the Pod
          port: 80          # The port the Service itself listens on
        
    # The Glue: Routes traffic to any Pod with these matching labels
    selector:
        app: myapp
        type: back-end
```

## Essential Commands

* Create the Service:
    
    `kubectl create -f clusterip-definition.yml`

* View Services (to see the assigned Virtual IPs):
    
    `kubectl get services (or kubectl get svc)`