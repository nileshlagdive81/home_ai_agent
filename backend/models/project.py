from sqlalchemy import Column, String, Boolean, Text, Date, ForeignKey, Integer
from sqlalchemy.orm import relationship
from .base import Base, TimestampMixin

class Project(Base, TimestampMixin):
    __tablename__ = "projects"
    
    id = Column(String, primary_key=True, index=True)  # UUID as string
    name = Column(String(200), nullable=False, index=True)
    developer_id = Column(String, ForeignKey("developers.id"), nullable=True)
    description = Column(Text, nullable=True)
    project_type = Column(String(100), nullable=True)
    total_units = Column(Integer, nullable=True)
    units_per_floor = Column(Integer, nullable=True)
    total_floors = Column(Integer, nullable=True)
    project_status = Column(String(50), nullable=True, index=True)
    rera_number = Column(String(50), nullable=True)
    possession_date = Column(Date, nullable=True)
    completion_date = Column(Date, nullable=True)
    
    # Relationships
    project_locations = relationship("ProjectLocation", back_populates="project", cascade="all, delete-orphan")
    properties = relationship("Property", back_populates="project", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Project(id={self.id}, name='{self.name}', status='{self.project_status}')>"
