from sqlalchemy import Column, String, ForeignKey, Numeric
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from .base import Base, TimestampMixin

class ProjectNearby(Base, TimestampMixin):
    __tablename__ = "project_nearby"
    
    id = Column(UUID(as_uuid=True), primary_key=True, index=True)  # UUID type
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id"), nullable=False)
    nearby_place_id = Column(UUID(as_uuid=True), ForeignKey("nearby_places.id"), nullable=False)
    distance_km = Column(Numeric(5, 2))
    
    # Relationships
    project = relationship("Project", back_populates="project_nearby")
    nearby_place = relationship("NearbyPlace", back_populates="project_nearby")
    
    def __repr__(self):
        return f"<ProjectNearby(project_id={self.project_id}, nearby_place_id={self.nearby_place_id}, distance={self.distance_km}km)>"
