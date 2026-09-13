from sqlalchemy import Column, Integer, String, DateTime, Numeric, Text
from sqlalchemy.sql import func

from database import Base


class Server(Base):
    __tablename__ = "servers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    ip_address = Column(String(45))
    status = Column(String(30), default="unknown")
    environment = Column(String(30), default="development")
    created_at = Column(DateTime, server_default=func.now())


class Metric(Base):
    __tablename__ = "metrics"

    id = Column(Integer, primary_key=True, index=True)
    server_id = Column(Integer)
    cpu_usage = Column(Numeric(5, 2))
    memory_usage = Column(Numeric(5, 2))
    disk_usage = Column(Numeric(5, 2))
    network_usage = Column(Numeric(10, 2))
    recorded_at = Column(DateTime, server_default=func.now())


class Incident(Base):
    __tablename__ = "incidents"

    id = Column(Integer, primary_key=True, index=True)
    server_id = Column(Integer)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    severity = Column(String(20), default="medium")
    status = Column(String(30), default="open")
    detected_at = Column(DateTime, server_default=func.now())
    resolved_at = Column(DateTime, nullable=True)


class Deployment(Base):
    __tablename__ = "deployments"

    id = Column(Integer, primary_key=True, index=True)
    server_id = Column(Integer)
    application_name = Column(String(200))
    version = Column(String(100))
    status = Column(String(30), default="pending")
    deployed_at = Column(DateTime, server_default=func.now())

