from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base, TimestampMixin

class Locality(Base, TimestampMixin):
    __tablename__ = "localities"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    city_id = Column(Integer, ForeignKey("cities.id"), nullable=False)
    pincode = Column(String(10))
    is_active = Column(Boolean, default=True)
    
    # Relationships
    city = relationship("City", back_populates="localities")
    nearby_places = relationship("NearbyPlace", back_populates="locality", cascade="all, delete-orphan")
    projects = relationship("Project", back_populates="locality", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Locality(id={self.id}, name='{self.name}', city_id={self.city_id})>"
