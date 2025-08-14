from sqlalchemy import Column, Integer, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from .base import Base

class ProjectNearby(Base):
    __tablename__ = "project_nearby"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    nearby_place_id = Column(Integer, ForeignKey("nearby_places.id"), nullable=False)
    distance_km = Column(Numeric(5, 2))
    
    # Relationships
    project = relationship("Project", back_populates="project_nearby")
    nearby_place = relationship("NearbyPlace", back_populates="project_nearby")
    
    def __repr__(self):
        return f"<ProjectNearby(project_id={self.project_id}, nearby_place_id={self.nearby_place_id})>"
