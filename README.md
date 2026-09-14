\# AIOpsHub – AI-Powered DevOps Monitoring and Deployment System



AIOpsHub is a medium-level DevOps and monitoring project designed to demonstrate how a modern application can be developed, containerized, tested, secured, monitored, and deployed using DevOps tools.



The project combines a React frontend, FastAPI backend, PostgreSQL database, Docker, GitHub Actions, Docker Hub, Trivy, Prometheus, and Grafana.



\## Project Goal



The goal of AIOpsHub is to provide a centralized system for monitoring application and server health, recording deployments, detecting incidents, and providing AI-based recommendations.



\## Features



\* React-based monitoring dashboard

\* FastAPI REST API

\* PostgreSQL database

\* Server management

\* CPU, memory, disk, and network monitoring

\* Automatic incident detection

\* Incident resolution

\* Deployment history tracking

\* AI-based system health analysis

\* Docker and Docker Compose

\* GitHub Actions CI/CD

\* Docker Hub image publishing

\* Trivy Docker image security scanning

\* Prometheus metrics collection

\* Grafana monitoring dashboard

\* Grafana CPU alerting



\## Technology Stack



| Technology     | Purpose                         |

| -------------- | ------------------------------- |

| React + Vite   | Frontend                        |

| FastAPI        | Backend REST API                |

| Python         | Backend development             |

| PostgreSQL     | Database                        |

| SQLAlchemy     | Database ORM                    |

| Docker         | Containerization                |

| Docker Compose | Multi-container setup           |

| Git + GitHub   | Source control                  |

| GitHub Actions | CI/CD automation                |

| Docker Hub     | Container image registry        |

| Trivy          | Security vulnerability scanning |

| Prometheus     | Metrics collection              |

| Grafana        | Monitoring and visualization    |

| psutil         | System metrics collection       |



\## Architecture



```text

&#x20;                   AIOpsHub

&#x20;                      |

&#x20;            +---------+---------+

&#x20;            |                   |

&#x20;       React Frontend      FastAPI Backend

&#x20;                                |

&#x20;                   +------------+------------+

&#x20;                   |            |            |

&#x20;              PostgreSQL     psutil      AI Analysis

&#x20;                   |            |

&#x20;                   |            v

&#x20;                   |       System Metrics

&#x20;                   |

&#x20;                   v

&#x20;              Data Storage



FastAPI /prometheus

&#x20;       |

&#x20;       v

&#x20;  Prometheus

&#x20;       |

&#x20;       v

&#x20;    Grafana

&#x20;       |

&#x20;       v

&#x20;Monitoring + Alerts

```



\## Monitoring Flow



```text

System Metrics

&#x20;     |

&#x20;     v

&#x20;   psutil

&#x20;     |

&#x20;     v

FastAPI /prometheus

&#x20;     |

&#x20;     v

&#x20;Prometheus

&#x20;     |

&#x20;     v

&#x20; Grafana

&#x20;     |

&#x20;     +---- CPU Usage

&#x20;     +---- Memory Usage

&#x20;     +---- Disk Usage

&#x20;     +---- Network Usage

&#x20;     +---- AIOpsHub Status

&#x20;     |

&#x20;     v

&#x20;  Alerts

```



\## CI/CD Pipeline



Every push to the `main` branch runs the GitHub Actions pipeline.



```text

Developer

&#x20;   |

&#x20;   v

GitHub Repository

&#x20;   |

&#x20;   v

GitHub Actions

&#x20;   |

&#x20;   +---- Backend Python checks

&#x20;   |

&#x20;   +---- Docker image build

&#x20;   |

&#x20;   +---- Docker Hub push

&#x20;   |

&#x20;   +---- Trivy security scan

&#x20;   |

&#x20;   v

Docker Hub

```



\## Docker Services



The local Docker Compose environment contains:



```text

aiopshub-db

aiopshub-backend

aiopshub-prometheus

aiopshub-grafana

```



Default local URLs:



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

```



\## Main Backend Endpoints



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

PUT  /incidents/{incident\_id}/resolve



GET  /deployments

POST /deployments



GET  /ai-analysis



GET  /prometheus

```



\## Running the Project Locally



\### Start Docker services



```bash

docker compose up -d

```



\### Check running containers



```bash

docker ps

```



\### Start the frontend



```bash

cd frontend

npm run dev

```



\### Open the application



```text

http://localhost:5173

```



\## Prometheus Metrics



AIOpsHub exposes the following metrics:



```text

aiopshub\_up

aiopshub\_cpu\_usage

aiopshub\_memory\_usage

aiopshub\_disk\_usage

aiopshub\_network\_usage

```



Example:



```text

aiopshub\_cpu\_usage

```



These metrics are collected by Prometheus and visualized in Grafana.



\## Grafana Dashboard



The AIOpsHub Grafana dashboard contains:



\* CPU Usage

\* Memory Usage

\* Disk Usage

\* Network Usage

\* AIOpsHub Status



The project also includes a High CPU alert:



```text

CPU usage > 80%

&#x20;       |

&#x20;       v

Grafana Alert

```



\## Security



Trivy is used in the GitHub Actions pipeline to scan the Docker image for known vulnerabilities.



The pipeline scans:



```text

rakeshbulli/aiopshub-backend:latest

```



\## Docker Hub



Docker image repository:



```text

rakeshbulli/aiopshub-backend

```



\## Future Enhancements



\* AWS EC2 deployment

\* Nginx reverse proxy

\* HTTPS configuration

\* Additional Grafana alerts

\* More detailed Prometheus metrics

\* Infrastructure as Code using Terraform

\* Production deployment improvements



\## Project Status



Completed:



\* Application development

\* PostgreSQL integration

\* Docker containerization

\* GitHub repository

\* GitHub Actions CI/CD

\* Docker Hub publishing

\* Trivy security scanning

\* Prometheus monitoring

\* Grafana dashboard

\* Grafana alerting



Planned:



\* AWS EC2 deployment

\* Nginx reverse proxy

\* Final production deployment



\## Author



Rakesh Bulli



BTech 3rd Year – Computer Science and Engineering

HITAM



