# 🚀 CancerCareSystem – Deployment Guide

Complete guide for deploying the CancerCareSystem application locally, with Docker, or to the cloud.

---

## Table of Contents

1. [Local Development](#1-local-development)
2. [Docker Deployment](#2-docker-deployment)
3. [Cloud Deployment](#3-cloud-deployment)
4. [Environment Variables](#4-environment-variables)
5. [Troubleshooting](#5-troubleshooting)

---

## 1. Local Development

### Prerequisites

- **Python 3.10+** with pip
- **Node.js 18+** with npm
- **Git**

### Backend Setup

```bash
# Navigate to backend
cd backend

# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Copy environment file
copy .env.example .env         # Windows
# cp .env.example .env         # macOS/Linux

# Start the server (development mode with auto-reload)
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

**Verify**: Open http://localhost:8000/docs to see the API documentation.

### Frontend Setup

```bash
# Navigate to frontend (in a new terminal)
cd frontend

# Install dependencies
npm install

# Copy environment file
copy .env.example .env         # Windows
# cp .env.example .env         # macOS/Linux

# Start dev server
npm run dev
```

**Verify**: Open http://localhost:5173 to see the application.

> **Note**: The Vite dev server automatically proxies API requests (`/api/*`, `/predict/*`) to `http://localhost:8000`, so no CORS issues in development.

---

## 2. Docker Deployment

### Prerequisites

- **Docker** 20.10+
- **Docker Compose** v2+

### One-Command Deploy

```bash
# From the project root
docker-compose up --build -d
```

This will:
1. Build the backend image (Python 3.11 + ML models)
2. Build the frontend image (Node build → Nginx serve)
3. Start both containers with networking
4. Wait for backend health check before starting frontend

### Access

| Service  | URL                      |
|----------|--------------------------|
| Frontend | http://localhost         |
| Backend  | http://localhost:8000    |
| API Docs | http://localhost:8000/docs |
| Health   | http://localhost/health   |

### Useful Commands

```bash
# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Rebuild after code changes
docker-compose up --build -d

# View running containers
docker-compose ps
```

---

## 3. Cloud Deployment

### Option A: Render (Free Tier)

**Backend (Web Service):**
1. Connect your GitHub repo to [Render](https://render.com)
2. Create a "Web Service" with:
   - **Root Directory**: `backend`
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
3. Add environment variables from the table below

**Frontend (Static Site):**
1. Create a "Static Site" with:
   - **Root Directory**: `frontend`
   - **Build Command**: `npm ci && npm run build`
   - **Publish Directory**: `dist`
2. Set `VITE_API_URL` to your backend Render URL (e.g., `https://cancercare-api.onrender.com`)
3. Add rewrite rule: `/*` → `/index.html` (for SPA routing)

### Option B: Railway

1. Connect your GitHub repo to [Railway](https://railway.app)
2. Railway auto-detects both services from the Dockerfiles
3. Set environment variables in the Railway dashboard
4. Railway provides HTTPS URLs automatically

### Option C: VPS (DigitalOcean / AWS EC2)

```bash
# SSH into your server
ssh user@your-server-ip

# Clone the repo
git clone https://github.com/your-username/CancerCareSystem.git
cd CancerCareSystem

# Set environment variables
export SECRET_KEY="your-secure-random-key"

# Deploy with Docker Compose
docker-compose up --build -d
```

For HTTPS, add a reverse proxy like Caddy or use Certbot with Nginx.

---

## 4. Environment Variables

### Backend

| Variable       | Required | Default                                             | Description                     |
|---------------|----------|------------------------------------------------------|---------------------------------|
| `HOST`        | No       | `127.0.0.1`                                         | Server bind address             |
| `PORT`        | No       | `8000`                                               | Server port                     |
| `DEBUG`       | No       | `false`                                              | Enable debug mode               |
| `SECRET_KEY`  | Yes (prod)| `change-me-in-production`                           | JWT/session signing key         |
| `CORS_ORIGINS`| No       | `http://localhost:5173,http://127.0.0.1:5173`       | Allowed origins (comma-sep)     |
| `DATABASE_URL`| No       | `sqlite:///./cancercare_secure.db`                  | Database connection             |

### Frontend

| Variable       | Required | Default                | Description          |
|---------------|----------|------------------------|----------------------|
| `VITE_API_URL`| No       | `http://localhost:8000` | Backend API base URL |

---

## 5. Troubleshooting

### Backend won't start
- Ensure Python 3.10+ is installed: `python --version`
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Check if port 8000 is available: `netstat -an | findstr 8000`

### Frontend can't reach backend
- In dev: check that the backend is running on port 8000
- In Docker: ensure both containers are on the same network (`docker-compose ps`)
- Check browser console for CORS errors → update `CORS_ORIGINS` env var

### Docker build fails
- Ensure Docker is installed: `docker --version`
- For ML model issues: verify `.h5` files exist in `backend/` directory
- For memory issues: Docker needs 4GB+ RAM for TensorFlow

### Large Docker image size
- The backend image includes ML models (~270MB). This is expected.
- Use `.dockerignore` to exclude test files and datasets
- Consider hosting models on cloud storage (S3/GCS) for production

### SPA routing (404 on refresh)
- Docker/Nginx: handled automatically by `try_files` in `nginx.conf`
- Render Static Site: add rewrite rule `/*` → `/index.html`
- Other hosts: configure your web server for SPA fallback
