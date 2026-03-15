# 16 - Services (LoadBalancer)

While a `NodePort` Service successfully exposes your application to the outside world, it is not ideal for end-users. 

**The Problem with NodePort:** * Users have to access your app using a clunky combination of a Node's IP address and a high port number (e.g., `http://192.168.1.70:30008`).

* If you have a 4-node cluster, you have 4 different IP addresses. Which one do you give to the user?
* To give users a single, clean URL (like `www.example-app.com`), you would have to manually deploy, configure, and maintain your own external load balancer (like HAProxy or NGINX) to sit in front of your nodes. 

**The Solution:** The `LoadBalancer` Service.

## What is a LoadBalancer Service?

The `LoadBalancer` Service type instructs Kubernetes to reach out to the underlying cloud provider (AWS, Google Cloud, Azure) and automatically provision a native cloud load balancer.

* **Single Point of Entry:** The cloud provider spins up a load balancer, assigns it a single public IP address (or DNS name), and automatically configures it to route external traffic to your underlying worker nodes.
* **Hands-Off Management:** You don't have to manually configure HAProxy or update routing tables when nodes are added or removed. Kubernetes handles the integration automatically.

## The "Unsupported Environment" Fallback

**Crucial Note:** Native LoadBalancers *only* work if your cluster is hosted on a supported cloud platform (AWS, GCP, Azure, etc.). 

If you set a Service to `type: LoadBalancer` in an unsupported local environment (like VirtualBox, bare-metal servers, or a standard Minikube setup), **it will not crash**. Instead, Kubernetes will simply fall back to creating a standard `NodePort` service. It will open the high port on your nodes, but it won't be able to magically conjure an external cloud load balancer out of thin air.

## YAML Definition

The definition is nearly identical to a `NodePort`, except for the `type` declaration.

```yaml
apiVersion: v1
kind: Service
metadata:
    name: frontend-service
spec:
    # Instructs K8s to request a Load Balancer from the Cloud Provider
    type: LoadBalancer 
    
    ports:
        - targetPort: 80    # The port the app container listens on
          port: 80          # The port the Service listens on
          # Note: K8s still assigns a NodePort in the background, 
          # but the Cloud LB handles hitting it for you.
        
    selector:
        app: myapp
        type: front-end
```

## Commands

* Create the service.
    `kubectl apply -f loadbalancer-definition.yml`

* List the services.
    `kubectl get services`
    
    _Under the EXTERNAL-IP column, it will say <pending> for a few minutes while the cloud provider provisions the hardware, and will eventually populate with a public IP or URL._