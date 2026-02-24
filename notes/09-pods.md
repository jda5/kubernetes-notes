# 09 - Pods

Before diving into Pods, we assume that your application is already built into a container image, stored in an image registry (like Docker Hub), and that your Kubernetes cluster is up and running.

Our ultimate goal is to deploy our application containers onto the worker nodes. However, **Kubernetes does not deploy containers directly on worker nodes.**

## What is a Pod?

Instead of deploying a container directly, Kubernetes encapsulates the container into an object known as a **Pod**. 

* A Pod is a single instance of an application.
* It is the smallest and simplest deployable object that you can create in Kubernetes.
* You can think of a Pod as a logical "wrapper" or "host" specifically built to run your container.

## The Golden Rule of Scaling

When user demand increases, you need to scale your application. In Kubernetes, there is a strict rule for how to do this:

* **To scale UP:** You create *new* Pods altogether, each running a new instance of the application.
* **To scale DOWN:** You delete existing Pods.
* **The Rule:** You **do not** add additional application containers to an existing Pod to scale it. 

Typically, Pods maintain a **1-to-1 relationship** with the containers running your application. If a node runs out of physical capacity, the `kube-scheduler` will simply place your new Pods onto a different worker node in the cluster.

## Multi-Container Pods

While the 1-to-1 relationship is the standard, you are not strictly restricted to a single container per Pod. A single Pod *can* house multiple containers, but usually only when they serve different, complementary purposes.

**The Helper (Sidecar) Pattern**

Imagine your main web application needs a helper process to fetch data, process uploaded files, or forward logs. 

* By placing the helper container in the *same* Pod as the main application container, Kubernetes manages them as a single entity.
* **Shared Network:** They share the same network namespace. The two containers can communicate with each other directly by simply referencing `localhost`.
* **Shared Storage:** They can easily mount and share the exact same storage volumes.
* **Shared Fate:** They are created together and destroyed together. If the Pod dies, both containers die.

*(Note: While multi-container pods are incredibly powerful for these specific use cases, they are relatively rare. Most of the time, you will stick to single-container pods).*

## Managing Pods (CKA Crucial Commands)

To deploy and view Pods, you will use the `kubectl` command-line tool.

**Creating a Pod**

To deploy a Pod using an image from a registry (like the `nginx` image from Docker Hub), use the `run` command:
`kubectl run my-web-pod --image=nginx`

**Viewing Pods**

To see a list of all Pods currently in your cluster and their statuses:
`kubectl get pods`

**Common Pod States**

* `ContainerCreating`: The `kubelet` is currently instructing the runtime to pull the image and start the container.
* `Running`: The container is successfully running inside the Pod.

*(Note: Simply creating a Pod does not automatically make it accessible to external users. You can access it internally from within the cluster, but exposing it externally requires a **Service**).*