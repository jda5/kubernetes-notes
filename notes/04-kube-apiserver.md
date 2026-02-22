# 04 - `kube-apiserver`

The `kube-apiserver` is the primary management component and the central hub of a Kubernetes cluster. 

Whether you are using the `kubectl` command-line tool or making direct REST API calls (like `POST` requests), you are communicating directly with the `kube-apiserver`. 

## Core Responsibilities

The `kube-apiserver` acts as the cluster's gatekeeper and orchestrator. Its primary duties include:

* **Authentication:** Verifying *who* is making the request.
* **Validation:** Checking if the request is valid and authorized.
* **Retrieval & Updating:** Fetching data from and writing data to the `etcd` cluster.
* **Exclusive `etcd` Access:** It is the *only* Kubernetes component that interacts directly with the `etcd` data store. All other components (scheduler, controller-manager, kubelet) must use the API server to perform cluster updates.

## Workflow Example: Creating a Pod

When you run `kubectl run nginx --image=nginx`, the following step-by-step process occurs:

1. **Request Received:** The `kube-apiserver` authenticates and validates the `kubectl` request.
2. **Initial Creation:** The API server creates a Pod object *without* assigning it to a node, updates the `etcd` datastore, and tells the user the pod was created.
3. **Scheduling:** The `kube-scheduler` (which continuously monitors the API server) notices a new Pod with no assigned node. It determines the best node for the Pod and sends this decision back to the `kube-apiserver`.
4. **Update etcd:** The `kube-apiserver` updates `etcd` with the new node assignment.
5. **Kubelet Execution:** The `kube-apiserver` passes the Pod information to the `kubelet` on the assigned worker node.
6. **Container Creation:** The `kubelet` instructs the Container Runtime (e.g., `containerd`) to pull the image and run the container.
7. **Status Report:** The `kubelet` updates the Pod's status (e.g., "Running") back to the `kube-apiserver`.
8. **Final etcd Update:** The `kube-apiserver` writes this final state to the `etcd` cluster.

## Configuration and Setup

The `kube-apiserver` is essentially a binary executable run with a large number of parameters (handling certificates, authentication modes, encryption, etc.). 

* **Key Parameter:** `--etcd-servers=` is the parameter used to specify the location of the `etcd` server(s) so the API server knows where to save cluster state.
* **Port:** By default, the `kube-apiserver` listens on port **6443**.

### How to View `kube-apiserver` Options

How you inspect the API server's configuration depends entirely on how the cluster was built:

* **If deployed via `kubeadm`:**
  `kubeadm` deploys the API server as a **Static Pod** in the `kube-system` namespace on the master node.
  * **File Path:** You can view and edit its options in the manifest file located at: `/etc/kubernetes/manifests/kube-apiserver.yaml`
* **If deployed "The Hard Way" (Manual Setup):**
  The API server runs as a native systemd service on the master node.
  * **File Path:** You can view its options at: `/etc/systemd/system/kube-apiserver.service`
* **Universal Method:**
  `ps -aux | grep kube-apiserver`
  You can always see the running process and its effective flags by running this command on the master node: