# 07 - `kubelet`

The `kubelet` is the primary "agent" that runs on every single worker node in a Kubernetes cluster. 

**The Analogy**

If the worker node is a cargo ship, the `kubelet` is the captain of that ship. The captain handles the paperwork to join the fleet, receives direct orders from the command center (Master Node), loads/unloads cargo (containers), and radios back regular status reports.

## Core Responsibilities

The `kubelet` acts as the bridge between the Kubernetes Control Plane and the actual node's hardware/container runtime. Its main duties include:

* **Node Registration:** When a new node is provisioned, the `kubelet` is responsible for registering that node with the Kubernetes cluster (via the `kube-apiserver`).
* **Executing Instructions:** When it receives instructions to load a container or a Pod (indirectly from the scheduler, passed through the API server), it takes action.
* **Interacting with the Runtime:** It does not run containers itself. Instead, it instructs the Container Runtime Engine (like `containerd` or `CRI-O`) to pull the required image from a registry and run the container instance.
* **Monitoring & Reporting:** The `kubelet` continuously monitors the state and health of the Pods and containers running on its node. It sends these status reports back to the `kube-apiserver` on a regular, timely basis so the Control Plane always knows what is happening on the ground.

## Installation and Setup (CKA Crucial Detail)

**🚨 Important Exception:** Unlike the API Server, Scheduler, and Controller Manager, **the `kubeadm` tool does *not* automatically deploy the `kubelet` as a Pod.** Because the `kubelet` is the component responsible for creating Pods in the first place, it must already be running natively on the host machine to do its job. 

* You must manually install the `kubelet` on your worker nodes (and the master node, if it is also acting as a worker). 
* It is typically downloaded as an installer/binary, extracted, and configured to run as a native **systemd service** on the Linux host.

## How to View `kubelet` Configuration

Because it runs as a native system service rather than a Kubernetes Pod, you interact with it using standard Linux administrative tools:

* **View the Process:** You can view the running `kubelet` process and its effective configuration flags by logging into the node and running:
  `ps -aux | grep kubelet`
* **Manage the Service:** You will frequently use `systemctl` commands (like `systemctl status kubelet` or `systemctl restart kubelet`) during cluster troubleshooting.

*(Note: Advanced configurations like generating certificates and TLS bootstrapping the `kubelet` will be covered later in the course).*