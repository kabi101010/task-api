# Task API — DevOps Portfolio Project

A REST API for managing tasks, built as an end-to-end DevOps project covering
containerization, CI/CD with security scanning, Kubernetes deployment, and
GitOps.

## What this project demonstrates

- **Application**: A Flask REST API (`app.py`) with full CRUD endpoints,
  tested with `pytest`.
- **Containerization**: Packaged with Docker (`Dockerfile`), including a
  health check.
- **CI/CD with security scanning**: A GitHub Actions pipeline
  (`.github/workflows/ci.yml`) that on every push:
  - Runs the automated test suite
  - Scans the codebase for accidentally committed secrets (Gitleaks)
  - Builds the Docker image and scans it for known vulnerabilities (Trivy)
- **Kubernetes deployment**: Manifests (`k8s/deployment.yaml`,
  `k8s/service.yaml`) that run the app with 2 replicas, liveness/readiness
  health checks, and resource limits.
- **GitOps**: ArgoCD is configured to watch this repository's `k8s/` folder
  and keep the cluster's state in sync with what's committed to Git —
  deployments happen by pushing to GitHub, not by running `kubectl` by hand.

## Architecture

```
Developer pushes code
        |
        v
GitHub Actions (test -> secret scan -> build & scan image)
        |
        v
GitHub repo (k8s/ manifests)
        |
        v
ArgoCD (watches repo, syncs cluster state)
        |
        v
Kubernetes cluster (2 replicas of the Task API)
```

## Endpoints

| Method | Path          | Description     |
|--------|---------------|------------------|
| GET    | /health       | Health check      |
| GET    | /tasks        | List all tasks     |
| POST   | /tasks        | Create a task        |
| PATCH  | /tasks/<id>   | Update a task         |
| DELETE | /tasks/<id>   | Delete a task          |

## Run locally

**With Docker:**
```bash
docker build -t task-api .
docker run -p 5000:5000 task-api
```

**With Kubernetes (Minikube):**
```bash
minikube start --driver=docker
minikube image load task-api:latest
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
minikube service task-api-service
```

**With ArgoCD (GitOps):**
Once ArgoCD is installed in the cluster, create an Application pointing at
this repo's `k8s/` path, then sync — no manual `kubectl apply` needed for
future changes.

## What I learned building this

- Debugging real infrastructure issues: BIOS virtualization settings, PATH
  configuration on Windows, Docker driver connectivity, DNS resolution
  failures when pulling container images, and resource-constrained
  environments.
- How CI/CD pipelines gate code quality and security before deployment.
- How GitOps decouples "what should be running" (declared in Git) from
  "what is running" (reconciled automatically by ArgoCD).

## What's next

- Chaos engineering: intentionally killing pods to verify the app
  self-heals via Kubernetes health checks.
- Applying this same pipeline to a real small organization's project.
