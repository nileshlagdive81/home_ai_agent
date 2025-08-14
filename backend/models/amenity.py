from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from .base import Base, TimestampMixin

class Amenity(Base, TimestampMixin):
    __tablename__ = "amenities"
    
    id = Column(String, primary_key=True, index=True)  # UUID as string
    name = Column(String(100), unique=True, nullable=False)
    category = Column(String(50), nullable=False)  # basic, luxury, security, recreation
    # icon = Column(String(100))  # Commented out as database doesn't have this field
    # is_active = Column(Boolean, default=True)  # Commented out as database doesn't have this field
    
    # Relationships
    # project_amenities = relationship("ProjectAmenity", back_populates="amenity", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Amenity(id={self.id}, name='{self.name}', category='{self.category}')>"
