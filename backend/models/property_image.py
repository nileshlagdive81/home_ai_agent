from sqlalchemy import Column, String, Boolean, ForeignKey, Integer
from sqlalchemy.orm import relationship
from .base import Base, TimestampMixin

class PropertyImage(Base, TimestampMixin):
    __tablename__ = "property_images"
    
    id = Column(String, primary_key=True, index=True)  # UUID as string
    project_id = Column(String, ForeignKey("projects.id"), nullable=False)
    unit_id = Column(String, ForeignKey("properties.id"), nullable=True)
    image_url = Column(String(500), nullable=False)
    image_type = Column(String(50))  # exterior, interior, floor_plan, amenity, location
    is_primary = Column(Boolean, default=False)
    sort_order = Column(Integer, default=0)
    
    # Relationships
    project = relationship("Project", back_populates="property_images")
    
    def __repr__(self):
        return f"<PropertyImage(id={self.id}, type='{self.image_type}', url='{self.image_url[:50]}...')>"
