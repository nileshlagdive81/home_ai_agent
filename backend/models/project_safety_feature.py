from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from .base import Base, TimestampMixin
import uuid

class ProjectSafetyFeature(Base, TimestampMixin):
    __tablename__ = "project_safety_features"
    
    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    project_id = Column(String, ForeignKey("projects.id"), nullable=False)
    cctv_surveillance = Column(Boolean, default=False)
    fire_alarm_system = Column(Boolean, default=False)
    access_control = Column(Boolean, default=False)
    fire_staircase = Column(Boolean, default=False)
    refuge_areas = Column(Boolean, default=False)
    fire_extinguishers = Column(Boolean, default=False)
    emergency_exits = Column(Integer)
    security_personnel_count = Column(Integer)
    monitoring_24_7 = Column(Boolean, default=False)
    emergency_protocols = Column(Text)
    
    # Relationships
    project = relationship("Project", back_populates="safety_features")
    
    def __repr__(self):
        return f"<ProjectSafetyFeature(id={self.id}, project_id={self.project_id}, monitoring_24_7={self.monitoring_24_7})>"
