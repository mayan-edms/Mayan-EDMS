# Local Development Guide (Fibex EDMS)

This repository provides a self-contained local development environment with **Live Auto-Reload (Hot Reload)** for both **Podman** and **Docker Desktop** users.

---

## Quick Start

### Option 1: Using PowerShell (Windows — Podman or Docker)

The script [`dev.ps1`](./dev.ps1) auto-detects whether you are running Podman or Docker Desktop:

```powershell
# 1. Start the development server (auto-builds image if needed)
.\dev.ps1 start

# 2. View live server logs and file reload events
.\dev.ps1 logs

# 3. Enter container bash shell
.\dev.ps1 shell

# 4. Run Django management commands
.\dev.ps1 manage check
.\dev.ps1 manage showmigrations

# 5. Stop the development server
.\dev.ps1 stop
```

---

### Option 2: Using Standard Docker Compose (Mac / Linux / Windows with Docker Desktop)

```bash
# Build and start the development server
docker compose -f docker-compose.dev.yml up --build

# Or in background
docker compose -f docker-compose.dev.yml up -d
docker compose -f docker-compose.dev.yml logs -f
docker compose -f docker-compose.dev.yml down
```

---

## Access & Credentials

- **URL**: [http://localhost:8000](http://localhost:8000)
- **Default Username**: `admin`
- **Default Password**: `adminpassword`

---

## How It Works

1. **First-Run Auto-Setup**:
   - On the very first run (when `mayan/media/db.sqlite3` doesn't exist), the entrypoint script automatically runs Django migrations and creates the default admin user.
   - Subsequent starts skip setup and go directly to the dev server.

2. **Live Fast Reload**:
   - The root repository is mounted into `/app` inside the container.
   - Django's `StatReloader` watches for file changes.
   - Saving any Python, template, or CSS file triggers an automatic reload in ~1.5 seconds without restarting the container.

3. **Data Persistence**:
   - All uploaded documents and the SQLite database are stored in `mayan/media/db.sqlite3`.
   - Data persists on your local machine across container restarts.
   - `mayan/media/` is git-ignored to prevent test data from being committed.

4. **In-Memory Services**:
   - `mayan.settings.development` uses in-process Celery (`memory://`) and Django ORM search.
   - No external Redis, RabbitMQ, or PostgreSQL services are required for local development.

---

## Troubleshooting

| Problem | Solution |
|---|---|
| Port 8000 already in use | Stop any other service using port 8000, or `.\dev.ps1 stop` first |
| Image build fails | Run `.\dev.ps1 build` to rebuild from scratch |
| Cannot reach `http://localhost:8000` on Podman | `dev.ps1` uses `--network host` automatically for Podman on Windows |
| Need to reset the database | Delete `mayan/media/db.sqlite3` and restart; entrypoint re-creates it |

