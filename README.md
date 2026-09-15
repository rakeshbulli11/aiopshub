````markdown
# AIOpsHub – AI-Powered DevOps Monitoring and Deployment System

AIOpsHub is a medium-level DevOps monitoring and deployment project that demonstrates how an application can be developed, containerized, tested, security-scanned, monitored, versioned, deployed, and rolled back using modern DevOps tools.

The project combines a React frontend, FastAPI backend, PostgreSQL, Docker, GitHub Actions, Docker Hub, Trivy, Prometheus, Grafana, Loki, Grafana Alloy, and Terraform.

---

## Project Goal

The goal of AIOpsHub is to provide a centralized platform for:

- Monitoring application and server health
- Collecting CPU, memory, disk, and network metrics
- Detecting incidents automatically
- Recording deployment history
- Performing AI-based system health analysis
- Visualizing metrics in Grafana
- Centralizing application logs
- Scanning Docker images for vulnerabilities
- Publishing versioned Docker images
- Performing health checks after deployment
- Supporting rollback to a previous application version

---

## Features

- React + Vite monitoring dashboard
- FastAPI REST API
- PostgreSQL database
- SQLAlchemy ORM
- Server management
- CPU monitoring
- Memory monitoring
- Disk monitoring
- Network monitoring
- Automatic incident detection
- Incident resolution
- Deployment history tracking
- AI-based system health analysis
- Docker containerization
- Docker Compose
- GitHub Actions CI/CD
- Docker Hub image publishing
- Versioned Docker releases
- Trivy security scanning
- Prometheus metrics
- Grafana dashboards
- Grafana alerting
- Loki log aggregation
- Grafana Alloy log collection
- Deployment health checks
- Automatic local rollback
- Manual GitHub Actions rollback workflow
- Terraform infrastructure configuration

---

## Technology Stack

| Technology | Purpose |
|---|---|
| React + Vite | Frontend dashboard |
| FastAPI | Backend REST API |
| Python | Backend development |
| PostgreSQL | Application database |
| SQLAlchemy | Database ORM |
| Docker | Containerization |
| Docker Compose | Multi-container environment |
| Git + GitHub | Source control |
| GitHub Actions | CI/CD automation |
| Docker Hub | Container image registry |
| Trivy | Container security scanning |
| Prometheus | Metrics collection |
| Grafana | Monitoring and visualization |
| Loki | Log aggregation |
| Grafana Alloy | Log collection |
| psutil | System metrics collection |
| Terraform | Infrastructure as Code |

---

## Architecture

```text
                         AIOpsHub
                            |
              +-------------+-------------+
              |                           |
              v                           v
        React Frontend              FastAPI Backend
                                          |
                         +----------------+----------------+
                         |                |                |
                         v                v                v
                    PostgreSQL          psutil        AI Analysis
                         |                |
                         |                v
                         |          System Metrics
                         |                |
                         +-------+--------+
                                 |
                                 v
                            Data Storage
````

### Monitoring Architecture

```text
System Metrics
      |
      v
    psutil
      |
      v
FastAPI /prometheus
      |
      v
  Prometheus
      |
      v
   Grafana
      |
      +---- CPU Usage
      +---- Memory Usage
      +---- Disk Usage
      +---- Network Usage
      +---- AIOpsHub Status
      +---- Alerts
```

### Logging Architecture

```text
AIOpsHub Backend
      |
      v
Docker Container Logs
      |
      v
Grafana Alloy
      |
      v
     Loki
      |
      v
   Grafana
```

---

## CI/CD Pipeline

Every push to the `main` branch runs the GitHub Actions CI/CD pipeline.

```text
Developer
    |
    v
Git Push
    |
    v
GitHub Actions
    |
    +---- Checkout source
    |
    +---- Set up Python
    |
    +---- Install dependencies
    |
    +---- Python syntax validation
    |
    +---- Docker image build
    |
    +---- Trivy security scan
    |
    +---- Docker Hub login
    |
    +---- Docker image publishing
    |
    v
Docker Hub
```

### Release Pipeline

Version tags such as `v1.1.0` and `v1.2.0` trigger versioned image publishing.

```text
Git Tag
   |
   v
GitHub Actions
   |
   v
Docker Build
   |
   v
Trivy Scan
   |
   v
Docker Hub
   |
   +---- v1.1.0
   +---- v1.2.0
```

---

## Docker Services

The local Docker Compose environment contains:

```text
aiopshub-db
aiopshub-backend
aiopshub-prometheus
aiopshub-grafana
aiopshub-loki
aiopshub-alloy
```

---

## Local URLs

```text
Frontend:
http://localhost:5173

Backend:
http://localhost:8000

FastAPI Swagger:
http://localhost:8000/docs

Prometheus:
http://localhost:9090

Grafana:
http://localhost:3000

Loki:
http://localhost:3100

Grafana Alloy:
http://localhost:12345
```

---

## Main Backend Endpoints

```text
GET  /

GET  /health

GET  /servers
POST /servers

GET  /metrics
POST /metrics
GET  /metrics/latest
POST /metrics/collect

GET  /incidents
POST /incidents/test
PUT  /incidents/{incident_id}/resolve

GET  /deployments
POST /deployments
POST /deployments/rollback

GET  /ai-analysis

GET  /prometheus
```

---

## Running the Project Locally

### Start Docker services

```bash
docker compose up -d
```

### Check containers

```bash
docker ps
```

### Check backend health

```bash
curl http://localhost:8000/health
```

Expected response:

```json
{
  "status": "healthy",
  "database": "connected"
}
```

### Start the frontend

```bash
cd frontend
npm run dev
```

Open:

```text
http://localhost:5173
```

---

## Prometheus Metrics

AIOpsHub exposes the following metrics:

```text
aiopshub_up
aiopshub_cpu_usage
aiopshub_memory_usage
aiopshub_disk_usage
aiopshub_network_usage
```

Example:

```text
aiopshub_cpu_usage
```

The metrics are exposed through:

```text
http://localhost:8000/prometheus
```

Prometheus collects the metrics and Grafana visualizes them.

---

## Grafana Monitoring

The AIOpsHub Grafana dashboard includes:

* CPU usage
* Memory usage
* Disk usage
* Network usage
* AIOpsHub availability

### High CPU Alert

A high CPU condition is monitored using:

```text
CPU Usage > 80%
        |
        v
Grafana Alert
```

---

## Logging with Loki and Alloy

AIOpsHub collects Docker container logs using Grafana Alloy and sends them to Loki.

```text
Docker Logs
    |
    v
Grafana Alloy
    |
    v
Loki
    |
    v
Grafana Explore
```

Example LogQL query:

```logql
{container="aiopshub-backend"}
```

Example error query:

```logql
{container="aiopshub-backend"} |= "Database health check failed"
```

---

## Deployment Health Check

A deployment health check is provided through:

```text
scripts/health-check.bat
```

Run:

```cmd
scripts\health-check.bat
```

A successful deployment returns:

```text
Health check PASSED.
```

---

## Versioned Docker Releases

Docker Hub repository:

```text
rakeshbulli/aiopshub-backend
```

Current release versions include:

```text
v1.0.0
v1.1.0
v1.2.0
```

Example images:

```text
rakeshbulli/aiopshub-backend:v1.1.0
rakeshbulli/aiopshub-backend:v1.2.0
```

---

## Deployment

The deployment Compose file uses a configurable backend version.

Set the version:

```cmd
set BACKEND_VERSION=v1.2.0
```

Deploy:

```cmd
docker compose -f docker-compose.deploy.yml up -d --force-recreate backend
```

Verify the running image:

```cmd
docker inspect aiopshub-backend --format "{{.Config.Image}}"
```

Check application health:

```cmd
curl http://localhost:8000/health
```

---

## Automatic Rollback

A deployment can be performed with automatic health checking and rollback using:

```text
scripts/deploy-with-rollback.bat
```

Example:

```cmd
scripts\deploy-with-rollback.bat v1.2.0 v1.1.0
```

The process is:

```text
Deploy v1.2.0
      |
      v
Health Check
      |
   +--+--+
   |     |
  PASS  FAIL
   |     |
   v     v
Success Rollback
         |
         v
      v1.1.0
         |
         v
     Health Check
```

---

## Manual GitHub Actions Rollback

A manual rollback workflow is available through GitHub Actions.

Workflow:

```text
AIOpsHub Rollback
```

The workflow accepts a version such as:

```text
v1.1.0
```

and verifies the corresponding Docker Hub image.

Example rollback target:

```text
rakeshbulli/aiopshub-backend:v1.1.0
```

---

## Docker Image Security

Trivy is integrated into the GitHub Actions pipeline.

The Docker image is scanned for:

* HIGH vulnerabilities
* CRITICAL vulnerabilities
* Operating system package vulnerabilities
* Python dependency vulnerabilities
* Secrets

The current CI scan reports vulnerabilities without blocking the pipeline.

---

## Docker Hub Publishing

Docker images are automatically published to:

```text
rakeshbulli/aiopshub-backend
```

Main branch builds use:

```text
latest
<commit-sha>
```

Release builds use version tags such as:

```text
v1.1.0
v1.2.0
```

---

## Terraform

Terraform configuration is included for future infrastructure automation and cloud deployment.

The Terraform files are intended to support infrastructure provisioning when the project is moved to a cloud environment.

---

## Project Status

### Completed

* Application development
* React frontend
* FastAPI backend
* PostgreSQL integration
* SQLAlchemy integration
* Docker containerization
* Docker Compose
* GitHub repository
* GitHub Actions CI/CD
* Docker Hub publishing
* Versioned Docker images
* Trivy security scanning
* Prometheus monitoring
* Grafana dashboard
* Grafana alerting
* Loki logging
* Grafana Alloy log collection
* Deployment health checking
* Automatic local rollback
* Manual GitHub Actions rollback workflow
* Terraform configuration

### Planned

* AWS EC2 deployment
* Nginx reverse proxy
* HTTPS configuration
* Production cloud deployment
* Additional Grafana alerts
* More advanced automated recovery

---

## Release History

```text
v1.0.0
Initial AIOpsHub release

v1.1.0
Versioned Docker deployment and rollback support

v1.2.0
Versioned Docker release with CI/CD publishing
```

---

## Project Workflow

```text
Developer
   |
   v
GitHub
   |
   v
GitHub Actions
   |
   +---- Python Validation
   |
   +---- Docker Build
   |
   +---- Trivy Scan
   |
   v
Docker Hub
   |
   v
Versioned Docker Image
   |
   v
Deployment
   |
   v
Health Check
   |
   +--------+
   |        |
 Healthy   Failed
   |        |
 Success  Rollback
            |
            v
       Previous Version
```

---

## Future Cloud Architecture

```text
Developer
    |
    v
GitHub
    |
    v
GitHub Actions
    |
    +---- Build
    +---- Test
    +---- Trivy
    +---- Publish
    |
    v
Docker Hub
    |
    v
AWS EC2
    |
    +---- Nginx
    |
    +---- AIOpsHub Backend
    |
    +---- PostgreSQL
    |
    +---- Prometheus
    |
    +---- Grafana
```

---

## Author

**Rakesh Bulli**

BTech 3rd Year – Computer Science and Engineering

HITAM

````

### Save it

In CMD:

```cmd
cd C:\Users\ADMIN\OneDrive\Desktop\aiopshub
notepad README.md
````

Delete the old content, paste the new README, save and close.

Then:

```cmd
git add README.md
git commit -m "docs: update AIOpsHub README"
git push origin main
```

After this, your GitHub README will accurately present the project as a **monitoring + security + CI/CD + versioning + rollback** project rather than just a monitoring application.
