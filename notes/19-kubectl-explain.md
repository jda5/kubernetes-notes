# 19 - Exploring the API (kubectl explain)

When working in production environments, you might not want to waste time switching between your terminal and a web browser. Kubernetes actually has its entire documentation built directly into the command line.

## Finding Resources (`kubectl api-resources`)

If you ever forget the exact name of a resource, its shorthand abbreviation, or which `apiVersion` it belongs to, this is your starting point.

```sh
kubectl api-resources
```

This command:

- Identifies short names (e.g., `po` for pods, `deploy` for deployments, `svc` for services).
- Confirms the exact API group and version you need for your YAML (e.g., knowing whether to use `v1` or `apps/v1`).
- Verifies the strict spelling and casing required by Kubernetes.

## Understanding YAML Fields (`kubectl explain`)

Once you know the resource you want to create, you might forget the exact structure of its YAML file. The `explain` command is essentially a built-in dictionary for Kubernetes objects.

```sh
kubectl explain pods
```

Lists all the root-level fields for a Pod (`apiVersion`, `kind`, `metadata`, `spec`, `status`).

- Shows the exact data type required for each field (e.g., `<string>`, `<Object>`, `<[]Object>`).
- Provides a brief description of what the field actually does.

### Drilling Down into Subfields

```sh
kubectl explain pods.spec
```

- By appending a dot (`.`) and a field name, you can navigate down the YAML hierarchy.
- This specific command lists all the properties that belong strictly inside the spec block (such as `containers`, `volumes`, `nodeSelector`). You can chain these as deep as you need (e.g., `kubectl explain pods.spec.containers.ports`).

## The Recursive Flag (The Ultimate YAML Builder):

```sh
kubectl explain pods --recursive
```

- This outputs the entire, comprehensive tree of all possible fields and subfields for that resource.
- It prints out exactly how the fields are indented and nested, making it incredibly easy to construct a complex YAML file from scratch without ever checking the official docs.

## Quick Command Summary

| Goal | Command |
| --- | --- |
| List all K8s resources and their API versions | `kubectl api-resources` |
| Get definitions for a top-level resource | `kubectl explain <resource>` |
| Get definitions for a specific nested field | `kubectl explain <resource>.<field>` |
| View the entire nested YAML structure | `kubectl explain <resource> --recursive` |