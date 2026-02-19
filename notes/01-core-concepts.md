# 01 - Core Concepts

## The Purpose of Kubernetes

Kubernetes (often abbreviated as K8s) is an open-source container orchestration platform.

- Its primary purpose is to host your applications in the form of containers in an automated fashion.
- It allows you to seamlessly deploy, scale and manage as many instances of your application as required.
- It provides built-in mechanisms for load balancing, self-healing (restarting failed containers), and enabling communication between different services within your application architecture.

## Cluster Architecture Overview

A Kubernetes cluster is fundamentally divided into two main segments: the **Control Plane (Master Node)** and the **Worker Nodes**.

### The Control Plane (Master Node) Components

The _Master Node_ plans, schedules, and monitors the cluster using a set of components known collectively as the **Control Plane**.

* `kube-apiserver`: The primary management component and the "front door" of Kubernetes. It exposes the Kubernetes API and is responsible for orchestrating all operations. Every other component (and users) communicates through the API server.
* `etcd`: A highly-available, distributed key-value store. It serves as Kubernetes' backing store for all cluster data, storing the entire configuration and "state" of the cluster. (Note: Because it holds all cluster data, backing up etcd is a critical administrative task).
* `kube-scheduler`: The decision-maker for container placement. It identifies the right worker node to place a newly created container on based on resource requirements, hardware constraints, node capacity and user-defined rules (like taints and tolerations).
* `kube-controller-manager`: Runs continuous background loops (controllers) that monitor the cluster and work to bring the current state of the cluster to the desired state.
    * **Node-Controller**: Manages onboarding new nodes and handles situations where nodes become unavailable.
    * **Replication-Controller**: Ensures that the exact desired number of container instances are running at all times.

### Worker Node Components

Worker nodes are the machines (physical or virtual, on-premise or in the cloud) that do the actual work of hosting your applications as containers. Think of them as the cargo ships carrying your containers.

* `kubelet`: The primary Kubernetes "agent" that runs on every worker node. It listens for instructions from the `kube-apiserver` and executes them (deploying, updating, or destroying containers). It also continuously reports the health and status of the node and its containers back to the **Master Node**.
* `kube-proxy`: A network proxy that runs on each node. It maintains network rules (using `iptables` or IPVS) to ensure that containers can communicate with each other across different nodes. For instance, it allows a web server container on Node A to seamlessly talk to a database container on Node B.
* **Container Runtime**: The underlying software responsible for actually running the containers. While Docker was historically the default, modern Kubernetes relies on runtimes compliant with the **Container Runtime Interface (CRI)**, such as `containerd` or `CRI-O`.

## Glossary of Key Terms

**Cluster**: A set of worker machines (nodes) that run containerized applications, managed by the control plane.

**Node**: A single machine (physical or virtual) within the Kubernetes cluster.

**Control Plane**: The collection of components (usually running on the Master Node) that make global decisions about the cluster and detect/respond to cluster events.

**Container**: A lightweight, standalone, executable package of software that includes everything needed to run an application (code, runtime, system tools, system libraries, and settings).

**Pod**: The smallest and simplest Kubernetes object. A Pod represents a set of running containers on your cluster. (You will learn much more about this soon!)

**Orchestration**: The automated configuration, management, and coordination of computer systems, applications, and services.

**Desired State**: The configuration you specify for your cluster (e.g., "I want 3 copies of this web server running"). Kubernetes constantly works to ensure the actual state matches this desired state.