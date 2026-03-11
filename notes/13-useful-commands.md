# 13 - Useful Commands

Here's a tip!

Manually writing YAML files from scratch is slow and prone to indentation errors. Use these Imperative Commands to generate templates or create objects instantly.

**Rule of Thumb:** Always try to generate a YAML file first using `--dry-run=client -o yaml`, modify it if needed, and then apply it.

* Create an NGINX Pod

    `kubectl run nginx --image=nginx`

* Generate POD Manifest YAML file (-o yaml). Don't create it(--dry-run)

    `kubectl run nginx --image=nginx --dry-run=client -o yaml`

* Create a deployment

    `kubectl create deployment --image=nginx nginx`

* Generate Deployment YAML file (-o yaml). Don't create it(--dry-run)

    `kubectl create deployment --image=nginx nginx --dry-run=client -o yaml`

* Generate Deployment YAML file (-o yaml). Don’t create it(–dry-run) and save it to a file.

    `kubectl create deployment --image=nginx nginx --dry-run=client -o yaml > nginx-deployment.yaml`

* Make necessary changes to the file (for example, adding more replicas) and then create the deployment.

    `kubectl create -f nginx-deployment.yaml`

    *or*
    
    In k8s version 1.19+, we can specify the `--replicas` option to create a deployment with 4 replicas.

    `kubectl create deployment --image=nginx nginx --replicas=4 --dry-run=client -o yaml > nginx-deployment.yaml `