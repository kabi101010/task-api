# Task API

A tiny REST API for managing tasks — built as the foundation for a larger
DevOps portfolio project (CI/CD, Kubernetes + GitOps, security scanning,
and chaos engineering will be layered on top of this in later steps).

## Endpoints

| Method | Path             | Description        |
|--------|------------------|---------------------|
| GET    | /health          | Health check        |
| GET    | /tasks           | List all tasks      |
| POST   | /tasks           | Create a task        |
| PATCH  | /tasks/<id>      | Update a task        |
| DELETE | /tasks/<id>      | Delete a task        |

## Run locally (no Docker)

```bash
pip install -r requirements.txt
python app.py
```

Visit http://localhost:5000/health — you should see `{"status": "ok"}`.

## Run with Docker

Build the image:

```bash
docker build -t task-api .
```

Run the container:

```bash
docker run -p 5000:5000 task-api
```

Test it:

```bash
curl http://localhost:5000/health

curl -X POST http://localhost:5000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Learn Docker"}'

curl http://localhost:5000/tasks
```

## Why this project exists

This is step 1 of a larger portfolio project. The plan:

1. **This step** — a simple, working app, containerized with Docker.
2. CI/CD pipeline with security scanning (GitHub Actions + Trivy).
3. Deploy to Kubernetes using GitOps (ArgoCD).
4. Chaos engineering — kill the container on purpose, show it recovers.
5. Document the architecture and reasoning.
6. Apply the same pipeline to a real small organization's app.

Each step builds directly on this one, so getting this part solid matters
more than making it fancy.
