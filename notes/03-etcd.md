# 03 - etcd

`etcd` is a distributed, reliable, key-value store. It acts as the absolute "source of truth" for configuration data, service discovery information, and coordination primitives in distributed systems. 

Think of it as a highly available database that multiple machines can read from and write to, with strong consistency guarantees.

## How `etcd` Works

### Consensus Algorithm

- `etcd` uses the **Raft** consensus algorithm to maintain consistency across multiple nodes.
- **Raft** is a protocol that ensures all nodes in a cluster agree on the order of operations and that data remains consistent even when some nodes fail.
- The cluster elects a **Leader** that handles all write requests, while **Followers** replicate the data.

### Key-Value Storage & MVCC (Multi-Version Concurrency Control)

- Keys in `etcd` can have associated metadata like TTL (time-to-live) for automatic expiration. The storage engine uses a B+ tree structure for efficient range queries.
- `etcd` maintains multiple versions of each key. This allows for consistent, reliable reads even while concurrent writes are happening.

### Watch API & Notifications

- Applications can subscribe to changes on specific keys or key ranges. When data changes, `etcd` immediately notifies all watchers, making it excellent for real-time configuration updates and service discovery.
- `etcd` provides both RESTful HTTP and more efficient gRPC interfaces for client communication.

## Redis vs `etcd`

| **Feature**              | **Redis**                           | **etcd**                              |
|----------------------|----------------------------------|-----------------------------------|
| Primary Purpose      | High-performance cache & DB     | Distributed coordination          |
| Storage Location     | In-memory (RAM)                 | On-disk with memory caching       |
| Performance          | 100,000+ ops/sec                | 1,000-10,000 ops/sec              |
| Consistency Model    | Eventually consistent (cluster) | Strongly consistent (Raft)        |
| Data Types           | Rich (lists, sets, hashes, etc) | Simple key-value only             |
| Typical Cluster Size | 3-1000+ nodes                   | 3-7 nodes                         |
| Best For             | Caching, sessions, real-time    | Service discovery, config         |
| Durability           | Optional (can persist to disk)  | Built-in (every write persisted)  |
| Watch/Notifications  | Pub/Sub, keyspace notifications | Native watch API                  |
| Use Case Examples    | User sessions, leaderboards     | Kubernetes state, service registry |

## etcd in Kubernetes

In Kubernetes, `etcd` is the ultimate backend data store. It stores absolutely everything regarding the cluster: nodes, pods, configs, secrets, service accounts, roles, role bindings, and the desired state of all resources.

- **The Single Source of Truth:** Every piece of information you see when you run a command like `kubectl get pods` is being fetched from the `etcd` server.
- **State Confirmation:** A change to your cluster (e.g., deploying a new pod, scaling a replica set) is only considered "complete" or "successful" once it has been securely written to the `etcd` database.
- **Exclusive Access:** The **`kube-apiserver`** is the *only* Kubernetes component that communicates directly with `etcd`. All other components (like the scheduler or kubelet) must go through the API server to read or write cluster state.

`etcd` listens on port **2379** for client communication (talking to the `kube-apiserver`) and port **2380** for server-to-server communication (talking to other `etcd` nodes in a cluster).

`etcd` can be deployed in two main ways:

1. **Stacked:** The `etcd` nodes sit on the exact same master nodes as the `kube-apiserver`. (Easier to manage, but if a node goes down, you lose both a control plane and an `etcd` instance).
2. **External:** The `etcd` cluster runs on its own dedicated set of servers, completely separate from the control plane nodes. (More complex, but highly resilient).

## Extra: Relational DB vs Document Store vs KV Store

| Name            | Relational DB   | Document Store     | Key-Value Store    |
|-----------------|-----------------|--------------------|--------------------|
| Schema          | ✅ Yes           | ❌ No               | ❌ No               |
| Complex Queries | ✅ Yes (SQL)     | ⚠️ Limited          | ❌ No               |
| Performance     | ✅ Good          | ✅ Good             | ✅✅ Great           |
| Flexibility     | ❌ Rigid         | ✅ Flexible         | ✅ Flexible         |
| Best For        | Structured data | Un/Semi-structured | Simple fast lookup |
