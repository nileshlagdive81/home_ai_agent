from sqlalchemy import Column, String, Boolean, Text, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from .base import Base, TimestampMixin

class NearbyPlace(Base, TimestampMixin):
    __tablename__ = "nearby_places"
    
    id = Column(String, primary_key=True, index=True)  # UUID as string
    place_name = Column(String(200), nullable=False)
    place_type = Column(String(100), nullable=False)
    project_id = Column(String, ForeignKey("projects.id"), nullable=False)
    distance_km = Column(Numeric(5, 2))
    address = Column(Text)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    project = relationship("Project", back_populates="project_nearby")
    
    def __repr__(self):
        return f"<NearbyPlace(id={self.id}, name='{self.name}', category_id={self.category_id})>"
