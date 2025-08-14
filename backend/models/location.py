from sqlalchemy import Column, String, Boolean, Numeric
from sqlalchemy.orm import relationship
from .base import Base, TimestampMixin

class Location(Base, TimestampMixin):
    """Location model mapping to the locations table"""
    __tablename__ = "locations"
    
    id = Column(String, primary_key=True, index=True)  # UUID as string
    city = Column(String(100), nullable=False)
    locality = Column(String(255), nullable=True)
    area = Column(String(255), nullable=True)
    pincode = Column(String(10), nullable=True)
    state = Column(String(100), nullable=True)
    metro_available = Column(Boolean, default=False)
    airport_distance_km = Column(Numeric(6, 2), nullable=True)
    railway_station_distance_km = Column(Numeric(6, 2), nullable=True)
    bus_stand_distance_km = Column(Numeric(6, 2), nullable=True)
    
    # Relationships
    project_locations = relationship("ProjectLocation", back_populates="location")
    
    def __repr__(self):
        return f"<Location(city='{self.city}', locality='{self.locality}')>"
