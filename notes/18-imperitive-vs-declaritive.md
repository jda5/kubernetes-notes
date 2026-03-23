# 18 - Imperative vs. Declarative Workflows

In the "Infrastructure as Code" world, there are two primary ways to manage your environments: Imperative and Declarative. 

**The Analogy:**

* **Imperative (The Taxi):** You give step-by-step instructions. "Turn left, go two blocks, turn right, stop at the red house." You define exactly *how* to get there.
* **Declarative (The Uber):** You simply provide the final destination. "Take me to Tom's house." The system figures out the best path to get there. You define *what* you want.

## The Imperative Approach (Commands & Explicit Actions)

In Kubernetes, the imperative approach means telling the cluster exactly what to do using explicit commands to create, update, or delete objects.

**Common Imperative Commands:**

* `kubectl run` (Create a pod)
* `kubectl create` (Create a deployment, service, namespace, etc.)
* `kubectl expose` (Create a service to expose an object)
* `kubectl edit` (Edit a live object's configuration)
* `kubectl scale` (Scale a deployment or replica set)
* `kubectl set image` (Update an image on a deployment)
* `kubectl replace -f file.yaml` (Replace an object using a file)
* `kubectl delete -f file.yaml` (Delete an object)

**Pros:**

* Extremely fast for one-off tasks.
* Essential for passing the CKA exam before time runs out.

**Cons:**

* **Hard to Track:** Commands are run once and only exist in your terminal history. If you leave the company, nobody knows how you built the cluster.
* **The `kubectl edit` Trap:** If you use `kubectl edit` to change a live object, it does *not* update your local YAML file. If a teammate later runs `kubectl apply -f` using the old local file, your live changes will be permanently overwritten and lost.
* **Error Prone:** If you run a `create` command but the object already exists, it crashes. If you run a `replace` command but the object *doesn't* exist, it crashes.

## The Declarative Approach (Infrastructure as Code)

The declarative approach uses a single command to tell Kubernetes: *"Read these YAML files, look at the cluster's current state, and figure out what needs to be added, changed, or deleted to make them match."*

**The Command:**

* `kubectl apply -f file.yaml` (or `kubectl apply -f /directory/`)

**Pros:**

* **Intelligent:** `apply` knows if an object exists or not. If it doesn't, it creates it. If it does, it simply updates the changed fields. It rarely throws "already exists" errors.
* **Auditable:** Your entire infrastructure lives in YAML files. You can save these to Git (Version Control), track exactly who made what changes, and require code reviews before applying them to Production.

## CKA Exam Tips: Mastering Imperative Commands

While production environments use the declarative (`apply`) approach, **the CKA exam demands the imperative approach to save time.** Instead of writing YAML from scratch, use these commands to generate templates instantly. 

### The Magic Flags

* `--dry-run=client`: Validates your command but does **not** actually create the resource in the cluster.
* `-o yaml`: Outputs the resulting configuration to your screen in YAML format.
* `> file.yaml`: Redirects that output into a file so you can edit it.

### Pods

* **Create a Pod instantly:** `kubectl run nginx --image=nginx`
* **Generate a Pod YAML:** `kubectl run nginx --image=nginx --dry-run=client -o yaml > pod.yaml`

### Deployments

* **Create a Deployment:** `kubectl create deployment nginx --image=nginx`
* **Create a Deployment with multiple replicas:** `kubectl create deployment nginx --image=nginx --replicas=4`
* **Scale an existing Deployment:** `kubectl scale deployment nginx --replicas=4`
* **Generate a Deployment YAML:** `kubectl create deployment nginx --image=nginx --dry-run=client -o yaml > deploy.yaml`

### Services

Creating services imperatively has some quirks. You have two options, but both have limitations: `expose` vs. `create service`.

**Option A: Using `expose` (Recommended)**

* **Command:** `kubectl expose pod redis --port=6379 --name redis-service --dry-run=client -o yaml`
* **Pros:** Automatically pulls the exact labels from the Pod and uses them as the Service's selectors.
* **Cons:** It cannot accept a `--node-port` flag. If you need a specific NodePort, generate the YAML first, manually type the `nodePort: X` under the ports array, and then `apply` it.

**Option B: Using `create service`**

* **Command:** `kubectl create service clusterip redis --tcp=6379:6379 --dry-run=client -o yaml`
* *(For NodePort):* `kubectl create service nodeport nginx --tcp=80:80 --node-port=30080 --dry-run=client -o yaml`
* **Pros:** Allows you to specify the exact ports and node ports right in the command.
* **Cons:** It does **not** use the pod's labels as selectors. It blindly assumes the selector is `app=redis`. If your pod's labels are different, the service will not connect to it. You must generate the YAML and fix the selectors manually.