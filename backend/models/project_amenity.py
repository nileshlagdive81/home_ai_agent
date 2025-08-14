from sqlalchemy import Column, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base, TimestampMixin

class ProjectAmenity(Base, TimestampMixin):
    __tablename__ = "project_amenities"
    
    id = Column(String, primary_key=True, index=True)  # UUID as string
    project_id = Column(String, ForeignKey("projects.id"), nullable=False)
    amenity_id = Column(String, ForeignKey("amenities.id"), nullable=False)
    is_available = Column(Boolean, default=True)
    
    # Relationships
    project = relationship("Project", back_populates="project_amenities")
    
    def __repr__(self):
        return f"<ProjectAmenity(project_id={self.project_id}, amenity_id={self.amenity_id})>"
