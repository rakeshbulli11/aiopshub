from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse
from sqlalchemy.orm import Session
from sqlalchemy import text
from datetime import datetime
from pydantic import BaseModel

from database import engine, get_db
from models import Server, Metric, Incident, Deployment
from monitor import get_system_metrics
from ai_analysis import analyze_metrics


class ServerCreate(BaseModel):
    name: str
    ip_address: str
    status: str = "unknown"
    environment: str = "development"


class MetricCreate(BaseModel):
    server_id: int
    cpu_usage: float
    memory_usage: float
    disk_usage: float
    network_usage: float 
    
class DeploymentCreate(BaseModel):
    server_id: int
    application_name: str
    version: str
    status: str = "success"
    
app = FastAPI(
    title="AIOpsHub",
    description="AI-Powered DevOps Monitoring and Deployment System",
    version="1.0.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {
        "message": "AIOpsHub API is running",
        "database": "PostgreSQL connected"
    }


@app.get("/health")
def health_check():
    try:
        with engine.connect() as connection:
            return {
                "status": "healthy",
                "database": "connected"
            }
    except Exception as e:
        return {
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e)
        }


@app.get("/servers")
def get_servers(db: Session = Depends(get_db)):
    servers = db.query(Server).all()
    return servers


@app.post("/servers")
def create_server(server: ServerCreate, db: Session = Depends(get_db)):
    new_server = Server(
        name=server.name,
        ip_address=server.ip_address,
        status=server.status,
        environment=server.environment
    )

    db.add(new_server)
    db.commit()
    db.refresh(new_server)

    return new_server


@app.get("/metrics")
def get_metrics(db: Session = Depends(get_db)):
    metrics = db.query(Metric).all()
    return metrics
@app.get("/metrics/latest")
def get_latest_metric(db: Session = Depends(get_db)):
    latest_metric = (
        db.query(Metric)
        .order_by(Metric.recorded_at.desc())
        .first()
    )

    if not latest_metric:
        return {
            "message": "No metrics available"
        }

    return latest_metric

@app.post("/metrics")
def create_metric(metric: MetricCreate, db: Session = Depends(get_db)):
    new_metric = Metric(
        server_id=metric.server_id,
        cpu_usage=metric.cpu_usage,
        memory_usage=metric.memory_usage,
        disk_usage=metric.disk_usage,
        network_usage=metric.network_usage
    )

    db.add(new_metric)
    db.commit()
    db.refresh(new_metric)

    return new_metric


@app.get("/incidents")
def get_incidents(db: Session = Depends(get_db)):
    incidents = db.query(Incident).all()
    return incidents
@app.get("/deployments")
def get_deployments(db: Session = Depends(get_db)):
    deployments = db.execute(
        text("""
            SELECT id, server_id, application_name, version, status, deployed_at
            FROM deployments
            ORDER BY deployed_at DESC
        """)
    ).fetchall()

    return [
        {
            "id": deployment.id,
            "server_id": deployment.server_id,
            "application_name": deployment.application_name,
            "version": deployment.version,
            "status": deployment.status,
            "deployed_at": deployment.deployed_at
        }
        for deployment in deployments
    ]
@app.post("/deployments")
def create_deployment(
    deployment: DeploymentCreate,
    db: Session = Depends(get_db)
):
    new_deployment = Deployment(
        server_id=deployment.server_id,
        application_name=deployment.application_name,
        version=deployment.version,
        status=deployment.status
    )

    db.add(new_deployment)
    db.commit()
    db.refresh(new_deployment)

    return {
        "message": "Deployment recorded successfully",
        "deployment_id": new_deployment.id,
        "application_name": new_deployment.application_name,
        "version": new_deployment.version,
        "status": new_deployment.status
    }
@app.post("/metrics/collect")
def collect_metrics(db: Session = Depends(get_db)):
    data = get_system_metrics()

    new_metric = Metric(
        server_id=1,
        cpu_usage=data["cpu_usage"],
        memory_usage=data["memory_usage"],
        disk_usage=data["disk_usage"],
        network_usage=data["network_usage"]
    )

    db.add(new_metric)
    db.commit()
    db.refresh(new_metric)

    # High CPU detection
    if data["cpu_usage"] > 80:
        existing_incident = db.query(Incident).filter(
            Incident.server_id == 1,
            Incident.title == "High CPU Usage",
            Incident.status == "open"
        ).first()

        if not existing_incident:
            incident = Incident(
                server_id=1,
                title="High CPU Usage",
                description=f"CPU usage reached {data['cpu_usage']}%",
                severity="high",
                status="open"
            )
            db.add(incident)

    # High Memory detection
    if data["memory_usage"] > 80:
        existing_incident = db.query(Incident).filter(
            Incident.server_id == 1,
            Incident.title == "High Memory Usage",
            Incident.status == "open"
        ).first()

        if not existing_incident:
            incident = Incident(
                server_id=1,
                title="High Memory Usage",
                description=f"Memory usage reached {data['memory_usage']}%",
                severity="high",
                status="open"
            )
            db.add(incident)

    # High Disk detection
    if data["disk_usage"] > 90:
        existing_incident = db.query(Incident).filter(
            Incident.server_id == 1,
            Incident.title == "High Disk Usage",
            Incident.status == "open"
        ).first()

        if not existing_incident:
            incident = Incident(
                server_id=1,
                title="High Disk Usage",
                description=f"Disk usage reached {data['disk_usage']}%",
                severity="high",
                status="open"
            )
            db.add(incident)

    db.commit()

    return {
        "message": "Metrics collected successfully",
        "cpu_usage": data["cpu_usage"],
        "memory_usage": data["memory_usage"],
        "disk_usage": data["disk_usage"],
        "network_usage": data["network_usage"]
    }


@app.put("/incidents/{incident_id}/resolve")
def resolve_incident(
    incident_id: int,
    db: Session = Depends(get_db)
):
    incident = db.query(Incident).filter(
        Incident.id == incident_id
    ).first()

    if not incident:
        return {
            "message": "Incident not found"
        }

    incident.status = "resolved"
    incident.resolved_at = datetime.now()

    db.commit()
    db.refresh(incident)

    return {
        "message": "Incident resolved successfully",
        "incident_id": incident.id,
        "title": incident.title,
        "status": incident.status,
        "resolved_at": incident.resolved_at
    }

@app.get("/ai-analysis")
def get_ai_analysis(db: Session = Depends(get_db)):
    latest_metric = (
        db.query(Metric)
        .order_by(Metric.recorded_at.desc())
        .first()
    )

    if not latest_metric:
        return {
            "message": "No metrics available for analysis"
        }

    recommendations = analyze_metrics(
        float(latest_metric.cpu_usage),
        float(latest_metric.memory_usage),
        float(latest_metric.disk_usage)
    )

    return {
        "metric_id": latest_metric.id,
        "cpu_usage": float(latest_metric.cpu_usage),
        "memory_usage": float(latest_metric.memory_usage),
        "disk_usage": float(latest_metric.disk_usage),
        "recommendations": recommendations
    }
@app.post("/incidents/test")
def create_test_incident(db: Session = Depends(get_db)):
    incident = Incident(
        server_id=1,
        title="Test High CPU Incident",
        description="Test incident created to verify AIOpsHub incident monitoring.",
        severity="high",
        status="open"
    )

    db.add(incident)
    db.commit()
    db.refresh(incident)

    return {
        "message": "Test incident created successfully",
        "incident_id": incident.id,
        "title": incident.title,
        "severity": incident.severity,
        "status": incident.status
    }
@app.get("/prometheus", response_class=PlainTextResponse)
def prometheus_metrics():
    data = get_system_metrics()

    return f"""# HELP aiopshub_up Whether the AIOpsHub backend is running
# TYPE aiopshub_up gauge
aiopshub_up 1

# HELP aiopshub_cpu_usage CPU usage percentage
# TYPE aiopshub_cpu_usage gauge
aiopshub_cpu_usage {data["cpu_usage"]}

# HELP aiopshub_memory_usage Memory usage percentage
# TYPE aiopshub_memory_usage gauge
aiopshub_memory_usage {data["memory_usage"]}

# HELP aiopshub_disk_usage Disk usage percentage
# TYPE aiopshub_disk_usage gauge
aiopshub_disk_usage {data["disk_usage"]}

# HELP aiopshub_network_usage Network usage in MB
# TYPE aiopshub_network_usage gauge
aiopshub_network_usage {data["network_usage"]}
"""