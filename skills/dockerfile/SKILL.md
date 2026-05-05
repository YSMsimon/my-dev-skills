---
name: dockerfile
description: Write, explain, debug, and optimise Dockerfiles and docker-compose.yml files for any language or stack. Use this skill whenever the user wants to containerise an application, write a Dockerfile, set up docker-compose, configure environment variables in containers, set up multi-stage builds, reduce image size, fix Docker build errors, or debug container networking issues. Trigger on words like "Dockerfile", "docker-compose", "containerise", "container", "docker build", "image size", "port", or "volume".
---

# Dockerfile & Docker Compose

Write correct, minimal, and production-ready container configurations. Goals: small images, fast builds via layer caching, no unnecessary privileges, and predictable behaviour between dev and prod.

---

## Layer caching — the most important concept

Docker rebuilds every layer below the first changed layer. Order instructions from **least to most frequently changed**:

1. Base image
2. System dependencies (apt-get)
3. Dependency manifest (requirements.txt / package.json)
4. Install dependencies (pip install / npm ci)
5. Source code — **always last**

**Common mistake:** `COPY . .` before installing deps. Every source file change triggers a full reinstall.

---

## Security rules

- **Never run as root** — create a non-root user and `USER app`
- **Never bake secrets into the image** — pass at runtime via env vars or `--env-file`
- **Pin base image versions** — `python:3.12.3-slim-bookworm` not `python:latest`
- **Minimise surface** — `--no-install-recommends` on apt, clean cache in the same `RUN` layer

---

## .dockerignore

Always create this or the build context balloons with `node_modules`, `.git`, `.env`:

```
.git
.env
.env.*
__pycache__
*.pyc
node_modules
.DS_Store
dist
build
.venv
venv
```

---

## Networking in docker-compose

Services in the same compose file reach each other by **service name**, not `localhost`:

```
# app connecting to db service
DATABASE_URL=postgresql://myuser:mypassword@db:5432/mydb   # inside compose
DATABASE_URL=postgresql://myuser:mypassword@localhost:5433/mydb  # from host machine
```

---

## Image size checklist

- [ ] `slim` or `alpine` base image
- [ ] Multi-stage build if there's a compile step
- [ ] `--no-cache-dir` (pip) or `--only=production` (npm)
- [ ] `rm -rf /var/lib/apt/lists/*` after apt-get
- [ ] `.dockerignore` excludes `node_modules`, `.git`, `.env`
- [ ] Non-root user set with `USER`
- [ ] Secrets passed at runtime, not baked in

---

## Useful commands

```bash
docker compose up -d                  # start detached
docker compose up -d --build          # rebuild then start
docker compose down                   # stop and remove containers
docker compose down -v                # also remove volumes (⚠ deletes DB data)
docker compose logs -f app            # stream logs for one service
docker compose ps                     # status of all services
docker exec -it <container> /bin/sh   # shell into running container
docker build --no-cache -t myapp .    # full rebuild
docker system prune -af               # remove all unused (⚠ nuclear)

# Postgres inside container
docker exec -it postgres_vector_db psql -U myuser -d agent_memory
```

---

## Additional resources

- For common issues and fixes, see [examples.md](examples.md)
- For Dockerfile and compose templates, see [template/](template/)
