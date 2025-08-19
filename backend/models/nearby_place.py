from sqlalchemy import Column, String, Boolean, Text, ForeignKey, Numeric
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from .base import Base, TimestampMixin

class NearbyPlace(Base, TimestampMixin):
    __tablename__ = "nearby_places"
    
    id = Column(UUID(as_uuid=True), primary_key=True, index=True)  # UUID type
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id"), nullable=False)
    place_type = Column(String(100), nullable=False)
    place_name = Column(String(200), nullable=False)
    distance_km = Column(Numeric(5, 2))
    walking_distance = Column(Boolean, default=False)
    
    # Relationships
    project = relationship("Project", back_populates="nearby_places")
    project_nearby = relationship("ProjectNearby", back_populates="nearby_place", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<NearbyPlace(id={self.id}, name='{self.place_name}', type='{self.place_type}', distance={self.distance_km}km)>"
