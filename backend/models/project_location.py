from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base, TimestampMixin

class ProjectLocation(Base, TimestampMixin):
    """ProjectLocation model mapping to the project_locations table"""
    __tablename__ = "project_locations"
    
    id = Column(String, primary_key=True, index=True)  # UUID as string
    project_id = Column(String, ForeignKey("projects.id"), nullable=False)
    location_id = Column(String, ForeignKey("locations.id"), nullable=False)
    
    # Relationships
    project = relationship("Project", back_populates="project_locations")
    location = relationship("Location", back_populates="project_locations")
    
    def __repr__(self):
        return f"<ProjectLocation(project_id={self.project_id}, location_id={self.location_id})>"
