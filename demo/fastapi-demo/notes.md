# Practical Lab: Deploying a Multi-Tier App (FastAPI + MySQL)

This lab translated a standard Docker Compose architecture (Frontend API + Database) into native Kubernetes objects.

## Key Conceptual Takeaways

* **Kubernetes Doesn't Build Source Code:** Unlike Docker Compose (`build: .`), Kubernetes expects container images to already be built. You must build your images locally or push them to a registry (like Docker Hub) before K8s can use them.
* **The "Translation" Map:**
  * **`.env` files** become **`Secret`** or **`ConfigMap`** objects.
  * **Docker Volumes** become **`PersistentVolumeClaim` (PVC)** objects.
  * **Docker Compose Services** become a combination of a **`Deployment`** (to run the pods) AND a **`Service`** (to handle the networking).
* **Internal DNS is Magic:** If you create a Kubernetes `Service` named `db`, Kubernetes automatically creates an internal DNS record for it. Your other apps can connect to the database simply by using `host="db"`.
* **Labels and Selectors are the Glue:** Deployments know which Pods to manage, and Services know where to send network traffic, entirely by matching `labels` (e.g., `app: fastapi`).
* **The `apply` Merge Quirk:** Running `kubectl apply -f` merges your text file with the cluster's current memory. If you delete a line from your YAML (like a secret password), `apply` will *not* delete it from the cluster. To truly remove it, you often have to `delete` and recreate the object.
* **External Access:** By default, everything inside K8s is isolated. To access a web app from your local browser, you must expose it using a `NodePort` Service, a `LoadBalancer`, or use a port-forwarding tunnel.

---

## Essential Commands Cheat Sheet

### Image Management (Local/Minikube)

* `docker build -t my-app:latest .` : Build the container image locally.
* `minikube image load my-app:latest` : Sideload the local image directly into Minikube's internal registry (bypassing Docker Hub).

### Deploying & Scaling
* `kubectl apply -f manifest.yaml` : Create or update resources defined in a YAML file.
* `kubectl delete -f manifest.yaml` : Completely tear down all resources defined in a YAML file.
* `kubectl get pods -w` : List pods and **watch** (`-w`) them update in real-time. Hit `Ctrl+C` to exit.
* `kubectl scale deployment my-app --replicas=5` : Instantly scale a deployment up or down to the specified number of pods.

### Troubleshooting (The "CrashLoopBackOff" Toolkit)

* `kubectl logs <pod-name>` : View the standard output/error logs for a specific pod.
* `kubectl logs <pod-name> --previous` : View the logs of the *previously crashed* container (crucial if the pod keeps restarting before you can read the logs).
* `kubectl describe pod <pod-name>` : View detailed metadata and the chronological "Events" leading up to a pod's failure (great for storage/image pull errors).

### Restarting Pods

* `kubectl delete pod <pod-name>` : Delete a specific pod. (If managed by a Deployment, a fresh one will instantly take its place).
* `kubectl delete pod -l app=my-app` : Delete all pods matching a specific label.
* `kubectl rollout restart deployment my-app` : Gracefully restart all pods in a deployment one-by-one (useful when you update your code/image but the YAML hasn't changed).

### Networking & Access

* `minikube service <service-name>` : Minikube-specific command to create a tunnel and automatically open the Service in your Mac's web browser.
* `kubectl port-forward service/<service-name> 8000:80` : The industry-standard way to securely map a port on your local machine (8000) to a port on the K8s Service (80).

### Extra

* `kubectl run [name] --image=[image] --dry-run=client -o yaml`: Creates a starter YAML file with a container with the Redis image.
    `--dry-run=client`: Tells `kubectl` not to send the request to the kube-apiserver. It just evaluates the command locally on your machine.
    -`o yaml`: Tells `kubectl` to take that "simulated" object and print it out as a YAML definition on your screen.