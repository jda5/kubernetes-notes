# 06 - `kube-scheduler`

The `kube-scheduler` is the component responsible for deciding which pod goes on which worker node. 

The scheduler *only* decides the placement. It does **not** actually place or run the pod on the node. Executing the deployment is strictly the job of the `kubelet` (the "captain of the ship").

## Why Do We Need a Scheduler?

In a cluster with many nodes (ships) and many pods (containers), you must ensure that the right workload ends up in the right place based on:

* **Capacity:** Making sure a node has enough CPU and memory to physically accommodate the pod.
* **Destination/Purpose:** Ensuring certain pods are placed on nodes dedicated to specific applications or environments.

## The Two-Phase Scheduling Process

When the `kube-scheduler` sees a new pod with no assigned node, it goes through a specific two-step process to find the perfect home for it:

### Phase 1: Filtering (Predicates)

The scheduler evaluates all nodes in the cluster and filters out the ones that physically cannot run the pod. 

* *Example:* If a pod requires 4 CPUs and 8GB of RAM, the scheduler immediately eliminates any nodes that do not have those resources available. 

### Phase 2: Ranking (Priorities)

After filtering, the scheduler is left with a list of capable nodes. It then ranks these remaining nodes to identify the absolute best fit.

* *Scoring:* It uses a priority function to assign a score to each node on a scale of 0 to 10.
* *Example:* The scheduler calculates how many resources would be left over on a node *after* placing the pod. A node that would have 6 CPUs free gets a higher score than a node that would only have 2 CPUs free. The node with the highest rank wins the pod.

## Configuration and Setup

If you are building the cluster from scratch, you download the `kube-scheduler` binary from the Kubernetes release page and run it as a service, specifying its configuration file.

### How to View `kube-scheduler` Options

Just like the other control plane components, locating its configuration depends on your installation method:

* **If deployed via `kubeadm` (Standard CKA environment):**
  It runs as a Static Pod in the `kube-system` namespace.
  * **File Path:** `/etc/kubernetes/manifests/kube-scheduler.yaml`
* **If deployed "The Hard Way" (Manual Setup):**
  It runs as a native systemd service.
  * **Universal Method to view:** Run `ps -aux | grep kube-scheduler` on the master node to see the running process and its effective flags.