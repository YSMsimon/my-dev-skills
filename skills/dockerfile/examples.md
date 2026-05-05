# Dockerfile — Common Issues and Fixes

## "Port already in use"
```bash
lsof -i :5432   # find what's using the port
# or change the host port in docker-compose:
ports:
  - "5434:5432"
```

## "Connection refused" to database
```bash
docker compose ps         # is the container running?
docker compose logs db    # is the healthcheck passing?
```

Remember: inside docker-compose use service name `db`, not `localhost`.

## "Module not found" after adding a dependency
```bash
docker compose up -d --build    # force rebuild
docker compose build --no-cache # full rebuild
```

## Image is too large
```bash
docker history myimage   # check layer sizes
```
Common culprits:
- apt cache not cleaned: add `&& rm -rf /var/lib/apt/lists/*`
- Dev dependencies included
- Source control included (check `.dockerignore`)
- Build tools not removed: use multi-stage build

## "Permission denied" on files
```dockerfile
COPY --chown=app:app . .   # set ownership at copy time
```

## Container exits immediately
```bash
docker compose logs app   # check the logs
```
Common causes: wrong CMD (process not in foreground), missing env var, database not ready (add `depends_on` with healthcheck).

## Changes to .env not picked up
```bash
docker compose down && docker compose up -d
```
