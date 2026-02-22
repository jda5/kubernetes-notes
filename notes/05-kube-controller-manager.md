# 05 - `kube-controller-manager`

In Kubernetes, a **controller** is a non-stop background process (a control loop) that continuously monitors the state of various components within the system. 

Its entire purpose is to constantly compare the **Current State** of the cluster against the **Desired State** (what you asked for), and take immediate action to remediate any differences.

**The Analogy** 

Imagine the Kubernetes cluster as a fleet of ships. A controller is like an administrative office on the command ship. One office monitors the status of the cargo ships (nodes). Another office specifically monitors the cargo containers (pods) to ensure none fall overboard, replacing them immediately if they do.

## The `kube-controller-manager` Component

Instead of running dozens of individual controller processes on your master node, Kubernetes packages all of these different controllers into a single, unified binary/process known as the `kube-controller-manager`.

Whenever you use constructs like Deployments, Services, Namespaces, or Persistent Volumes, the "intelligence" that makes them work is actually a specific controller living inside the `kube-controller-manager`.

## Key Controller Examples

### The Node Controller

Responsible for monitoring the health of the worker nodes and taking action if a node fails. It communicates through the `kube-apiserver` to check node status.

**The Node Failure Timeline**

1. **Status Check (`--node-monitor-period`):** Checks node health every **5 seconds**.
2. **Unreachable (`--node-monitor-grace-period`):** If it stops receiving a heartbeat, it waits **40 seconds** before marking the node as "Unreachable".
3. **Eviction (`--pod-eviction-timeout`):** Once marked unreachable, it gives the node **5 minutes** to recover. If it doesn't, the controller terminates the pods on the dead node and provisions them on healthy nodes.

### The Replication Controller

Responsible for monitoring the status of ReplicaSets. It ensures that the exact desired number of pods are running at all times. If a pod crashes or is deleted, this controller instantly spins up a replacement.

## Configuration and Setup

When you run the `kube-controller-manager`, you can customize its behavior using various flags. 

* **Timeouts and Periods:** The timing settings mentioned above (5s, 40s, 5m) can all be customized using flags like `--node-monitor-period`, `--node-monitor-grace-period`, and `--pod-eviction-timeout`.
* **Enabling/Disabling Controllers:** By default, all controllers are enabled. However, you can use the `--controllers` flag to specify exactly which ones to turn on. *(Troubleshooting tip: If a specific K8s feature like Deployments isn't working, check if its controller was accidentally disabled here!)*

## How to View Configuration Options

Just like the `kube-apiserver`, how you find the configuration depends on your cluster setup:

* **If deployed via `kubeadm` (Standard CKA environment):**
  It runs as a Static Pod in the `kube-system` namespace.
  * **File Path:** `/etc/kubernetes/manifests/kube-controller-manager.yaml`
* **If deployed "The Hard Way" (Manual Setup):**
  It runs as a native systemd service.
  * **File Path:** `/etc/systemd/system/kube-controller-manager.service`
* **Universal Method:**
  To see the active process and its effective flags, run:
  `ps -aux | grep kube-controller-manager`